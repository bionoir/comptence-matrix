from django.test import TestCase, LiveServerTestCase
from django.urls import reverse
from selenium import webdriver


class HostTest(LiveServerTestCase):

    def testhomepage(self):
        driver = webdriver.Chrome()
        driver.get('http://127.0.0.1:8000/')
        assert "Questionnary" in driver.title


class UnitTestQuestionnaryHome(TestCase):

    def test_index_page(self):
        response = self.client.get(reverse('questionnary:index'))
        self.assertEqual(response.status_code, 302)
        #self.assertContains(response, "Questionnary")
