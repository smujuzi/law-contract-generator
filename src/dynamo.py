import boto3

# Replace 'region_name' and 'table_name' with your actual AWS region and DynamoDB table name
region_name = 'eu-west-1'
table_name = 'contract-info-table'

# Create a Boto3 DynamoDB client
dynamodb = boto3.client('dynamodb', region_name=region_name)


def get_contract_keywords(contract_name):
    item = None
    try:
        response = dynamodb.get_item(
            TableName=table_name,
            Key={
                'contract_name': {'S': contract_name}
            }

        )
        # If the item is found, it will be in the 'Item' field of the response
        item = response.get('Item')['keywords']
    except Exception as e:
        print("Error:", e)
        return None

    keywords = convert_to_list(item)
    return keywords

def convert_to_list(dynamo_object):
    # Extract the 'L' attribute from the DynamoDB response
    dynamo_list = dynamo_object["L"]

    # Convert the DynamoDB list of dictionaries into a Python list
    keywords_list = []

    for item in dynamo_list:
        keywords_list.append(item["S"])

    return keywords_list



