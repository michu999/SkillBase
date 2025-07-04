from django.shortcuts import render, redirect
from .models import User, Skill, City, Section
from .forms import UserForm, CityForm, SectionForm
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .serializers import UserSerializer
from slack_integration.signals import update_slack_profile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
def landing_page(request):
    return render(request, 'landing.html')

@login_required
def section_view(request):
    user_profile, created = User.objects.get_or_create(auth_user=request.user)

    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            # Add debug logging
            print(f"Form is valid, data: {form.cleaned_data}")

            section = form.cleaned_data['section']
            user_profile.section = section
            user_profile.save()

            return redirect('success')
        else:
            # Log validation errors
            print(f"Form validation errors: {form.errors}")
    else:
        initial = {'section': user_profile.section.id} if user_profile.section else {}
        form = SectionForm(initial=initial)

    return render(request, 'section_form.html', {'form': form})

@login_required
def city_form_view(request):
    # Get or create user profile for the current logged-in user
    user_profile, created = User.objects.get_or_create(auth_user=request.user)

    # Handle the POST request for the city form submission
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            # Get the city name from the form
            city_name = form.cleaned_data['city_name']

            # Find or create the city
            city, created = City.objects.get_or_create(name=city_name)

            # Assign the city to the user profile
            user_profile.city = city
            user_profile.save()

            print(f"Updated city to: {city.name}")

            # Redirect to user form
            return redirect('section_form')
    else:
        # For GET requests, create a new form
        form = CityForm()

    # Always return a response
    return render(request, 'city_form.html', {
        'form': form,
        'current_city': user_profile.city.name if user_profile.city else "No city selected"
    })

@login_required
def user_form_view(request):
    from django.db.models.signals import m2m_changed, post_save
    from bot.models import User

    # Check if signals are registered
    m2m_receivers = m2m_changed._live_receivers(sender=User.skills.through)
    save_receivers = post_save._live_receivers(sender=User)

    print(f"Signal m2m receivers count: {len(m2m_receivers)}")
    print(f"Signal post_save receivers count: {len(save_receivers)}")
    # Get or create user profile for the current logged-in user
    user_profile, created = User.objects.get_or_create(auth_user=request.user)

    # Extract and save Slack user ID from social account if not already saved
    if not user_profile.user_id or not user_profile.email:
        try:
            # Get the social account for this user
            social_account = request.user.socialaccount_set.get(provider='slack')

            # Extract the user_id from the extra_data
            if not user_profile.user_id:
                slack_user_id = social_account.extra_data.get(
                    'https://slack.com/user_id') or social_account.extra_data.get('sub')
                if slack_user_id:
                    user_profile.user_id = slack_user_id
                    user_profile.save()
                    print(f"Updated user_id to: {slack_user_id}")

            # Extract the email from the extra_data
            if not user_profile.email:
                slack_user_email = social_account.extra_data.get('email')
                if slack_user_email:
                    user_profile.email = slack_user_email
                    user_profile.save()
                    print(f"Updated email to: {slack_user_email}")

        except Exception as e:
            # Handle case where social account doesn't exist
            print(f"Could not extract Slack data: {e}")

    # Get query parameter for skill search
    query = request.GET.get('search', '')

    # Filter skills based on search query
    if query:
        skills = Skill.objects.filter(name__icontains=query)
    else:
        skills = Skill.objects.all()

    # Handle form submission
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user_profile)
        if form.is_valid():
            # Get selected skills from form
            skill_ids = request.POST.getlist('skills')
            selected_skills = Skill.objects.filter(id__in=skill_ids)

            # Save the form first to update basic fields
            user = form.save(commit=False)
            user.save()

            # Update the user profile with the selected skills
            from slack_integration.signals import update_slack_profile
            update_slack_profile(user_profile)

            # Now update the many-to-many relationship
            user.skills.clear()
            user.skills.add(*selected_skills)

            # Ensure the form's save_m2m method is called
            form.save_m2m()

            print(f"Updated skills: {[s.name for s in selected_skills]}")

            # Redirect to prevent form resubmission
            return redirect('user_form')
    else:
        # For GET requests, create a new form instance
        form = UserForm(instance=user_profile)

    # Render the template with form and skills
    return render(request, 'user_form.html', {
        'form': form,
        'skills': skills,
        'query': query,
        'user_skills': user_profile.skills.all(),
    })

def update_user_profile(request):
    if request.method == "POST":
        user = request.user  # Get the logged-in user
        skills = request.POST.getlist("skills")  # Get updated skills
        city_id = request.POST.get("city")  # Get updated city

        # Update user's skills
        user.skills.set(Skill.objects.filter(id__in=skills))

        # Update user's city
        if city_id:
            user.city = City.objects.get(id=city_id)
        user.save()

        # The signal will handle the Slack update automatically
        return redirect("profile")

def success(request):
    return render(request, 'success.html')

@csrf_exempt
def slack_skill_search(request):
    if request.method == "POST":
        # Extract data from Slack's request
        slack_data = request.POST

        # Get the text after the slash command
        search_text = slack_data.get('text', '').strip()

        if not search_text:
            return JsonResponse({
                "response_type": "ephemeral",
                "text": "Please provide a skill to search for. Usage: /findskill python"
            })

        # Find users with the requested skill
        try:
            skill = Skill.objects.get(name__iexact=search_text)
            users = User.objects.filter(skills=skill)

            if users:
                # Format the response
                blocks = [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Users with {skill.name} skill:*"
                        }
                    }
                ]

                for user in users:
                    # Format user info with their skills, city, section
                    city = user.city.name if user.city else "No city"
                    section = user.section.name if user.section else "No section"
                    user_skills = ", ".join([s.name for s in user.skills.all()[:5]])

                    blocks.append({
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*<@{user.user_id}>*\n• *Skills:* {user_skills}\n• *City:* {city}\n• *Section:* {section}"
                        }
                    })

                return JsonResponse({
                    "response_type": "in_channel",
                    "blocks": blocks
                })
            else:
                return JsonResponse({
                    "response_type": "ephemeral",
                    "text": f"No users found with skill: {search_text}"
                })

        except Skill.DoesNotExist:
            return JsonResponse({
                "response_type": "ephemeral",
                "text": f"Skill '{search_text}' not found in the database"
            })

    return JsonResponse({"error": "Invalid request"}, status=400)