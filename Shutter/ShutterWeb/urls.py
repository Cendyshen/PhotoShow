from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth



urlpatterns = [
    # home page will be redirected to album_scenery_new.html
    url(r'^$', views.index, name='index'),

    # forum
    url(r'^forum/$',views.forum, name='forum'),
    url(r'^hot_topic/$', views.hot_topic, name='hot_topic'),
    url(r'^topic/(?P<topic_id>[0-9]+)/$', views.topic, name='topic'),
    url(r'^add_topic/$', views.add_topic, name='add_topic'),

    # message
    url(r'^inbox/$', views.inbox, name='inbox'),
    # url(r'^message_detail/$', views.message_detail, name='message_detail'),
    url(r'^message_detail/(?P<message_id>[0-9]+)/$', views.message_detail, name='message_detail'),

    # news
    # url(r'^news/$', views.news_list, name='news_list'),
    url(r'^news_content/(?P<news_id>[0-9]+)/$', views.news_content, name='news_content'),
    url(r'^news_list/$', views.news_list, name='news_list'),

    # album
    url(r'^album/$', views.index, name='album'),
    url(r'^album/scenery/$', views.index, name='scenery'),
    url(r'^album/scenery/new/$', views.album_scenery_new, name='album_scenery_new'),
    url(r'^album/scenery/hot/$', views.album_scenery_hot, name='album_scenery_hot'),
    url(r'^album/people/new/$', views.album_people_new, name='album_people_new'),
    url(r'^album/people/hot/$', views.album_people_hot, name='album_people_hot'),
    url(r'^album/photo/(\d+)/$', views.album_photo, name='album_photo'),
    url(r'^album/upload_image/$', views.album_upload_image, name='album_upload_image'),
    url(r'^album/thumbs_up/(\d+)/$', views.thumbs_up, name='thumbs_up'),
    url(r'^album/delete_photo/(\d+)/$', views.delete_photo, name='delete_photo'),
    url(r'^album/delete_comment/(\d+)/$', views.delete_comment, name='delete_comment'),

    # login,logout,register,change password,password reset by email
    url(r'^login/$', views.user_login, name="login"),
    url(r'^logout/$', views.user_logout, name="logout"),
    url(r'^register/', views.register, name='register'),
    url(r'^forget/$', views.register, name='register'),
    url(r'^info/', views.Userinfo, name='info'),
    url(r'^edit_profile/', views.editprofile, name='edit_profile'),

    url(r'^pwdc/$', auth.PasswordChangeView.as_view(
        template_name='password_change_form.html'), name='password_change'),
    url(r'^pwdd/$', auth.PasswordChangeDoneView.as_view(
        template_name='password_change_done.html'), name='password_change_done'),

    url(r'^reset_form$', auth.PasswordResetView.as_view(template_name='password_reset_form.html'),
        name='password_reset'),
    url(r'^reset_done$', auth.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), name='password_reset_done'),
    url(r'^reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^reset_complete/$',
        auth.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),

]



