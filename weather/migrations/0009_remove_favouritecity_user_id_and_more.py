# Generated by Django 5.0.4 on 2024-05-06 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0008_userdetails_cognito_user_userdetails_is_verified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favouritecity',
            name='user_id',
        ),
        migrations.AddField(
            model_name='favouritecity',
            name='cognito_user',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='UserDetails',
        ),
    ]
