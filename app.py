from flask import Flask, render_template, request, redirect, jsonify
import csv
import pandas as pd
import os
from openai import OpenAI




# Load environment variables from .env file

app = Flask(__name__)

CSV_FILE = 'assets.csv'

# Set the API key directly (for testing purposes)
api_key = "HERE!!!!!!!"
print(f"API Key: {api_key}")  # Print the API key to verify

# Instantiate the OpenAI client
client = OpenAI(api_key=api_key)

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

@app.route('/delete', methods=['POST'])
def delete_assets():
    ids_to_delete = request.form.getlist('delete')
    if ids_to_delete:
        with open(CSV_FILE, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)

        headers = rows[0]
        rows = [row for row in rows if row[0] not in ids_to_delete]

        with open(CSV_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(rows)

    return redirect('/view')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("input")
    df = pd.read_csv(CSV_FILE)
    
    # Preparing the prompt for GPT with full access to the assets data
    prompt = f"User Input: {user_input}\n\nAssets Data:\n{df.to_string()}\n\nProvide insights and recommendations based on the assets data."

    # Mock response for development
    mock_response = {
        'choices': [
            {
                'message': {
                    'content': 'Based on the assets data, I recommend reviewing older assets for potential upgrades or maintenance.'
                }
            }
        ]
    }

    # Check if running in development mode to use mock response
    if os.getenv("FLASK_ENV") == "development":
        response = mock_response
    else:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            response = response.model_dump()
        except Exception as e:
            return jsonify({"error": str(e)})
    
    return jsonify({"response": response['choices'][0]['message']['content']})

if __name__ == '__main__':
    app.run(debug=True)







# from flask import Flask, render_template, request, redirect, jsonify
# import csv
# import pandas as pd
# import os
# from openai import OpenAI
# from dotenv import load_dotenv, dotenv_values

# # Load environment variables from .env file
# load_dotenv()

# app = Flask(__name__)

# CSV_FILE = 'assets.csv'

# # Set the API key from the environment variable
# api_key = os.getenv("OPENAI_API_KEY")
# if not api_key:
#     raise ValueError("API Key not found. Please set the OPENAI_API_KEY environment variable.")
# print(f"API Key Loaded: {api_key}")  # Print a confirmation (optional)

# # Instantiate the OpenAI client
# client = OpenAI(api_key=api_key)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/add', methods=['GET', 'POST'])
# def add_asset():
#     if request.method == 'POST':
#         asset_data = [
#             request.form['asset_id'],
#             request.form['asset_type'],
#             request.form['asset_name'],
#             request.form['owner'],
#             request.form['academic_department'],
#             request.form['location'],
#             request.form['manufacturer'],
#             request.form['model'],
#             request.form['serial_number'],
#             request.form['purchase_date'],
#             request.form['warranty_expiry'],
#             request.form['os'],
#             request.form['cpu'],
#             request.form['ram']
#         ]
#         with open(CSV_FILE, 'a', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(asset_data)
#         return render_template('add_asset.html', message="Asset added successfully!")
#     return render_template('add_asset.html')

# @app.route('/view')
# def view_assets():
#     assets = []
#     with open(CSV_FILE, 'r') as file:
#         reader = csv.reader(file)
#         next(reader)  # Skip header row
#         for row in reader:
#             assets.append(row)
#     return render_template('view_assets.html', assets=assets)

# @app.route('/delete', methods=['POST'])
# def delete_assets():
#     ids_to_delete = request.form.getlist('delete')
#     if ids_to_delete:
#         with open(CSV_FILE, 'r') as file:
#             reader = csv.reader(file)
#             rows = list(reader)

#         headers = rows[0]
#         rows = [row for row in rows if row[0] not in ids_to_delete]

#         with open(CSV_FILE, 'w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(headers)
#             writer.writerows(rows)

#     return redirect('/view')

# @app.route('/chat', methods=['POST'])
# def chat():
#     user_input = request.json.get("input")
#     df = pd.read_csv(CSV_FILE)

#     # Preparing the prompt for GPT with full access to the assets data
#     prompt = f"User Input: {user_input}\n\nAssets Data:\n{df.to_string()}\n\nProvide insights and recommendations based on the assets data."

#     # Mock response for development
#     mock_response = {
#         'choices': [
#             {
#                 'message': {
#                     'content': 'Based on the assets data, I recommend reviewing older assets for potential upgrades or maintenance.'
#                 }
#             }
#         ]
#     }

#     # Check if running in development mode to use mock response
#     if os.getenv("FLASK_ENV") == "development":
#         response = mock_response
#     else:
#         try:
#             response = client.chat.completions.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "system", "content": "You are a helpful assistant."},
#                     {"role": "user", "content": prompt}
#                 ]
#             )
#             response = response.model_dump()
#         except Exception as e:
#             return jsonify({"error": str(e)})

#     return jsonify({"response": response['choices'][0]['message']['content']})

# if __name__ == '__main__':
#     app.run(debug=True)

