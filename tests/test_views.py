```python
import pytest
from django.urls import reverse
from django.test import Client

# Fixtures (if needed,  none explicitly needed for this simple example)
# @pytest.fixture
# def some_fixture():
#     # ...


def test_home_view_happy_path():
    client = Client()
    url = reverse('home')  # Assuming 'home' is the name in urls.py
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from app1!"}


def test_contact_view_happy_path():
    client = Client()
    url = reverse('contact') # Assuming 'contact' is the name in urls.py
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == {"message": "Contact us!"}


# Negative scenarios (example: testing for unexpected input - not applicable in this case without additional logic in the views)
# def test_home_view_negative_scenario():
#     # Example: Test with invalid input (if applicable)
#     client = Client()
#     url = reverse('home') + "?invalid=param"
#     response = client.get(url)
#     assert response.status_code == 400 # or appropriate status code

# def test_contact_view_negative_scenario():
#     # Example: Test with invalid input (if applicable) -  none explicitly needed here
#     pass


```