
import sys

from flask import Flask, render_template, request
from forms import InputForm, get_us_states_from_api

app = Flask(__name__)

app.config['SECRET_KEY'] = "Development"

@app.route("/", methods=["GET","POST"])
def index():

    form = InputForm()

    if request.method == "POST":
        if form.validate_on_submit():
            print("Validation successful", file=sys.stderr)
        else:
            print("validation unsuccessful")

    return render_template("states.html", form=form)


@app.route("/search")
def search():
    text = request.args["searchText"]

    result = [c for c in get_us_states_from_api() if text.lower() in c.lower()]
    return {"results": result}


if __name__ == '__main__':
    app.run(host="localhost", port=5001, debug=True)
