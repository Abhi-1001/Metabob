from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/new_page")
def new_page():
    return "<h1>New Page</h1>"

if __name__ == '__main__':
    app.run(debug=True)