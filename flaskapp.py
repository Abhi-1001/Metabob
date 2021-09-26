from flask import Flask, render_template, url_for
from home import get_file_data, get_stats

app = Flask(__name__)

@app.route("/")
def home():
	return render_template('home.html')

@app.route("/new_page")
def new_page():
	return "<h1>New Page</h1>"

@app.route("/chart")
def google_pie_chart():
	problems = get_file_data()
	stats = get_stats()
	data = {"problems": problems, "stats": stats}
	return render_template('pie-chart.html', data=data)

if __name__ == '__main__':
	app.run(debug=True)