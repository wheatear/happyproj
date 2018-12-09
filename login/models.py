from django.db import models

# Create your models here.
class User(models.Model):
    '''用户表'''

    gender = (
        ('male', '男'),
        ('female', '女'),
    )

    name=models.CharField(max_length=128,unique=True)
    passwd=models.CharField(max_length=256)
    sex = models.CharField(max_length=32, choices=gender, default='男')
    createTime = models.DateTimeField(auto_now_add=True)
    qq = models.CharField(max_length=32,null=True,blank=True)
    weChat = models.CharField(max_length=64,null=True,blank=True)
    phone = models.CharField(max_length=32,null=True,blank=True)
    eMail = models.CharField(max_length=64,null=True,blank=True)
    realName = models.CharField(max_length=32,null=True)
    school = models.CharField(max_length=64,null=True)
    gradeClass = models.CharField(max_length=64,null=True)

    class Meta:
        db_table='lw_user'
    def __str__(self):
        return self.name

    @classmethod
    def create(cls, user, passwd):
        user = cls(name=user,passwd=passwd)
        return user


