import http.server
import socketserver
import requests
import random
import markdown
from bs4 import BeautifulSoup

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

def generate_index_html(package_details):
    # Convert Markdown description to HTML
    html_description = markdown.markdown(package_details['description'])

    # Generate HTML content for the index page
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Random PyPI Package Details</title>
    </head>
    <body>
        <h1>Package Name: {package_details['name']}</h1>
        <p>Description: {html_description}</p>
        <p>Subtitle: {package_details['subtitle']}</p>
        <p>Release Date: {package_details['release_date']}</p>
        <script>
            // Reload the page on window load to fetch new package details
            window.onload = function() {{
                window.location.reload(true);
            }};
        </script>
    </body>
    </html>
    """

    return html_content

# Set up the HTTP server
PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Get random package details
        random_package_details = get_random_pypi_package_details()

        if random_package_details:
            # Generate HTML content
            html_content = generate_index_html(random_package_details)

            # Send HTTP response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode())

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving at port {PORT}")
    # Serve the current directory
    httpd.serve_forever()
