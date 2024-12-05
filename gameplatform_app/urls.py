from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('minigame/<int:id>/', views.detalhes_minigame, name='detalhes_minigame'),
    path('minigame/<int:id>/avaliar/', views.avaliar_minigame, name='avaliar_minigame'),
    path('minigame/<int:id>/denunciar/', views.denunciar_minigame, name='denunciar_minigame'),
]
