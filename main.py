import boto3
import requests
import socket
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('phemg-server-02')

def update_field_string_repository(pk, sk, field, value):
    print("====>>>>",field, value )

    current_time = datetime.utcnow().isoformat()
    if isinstance(value, float):
        value = Decimal(value)

    if isinstance(value, list) and all(isinstance(item, tuple) for item in value):
        value = f"{value}"

    try:
        response = table.update_item(
            Key={
                'PK': pk,
                'SK': sk
            },
            UpdateExpression=f"SET #{field} = :{field}, #last_update = :last_update",
            ExpressionAttributeValues={
                f":{field}": value,
                ":last_update": current_time
            },
            ExpressionAttributeNames={
                f"#{field}": field,
                "#last_update": "last_update"
            },
            ReturnValues="UPDATED_NEW"  # Retorna os valores atualizados
        )
        return response

    except err:
        print(f"Erro ao atualizar item. Erro: {err}")
        return None

def my_ip():
    response = requests.get('https://ipinfo.io/ip')
    return response.text.strip()

def main():
    hostname = socket.gethostname()
    update_field_string_repository("My-IP", hostname, "IP", my_ip())
    pass

if __name__ == "__main__":
    main()