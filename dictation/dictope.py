#!/usr/bin/env python

import os,sys
import datetime



pathname = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, pathname)
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "happyproj.settings")


import django
django.setup()

from dictation.models import Test,User

if __name__ == "__main__":
    dateScope = datetime.datetime.now().date() - datetime.timedelta(days=1)
    testToday = Test.tests.filter(testtime__gte=dateScope)
    print('there are %d testes tested today:' % testToday.count())
    # print(['%s%s' % (t.testname,os.linesep) for t in testToday])
    for t in testToday:
        print('%s' % (t.testname) )

    usersTody = User.objects.filter(createTime__gte=dateScope)
    print('there are %d users added today:' % usersTody.count())
    # print(['%s%s' % (t.testname,os.linesep) for t in testToday])
    for u in usersTody:
        print('%s %s' % (u.name, u.realName))

pass
