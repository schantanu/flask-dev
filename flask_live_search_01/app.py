import sys

from flask import Flask, render_template, request

from forms import InputForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "Development"

US_STATES = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", "Connecticut", "District ", "of Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]

@app.route("/", methods=["GET","POST"])
def index():

    form = InputForm()

    if request.method == "POST":

        print(form.states.data, file=sys.stderr)
        print(form.territory.data, file=sys.stderr)
        print("Hello from outside Validate.", file=sys.stderr)

        if form.validate_on_submit():
            print(form.states.data, file=sys.stderr)
            print(form.territory.data, file=sys.stderr)
            print("Hello from inside Validate.", file=sys.stderr)
        else:
            print(form.errors)

    return render_template("states.html", form=form)


@app.route("/search")
def search():
    text = request.args["searchText"]

    result = [c for c in US_STATES if text.lower() in c.lower()]
    return {"results": result}


if __name__ == '__main__':
    app.run(host="localhost", port=5001, debug=True)