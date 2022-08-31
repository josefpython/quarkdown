from flask import Flask, request, render_template
from os import environ as env
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

#QUARK SETTINGS
LIVE_ACCESS_KEY = env.get("LIVE_ACCESS_KEY")
REPOSITORY_URL = env.get("REPOSITORY_URL")

@app.route("/", methods=["GET"])
def main():
    """
    Serve the main page listing all the articles,
    using landing.html
    """
    return "Hello World"

@app.route("/forceupdate", methods=["POST"])
def force_update():
    """
    The post request must contain the key
    specified when setting up the Quark site.
    If present, the request invokes the Quarkbase.render_article
    and Quarkbase.render_landing methods, updating
    the page with new content in the linked github repository.
    """
    
    key = request.args.get("key", default="", type=str)

    if key == LIVE_ACCESS_KEY:
        return "Updated articles.", 201
    else:
        return "", 401

@app.route("/article/<id>")
def article(id):
    """
    Path to serve rendered articles
    """
    return render_template(id+".html")

if __name__ == "__main__":
    app.run(debug=True)