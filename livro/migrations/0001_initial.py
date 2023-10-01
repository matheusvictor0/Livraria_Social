# Generated by Django 4.2.5 on 2023-09-13 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Livros',
            fields=[
                ('isbn', models.TextField(primary_key=True, serialize=False, unique=True)),
                ('nome', models.CharField(max_length=100)),
                ('autor', models.CharField(max_length=30)),
                ('capa_url', models.URLField()),
                ('descricao', models.TextField(max_length=100)),
                ('genero', models.CharField(default='Outros', max_length=100)),
            ],
        ),
    ]