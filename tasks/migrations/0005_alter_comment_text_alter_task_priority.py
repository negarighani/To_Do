# Generated by Django 4.2.6 on 2023-11-01 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_alter_task_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('1', 'High Priority'), ('2', 'Medium Priority'), ('3', 'Low Priority')], default='M', max_length=1),
        ),
    ]