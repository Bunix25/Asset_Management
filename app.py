from flask import Flask, render_template, request
import csv

app = Flask(__name__)

CSV_FILE = 'assets.csv'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_asset():
    if request.method == 'POST':
        asset_data = [
            request.form['asset_id'],
            request.form['asset_type'],
            request.form['asset_name'],
            request.form['owner'],
            request.form['academic_department'],
            request.form['location'],
            request.form['manufacturer'],
            request.form['model'],
            request.form['serial_number'],
            request.form['purchase_date'],
            request.form['warranty_expiry'],
            request.form['os'],
            request.form['cpu'],
            request.form['ram']
        ]
        with open(CSV_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(asset_data)
        return render_template('add_asset.html', message="Asset added successfully!")
    return render_template('add_asset.html')

@app.route('/view')
def view_assets():
    assets = []
    with open(CSV_FILE, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            assets.append(row)
    return render_template('view_assets.html', assets=assets)

if __name__ == '__main__':
    app.run(debug=True)