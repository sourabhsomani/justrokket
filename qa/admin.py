from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin
from qa.models import (Answer, AnswerComment, AnswerVote, Question,
                       QuestionComment, tag, UserQAProfile,BlogContent)

# admin.site.register(Question)
admin.site.register(Answer, MarkdownModelAdmin)
admin.site.register(AnswerComment)
admin.site.register(QuestionComment)
admin.site.register(AnswerVote)
admin.site.register(tag)
admin.site.register(UserQAProfile)
admin.site.register(BlogContent)



class AnswerInline(admin.TabularInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline,]


admin.site.register(Question, QuestionAdmin)