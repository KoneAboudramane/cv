# Generated by Django 5.1.7 on 2025-05-24 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generateurcv', '0006_sitelogo'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResumeTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifiant', models.CharField(max_length=100, unique=True)),
                ('nom', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image', models.URLField()),
                ('preview_image', models.URLField()),
                ('premium', models.BooleanField(default=False)),
                ('auteur', models.CharField(max_length=255)),
                ('type', models.CharField(default='CV', max_length=50)),
                ('url', models.CharField(max_length=255)),
            ],
        ),
    ]
