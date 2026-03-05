from flask import Flask, render_template, request, jsonify
import numpy as np
from scipy.stats import t
from statistics import stdev
import os

app = Flask(__name__)

alpha = 0.05


def twottest(a, b, alt):

    n1 = len(a)
    n2 = len(b)

    x1 = np.mean(a)
    x2 = np.mean(b)

    sd1 = stdev(a)
    sd2 = stdev(b)

    se = np.sqrt((sd1**2 / n1) + (sd2**2 / n2))

    t_cal = (x1 - x2) / se

    if alt == "two-sided":

        t_pos = t.ppf((1 - alpha/2), n1 + n2 - 2)
        t_neg = t.ppf((alpha/2), n1 + n2 - 2)

        p = 1 - t.cdf(abs(t_cal), n1 + n2 - 2)

        return {
            "t_cal": round(t_cal, 4),
            "t_pos": round(t_pos, 4),
            "t_neg": round(t_neg, 4),
            "p_value": round(p, 4)
        }

    elif alt == "greater":

        t_pos = t.ppf((1 - alpha), n1 + n2 - 2)

        p = 1 - t.cdf(t_cal, n1 + n2 - 2)

        return {
            "t_cal": round(t_cal, 4),
            "t_pos": round(t_pos, 4),
            "p_value": round(p, 4)
        }

    elif alt == "lesser":

        t_neg = t.ppf(alpha, n1 + n2 - 2)

        p = t.cdf(t_cal, n1 + n2 - 2)

        return {
            "t_cal": round(t_cal, 4),
            "t_neg": round(t_neg, 4),
            "p_value": round(p, 4)
        }


@app.route("/")
def home():
    return render_template("app.html")


@app.route("/calculate", methods=["POST"])
def calculate():

    try:
        a = request.form["sample1"]
        b = request.form["sample2"]
        alt = request.form["alt"]

        a = [float(i.strip()) for i in a.split(",")]
        b = [float(i.strip()) for i in b.split(",")]

        result = twottest(a, b, alt)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)