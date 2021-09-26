from flask.wrappers import Response
from requests import get

def get_problem_data():
    response = get('https://dev-api.metabob.com/repository/72/analysis?include=problems')
    if response.status_code == 200:
        problem_list = response.json()['problems']
        problems = {}
        for item in problem_list:
            problem_name = item['category']['name']
            if problem_name in problems.keys():
                problems[problem_name].append([item['id'], item['location'], item['path'], item['explanation']])
            else:
                problems[problem_name] = []
                problems[problem_name].append([item['id'], item['location'], item['path'], item['explanation']])
        return
    else:
        print('failed')
        return 

def get_stats_data(data):
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

problem_list = get_problem_data()

