"""Database controller for Admin to add/edit Question and Choice."""
from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    """Custom Choice field for admin to create/edit a question."""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """Custom Question field for admin to create/edit a question."""

    fieldsets = [
        (None, {
            'fields': ['question_text']
        }),
        ('Date information', {
            'fields': ['pub_date', 'end_date'],
            'classes': ['collapse']
        }),
    ]
    inlines = [ChoiceInline]
    list_display = (
        'question_text',
        'pub_date',
        'is_published',
        'end_date',
        'was_closed'
    )
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
