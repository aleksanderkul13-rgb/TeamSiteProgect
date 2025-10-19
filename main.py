from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Важно для безопасности!

@app.route("/")
def index():
    return render_template("main.html")

@app.route("/lamp")
def lamp():
    return render_template("lamp.html")

@app.route("/tplans")
def tplans():
    return render_template("true_plans.html")

@app.route("/fplans")
def fplans():
    return render_template("false_plans.html")

if __name__ == "__main__":
    app.run(debug=True)  # debug=True для разработки
