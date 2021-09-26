from flask import Flask, render_template, url_for, request
from werkzeug.utils import redirect
# from requests.api import request
from home import get_problem_data, get_stats, get_repo, get_file_data

app = Flask(__name__)

@app.route("/", methods = ['GET', 'POST'])
def home():
	data = []
	if request.method == 'GET':
		return render_template('home.html', data = data)
	else:
		name = request.form.get("repo")
		data = get_repo(name)
		if not data:
			return 1
		return redirect(f"/chart/{data[0][1]}")
		# return render_template('home.html', data = data)

@app.route("/chart/<id>", methods=['GET', 'POST'])
def google_pie_chart(id):
	repo_id = id
	problems = get_file_data(repo_id)
	stats = get_stats(repo_id)
	data = {"id": id, "problems": problems, "stats": stats}

	if request.method == 'GET':
		return render_template('pie-chart.html', data=data)
	else:
		json_data = request.form.get('json_data')
		problem_list = get_problem_data(json_data)
		print(problem_list)
		data['problem_list'] = problem_list
		return render_template('pie-chart.html', data=data)

if __name__ == '__main__':
	app.run(debug=True)