from flask import Flask, render_template, url_for
from home import get_stats_data

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/new_page")
def new_page():
    return "<h1>New Page</h1>"

@app.route("/chart")
def google_pie_chart():
	data = {}
	data = get_stats_data(data)
	return render_template('pie-chart.html', data=data)

@app.route("/modal")
def modal_page():
    return render_template('modal.html')

if __name__ == '__main__':
    app.run(debug=True)