import requests


def create_response(status_code, json_body={}):
    response = requests.Response()
    response.status_code = status_code
    response.json = lambda: json_body
    return response
