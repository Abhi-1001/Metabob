from flask import Flask, render_template, url_for, request
from werkzeug.utils import redirect
# from requests.api import request
from home import get_problem_data, get_stats, get_file_data, get_repo_ref, analyse

app = Flask(__name__)

@app.route("/", methods = ['GET', 'POST'])
def home():
	data = []
	if request.method == 'GET':
		return render_template('home.html', data = data)
	else:
		input = request.form.get("repo")
		if input.isnumeric():
			input = int(input)
		
		if type(input) == type('str'):
			input = get_repo_ref(input)
			return redirect(f"/chart/{input}")
		elif type(input) == type(0):
			return redirect(f"/chart/{input}")

@app.route("/chart/<id>", methods=['GET', 'POST'])
def google_pie_chart(id):
	ref_id = id
	problems = get_file_data(ref_id)
	stats = get_stats(ref_id)
	data = {"id": id, "problems": problems, "stats": stats}

	if request.method == 'GET':
		return render_template('pie-chart.html', data=data)
	else:
		json_data = request.form.get('json_data')
		problem_list = get_problem_data(json_data, id)
		data['problem_list'] = problem_list
		print(data['problem_list'])
		return render_template('pie-chart.html', data=data)

@app.route("/analysis/<repo_id>/<problem_id>")
def analysis(repo_id, problem_id):
    data = analyse(repo_id, problem_id)
    return render_template("analysis.html", data = data)

if __name__ == '__main__':
	app.run(debug=True)