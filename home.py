# from flask.wrappers import Response
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

def get_file_data(repo_id):
    response = get(f'https://dev-api.metabob.com/repository/{repo_id}/analysis')
    data = {}
    if response.status_code == 200:

        ref_id = response.json()['ref']['id']
        response = get(f'https://dev-api.metabob.com/analysis/{ref_id}/problems/?current_page=0&page_size=100')
        
        if response.status_code == 200:
            response = response.json()
            for item in response['problems']:
                if item['path'] not in data:
                    data[item['path']] = [0]*6
                data[item['path']][item['category']['id']] += 1
                
            data = dict(sorted(data.items(), key=lambda x: sum(x[1]), reverse=True))
            return data
    return {}

def get_stats(repo_id):
    response = get(f'https://dev-api.metabob.com/repository/{repo_id}/analysis?include=stats')
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

