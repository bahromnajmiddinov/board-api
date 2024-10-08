# Generated by Django 5.0.8 on 2024-08-16 04:18

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teams', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('is_public', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('participants', models.ManyToManyField(related_name='boards', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='BoardElement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('element_type', models.CharField(max_length=50)),
                ('content', models.TextField(blank=True, null=True)),
                ('x_position', models.FloatField()),
                ('y_position', models.FloatField()),
                ('width', models.FloatField()),
                ('height', models.FloatField()),
                ('rotation', models.FloatField(default=0.0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elements', to='boards.board')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='board_elements', to=settings.AUTH_USER_MODEL)),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='boards', to='teams.team')),
            ],
        ),
        migrations.CreateModel(
            name='BoardSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grid_size', models.PositiveIntegerField(default=10)),
                ('zoom_level', models.PositiveIntegerField(default=1)),
                ('background_color', models.CharField(default='#FFFFFF', max_length=7)),
                ('board', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='settings', to='boards.board')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('color', models.CharField(default='#000000', max_length=7)),
                ('resolve', models.BooleanField(default=False)),
                ('pin', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='boards.board')),
                ('muted', models.ManyToManyField(related_name='muted_comments', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boards', models.ManyToManyField(related_name='projects', to='boards.board')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddIndex(
            model_name='board',
            index=models.Index(fields=['created_at', 'updated_at'], name='boards_boar_created_a4c754_idx'),
        ),
        migrations.AddIndex(
            model_name='board',
            index=models.Index(fields=['title', 'is_public'], name='boards_boar_title_af238d_idx'),
        ),
        migrations.AddIndex(
            model_name='board',
            index=models.Index(fields=['created_by'], name='boards_boar_created_113f44_idx'),
        ),
        migrations.AddIndex(
            model_name='board',
            index=models.Index(fields=['created_at'], name='boards_boar_created_231bdc_idx'),
        ),
        migrations.AddIndex(
            model_name='board',
            index=models.Index(fields=['updated_at'], name='boards_boar_updated_34c39d_idx'),
        ),
    ]
