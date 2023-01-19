# Generated by Django 4.1.5 on 2023-01-19 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_post_cuisine'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='restourant_name',
        ),
        migrations.AlterField(
            model_name='category',
            name='cuisine',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rest_category', to='main.restaurant'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title_of_restourant',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, related_name='restourant_name', to='main.restaurant'),
        ),
    ]