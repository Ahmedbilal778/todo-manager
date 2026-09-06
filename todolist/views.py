from django.shortcuts import render, redirect
from todolist.models import Task
from todolist.forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

def homepage(request):
     context ={
          "page":"homepage"
     }
     return render(request, "main.html",context)
@login_required
def todolist(request):
     if request.method == "POST":
          form = TaskForm(request.POST or None)
          if form.is_valid():
               isinstance = form.save(commit=False)
               isinstance.user = request.user
               isinstance.save()
               messages.success(request,"Task added successfully")
               return redirect("todolist")

          messages.error(request,"Something went wrong")
     else:
          form = TaskForm()
     all_tasks = Task.objects.filter(user=request.user)
     paginator = Paginator(all_tasks, 8)  # Show 8 tasks per page
     page_number = request.GET.get('page')
     all_tasks = paginator.get_page(page_number)
     context ={
               "page":"aboutpage",
               'all_tasks': all_tasks,
               'form': form,
     }    
     return render(request, "todolist.html",context)
@login_required
def delete_task(request, task_id):
     task = Task.objects.get(id=task_id)
     if task.user == request.user:
         task.delete()
         messages.success(request,f"Task {task_id} deleted successfully")
     else:
         messages.error(request, "You are not authorized to delete this task.")
     return redirect("todolist")

@login_required
def edit_task(request, task_id):
     task_obj = Task.objects.get(id=task_id)
     if request.method == "POST":
          form_data = TaskForm(request.POST or None, instance=task_obj)
          if form_data.is_valid():
                form_data.save()
                messages.success(request,"Task updated successfully")
                return redirect("todolist")
          messages.error(request,"Something went wrong")
     else:
          form_data = TaskForm(instance=task_obj)
     context = {
          "page":"editpage",
          "task": task_obj
     }
     return render(request, "edit.html", context)

@login_required
def complete_task(request, task_id):
     task_obj = Task.objects.get(id=task_id)
     if task_obj.user == request.user:
       task_obj.is_completed = True
       task_obj.save()
       messages.success(request, "status changed successfully")
     else:
       messages.error(request, "You are not authorized to change this task.") 
     return redirect("todolist") 
@login_required
def pending_task(request, task_id):
     task_obj = Task.objects.get(id=task_id)
     if task_obj.user == request.user:
         task_obj.is_completed = False
         task_obj.save()
         messages.success(request, "status changed successfully")
     else:
         messages.error(request, "You are not authorized to change this task.")
     return redirect("todolist")


def contact(request):
     context ={
               "page":"contactpage"
     }
     return render(request, "contact.html",context)

def about(request):
     context ={
               "page":"aboutpage"
     }
     return render(request, "about.html",context)
