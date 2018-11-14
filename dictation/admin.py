from django.contrib import admin
from dictation.models import Press,Book,Unit,Lesson,Word

class BookInline(admin.TabularInline):
    model = Book
    extra = 3

class UnitInline(admin.TabularInline):
    model = Unit
    extra = 3

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 3

class WordInline(admin.TabularInline):
    model = Word
    extra = 3

class PressAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    inlines = [BookInline]

class BookAdmin(admin.ModelAdmin):
    list_display = ['id','bookname','name']
    inlines = [UnitInline]

class UnitAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    inlines = [LessonInline]

class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'lessoncode', 'lessonname']
    inlines = [WordInline]

class WordAdmin(admin.ModelAdmin):
    list_display = ['id', 'word']


# Register your models here.
admin.site.register(Press, PressAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Word, WordAdmin)

