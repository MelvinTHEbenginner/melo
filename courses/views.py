from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Course, Lesson, Subject
from .forms import CourseForm, LessonForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.views.generic import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff  # Seuls les staff/admin peuvent accéder
    
    def handle_no_permission(self):
        from django.contrib import messages
        messages.error(self.request, "Accès réservé aux administrateurs")
        return redirect('course_list')

class CourseCreateView(AdminRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('course_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return redirect('login')

from django.db.models import Count

class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        subject_slug = self.request.GET.get('subject')
        sort = self.request.GET.get('sort', 'newest')  # Tri par défaut: plus récent
        
        # Filtrage par sujet
        if subject_slug:
            subject = get_object_or_404(Subject, slug=subject_slug)
            queryset = queryset.filter(subject=subject)
        
        # Options de tri
        if sort == 'newest':
            queryset = queryset.order_by('-created')
        elif sort == 'oldest':
            queryset = queryset.order_by('created')
        elif sort == 'popular':
            queryset = queryset.annotate(
                student_count=Count('students')
            ).order_by('-student_count')
        elif sort == 'title_asc':
            queryset = queryset.order_by('title')
        elif sort == 'title_desc':
            queryset = queryset.order_by('-title')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subjects'] = Subject.objects.annotate(
            course_count=Count('courses')
        )
        context['current_sort'] = self.request.GET.get('sort', 'newest')
        return context

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

class LessonDetailView(DetailView): 
    model = Lesson
    template_name = 'courses/lesson_detail.html'
    context_object_name = 'lesson'

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    request.user.courses_joined.add(course)
    return redirect('course_detail', slug=course.slug)



class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'

class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    success_url = reverse_lazy('course_list')

class LessonCreateView(LoginRequiredMixin, CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'courses/lesson_form.html'
    
    def form_valid(self, form):
        module = get_object_or_404(Module, id=self.kwargs['module_id']) # type: ignore
        form.instance.module = module
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('course_detail', kwargs={'slug': self.object.module.course.slug})