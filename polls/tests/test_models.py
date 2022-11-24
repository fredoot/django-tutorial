import datetime

from django.utils import timezone

from polls.models import Question


class TestQuestionModel:
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_q = Question(pub_date=time)
        assert future_q.was_published_recently() is False

        # self.assertIs(future_q.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_q = Question(pub_date=time)
        assert old_q.was_published_recently() is False

        # self.assertIs(old_q.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        assert recent_question.was_published_recently() is True

        # self.assertIs(recent_question.was_published_recently(), True)
