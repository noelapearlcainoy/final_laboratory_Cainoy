from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_view, name='login'),              
    path('signup/', views.signup_view, name='signup'),     
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('report/', views.report_item, name='report'),     
    path('edit-profile/', views.edit_profile, name='edit_profile'),  
    path('logout/', views.logout_view, name='logout'),
    path('claim/<int:pk>/', views.claim_item, name='claim'),  
    path('confirm-claim/<int:pk>/', views.confirm_claim, name='confirm_claim'),

]

# Serve media files (images)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
