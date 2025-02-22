from django import forms
from .models import Quiz, Question, Answer
from django.forms import inlineformset_factory

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'total_timer', 'question_count', 'logo']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows':4}),
            'total_timer': forms.NumberInput(attrs={'class': 'form-control'}),
            'question_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'time_limit', 'photo']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
            'time_limit': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'photo', 'is_correct']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# Створимо inline formset-и
QuestionFormSet = inlineformset_factory(Quiz, Question, form=QuestionForm,
                                         fields=['text', 'time_limit', 'photo'], extra=1, can_delete=True)

AnswerFormSet = inlineformset_factory(Question, Answer, form=AnswerForm,
                                       fields=['text', 'photo', 'is_correct'], extra=2, min_num=2, validate_min=True,
                                       max_num=6, validate_max=True, can_delete=True)
