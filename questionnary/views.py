from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext
from .models import Answer, Question
from .forms import RawAnswerForm


class FormModel:
    question = Question()
    form_question = list()
    form_choices = list()
    form_answers = list()

    def __init__(self):
        question = Question()
        self.form_question = list()
        self.form_choices = list()
        self.form_answers = list()


@login_required
def questionnary_about_view(request):
    return render(request, 'questionnary/about.html', {'title': 'About'})


@login_required
def questionnary_answers_view(request):
    msg_questionnary_header = ugettext("QuestionnaryHeader")
    print(f'Message translated is : {msg_questionnary_header}')
    questions = Question.objects.all()

    form_list = list()

    for question in questions:
        form_model = FormModel()
        print(question.pk)
        form_model.form_question.append(question)
        form_model.question = question
        choices = question.choice_set.all()
        for choice in choices:
            form_model.form_choices.append(choice)

        answers = question.answer_set.filter(user=request.user.id)
        for answer in answers:
            form_model.form_answers.append(answer)

        form_list.append(form_model)

    context = {
        'form_list': form_list,
        'quest_header': msg_questionnary_header
    }
    return render(request, 'questionnary/index.html', context)


@login_required
def questionnary_answer_edit(request, question_id):
    print(f'Edition formulaire avec utilisateur : {request.user}')
    my_raw_form = RawAnswerForm(request.POST or None, user=request.user, question_id=question_id)
    if my_raw_form.is_valid():
        print('Data are valid!')
        print(my_raw_form.cleaned_data)
        new_answer = Answer()
        new_answer.user = request.user
        new_answer.question = Question.objects.filter(pk=question_id).get()

        drop_down_text = my_raw_form.cleaned_data["answer_text"]
        if drop_down_text == 'Other':
            new_answer.answer_text = my_raw_form.cleaned_data["other_choice"]
        else:
            new_answer.answer_text = my_raw_form.cleaned_data["answer_text"]

        new_answer.answer_level = my_raw_form.cleaned_data["answer_level"]

        new_answer.save()
        my_raw_form = RawAnswerForm(user=request.user, question_id=question_id)
    else:

        print(my_raw_form.errors)

    question = Question.objects.filter(pk=question_id).get()
    answers = Answer.objects.filter(user=request.user.id, question__pk=question.id)
    choices = question.choice_set.all()

    context = {
        'question_edit': question,
        'answer_list': answers,
        'choice_list': choices,
        'form': my_raw_form,
    }
    return render(request, 'questionnary/edit_answer.html', context)


@login_required
def questionnary_answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    question_id = answer.question.pk

    if request.method == 'POST':
        answer.delete()

    return redirect('questionnary:edit_answer', question_id)

