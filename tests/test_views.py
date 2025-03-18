```python
import pytest
from django.urls import reverse
from django.test import Client

@pytest.fixture
def api_client():
    return Client()

def test_home_view(api_client):
    url = reverse('home')
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from app1!"}

def test_contact_view(api_client):
    url = reverse('contact')
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.json() == {"message": "Contact us!"}


#Negative scenarios (though there aren't obvious negative scenarios for these simple views, we can test for unexpected methods)

def test_home_view_post_request(api_client):
    url = reverse('home')
    response = api_client.post(url)
    assert response.status_code == 405 # Or another appropriate status code indicating method not allowed


def test_contact_view_post_request(api_client):
    url = reverse('contact')
    response = api_client.post(url)
    assert response.status_code == 405 # Or another appropriate status code indicating method not allowed

```