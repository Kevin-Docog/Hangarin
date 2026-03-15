from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from taskmanager.models import Task, SubTask, Note, Category, Priority
from taskmanager.forms import TaskForm, SubTaskForm, NoteForm, CategoryForm, PriorityForm
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone

class HomePageView(ListView):
    model = Task
    context_object_name = 'home'
    template_name = "home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Total tasks
        context["total_tasks"] = Task.objects.count()

        # Tasks completed this year
        today = timezone.now().date()
        tasks_completed_this_year = Task.objects.filter(
            status="Completed",
            deadline__year=today.year
        ).count()
        context["tasks_completed_this_year"] = tasks_completed_this_year

        # Total subtasks
        context["total_subtasks"] = SubTask.objects.count()

        # Total notes
        context["total_notes"] = Note.objects.count()

        return context


#Task
class TaskList(ListView):
    model = Task
    context_object_name = 'task'
    template_name = 'task_list.html'
    paginate_by = 10
    ordering = ["title","deadline", "category__name", "status"]

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
        return qs
    
    def get_ordering(self):
        allowed = ["title","deadline", "category__name", "status"]
        sort_by = self.request.GET.get("sort_by")

        if sort_by in allowed:
            return sort_by
        return "title"
    
    

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'task_del.html'
    success_url = reverse_lazy('task-list')


#Sub Task
class SubTaskList(ListView):
    model = SubTask
    context_object_name = 'subtask'
    template_name = 'subtask_list.html'
    paginate_by = 10
    ordering = ["parent_task__title","title"]

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(parent_task__title__icontains=query)
            )
        return qs
    
    def get_ordering(self):
        allowed = ["parent_task__title","title"]
        sort_by = self.request.GET.get("sort_by")

        if sort_by in allowed:
            return sort_by
        return "parent_task__title"

class SubTaskCreateView(CreateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = 'subtask_form.html'
    success_url = reverse_lazy('subtask-list')

class SubTaskUpdateView(UpdateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = 'subtask_form.html'
    success_url = reverse_lazy('subtask-list')

class SubTaskDeleteView(DeleteView):
    model = SubTask
    template_name = 'subtask_del.html'
    success_url = reverse_lazy('subtask-list')


#Note
class NoteList(ListView):
    model = Note
    context_object_name = 'note'
    template_name = 'note_list.html'
    paginate_by = 10
    ordering = ["task__title"]


    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            qs = qs.filter(
                Q(task__title__icontains=query) |
                Q(content__icontains=query)
            )
        return qs
    
    def get_ordering(self):
        allowed = ["task__title"]
        sort_by = self.request.GET.get("sort_by")

        if sort_by in allowed:
            return sort_by
        return "task__title"


class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('note-list')

class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('note-list')

class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'note_del.html'
    success_url = reverse_lazy('note-list')

#Category
class CategoryList(ListView):
    model = Category
    context_object_name = 'category'
    template_name = 'category_list.html'
    paginate_by = 5
    ordering = ["name"]

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            qs = qs.filter(
                Q(name__icontains=query)
            )
        return qs

    def get_ordering(self):
        allowed = ["name"]
        sort_by = self.request.GET.get("sort_by")

        if sort_by in allowed:
            return sort_by
        return "name"


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_form.html'
    success_url = reverse_lazy('category-list')

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_form.html'
    success_url = reverse_lazy('category-list')

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category_del.html'
    success_url = reverse_lazy('category-list')

#Priority
class PriorityList(ListView):
    model = Priority
    context_object_name = 'priority'
    template_name = 'priority_list.html'
    paginate_by = 5
    ordering = ["name"]

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            qs = qs.filter(
                Q(name__icontains=query)
            )
        return qs
    
    def get_ordering(self):
        allowed = ["name"]
        sort_by = self.request.GET.get("sort_by")

        if sort_by in allowed:
            return sort_by
        return "name"

class PriorityCreateView(CreateView):
    model = Priority
    form_class = PriorityForm
    template_name = 'priority_form.html'
    success_url = reverse_lazy('priority-list')

class PriorityUpdateView(UpdateView):
    model = Priority
    form_class = PriorityForm
    template_name = 'priority_form.html'
    success_url = reverse_lazy('priority-list')

class PriorityDeleteView(DeleteView):
    model = Priority
    template_name = 'priority_del.html'
    success_url = reverse_lazy('priority-list')