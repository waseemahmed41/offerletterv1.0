from django.contrib import admin
from .models import Candidate, Template, OfferLetter

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['work_id', 'name', 'email', 'role', 'status', 'created_by_username', 'created_at']
    list_filter = ['status', 'role', 'created_at']
    search_fields = ['name', 'email', 'work_id', 'created_by_username']
    readonly_fields = ['work_id', 'created_at', 'updated_at']
    
    def get_queryset(self, request):
        return Candidate.objects.using('neon').all()

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'is_active', 'created_by_username', 'created_at']
    list_filter = ['role', 'is_active', 'created_at']
    search_fields = ['name', 'created_by_username']
    list_editable = ['is_active']

@admin.register(OfferLetter)
class OfferLetterAdmin(admin.ModelAdmin):
    list_display = ['candidate_work_id', 'template_name', 'sent_at', 'created_at']
    list_filter = ['sent_at', 'created_at']
    search_fields = ['candidate_work_id', 'template_name']
    readonly_fields = ['created_at']
