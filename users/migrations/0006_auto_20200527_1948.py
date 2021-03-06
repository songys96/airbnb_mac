# Generated by Django 3.0.6 on 2020-05-27 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200511_2039'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='login_method',
            field=models.CharField(blank=True, choices=[('signup', 'Signup'), ('github', 'Github'), ('kakao', 'Kakao')], default='signup', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='currency',
            field=models.CharField(blank=True, choices=[('usd', 'USD'), ('krw', 'KRW')], default='krw', max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.CharField(blank=True, choices=[('english', 'Eng'), ('korea', 'Kor')], default='korea', max_length=10, null=True),
        ),
    ]
