import requests, csv

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()

keys = data[0]["rates"][0].keys()
rates = data[0]["rates"]

with open("out.csv", "w", newline="") as f:
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(rates)

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/calculator/", methods=["GET", "POST"])
def calculate():
    if request.method == "POST":
        data_2 = request.form
        code = data_2.get('currency')
        quantity = data_2.get('quantity')

        i = 0
        for i in range(12):
            if code == rates[i]['code']:
                count = quantity * rates[i]['ask']
                return f'Za {quantity} PLN dostaniesz {count} {code}'
            else:
                return f'Nie ma takiej waluty'

    return render_template("main.html")

if __name__ == "__main__":
    app.run(debug=True)
