"""
Author: Alex R. Mead
Date: April 2025

Dsecription:
Short script to test the AWS API Gateway with a simple GET request.

"""
import pprint
import requests

pp = pprint.PrettyPrinter(indent=2)

url = "https://emjp73uf09.execute-api.us-east-2.amazonaws.com/health"
# url = "https://emjp73uf09.execute-api.us-east-2.amazonaws.com/products"


token = "yiuUgYafa8GmUkftsrMTQEAwJCrbMQwa"
headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get(url, headers=headers)

print(response.status_code)
pp.pprint(response.json())
