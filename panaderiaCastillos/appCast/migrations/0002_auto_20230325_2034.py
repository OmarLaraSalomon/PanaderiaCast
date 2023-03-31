# Generated by Django 3.2.10 on 2023-03-26 02:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('appCast', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lineapedido',
            name='user',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='user',
        ),
        migrations.AddField(
            model_name='pedido',
            name='usuario',
            field=models.CharField(default=django.utils.timezone.now, max_length=90),
            preserve_default=False,
        ),
    ]
