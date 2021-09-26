from flask import Flask, render_template, url_for, request
from werkzeug.utils import redirect
# from requests.api import request
from home import get_stats, get_repo

app = Flask(__name__)

@app.route("/", methods = ['GET', 'POST'])
def home():
    data = []
    if request.method == 'GET':
        return render_template('home.html', data = data)
    else:
        name = request.form.get("repo")
        data = get_repo(name)
        return redirect(f"/chart/{data[0][1]}")
        # return render_template('home.html', data = data)


@app.route("/new_page")
def new_page():
    return "<h1>New Page</h1>"

@app.route("/chart/<id>")
def google_pie_chart(id):
	data = {'Problem' : 'Frequency'}
	data = get_stats(data, id)
	return render_template('pie-chart.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)