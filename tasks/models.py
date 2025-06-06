from django.db import models
from django.db import connection

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=250)
    start_date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]
    project = models.ForeignKey(
        Project,
        on_delete = models.CASCADE,
        default = 1)
    assigned_to = models.ManyToManyField(Employee, related_name = 'tasks')
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TaskDetail(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    PRIORITY_CHOICES =[
        (HIGH,'High'),
        (MEDIUM,'Medium'),
        (LOW,'Low'),
    ]
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='details')
    assigned_to = models.CharField(max_length=250)
    priority = models.CharField(
        max_length=1, choices=PRIORITY_CHOICES,default=LOW)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f'Details form Task {self.task.title}'





    