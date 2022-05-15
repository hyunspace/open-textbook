from django.urls import path
from . import views

app_name = 'anonymouses'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.article_create, name='article_create'),
    path('<int:anonymous_pk>/', views.article_detail, name='article_detail'),
    path('<int:anonymous_pk>/update', views.article_update, name='article_update'),
    path('<int:anonymous_pk>/delete', views.article_delete, name='article_delete'),
    path('<int:anonymous_pk>/like/', views.article_like, name='article_like'),
    path('<int:anonymous_pk>/comment/', views.comment_create, name='comment_create'),
    # path('<int:anonymous_pk>/comment/<int:comment_id>/', views.comment_update, name='comment_update'),
    path('<int:anonymous_pk>/comment/<int:comment_id>/', views.comment_delete, name='comment_delete'),
]