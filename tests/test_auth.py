import pytest
import requests

@pytest.fixture
def api_url():
    return "http://localhost:8000"  # Replace with the actual URL of your FastAPI app


def test_signup(api_url):
    # Create a user object to send in the request
    user_data = {
        "username":"test",
        "email": "test@example.com",
        "password": "testpassword"
    }

    # Send a POST request to the signup endpoint with the user data
    response = requests.post(f"{api_url}/signup", json=user_data)

    # Check the response status code
    assert response.status_code == 200

    # Check if the response message is as expected
    assert response.json() == {"message": "User registered successfully"}

    # Check if attempting to create the same user again raises an HTTPException (user already registered)
    response_duplicate = requests.post(f"{api_url}/signup", json=user_data)
    assert response_duplicate.status_code == 400
    assert response_duplicate.json() == {"detail": "User already registered"}


def test_login(api_url):

    # Now, attempt to log in with the registered user's credentials
    login_data = {
        "username": "test",
        "email": "test@example.com",
        "password": "testpassword"
    }

    # Send a POST request to the login endpoint with the login data
    response_login = requests.post(f"{api_url}/login", json=login_data)

    # Check the response status code for successful login
    assert response_login.status_code == 200
    print(response_login)
    assert "access_token" in response_login.json()