from django.urls import path
from . import views

#rotas
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_docente, name='login'),
    path('logout/', views.logout_docente, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('criar_turma/', views.criar_turma, name='criar_turma'),
]
