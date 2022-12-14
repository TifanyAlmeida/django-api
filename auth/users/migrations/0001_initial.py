# Generated by Django 4.1.3 on 2022-12-01 01:32

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nome', models.CharField(max_length=255)),
                ('nascimento', models.DateField()),
                ('cpf', models.CharField(max_length=13, unique=True)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Conta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agencia', models.IntegerField()),
                ('conta', models.IntegerField(unique=True)),
                ('saldo', models.DecimalField(decimal_places=2, max_digits=8)),
                ('fk_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Emprestimo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_total_pedido', models.DecimalField(decimal_places=2, max_digits=8)),
                ('valor_total_a_pagar', models.DecimalField(decimal_places=2, max_digits=8)),
                ('qtd_parcelas', models.IntegerField()),
                ('data_pedido', models.DateTimeField(default=django.utils.timezone.now, verbose_name='data')),
                ('fk_conta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.conta')),
            ],
        ),
        migrations.CreateModel(
            name='Transferecia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=30)),
                ('tipo_transferencia', models.CharField(choices=[('P', 'PIX'), ('B', 'Boleto'), ('C', 'Banc??ria')], default='P', max_length=1)),
                ('valor_transferencia', models.DecimalField(decimal_places=2, max_digits=8)),
                ('fk_pagador_conta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fk_pagador_conta', to='users.conta')),
                ('fk_recebedor_conta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fk_recebedor_conta', to='users.conta')),
            ],
        ),
        migrations.CreateModel(
            name='TentativaLogin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qtd_acesso_errado', models.IntegerField()),
                ('data', models.DateTimeField(default=django.utils.timezone.now, verbose_name='data')),
                ('fk_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ParcelaEmprestimo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_parcela', models.DecimalField(decimal_places=2, max_digits=8)),
                ('data_vencimento', models.DateField()),
                ('fk_emprestimo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emprestimo', to='users.emprestimo')),
            ],
        ),
        migrations.CreateModel(
            name='Extrato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(default=django.utils.timezone.now, verbose_name='data')),
                ('titulo', models.CharField(max_length=30)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=8)),
                ('tipo', models.CharField(max_length=30)),
                ('fk_pagador', models.IntegerField()),
                ('fk_recebedor', models.IntegerField()),
                ('entrada', models.BooleanField()),
                ('fk_transferencia', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.transferecia')),
            ],
        ),
        migrations.CreateModel(
            name='Cartao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField(unique=True)),
                ('validade', models.DateField()),
                ('cvv', models.IntegerField(unique=True)),
                ('limite_credito', models.DecimalField(decimal_places=2, max_digits=8)),
                ('fk_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
