import logging
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Task
from .forms import TaskForm

audit_logger = logging.getLogger("audit")

@login_required
def task_list(request):
    if request.user.is_staff:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(owner=request.user)
    return render(request, "tasks/task_list.html", {"tasks": tasks})

@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()

            audit_logger.info(f"CREATE | user={request.user.username} | task_id={task.id} | title={task.title}")
            return redirect("task_list")
    else:
        form = TaskForm()

    return render(request, "tasks/task_create.html", {"form": form})

@require_POST
@login_required
def task_delete(request, task_id):
    # Admin/staff: boleh delete semua tasks
    if request.user.is_staff:
        task = get_object_or_404(Task, id=task_id)
    else:
        # Normal user: boleh delete task sendiri sahaja (anti-IDOR)
        task = get_object_or_404(Task, id=task_id, owner=request.user)

    audit_logger.info(f"DELETE | user={request.user.username} | task_id={task.id} | title={task.title}")
    task.delete()
    return redirect("task_list")

@staff_member_required
def admin_task_list(request):
    tasks = Task.objects.all()
    return render(request, "tasks/admin_task_list.html", {"tasks": tasks})

@login_required
def task_update(request, task_id):
    if request.user.is_staff:
        task = get_object_or_404(Task, id=task_id)
    else:
        # anti-IDOR: users can only edit their own tasks
        task = get_object_or_404(Task, id=task_id, owner=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            updated = form.save()
            audit_logger.info(f"UPDATE | user={request.user.username} | task_id={updated.id} | title={updated.title}")
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)

    return render(request, "tasks/task_update.html", {"form": form, "task": task})
