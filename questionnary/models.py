from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=500)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    choice_text = models.CharField(max_length=500)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)

    def __str__(self):
        return self.choice_text

    class Meta:
        ordering = ('question', 'choice_text',)


class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=500)
    answer_level = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s with level %i" % (self.question, self.answer_text, self.answer_level)
