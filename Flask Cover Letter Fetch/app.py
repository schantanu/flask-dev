from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def homepage():
    if request.method == 'POST':
        data = request.get_json()
        story = data.get('story')
        if story:
            result = story.upper()
            return jsonify(result=result)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)