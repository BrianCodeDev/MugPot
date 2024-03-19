from django.shortcuts import render, redirect
from .models import Task
from django.shortcuts import render, redirect 
from django.contrib.auth import login, authenticate 
from .forms import SignUpForm 

from .forms import SignUpForm, ProfileForm  # Import the ProfileForm
from .models import Profile

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Retrieve the profile image from the form
            profile_image = request.FILES.get('profile_image')
            if profile_image:
                # Create a profile instance and associate it with the user
                profile = Profile(user=user, image=profile_image)
                profile.save()
            # Authenticate and login the user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            # Redirect to the desired page after signup
            return redirect('app-index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
def index(request):
    if request.method == 'POST':
        # Process the form submission
        task = Task(
            task_name=request.POST['task_name'],
            task_date=request.POST['task_date'],
            task_status=request.POST['task_status'],
            task_info=request.POST['task_info'],
            task_comment=request.POST.get('task_comment', '')  # Use get() to avoid KeyError if task_comment is not in the form
        )
        task.save()  # Save the task object to the database
        return redirect('app-index')  # Redirect to the task change page in Django admin
    else:
        tasks = Task.objects.all()
        user = request.user

        return render(request, 'index.html', {'tasks': tasks, 'user': user})
    
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Task

@csrf_exempt
def update_task_order(request):
    if request.method == 'POST':
        task_ids = request.POST.getlist('task_ids[]')
        for index, task_id in enumerate(task_ids, start=1):
            Task.objects.filter(pk=task_id).update(order=index)
        return JsonResponse({'message': 'Task order updated successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
