# Generated by Django 2.2.1 on 2019-05-10 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='YibanUser',
            fields=[
                ('user_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('today', models.IntegerField()),
                ('history', models.CharField(default='{}', max_length=10000)),
            ],
        ),
    ]
