from django.shortcuts import render
from django.http import HttpResponse
from tasks.models import Task, TaskDetail, Project, Employee
from tasks.forms import TaskModelForm
from django.db.models import Q,Count,Max, Min, Avg, Sum

# Create your views here.
def admin_dashboard(request):
    type = request.GET.get('type', 'all')
    
    counts = Task.objects.aggregate(
        total_tasks = Count('id'),
        completed_tasks = Count('id', filter=Q(status='COMPLETED')),
        pending_tasks = Count('id', filter=Q(status='PENDING')),
        in_progress_tasks = Count('id', filter=Q(status='IN_PROGRESS'))
    )
    base_query = Task.objects.select_related('details'). prefetch_related('assigned_to')

    if type == 'completed':
        tasks = base_query.filter(status='COMPLETED')
    elif type == 'in_progress':
        tasks = base_query.filter(status='IN_PROGRESS')
    elif type == 'pending':
        tasks = base_query.filter(status='PENDING')
    else:
        tasks = base_query.all()

    context = {
        'tasks': tasks,
        'counts': counts
    }
    return render(request, 'dashboard/admin-dashboard.html', context)

def user_dashboard(request):
    return render(request, 'dashboard/user-dashboard.html')

def test(request):
    names = ['John', 'Jane', 'Jim', 'Jill']
    count = 0
    for name in names:
        count += 1
    context = {
        'names': names,
        'age': 23,
        'count': count
    }
    return render(request, 'test.html', context)



def create_task(request):
    form = TaskModelForm()

    if request.method == 'POST':
        form = TaskModelForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'task_form.html', {'form': form, "message": "Task created successfully"}) 
    context = {'form': form}
    return render(request, 'task_form.html', context)

def view_task(request):
    projects = Project.objects.annotate(
        total_tasks = Count('task')).order_by('total_tasks')
    return render(request, 'show_tasks.html', {'projects': projects})
