from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .serializers import UserSerializer, ContaSerializer, CartaoSerializer, TentativaLoginSerializer, TransferenciaSerializer, ExtratoSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from .models import User, Conta, Cartao, TentativaLogin, Extrato
import jwt, datetime
from datetime import date, timedelta
from random import randint

class RegisterView(APIView):

    def gerar_conta(self):
        self.random_agencia = ''
        self.random_conta = ''

        # agencia
        for i in range(0, 4):
            self.random_agencia += str(randint(0,9))
        
        # conta
        for i in range(0, 8):
            self.random_conta += str(randint(0,9))

        return self.random_agencia, self.random_conta

    # criando a conta
    def criar_conta_automaticamente(self, id_user):
        
        agencia, conta = self.gerar_conta()

        print(id_user)
        minha_conta = {
            "agencia": int(agencia), 
            "conta": int(conta),
            "saldo": 3000,
            "fk_user": id_user, 
        }
        serializer_conta = ContaSerializer(data=minha_conta)
        serializer_conta.is_valid(raise_exception=True)
        serializer_conta.save()
        return Response('ok')


    # criando cartão

    def gerar_cartao(self):

        self.random_numero = ""
        self.random_cvv = ""
        
        # numero
        for i in range(0,8):
            self.random_numero += str(randint(0,9))
        
        # cvv
        for i in range(0,3):
            self.random_cvv += str(randint(0,9))

        # validade
        data_hoje = date.today()
        self.validade =  data_hoje + (timedelta(5*365))

        return self.random_numero, self.validade, self.random_cvv

    def criar_cartao_automaticamente(self, id_user):
        
        numero, validade, cvv = self.gerar_cartao()

        meu_cartao = {

            "numero": int(numero),
            "validade": validade,
            "cvv": int(cvv),
            "limite_credito": 5000,
            "fk_user": id_user
        }

        serializer_cartao = CartaoSerializer(data=meu_cartao)

        serializer_cartao.is_valid(raise_exception=True)
        serializer_cartao.save()
        return Response('ok')

    def post(self, request):

        serializer_register = UserSerializer(data=request.data)
        
        serializer_register.is_valid(raise_exception=True)
        serializer_register.save()
        self.criar_conta_automaticamente(serializer_register.data['id'])
        self.criar_cartao_automaticamente(serializer_register.data['id'])

        return Response(serializer_register.data)


class ContaView(ListAPIView):

    queryset = Conta.objects.all()
    serializer_class = ContaSerializer

class CartaoView(ListAPIView):
    queryset = Cartao.objects.all()
    serializer_class = CartaoSerializer


class LoginView(APIView):

    def registrar_log_acesso(self, id_user):
        
        try:
            item_tentativas = TentativaLogin.objects.get(pk=id_user)

        except TentativaLogin.DoesNotExist:
            item_tentativas = None
        
        if item_tentativas is not None:
            soma_acesso_errado = item_tentativas.qtd_acesso_errado + 1
        else:
            soma_acesso_errado = 1

        meu_log_acesso = {
            "qtd_acesso_errado" : soma_acesso_errado,
            "fk_user" : id_user,
        }

        if item_tentativas is not None:
            serializer_log = TentativaLoginSerializer(item_tentativas, data=meu_log_acesso)
        else:
            serializer_log = TentativaLoginSerializer(data=meu_log_acesso)

        if serializer_log.is_valid():
            serializer_log.save()
            return True
        else:
            print(serializer_log.errors)
            return False
          

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('Usuário não encontrado!')

        if not user.check_password(password):

            self.registrar_log_acesso(user.id)
    
            raise AuthenticationFailed('Senha incorreta!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120),
            'iat': datetime.datetime.utcnow(),
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response



class TentativaLoginView(ListAPIView):
    queryset = TentativaLogin.objects.all()
    serializer_class = TentativaLoginSerializer


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Não Autenticado!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Acesso Expirado!')
        
        user = User.objects.filter(id=payload['id']).first()
        serializer_user = UserSerializer(user)

        return Response(serializer_user.data)

# reutilizar a autenticação e o logout nos outros métodos para limpar os dados
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Deslogou'
        }
        return response


def criar_extrato_automaticamente(self, id_transferencia, descricao, tipo, id_pagador, id_recebedor, valor):
    # verificar de trazer o nome da pessoa
    id_conta_pagador = Conta.objects.get(pk=id_pagador)
    id_conta_recebedor = Conta.objects.get(pk=id_recebedor)

    id_user_pagador = User.objects.get(pk=id_conta_pagador.fk_user)
    id_user_recebedor = User.objects.get(pk=id_conta_recebedor.fk_user)

    nome_pagador = User.objects.filter(id=id_user_pagador).first().nome
    nome_recebedor = User.objects.filter(id=id_user_recebedor).first().nome

    meu_extrato = {
        "titulo": descricao,
        "valor": valor,
        "tipo": tipo,
        "fk_pagador": nome_pagador,
        "fk_recebedor": nome_recebedor,
        "fk_transferencia": id_transferencia
    }

    serializer_extrato = ExtratoSerializer(data=meu_extrato)

    serializer_extrato.is_valid(raise_exception=True)
    serializer_extrato.save()
    return Response('ok')
# entrada ou saida de dinheiro

class TransferenciaView(APIView):
    def post(self, request):

        serializer_transferencia = TransferenciaSerializer(data=request.data)
        
        serializer_transferencia.is_valid(raise_exception=True)
        serializer_transferencia.save()
        pegar_dados = serializer_transferencia.data
        self.criar_extrato_automaticamente(pegar_dados['id'], pegar_dados['descricao'], pegar_dados['tipo_transferencia'], pegar_dados['fk_pagador_conta'], \
            pegar_dados["fk_recebedor_conta"], pegar_dados["valor_transferencia"])


            # fazer a conta de tirar de um e colocar no outro

        return Response(pegar_dados)

class ExtratoView(ListAPIView):

    queryset = Extrato.objects.all()
    serializer_class = ExtratoSerializer

# extrato
# transferencia
# emprestimo
# parcela do emprestimo