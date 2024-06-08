from flask import Flask, render_template
import pandas as pd
import os

app = Flask("__name__")

stations = pd.read_csv("data_small/stations.txt", skiprows=17)
stations = stations[["STAID", "STANAME                                 "]]

@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    if os.path.exists(filename):
        df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
        temperature = df.loc[df["    DATE"] == date]["   TG"].squeeze() / 10
        return {"station": station,
                "date": date,
                "temperature": temperature}
    else:
        return "<h3>Enter a valid station ID.</h3>"


@app.route("/api/v1/<station>")
def station_all(station):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    if os.path.exists(filename):
        df = pd.read_csv(filename, skiprows=20)
        df["   TG"] = df["   TG"] / 10
        return df.to_dict(orient="records")
    else:
        return "<h3>Enter a valid station ID.</h3>"

@app.route("/api/v1/yearly/<station>/<date>")
def by_year(station, date):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    if os.path.exists(filename):
        df = pd.read_csv(filename, skiprows=20)
        df["   TG"] = df["   TG"] / 10
        df["    DATE"] = df["    DATE"].astype(str)
        return df[df["    DATE"].str.startswith(date)].to_dict(orient="records")
    else:
        return "<h3>Enter a valid station ID.</h3>"

if __name__ == "__main__":
    app.run(debug=True)