import datetime

import pytest
from django.urls import reverse
from django.utils import timezone

from polls.models import Question


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


@pytest.mark.django_db
class TestIndexViews:
    def test_no_questions(self, client):
        response = client.get(reverse("polls:index"))
        assert response.status_code == 200
        assert b"No polls are available." in response.content
        assert response.context["latest_question_list"].count() == 0

        # self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "No polls are available.")
        # self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_question_exists(self, client):
        question = create_question(question_text="Past question.", days=-30)
        response = client.get(reverse("polls:index"))
        assert response.context["latest_question_list"][0].id == question.id

        """
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [question],
        )
        """

    def test_future_question_not_exists(self, client):
        create_question(question_text="Future question.", days=30)
        response = client.get(reverse("polls:index"))

        assert b"No polls are available" in response.content
        assert response.context["latest_question_list"].count() == 0

        # self.assertContains(response, "No polls are available.")
        # self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_question_not_exists_and_past_question_exists(self, client):
        past_q = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = client.get(reverse("polls:index"))

        assert response.context["latest_question_list"].count() == 1
        assert response.context["latest_question_list"][0] == past_q

        """
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_q],
        )
        """

    def test_two_past_questions_exist(self, client):
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = client.get(reverse("polls:index"))

        q_list = [q for q in response.context["latest_question_list"]]
        assert q_list == [question2, question1]

        """
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )
        """


@pytest.mark.django_db
class TestDetailView:
    def test_future_question_not_found(self, client):
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = client.get(url)

        assert response.status_code == 404

        # self.assertEqual(response.status_code, 404)

    def test_past_question_exists(self, client):
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = client.get(url)

        assert bytes(past_question.question_text, response.charset) in response.content

        # self.assertContains(response, past_question.question_text)
