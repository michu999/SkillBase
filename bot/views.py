from django.shortcuts import render
from .models import User, Skill
from .forms import UserForm
from django.contrib.auth.decorators import login_required

def landing_page(request):
    return render(request, 'landing.html')

@login_required
def user_form_view(request):
    # Get the search query from the GET parameters (default to an empty string if not provided)
    query = request.GET.get('search', '')  # Get search query from the URL (GET parameter)

    # If there is a search query, filter the skills; otherwise, show all skills
    if query:
        skills = Skill.objects.filter(name__icontains=query)  # Case-insensitive search
    else:
        skills = Skill.objects.all()  # Show all skills if no query is provided

    # Handle the POST request for the user form submission
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'success.html', {'form': form})  # Redirect or show success page
    else:
        form = UserForm()

    return render(request, 'user_form.html', {
        'form': form,
        'skills': skills,
        'query': query,  # Pass the query back to the template for the search box
    })



