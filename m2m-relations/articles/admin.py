from django import forms
from django.contrib import admin
from .models import Article, Tag, Scope
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet


class ScopeInline(admin.TabularInline):
    model = Scope

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]

class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        count = 0
        for form in self.forms:
            if form.deleted_forms and self._should_delete_form(form):
                continue
            if self.cleaned_data.get('is_main'):
                count += 1
            if count > 1:
                raise forms.ValidationError('Основной раздел, - может быть только один.')
            elif count == 0:
                raise forms.ValidationError('Укажите основной раздел')    
            return super().clean()  # вызываем базовый код переопределяемого метода

class ScopeInline(admin.TabularInline):
    model = ScopeInline
    formset = ScopeInlineFormset

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']

    
