from django import forms

from dasha.models import *


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        exclude = ('date',)


class TeachingMaterialForm(forms.ModelForm):
    class Meta:
        model = TeachingMaterial
        exclude = ('date',)


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ('date',)
