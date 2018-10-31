# Generated by Django 2.1.1 on 2018-10-25 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(db_column='bookid', primary_key=True, serialize=False)),
                ('bookname', models.CharField(max_length=100)),
                ('grade', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'lw_book',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(db_column='lessonid', primary_key=True, serialize=False)),
                ('lessoncode', models.CharField(max_length=10)),
                ('lessonname', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'lw_lesson',
            },
        ),
        migrations.CreateModel(
            name='Press',
            fields=[
                ('id', models.AutoField(db_column='pressid', primary_key=True, serialize=False)),
                ('pname', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'lw_press',
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(db_column='unitid', primary_key=True, serialize=False)),
                ('unitname', models.CharField(max_length=50)),
                ('book', models.ForeignKey(db_column='bookid', on_delete=django.db.models.deletion.CASCADE, to='dictation.Book')),
            ],
            options={
                'db_table': 'lw_unit',
            },
        ),
        migrations.AddField(
            model_name='lesson',
            name='unit',
            field=models.ForeignKey(db_column='unitid', on_delete=django.db.models.deletion.CASCADE, to='dictation.Unit'),
        ),
        migrations.AddField(
            model_name='book',
            name='press',
            field=models.ForeignKey(db_column='pressid', on_delete=django.db.models.deletion.CASCADE, to='dictation.Press'),
        ),
    ]