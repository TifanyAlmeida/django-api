from rest_framework import serializers
from .models import User, TentativaLogin, Conta, Cartao, Transferecia, \
Extrato, Emprestimo, ParcelaEmprestimo

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nome', 'nascimento', 'cpf', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class TentativaLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = TentativaLogin
        fields = ['id', 'qtd_acesso_errado', 'data', 'fk_user']


class ContaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conta
        fields = ['id', 'agencia', 'conta', 'saldo', 'fk_user']


class CartaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cartao
        fields = ['id', 'numero', 'validade', 'cvv', 'limite_credito', 'fk_user']



class TransferenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transferecia
        fields = ['id', 'descricao', 'tipo_transferencia', 'fk_pagador_conta', 'fk_recebedor_conta',
         'valor_transferencia']


class ExtratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extrato
        fields = ['id', 'data', 'hora', 'titulo', 'valor', 'fk_transferencia']


class EmprestimoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emprestimo
        fields = ['id', 'valor_total_pedido', 'valor_total_a_pagar', 'qtd_parcelas', 'data_pedido', 'fk_conta']

class  ParcelaEmprestimoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParcelaEmprestimo
        fields = ['id', 'valor_parcela', 'data_vencimento', 'fk_emprestimo']
