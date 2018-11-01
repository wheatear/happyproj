from django.db import models

# Create your models here.

class Press(models.Model):
    id=models.AutoField(primary_key=True,db_column='pressid')
    name=models.CharField(max_length=50,db_column='pname')
    class Meta:
        db_table='lw_press'
    def __str__(self):
        return self.name

class Book(models.Model):
    id=models.AutoField(primary_key=True,db_column='bookid')
    bookname=models.CharField(max_length=100,db_column='bookname')
    name=models.CharField(max_length=20,db_column='grade')
    press=models.ForeignKey('Press',models.CASCADE, db_column='pressid')
    class Meta:
        db_table='lw_book'
    def __str__(self):
        return self.name

class Unit(models.Model):
    id=models.AutoField(primary_key=True, db_column='unitid')
    name=models.CharField(max_length=50,db_column='unitname')
    book=models.ForeignKey('Book',on_delete=models.CASCADE,db_column='bookid')
    class Meta:
        db_table='lw_unit'
    def __str__(self):
        return self.name

class Lesson(models.Model):
    id=models.AutoField(primary_key=True, db_column='lessonid')
    lessoncode=models.CharField(max_length=10)
    lessonname=models.CharField(max_length=50)
    unit=models.ForeignKey(Unit, on_delete=models.CASCADE,db_column='unitid')
    class Meta:
        db_table='lw_lesson'
    def __str__(self):
        return '%s %s' % (self.lessoncode, self.lessonname)

class Word(models.Model):
    id=models.AutoField(primary_key=True)
    word=models.CharField(max_length=20)
    lesson=models.ForeignKey(Lesson,None,db_column='lessonid')
    class Meta:
        db_table='lw_word'
    def __str__(self):
        return self.word

class ChoiceSelected(models.Model):
    choicename=models.CharField(max_length=20)
    choicevalue=models.CharField(max_length=100)
    choicecode = models.IntegerField()
    class Meta:
        db_table='lw_choiceselected'

class TestManager(models.Manager):
    def create(self,press,book,unit=None,lesson=None):
        test = self.model()
        test.press = press
        test.book = book
        test.unit = unit
        test.lesson = lesson
        test.testname = book.bookname
        if lesson:
            test.testname += lesson.lessonname
        elif unit:
            test.testname += unit.name

class Test(models.Model):
    id=models.IntegerField(db_column='testid',primary_key=True)
    testtime=models.DateTimeField(auto_now_add=True)
    testname=models.CharField(max_length=50)
    testcontent=models.CharField(max_length=200,null=True)
    level=models.CharField(max_length=20,null=True)
    type=models.CharField(max_length=20)
    press=models.ForeignKey(Press,None,db_column='pressid')
    book = models.ForeignKey(Book, None, db_column='bookid')
    unit = models.ForeignKey(Unit, None, db_column='unitid',null=True)
    lesson = models.ForeignKey(Lesson, None, db_column='lessonid',null=True)

    tests = TestManager()

