import requests
from flask import Flask, render_template, request
import fusion.FusedSpecies as fs 

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def fusion():
    if request.method == 'POST':
        head = request.form.get("headmon")
        body = request.form.get("bodymon")
        result = fs.calculate_fusion(head, body)
        return render_template("results_data.html", result=result)

    return render_template("form.html")