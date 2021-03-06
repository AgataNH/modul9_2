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
        for rate in rates:
            print(code, rate['code'])
            if code == rate['code']:
                count = int(quantity) * rate['ask']
                return f'Żeby kupić {quantity} {code} musisz zapłacić {count} PLN'
        else:
            return f'Nie ma takiej waluty'

    return render_template("main.html")

if __name__ == "__main__":
    app.run(debug=True)
