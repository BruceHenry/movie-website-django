from django.conf.urls import url
from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views
#add reset password from auth django 

urlpatterns = [
    url(r'^login/', views.user_login, name='login'),
    url(r'^logout/', views.user_logout, name='logout'),
    url(r'^register/', views.user_register, name='register'),
    url(r'^facebook/', views.facebook, name='facebook'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html') ,name='password_reset_done'),
    path('password_reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html') ,name='password_reset_confirm'),
    path('password_reset/reset/complete', auth_views.PasswordResetCompleteView.as_view(template_name= "templates/password_reset_complete.html") ,name='password_reset_complete'),
    
    #detail and profile
    url('detail/', views.user_detail, name='detail'),
    path('activate/<uidb64>/',views.activate, name='activate'),  
]
