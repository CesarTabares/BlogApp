from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.post_list, name='post_list'),
    path('post/<int:pk>', views.post_detail , name='post_detail'),
    path('post/new/' , views.post_new, name='post_new'),
    path('post/<int:pk>/edit', views.post_edit, name='post_edit'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<int:pk>/publish', views.post_publish, name='post_publish'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/remove', views.comment_remove, name='comment_remove'),
    path('comment/<int:pk>/approve', views.comment_approve, name='comment_approve'),


    #vamos a eliminar este path de esta ruta, pq en caso que tengamos en la misma web 2 aplicaciones, el estado de login, debe ser para todas las aplicaciones
    # no solamente blogapp
    #path('accounts/login/', auth_views.LoginView.as_view(), name='login'), #este path, debe ir acompañado de una configuracion en settings ,
    #para que cuando se ingresen los datos de usuario, se redireccione a la pagina de inicio 'post_list'
]
