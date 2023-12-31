# Generated by Django 4.2.4 on 2023-08-14 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_alter_report_writer'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='next_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='다음 단어 ID'),
        ),
        migrations.AddField(
            model_name='post',
            name='prev_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='이전 단어 ID'),
        ),
    ]
