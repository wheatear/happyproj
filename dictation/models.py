from django.db import models
import datetime

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

# class WordManager(models.Manager):
#     def create(self,lessonId, word):
#         wd = self.model()
#         wd.lesson_id = lessonId
#         wd.word = word
#         return wd

class Word(models.Model):
    id=models.AutoField(primary_key=True)
    word=models.CharField(max_length=20)
    lesson=models.ForeignKey(Lesson,on_delete=models.CASCADE,db_column='lessonid')
    # objects = WordManager()
    class Meta:
        db_table='lw_word'
    def __str__(self):
        return self.word

class ChoiceSelectedManager(models.Manager):
    def create(self,name,code):
        chse = self.model()
        chse.choicename = name
        chse.setChoicecode(name, code)
        # if name == 'dictype':
        #     chse.choicevalue = code
        #     if code == 'newword':
        #         chse.choicecode = 1
        #     elif code == 'wrongword':
        #         chse.choicecode = 2
        #     else:
        #         chse.choicecode = 3
        # else:
        #     chse.choicecode = code
        return chse

class ChoiceSelected(models.Model):
    choicename=models.CharField(max_length=20,unique=True)
    choicevalue=models.CharField(max_length=100, null=True, blank=True)
    choicecode = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table='lw_choiceselected'
    objects = ChoiceSelectedManager()
    def setChoicecode(self,name,code):
        if name == 'dictype':
            self.choicevalue = code
            if code == 'newword':
                self.choicecode = 1
            elif code == 'wrongword':
                self.choicecode = 2
            else:
                self.choicecode = 3
        else:
            self.choicecode = code

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
        test.testname += datetime.datetime.now().strftime('%y%m%d%H%M%S')
        return test

class Test(models.Model):
    id=models.AutoField(db_column='testid',primary_key=True)
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
    class Meta:
        db_table='lw_test'

class TestWordManager(models.Manager):
    def create(self,testid,wordid, wrong=False):
        testWord = self.model()
        testWord.test_id = testid
        testWord.word_id = wordid
        testWord.wrong = wrong

        return testWord

class TestWord(models.Model):
    test=models.ForeignKey(Test,None,db_column='testid')
    wrong=models.BooleanField(db_column='wrong',default=False)
    word=models.ForeignKey(Word,None,db_column='wordid')
    class Meta:
        db_table='lw_testwords'

    objects = TestWordManager()

class ChoiceManager(models.Manager):
    def create(self, type, name,condition):
        choice = self.model()
        choice.type = type
        choice.name = name
        choice.condition = condition
        return choice

class Choice(models.Model):
    type=models.CharField(max_length=20,db_column='choicetype',default='time')
    name=models.CharField(max_length=50,db_column='choicename')
    condition=models.CharField(max_length=60)

    class Meta:
        db_table='lw_choice'
    objects = ChoiceManager()


