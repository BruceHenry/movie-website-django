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
    path('detail/', views.user_detail, name='detail'),
    path('detail/edit_profile', views.user_detail_edit_profile, name='detail-edit-profile'),
    #add comunity page

    path('comunity/', views.comunity, name='comunity'),

    path('detail/<int:profile_id>/', views.detail_user, name='detail-user'),

    path('activate/<uidb64>/',views.activate, name='activate'),


    path('likePost/', views.like_post, name='like-post'),
    path('reportPost/', views.report_post, name='report-post'),

    path('follow/', views.follow, name='follow'),

    path('seen-noti/', views.seen_noti, name='seen-noti'),

    #test image upload

    path('getdatachart1/', views.get_data_chart1, name='get_data'),
    # path('success', views.success, name='display'),


]
