import requests
import time

def check_uptime(url):
    while True:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for non-200 status codes
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Application is up and running")
        except requests.exceptions.RequestException as e:
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Application is down: {e}")
        time.sleep(60)  # Check every 60 seconds

if __name__ == "__main__":
    url = input("Enter the URL of the application to monitor: ")
    check_uptime(url)
