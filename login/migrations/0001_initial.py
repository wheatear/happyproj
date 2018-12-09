# Generated by Django 2.1.1 on 2018-12-09 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('passwd', models.CharField(max_length=256)),
                ('sex', models.CharField(choices=[('male', '男'), ('female', '女')], default='男', max_length=32)),
                ('createTime', models.DateTimeField(auto_now_add=True)),
                ('qq', models.CharField(blank=True, max_length=32, null=True)),
                ('weChat', models.CharField(blank=True, max_length=64, null=True)),
                ('phone', models.CharField(blank=True, max_length=32, null=True)),
                ('eMail', models.CharField(blank=True, max_length=64, null=True)),
                ('realName', models.CharField(max_length=32, null=True)),
                ('school', models.CharField(max_length=64, null=True)),
                ('gradeClass', models.CharField(max_length=64, null=True)),
            ],
            options={
                'db_table': 'lw_user',
            },
        ),
    ]