from django import forms
from .models import Question, Choice, Answer
from django.core.validators import MaxValueValidator, MinValueValidator


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'question_text'
        ]


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = [
            'answer_text',
            'answer_level'
        ]


class RawAnswerForm(forms.Form):
    answer_text = forms.CharField(max_length=500)
    answer_level = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    other_choice = forms.CharField(max_length=500, required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.question_id = kwargs.pop('question_id')
        print(f'The user for the form is {self.user}')
        super(RawAnswerForm, self).__init__(*args, **kwargs)

    def clean_answer_text(self):
        answer_text = self.cleaned_data.get("answer_text")
        question = Question.objects.filter(pk=self.question_id).get()
        answers_set = Answer.objects.filter(user=self.user, question=question) \
            .values_list('answer_text', flat=True) \
            .distinct()
        if answer_text in answers_set:
            raise forms.ValidationError("Duplicate entry!", code="invalid_choice_duplicate")
        return answer_text

    def clean_other_choice(self):
        answer_text = self.cleaned_data.get("answer_text")
        other_choice = self.cleaned_data.get("other_choice")

        if answer_text == "Other":
            if not other_choice:
                raise forms.ValidationError("Other choice must not be empty!", code="invalid_choice")
            else:
                question = Question.objects.filter(pk=self.question_id).get()
                answers_set = Answer.objects.filter(user=self.user, question=question)\
                                            .values_list('answer_text', flat=True)\
                                            .distinct()
                if other_choice in answers_set:
                    raise forms.ValidationError("Duplicate entry!", code="invalid_choice_duplicate")
                return other_choice
        else:
            return other_choice


