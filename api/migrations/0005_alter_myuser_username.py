# Generated by Django 3.2.13 on 2022-08-14 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20220814_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='username',
            field=models.CharField(default='646e72c7-8063-4259-9a6f-300b649156ae', editable=False, max_length=100, primary_key=True, serialize=False),
        ),
    ]
