```python
import pytest
from django.urls import reverse
from django.test import Client

@pytest.fixture
def api_client():
    return Client()

def test_home_happy_path(api_client):
    url = reverse('home')
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from app1!"}

def test_contact_happy_path(api_client):
    url = reverse('contact')
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.json() == {"message": "Contact us!"}

# Negative scenarios are difficult to implement meaningfully without 
#  more context about potential errors (e.g., invalid requests, exceptions).
#  The following are placeholders for negative tests; adapt as needed.

def test_home_invalid_method(api_client):
    url = reverse('home')
    response = api_client.post(url) # Or any other invalid method
    assert response.status_code == 405 # Or appropriate error code


def test_contact_invalid_method(api_client):
    url = reverse('contact')
    response = api_client.post(url) # Or any other invalid method
    assert response.status_code == 405 # Or appropriate error code

#Further negative tests could include:
# - Testing for exception handling within the views (if any are implemented)
# - Testing with different request parameters (if the views accept any)


```