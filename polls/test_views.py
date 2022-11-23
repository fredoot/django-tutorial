import pytest
from django.urls import reverse


class TestViews:
    @pytest.mark.django_db
    def test_index(self, client):
        response = client.get(reverse("polls:index"))
        assert response.status_code == 200
