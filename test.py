import requests

BASE = "http://127.0.0.1:5000"

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MTA0Mzc3NSwianRpIjoiMWM5NjIxY2YtMTYzMS00YzE1LWE4MjctOWE1YjI0MzQxOGM5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Im96ZWJvY2hpZ296aXJpbWNoYXJsZXMyMDIzQGdtYWlsLmNvbSIsIm5iZiI6MTc2MTA0Mzc3NSwiY3NyZiI6IjA3NTI4NjA4LTcyMGUtNDg4ZS1hOTQ3LWMzZjVhYjZlMmUzYyIsImV4cCI6MTc2MTA0NDM3NX0.VdAqjWjKxlXYJk0P3t8x-A2XlAlt9aem7MDAPBQYqw8"

data = {
    "new_password": "newStrongPassword2025"
}

response = requests.post(BASE + f"/reset-password/{token}", json=data)
print(response.json())
