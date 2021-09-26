# from flask.wrappers import Response
from requests import get
from flask.wrappers import Response
from werkzeug.wrappers import ResponseStreamMixin
from run import get_report

def get_problem_data(category_name):
    response = get('https://dev-api.metabob.com/repository/74/analysis?include=problems')
    if response.status_code == 200:
        problem_list = response.json()['problems']
        problems = []
        for item in problem_list:
            problem_name = item['category']['name']
            if problem_name == category_name:
                problems.append([item['id'], item['location'], item['path'], item['explanation']])
        return problems
    else:
        print('failed')
        return 

def get_file_data(ref_id):
    response = get(f'https://dev-api.metabob.com/analysis/{ref_id}/problems/?current_page=0&page_size=100')
    data={}
    if response.status_code == 200:
        response = response.json()
        for item in response['problems']:
            if item['path'] not in data:
                data[item['path']] = [0]*6
            data[item['path']][item['category']['id']] += 1
            
        data = dict(sorted(data.items(), key=lambda x: sum(x[1]), reverse=True))
        return data

def get_stats(ref_id):
    response = get(f'https://dev-api.metabob.com/analysis/{ref_id}?include=stats')
    data = {'Problem' : 'Frequency'}
    if response.status_code == 200:
        response = response.json() 
        response = response['stats']
        total_responses = response['total_found']
        for item in response['categories']:
            data[item['category']] = item['problem_frequency']
        return data
    else:
        return {}

def get_repo(name):
    i = 0
    data = []
    response = get(f'https://dev-api.metabob.com/repositories/?current_page=0&page_size=100')
    response = response.json()
    for rep in response:
        if rep["name"] == name:
            data.append([rep["name"], rep["id"]])
    return data

def get_repo_ref(name):
    data = get_repo(name)
    repo_id = data[0][1]
    response = get(f'https://dev-api.metabob.com/repository/{repo_id}/analysis').json()
    ref_id = response['ref']['id']
    return ref_id


def analyse(repo_id, problem_id):
    response = get(f'https://dev-api.metabob.com/repository/{repo_id}/analysis?include=problems')
    response = response.json()
    for problem in response["problems"]:
        if int(problem["id"]) == int(problem_id):
            return get_report(problem["explanation"])
