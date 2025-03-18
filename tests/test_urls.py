```python
import pytest
from django.urls import reverse, resolve
from testingapp import views

# Happy path test cases

def test_home_url_resolves():
    url = reverse('home')
    assert resolve(url).func == views.home

def test_contact_url_resolves():
    url = reverse('contact')
    assert resolve(url).func == views.contact


# Negative scenario test cases (these assume there's some form of error handling in views.contact)

def test_contact_url_invalid_method(rf): # rf is a RequestFactory fixture
    request = rf.get(reverse('contact'))
    with pytest.raises(Exception) as e: # Replace Exception with specific exception if known
        views.contact(request)
    assert "Method not allowed" in str(e.value) # or adapt based on actual error handling


@pytest.mark.parametrize("invalid_url", ["/contact/invalid", "/invalid"])
def test_contact_url_invalid_path(invalid_url, client):
    response = client.get(invalid_url)
    assert response.status_code == 404 # Or another appropriate status code


# Fixture for RequestFactory (if not already defined in conftest.py)
@pytest.fixture
def rf():
    from django.test import RequestFactory
    return RequestFactory()

@pytest.fixture
def client():
    from django.test import Client
    return Client()

```