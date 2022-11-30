from django.urls import path
from .views import RegisterView, ContaView, CartaoView, LoginView, TentativaLoginView, UserView, LogoutView, TransferenciaView, ExtratoView

urlpatterns = [
    path('cadastro/', RegisterView.as_view()),
    path('conta/', ContaView.as_view()),
    path('cartao/', CartaoView.as_view()),

    path('login/', LoginView.as_view()),
    path('tentativa_login/', TentativaLoginView.as_view()),

    path('usuario/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
    
    path('transferencia/', TransferenciaView.as_view()),
    path('extrato/', TransferenciaView.as_view()),

]
