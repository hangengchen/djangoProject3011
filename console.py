import requests
from getpass import getpass


def login_to_service(service_url):
    # Prompt the user for their username and password
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")

    # Make the POST request to the service URL with the username and password
    response = requests.post(
        f"{service_url}/api/login",
        data={"username": username, "password": password}
    )

    # Check if the login was successful
    if response.status_code == 200:
        print("Login successful!")
        return True
    else:
        print("Login failed:", response.text)
        return False


# Usage
if __name__ == "__main__":
    # Get the service URL from the command line input
    service_url = input("Enter the service URL: ")
    login_to_service(service_url)
