import socket
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from threading import Thread, Lock

# Lock for threading
lock = Lock()

# Logo function
def display_logo():
    logo = """
    ███╗   ██╗ ██████╗  ██████╗ ██████╗ ██╗  ██╗
    ████╗  ██║██╔═══██╗██╔═══██╗██╔══██╗██║ ██╔╝
    ██╔██╗ ██║██║   ██║██║   ██║██████╔╝█████╔╝ 
    ██║╚██╗██║██║   ██║██║   ██║██╔═══╝ ██╔═██╗ 
    ██║ ╚████║╚██████╔╝╚██████╔╝██║     ██║  ██╗
    ╚═╝  ╚═══╝ ╚═════╝  ╚═════╝ ╚═╝     ╚═╝  ╚═╝
                 Noob Hacker BD
    """
    print(logo)

# Function to scan a single port
def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            if sock.connect_ex((ip, port)) == 0:
                with lock:
                    print(f"Port {port} is OPEN on {ip}")
    except Exception:
        pass

# Multi-threaded port scanner
def port_scanner(domain, start_port, end_port):
    ip = socket.gethostbyname(domain)
    print(f"Scanning ports on {domain} ({ip})...")
    threads = []
    for port in range(start_port, end_port + 1):
        thread = Thread(target=scan_port, args=(ip, port))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# Function to check for vulnerabilities
def vulnerability_scanner(url):
    print("\nScanning for vulnerabilities...")
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"Website is reachable: {url}")
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Check for XSS vulnerabilities (basic check)
            forms = soup.find_all("form")
            for form in forms:
                print(f"Form detected with action: {form.get('action')}")
                if not form.get("action"):
                    print("Potential vulnerability: Form without action attribute")
            
            # Check for server headers
            print("\nServer Headers:")
            for header, value in response.headers.items():
                print(f"{header}: {value}")
                if "Server" in header and "Apache" in value:
                    print("Potential Issue: Server type is exposed.")

        else:
            print(f"Failed to fetch the website. Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error while scanning vulnerabilities: {e}")

# Main function
def scan_website(url, start_port, end_port):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc or parsed_url.path

    print(f"Starting scan for: {url}")
    port_scanner(domain, start_port, end_port)
    vulnerability_scanner(url)

# Entry point for the script
if __name__ == "__main__":
    display_logo()
    print("Welcome to Noob Hacker BD Tool!\n")
    website = input("Enter the website URL (e.g., https://example.com): ")
    start_port = 1  # Default port range for comprehensive scanning
    end_port = 100  # Adjust as needed
    scan_website(website, start_port, end_port)
