from flask import Flask, jsonify, redirect, render_template, request
from helper import textsearch, compare


# Config the application
app= Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET"])
def get_index():
    return render_template("/index.html")

@app.route("/search", methods=["POST","GET"])
def get_search():
    if request.method == "POST":
        # get the user input and split it
        text = request.form.get("search").split()

        # handle mutil search
        if len(text) == 3:

            # variable declare
            publish_1 = textsearch(text[0])
            publish_2 = textsearch(text[2])
            operate = text[1]

            if str(operate) != "&" and str(operate) != "+":
                return render_template("apology.html", error ="operate error")

            result = compare(publish_1, publish_2, operate)
            count = len(result)

            return render_template("search.html", result=result, count=count)

                
        elif len(text) == 1:
            result = textsearch(text[0])
            count = len(result)
            return render_template("search.html", result=result, count=count)
        
        else:
            return render_template("apology.html", error="len error" ,text=text)

        


if __name__ == '__main__':
    app.run()