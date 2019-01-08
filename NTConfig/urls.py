"""nagetiveSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from NTWebsite import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('regist/', views.Regist),
    path('', views.indexView),
    path('uploadImg/', views.UploadImg),
    path('logout/', views.Logout),
    path('CommentSubmit/', views.Comment),
    path('RollCallReplay/', views.RollCallReplay),
    path('LongDissSubmit/', views.CreateUserArticle),
    path('StatisticTaste/', views.StatisticTasteData),
    path('Topics', views.TopicsInfoGet),
    path('Circusee', views.Circusee),
    path('RollCallSquare', views.RollCallSquareInfoGet),
    path('RollCallPublish/', views.RollCallPublish),
    path('SpecialTopicSquare', views.SpecialTopicsSquareInfoGet),
    path('UserProfile', views.UserProfile),
    path('UserProfileUpdate/', views.UserProfileUpdate),
    path('UserLink/', views.Link),
    path('Collect/', views.Collect),
    path('Follow/', views.Follow),
    path('CollectCancel/', views.CollectCancel),
    path('Replay/', views.Replay),
    path('GetNotificationInfo/', views.GetNotificationInfo),
    path('CommentConversation', views.CommentConversation),
    path('RemoveNotificationInfo/', views.RemoveNotificationInfo),
    path('BlackListOperation/', views.BlackListOperation),
    path('PageMiss/', views.PageMiss),
    path('GetParam/', views.GetParam),
    re_path(r'^login/.*$', views.Login),
    re_path(r'^$', views.indexView),
    #re_path(r'^Topics/(?P<section>.*)/(?P<filterValue>.*)$', views.renderView),
]
