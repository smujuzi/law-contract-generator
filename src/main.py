from flask import Flask, request, jsonify
from dynamo import get_contract_keywords
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Connect to Google Sheets using credentials
# scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
# credentials = ServiceAccountCredentials.from_json_keyfile_name('YOUR_CREDENTIALS.json', scope)
# gc = gspread.authorize(credentials)
# spreadsheet_key = 'YOUR_SPREADSHEET_KEY'  # Replace this with the key of your Google Sheets document

# @app.route('/submit_form', methods=['POST'])
# def submit_form():
#     try:
#         data = request.json
#         # Extract data from the POST request (assuming it's in JSON format)
#         # Modify the following lines based on your form's questions
#         name = data['name']
#         email = data['email']
#         message = data['message']

#         # Open the Google Sheets document and the desired worksheet
#         worksheet = gc.open_by_key(spreadsheet_key).sheet1

#         # Append the form data to the worksheet
#         row = [name, email, message]
#         worksheet.append_row(row)

#         return jsonify({"status": "success", "message": "Form submitted successfully!"})
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)})

@app.route('/get_keywords', methods=['GET'])
def get_keywords():
    try:
        data = request.json
        # Extract data from the POST request (assuming it's in JSON format)
        # Modify the following lines based on your form's questions
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
