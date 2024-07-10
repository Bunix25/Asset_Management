# app.py
from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)
CSV_FILE = 'expenses.csv'

# Ensure the CSV file exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Category', 'Description', 'Amount'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        date = request.form['date']
        category = request.form['category']
        description = request.form['description']
        amount = request.form['amount']
        
        with open(CSV_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, category, description, amount])
        
        return redirect('/view')
    
    return render_template('add_expense.html')

@app.route('/view')
def view_expenses():
    expenses = []
    with open(CSV_FILE, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            expenses.append(row)
    
    return render_template('view_expenses.html', expenses=expenses)

if __name__ == '__main__':
    app.run(debug=True)