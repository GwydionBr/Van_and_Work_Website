from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", title="Home")

@app.route("/spots")
def spots():
    return render_template("spots.html", title="Spots")

@app.route("/about")
def about():
    return render_template("About.html", title="About")

@app.route("/contact")
def contact():
    return render_template("Kontakt.html", title="Contact")

@app.route("/learn_more")
def learn_more():
    return render_template("Learn_more.html", title="Learn_more")

if __name__ == '__main__':
    app.run(debug=True, port=5001)
