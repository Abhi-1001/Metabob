from flask.wrappers import Response
from requests import get

def get_data():
    response = get('https://dev-api.metabob.com/repository/72/analysis?include=problems')
    if response.status_code == 200:
        obj = response.json()
        problems = obj['problems']
        for item in problems:
            print(item['id'], item['explanation'])
    else:
        print('failed')
    return

def get_stats(data):
    response = get('https://dev-api.metabob.com/repository/72/analysis?include=stats')
    if response.status_code == 200:
        response = response.json()  
        response = response['stats']
        total_responses = response['total_found']
        for item in response['categories']:
            data[item['category']] = item['problem_frequency']
        return data
    else:
        return {}