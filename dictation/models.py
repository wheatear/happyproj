from django.db import models

# Create your models here.

class Press(models.Model):
    id=models.AutoField(primary_key=True,db_column='pressid')
    pname=models.CharField(max_length=50)
    class Meta:
        db_table='lw_press'

class Book(models.Model):
    id=models.AutoField(primary_key=True,db_column='bookid')
    bookname=models.CharField(max_length=100)
    grade=models.CharField(max_length=20)
    press=models.ForeignKey('Press',on_delete='', db_column='pressid')
    class Meta:
        db_table='lw_book'

class Unit(models.Model):
    id=models.AutoField(primary_key=True, db_column='unitid')
    unitname=models.CharField(max_length=50)
    book=models.ForeignKey('Book',db_column='bookid')
    class Meta:
        db_table='lw_unit'

class Lesson(models.Model):
    id=models.AutoField(primary_key=True, db_column='lessonid')
    lessoncode=models.CharField(max_length=10)
    lessonname=models.CharField(max_length=50)
    unit=models.ForeignKey(Unit, db_column='unitid')
    class Meta:
        db_table='lw_lesson'
