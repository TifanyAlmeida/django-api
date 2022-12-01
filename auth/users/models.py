from django.db import models
from django.contrib.auth.models import AbstractUser
import django.utils.timezone

class User(AbstractUser):
    nome = models.CharField(max_length=255)
    nascimento = models.DateField()
    cpf = models.CharField(max_length=13, unique=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class TentativaLogin(models.Model):
    qtd_acesso_errado = models.IntegerField()#contar automatico
    data = models.DateTimeField(default=django.utils.timezone.now, verbose_name='data')
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE)


class Conta(models.Model):
    agencia = models.IntegerField()
    conta = models.IntegerField(unique=True)
    saldo = models.DecimalField(decimal_places=2, max_digits=8)
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE)


class Cartao(models.Model):
    numero = models.IntegerField(unique=True) # gerar aleatório
    validade = models.DateField()# fazer conta
    cvv = models.IntegerField(unique=True)# gerar aleatório
    limite_credito = models.DecimalField(decimal_places=2, max_digits=8)
    fk_user = models.ForeignKey(User, on_delete=models.PROTECT)


class Transferecia(models.Model):
    descricao = models.CharField(max_length=30)
    PIX = 'P'
    BOLETO = 'B'
    BANCARIA = 'C'

    TIPO_TRANSFERENCIA_CHOICES = [
        (PIX, 'PIX'),
        (BOLETO, 'Boleto'),
        (BANCARIA, 'Bancária'),
    ]
    tipo_transferencia = models.CharField(max_length=1, choices=TIPO_TRANSFERENCIA_CHOICES, default=PIX)
    
    fk_pagador_conta = models.ForeignKey(Conta, on_delete=models.PROTECT, related_name='fk_pagador_conta')#id_conta
    fk_recebedor_conta = models.ForeignKey(Conta, on_delete=models.PROTECT, related_name='fk_recebedor_conta')#id_conta
    valor_transferencia = models.DecimalField(decimal_places=2, max_digits=8)

class Extrato(models.Model):
    data =  models.DateTimeField(default=django.utils.timezone.now, verbose_name='data')
    titulo = models.CharField(max_length=30)
    valor = models.DecimalField(decimal_places=2, max_digits=8)
    tipo = models.CharField(max_length=30)
    fk_pagador = models.IntegerField()
    fk_recebedor = models.IntegerField()
    fk_transferencia = models.ForeignKey(Transferecia, on_delete=models.PROTECT)
    entrada = models.BooleanField()

class Emprestimo(models.Model):
    valor_total_pedido = models.DecimalField(decimal_places=2, max_digits=8)# usuario escolhe
    valor_total_a_pagar = models.DecimalField(decimal_places=2, max_digits=8)# fazer conta dos juros**
    qtd_parcelas = models.IntegerField()# usuario escolhe
    data_pedido =  models.DateTimeField(default=django.utils.timezone.now, verbose_name='data')
    fk_conta = models.ForeignKey(Conta, on_delete=models.PROTECT)


class ParcelaEmprestimo(models.Model):
    valor_parcela = models.DecimalField(decimal_places=2, max_digits=8)
    data_vencimento = models.DateField()
    fk_emprestimo = models.ForeignKey(Emprestimo, on_delete=models.CASCADE, related_name='emprestimo')

