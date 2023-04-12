from django import forms
from django.contrib import admin
from .models import Article, Tag, Scope
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet


# class ScopeInline(admin.TabularInline):
#     model = Scope

class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        count = 0
        for form in self.forms:
            if self.deleted_forms and self._should_delete_form(form):
                continue
            if form.cleaned_data.get('is_main'):
                count += 1
            if count > 1:
                raise ValidationError('Основной раздел, - может быть только один.')
            elif count == 0:
                raise ValidationError('Укажите основной раздел')    
            return super().clean()  # вызываем базовый код переопределяемого метода


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline, ]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']    
