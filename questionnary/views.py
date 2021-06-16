from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.forms import formset_factory
from django.shortcuts import render, redirect,get_object_or_404
from django.utils.translation import ugettext
from .models import Answer, Question, Choice, Translations, KeyWords
from .utility_classes import QuestionTranslation
from .forms import RawAnswerForm, QuestionForm, QuestionFormNoModel, LanguageTradForm


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
    print(f'Form data: {my_raw_form}')
    if my_raw_form.is_valid():
        print('Data are valid!')
        print(my_raw_form.cleaned_data)
        new_answer = Answer()
        new_answer.user = request.user
        new_answer.question = Question.objects.filter(pk=question_id).get()

        drop_down_text = my_raw_form.cleaned_data["answer_text"]
        if drop_down_text == 'Other':
            new_answer.answer_text = my_raw_form.cleaned_data["other_choice"]
            # Adding the new choice to the list of available skills
            new_choice = Choice()
            new_choice.choice_text = new_answer.answer_text
            new_choice.question = new_answer.question
            new_choice.save()
        else:
            new_answer.answer_text = my_raw_form.cleaned_data["answer_text"]

        new_answer.answer_level = my_raw_form.cleaned_data["answer_level"]

        new_answer.save()
        my_raw_form = RawAnswerForm(user=request.user, question_id=question_id)
    else:
        print(f'ERRORS! ===> {my_raw_form.errors}')

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


@login_required
def questionnary_admin_view(request):
    questions = Question.objects.all()

    question_to_display = list()

    print(request.LANGUAGE_CODE)

    for question in questions:
        question_translation = QuestionTranslation()
        question_translation.question_tag = question.question_text
        question_translation.translation_text = 'TODO'

        print(question.question_text)
        keyword = KeyWords.objects.filter(key_word=question.question_text).first()

        if keyword:
            available_translations = Translations\
                                        .objects\
                                        .filter(key_word=keyword.id)\
                                        .filter(language_code=request.LANGUAGE_CODE)\
                                        .first()
            if available_translations:
                question_translation.translation_text = available_translations.translation

        question_to_display.append(question_translation)

    context = {
        'questions_to_display': question_to_display
    }
    return render(request, 'questionnary/admin/admin_view_question.html', context)


@login_required
@permission_required('questionnary.add_question', raise_exception=True)
def questionnary_admin_create_view(request):
    extra_number = len(settings.LANGUAGES)
    LanguageTradFormSet = formset_factory(LanguageTradForm, extra=extra_number)

    if request.method == 'POST':
        form_question = QuestionFormNoModel(request.POST)
        form_lang_tradset = LanguageTradFormSet(request.POST)
        if form_question.is_valid() and form_lang_tradset.is_valid():
            print(form_question.cleaned_data)
            for form_lang in form_lang_tradset:
                print(form_lang.cleaned_data)
            #new_question = Question()
            #new_question.question_text = form_question.cleaned_data["question_text"]
            #new_question.save()
        else:
            print(f'Errors recovered {form_lang_tradset.errors}')
    else:
        form_question = QuestionFormNoModel()
        form_lang_tradset = LanguageTradFormSet()

    context = {
        'form_question': form_question,
        'form_lang_tradset': form_lang_tradset,
    }
    return render(request, 'questionnary/admin/admin_create_question.html', context)

    # form_question = QuestionFormNoModel(request.POST or None)
    #
    #
    # if form_question.is_valid():
    #     new_question = Question()
    #     new_question.question_text = form_question.cleaned_data["question_text"]
    #     new_question.save()
    # else:
    #     print(f'Errors:{form_question.errors}')
    #
    # context = {
    #     'form': form_question,
    # }
    #
    # return render(request, 'questionnary/admin/admin_input_question.html', context)
