from flask import Flask, jsonify, redirect, render_template, request
from helper import textsearch, compare, preprocess, predict


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

@app.route("/search", methods=["POST"])
def get_search():
    if request.method == "POST":
        # get the user input and split it
        text = request.form.get("search").split()

        # handle mutil search
        if len(text) == 3:

            # variable declare
            publish_1, author_1, link_1 = textsearch(text[0])
            publish_2, author_2, link_2 = textsearch(text[2])
            operate = text[1]

            if str(operate) != "&" and str(operate) != "+":
                return render_template("apology.html", error ="operate error")

            publish, author, link = compare(publish_1, publish_2, author_1, author_2, link_1, link_2, operate)
            count = len(publish)
            
            forecast = predict(preprocess(publish))

            return render_template("searched.html", publish=publish, author=author, link=link, forecast=forecast,count=count)

                
        elif len(text) == 1:
            publish, author, link = textsearch(text[0])
            count = len(publish)

            forecast = predict(preprocess(publish))

            return render_template("searched.html", publish=publish, author=author, link=link, forecast=forecast,count=count)
        
        else:
            return render_template("apology.html", error="len error" ,text=text)

        


if __name__ == '__main__':
    app.run()