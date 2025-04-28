from django.contrib import admin
from .models import Subject, Course, Module, Lesson

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}

class ModuleInline(admin.StackedInline):
    model = Module

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'owner')
    list_filter = ('subject',)
    search_fields = ('title', 'overview')

admin.site.register(Course, CourseAdmin)

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    list_filter = ['course']
    search_fields = ['title', 'description']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'order']
    list_filter = ['module']
    search_fields = ['title', 'content']