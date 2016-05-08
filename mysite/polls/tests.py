import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Question

def create_question(question_text,days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date=time)

class QuestionIndexDetailTest(TestCase):
    def test_detail_view_with_a_future_question(self):
        future_question = create_question(question_text='Future question',days=5)
        response = self.client.get(reverse('polls:detail',args=(future_question.id)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_question(self):
        past_question = create_question(question_text='Past question', days=-5)
        response = self.client.get(reverse('polls:detail',args=(past_question.id)))
        self.assertContains(response, past_question.question_text, status_code=200)

class QuestionViewTest(TestCase):
    def test_index_view_with_no_question(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are aveilable")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],['<Question: Past question.>']
        )

    def test_index_view_with_a_future_question(self):
        create_question(question_text='Future Questin',days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response,'No Polls are Avaible',status_code=200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index__view_with_future_and_past_question(self):
        create_question(question_text='Past Question', days=-30)
        create_question(question_text='Future Question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question>'])

    def test_index_view_with_two_past_question(self):
        create_question(question_text='Past question 1', days=-30)
        create_question(question_text="Past question 2" , days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question 2.>', '<Question: Past question 1.>'])
