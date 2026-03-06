from flask import Flask, render_template, request
from processor import process_csv

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():

    results = None

    if request.method == "POST":

        crop = request.form.get("crop")
        file = request.files["file"]

        if file:
            results = process_csv(file, crop)

    return render_template("index.html", results=results)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)