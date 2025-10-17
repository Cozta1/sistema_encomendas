from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Autenticação
    path('login/', auth_views.LoginView.as_view(template_name='encomendas/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastro/', views.register, name='register'),

    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Encomendas (CRUD Completo)
    path('encomendas/', views.encomenda_list, name='encomenda_list'),
    path('encomendas/nova/', views.encomenda_create, name='encomenda_create'),
    path('encomendas/<int:pk>/', views.encomenda_detail, name='encomenda_detail'),
    path('encomendas/<int:pk>/editar/', views.encomenda_edit, name='encomenda_edit'),
    path('encomendas/<int:pk>/excluir/', views.encomenda_delete, name='encomenda_delete'),
    
    # Clientes
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('clientes/novo/', views.cliente_create, name='cliente_create'),
    
    # Produtos
    path('produtos/', views.produto_list, name='produto_list'),
    path('produtos/novo/', views.produto_create, name='produto_create'),
    
    # Fornecedores
    path('fornecedores/', views.fornecedor_list, name='fornecedor_list'),
    path('fornecedores/novo/', views.fornecedor_create, name='fornecedor_create'),
    
    # API endpoints
    path('api/produto/<int:produto_id>/', views.api_produto_info, name='api_produto_info'),
    path('api/encomenda/<int:encomenda_pk>/status/', views.api_update_status, name='api_update_status'),
]