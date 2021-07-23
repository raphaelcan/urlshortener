import json

from django.test import Client
from django.test import TestCase

from core.models import ShortURL


def create_url_and_get_short_url(initial_url):
    c = Client()
    response1 = c.post("/create", {"url": initial_url}, content_type="application/json")
    assert response1.status_code == 201
    payload = json.loads(response1.content)
    assert "url" in payload
    url = payload["url"]
    return url


class ShortURLTestCase(TestCase):

    def test_create_url(self):
        initial_url = "https://ravkavonline.co.il"
        c = Client()

        url = create_url_and_get_short_url(initial_url)
        response2 = c.get(f"/s/{url.split('/')[-1]}")
        assert response2.status_code == 302
        assert response2.url == initial_url

    def test_hitting_counter(self):
        initial_url = "https://ravkavonline.co.il"
        c = Client()

        url = create_url_and_get_short_url(initial_url)
        short_url = url.split('/')[-1]

        for i in range(10):
            c.get(f"/s/{short_url}")
        counter = ShortURL.objects.get(short_url=short_url).counter
        assert ShortURL.objects.get(short_url=short_url).counter == 10

    def test_non_existing_url(self):
        c = Client()
        response = c.get("/s/112d0")
        assert response.status_code == 404

    def test_create_url_with_bad_format(self):
        c = Client()
        response = c.post("/create", {"url": "badformaturl"}, content_type="application/json")
        assert response.status_code == 422

    def test_create_url_without_post(self):
        initial_url = "https://ravkavonline.co.il"

        c = Client()
        response = c.patch("/create", {"url": initial_url}, content_type="application/json")
        assert response.status_code == 405

        response = c.put("/create", {"url": initial_url}, content_type="application/json")
        assert response.status_code == 405

        response = c.get("/create", {"url": initial_url}, content_type="application/json")
        assert response.status_code == 405
