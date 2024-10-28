from itertools import count
from os.path import pathsep

from django.contrib import admin
from django.db.models import Count
from django.template.response import TemplateResponse
from django.urls import path
from .models import Category, Course, Lesson, Tag, LessonTags


# Register your models here.
class LessonTagsInlineAdmin(admin.TabularInline):
    model = LessonTags
    fk_name = 'lesson'

class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'created_at', 'course')
    list_filter = ('subject', 'created_at', 'course__subject')
    search_fields = ['subject', 'course__subject']
    inlines = [LessonTagsInlineAdmin]


class CourseAppAdminSite(admin.AdminSite):
    site_header = 'Hệ thống khoá học trực tuyến'

    def get_urls(self):
        return [
            path('course-stats/', self.stats_view, name='course-stats')
        ] + super().get_urls()

    def stats_view(self, request):
        course_count = Course.objects.filter(active=True).count()
        course_stats = Course.objects.annotate(lesson_count=Count('lesson')).values('id', 'subject', 'lesson_count')

        course_subjects = [course['subject'] for course in course_stats]
        lesson_counts = [course['lesson_count'] for course in course_stats]

        return TemplateResponse(request, 'admin/course-stats.html', {
            'course_count': course_count,
            'course_stats': course_stats,
            'course_subjects': course_subjects,
            'lesson_counts': lesson_counts
        })


admin_site = CourseAppAdminSite(name='myadmin')

admin_site.register(Category)
admin_site.register(Course)
admin_site.register(Lesson, LessonAdmin)
admin_site.register(Tag)