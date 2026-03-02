from django.urls import path
from . import views

app_name = 'offers'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('bulk-upload/', views.bulk_upload, name='bulk_upload'),
    path('create-offer/', views.create_offer, name='create_offer'),
    path('templates/', views.templates, name='templates'),
    path('templates/upload/', views.upload_template, name='upload_template'),
    path('templates/edit/<int:template_id>/', views.edit_template, name='edit_template'),
    path('templates/delete/<int:template_id>/', views.delete_template, name='delete_template'),
    path('candidates/', views.candidate_list, name='candidate_list'),
    path('candidate/<int:candidate_id>/', views.CandidateDetailView.as_view(), name='candidate_detail'),
    path('generate-and-send/', views.generate_and_send_offer, name='generate_and_send'),
    path('get-next-work-id/', views.get_next_work_id, name='get_next_work_id'),
    path('cleanup-pdfs/', views.cleanup_pdfs, name='cleanup_pdfs'),
]
