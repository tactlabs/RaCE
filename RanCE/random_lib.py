import requests
import random
from bs4 import BeautifulSoup

import requests
import random

def get_random_pypi_package_details():
    # Get a random package name
    random_package_name = get_random_pypi_package_name()

    # Fetch package details from PyPI JSON API
    response = requests.get(f'https://pypi.org/pypi/{random_package_name}/json')

    # Check if the response is successful
    if response.status_code != 200:
        print(f"Failed to fetch details for package {random_package_name}. Status code: {response.status_code}")
        return None

    try:
        # Attempt to parse JSON response
        package_details = response.json()
    except Exception as e:
        # Print response content if JSON decoding fails
        print("Failed to parse JSON response:")
        print(response.text)
        return None

    # Extract relevant information
    package_info = package_details['info']
    release_date = package_details['releases'][package_info['version']][0]['upload_time']

    return {
        'name': package_info['name'],
        'description': package_info['description'],
        'subtitle': package_info['summary'],
        'release_date': release_date
    }

def get_random_pypi_package_name():
    # Fetch list of all package names from PyPI
    response = requests.get('https://pypi.org/simple/')

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to fetch package list. Status code: {response.status_code}")
        return None

    # Parse the HTML response
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <a> tags containing package names
    package_links = soup.find_all('a')

    # Extract package names from the <a> tags
    packages = [link.text.strip() for link in package_links if link.text.strip()]

    # Select a random package name
    return random.choice(packages)

# Call the function to get details about a random package
random_package_details = get_random_pypi_package_details()

def print_divider():

    print('-'*100)

def print_with_divider(content):

    print(content)
    print_divider()

if random_package_details:
    # Print package details
    print_with_divider(f"Package Name: {random_package_details['name']}")
    print_with_divider(f"Description: {random_package_details['description']}")
    print_with_divider(f"Subtitle: {random_package_details['subtitle']}")
    print_with_divider(f"Release Date: {random_package_details['release_date']}")
