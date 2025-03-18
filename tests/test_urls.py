```python
import pytest
from django.urls import resolve, reverse
from testingapp import views


@pytest.mark.django_db
class TestUrls:
    def test_home_url_resolves(self):
        """Test that the home URL resolves to the correct view."""
        url = reverse('home')
        assert resolve(url).func == views.home

    def test_home_url_happy_path(self, rf):
        """Test a happy path request to the home view."""
        request = rf.get('/')
        response = views.home(request)
        assert response.status_code == 200  # Or whatever your expected status code is


    def test_contact_url_resolves(self):
        """Test that the contact URL resolves to the correct view."""
        url = reverse('contact')
        assert resolve(url).func == views.contact

    def test_contact_url_happy_path(self, rf):
        """Test a happy path request to the contact view."""
        request = rf.get('/contact/')
        response = views.contact(request)
        assert response.status_code == 200 # Or whatever your expected status code is

    def test_contact_url_post_request(self, rf):
        """Test a POST request to the contact view (example negative scenario)."""
        request = rf.post('/contact/', {'name': 'Test', 'email': 'test@example.com', 'message': 'Test message'})
        response = views.contact(request)
        # Assert based on your contact view's expected behavior for a POST request.  This might involve checking for redirects, database changes, or error messages.  Example:
        assert response.status_code == 302 #Example: Redirects after successful submission


    def test_invalid_url(self, client):
        """Test accessing a non-existent URL."""
        response = client.get('/invalid-url/')
        assert response.status_code == 404 #Or handle accordingly in your views


#Example of a fixture if your views use database interaction.  Adapt as needed.
#@pytest.fixture
#def create_test_data(db):
#    # Create sample data for your tests if necessary.
#    pass

```

**Explanation:**

* **`test_home_url_resolves` and `test_contact_url_resolves`:** These tests verify that the URLs defined in `urls.py` correctly map to their respective view functions using Django's `resolve` and `reverse` functions.  This is a crucial test for URL routing.

* **`test_home_url_happy_path` and `test_contact_url_happy_path`:** These demonstrate a happy path test.  They make GET requests to the URLs and assert that the response status code is as expected (200 - OK).  You'll need to replace `200` with the actual expected status code from your views.

* **`test_contact_url_post_request`:** This illustrates a negative (or edge case) scenario testing the POST request to the contact view.  The assertion here will depend heavily on how your `views.contact` handles POST requests.  It might involve checking for database changes (if you store contact messages), redirects (if you redirect after submission), or error messages (if the form is invalid).

* **`test_invalid_url`:** Tests for a non-existent URL, ensuring that a proper 404 response is returned.

* **Fixtures:**  The commented-out `create_test_data` fixture shows how you might create test data using the `db` fixture (which automatically handles database setup and teardown).  Use this if your views interact with the database.  Remember to uncomment and adapt it to your specific needs.

* **`rf` fixture:** The `rf` fixture (RequestFactory) is used to create mock requests without needing a full Django test client, which makes these tests faster and simpler.


Remember to adapt the assertions (`assert response.status_code == ...`) within the tests to match the expected behavior of your `views.home` and `views.contact` functions.  You'll need to adjust the POST request data and assertions in `test_contact_url_post_request` depending on how your contact form is implemented.  Also, install the `pytest-django` plugin: `pip install pytest-django`.  You'll need to configure your `pytest.ini` file or use `--django-settings-module` in your command line.