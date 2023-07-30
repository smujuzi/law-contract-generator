from flask import Flask, request, jsonify
from dynamo import get_contract_keywords
from s3 import generate_contract
import os
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Connect to Google Sheets using credentials
# scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
# credentials = ServiceAccountCredentials.from_json_keyfile_name('YOUR_CREDENTIALS.json', scope)
# gc = gspread.authorize(credentials)
# spreadsheet_key = 'YOUR_SPREADSHEET_KEY'  # Replace this with the key of your Google Sheets document

# NOTE: This was in the post function
# # Open the Google Sheets document and the desired worksheet
        # worksheet = gc.open_by_key(spreadsheet_key).sheet1

        # # Append the form data to the worksheet
        # row = [name, email, message]
        # worksheet.append_row(row)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        data = request.json
        contract_link = generate_contract(data)
        #Clean up
        os.remove(data['contract_name'])

        return jsonify(
                {
                    "status": "success", 
                    "message": "Form submitted successfully!",
                    "download_link": contract_link
                }
            )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/get_keywords', methods=['GET'])
def get_keywords():
    try:
        data = request.json
        contract_name = data['contract_name']
        
        keywords = get_contract_keywords(contract_name)
        if keywords:
            print("Item Found:", keywords)
        else:
            print("Item Not Found.")

        return jsonify(
                {
                    "status": "success",
                    "message": "Keywords returned successfully!",
                    "keywords": keywords,
                }
            )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
