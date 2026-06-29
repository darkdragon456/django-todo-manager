from django.shortcuts import render,redirect
from todolist.models import Task 
from todolist.forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
import json

@login_required
def homepage(request):

    user_tasks = Task.objects.filter(user=request.user)
    today = timezone.now().date()
    start_of_week =today-timedelta(days=today.weekday())
    week_labels =['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    weekly_data=[7,2,4,1,6,3]

    # use for loop
    for i in range(7):
        current_day=start_of_week + timedelta(days=i)

        count = Task.objects.filter(
            user=request.user,
            is_completed=True,
            completed_at__date=current_day
            
            ).count()
        weekly_data.append(count)

    total_tasks = user_tasks.count()
    completed_tasks = user_tasks.filter(is_completed=True).count()
    pending_tasks = user_tasks.filter(is_completed=False).count()

    recent_tasks = user_tasks.order_by('-id')[:5]

    # Total XP
    total_xp = sum(task.reward_points for task in user_tasks)

    # Level System
    if total_xp < 100:
        level = 'Beginner'
        progress = total_xp

    elif total_xp < 250:
        level = 'Learner'
        progress = total_xp - 100

    elif total_xp < 500:
        level = 'Professional'
        progress = total_xp - 250

    elif total_xp < 1000:
        level = 'Expert'
        progress = total_xp - 500

    else:
        level = 'Master'
        progress = 100

    # Achievements
    if completed_tasks >= 50:
        badge = "👑 Master"

    elif completed_tasks >= 25:
        badge = "🥇 Champion"

    elif completed_tasks >= 10:
        badge = "🥈 Productive"

    elif completed_tasks >= 1:
        badge = "🏅 First Task"

    else:
        badge = "No Badge"

    context = {
        'page': 'Home Page',
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'recent_tasks': recent_tasks,
        'total_xp': total_xp,
        'level': level,
        'progress': progress,
        'badge': badge,
        'week_labels': json.dumps(week_labels),
        'weekly_data': json.dumps(weekly_data),
    }

    return render(request, 'homepage.html', context)

#todo list view
@login_required
def todolist(request):

    if request.method=='POST':
        form_data=TaskForm(request.POST or None)
        if form_data.is_valid():
           task = form_data.save(commit=False)
           task.user = request.user
           task.save()
        messages.success(request,'task added successfully', "🎉 Congratulations! You earned +10 XP.")
        return redirect('todolist')
        messages.error(request,'something went wrong')


    all_tasks = Task.objects.filter(user=request.user).order_by('-id')
    
    paginator = Paginator(all_tasks, 8)
    page = request.GET.get("page")
    

    all_tasks = paginator.get_page(page)

    context={
        'page':'todolist',
        'all_tasks':all_tasks,
        
    }
    return render(request,'todolist.html',context) 
# Delete Task

@login_required
def Delete_task(request,task_id):
    task_obj = Task.objects.get(id=task_id)
    task_obj.delete()
    messages.success(request,'task deleted successfully')
    return redirect('todolist')

# edit task
@login_required
def edit_task(request,task_id):
    task_obj = Task.objects.get(id=task_id)
    if request.method == 'POST':
        form_data=TaskForm(request.POST or None,instance=task_obj)
        if form_data.is_valid():
            form_data.save()
            messages.success(request,'task updated')
            return redirect('todolist')
        messages.success(request,'error in updating task')
    else:
     context={ 
        'task_obj':task_obj
    }
    return render(request,"edit_task.html",context)

    
#complete task
@login_required
def complete_task(request,task_id):
    task_obj = Task.objects.get(id=task_id)
    
    if not task_obj.is_completed:
     task_obj.is_completed = True
     task_obj.reward_points = 10
    

     # save the completion date and time
     task_obj.completed_at = timezone.now()
     task_obj.save()


    # message section to alert the website
     messages.success(request,
     '🎉 Congratulations! Task Completed! ⭐ +10 XP Earned. Keep Going')
    return redirect('todolist')

# pending task
@login_required
def pending_task(request,task_id):
    task_obj = Task.objects.get(id=task_id)
    task_obj.is_completed = False

    # Remove completion date
    task_obj.completed_at = None

    task_obj.reward_points=0
    task_obj.save()

    messages.success(request,'task marked as pending')
    return redirect('todolist')

#contact page
@login_required
def contact(request):
    context={
        'page':'Contact page'
    }
    return render(request,'contact.html',context)

#about page
@login_required
def about(request):
    context={
        'page':'About page'
    }
    return render(request,'about.html',context)  




