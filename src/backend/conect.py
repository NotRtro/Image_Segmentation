import boto3

def connect_to_dynamodb(aws_access_key_id, aws_secret_access_key, region_name):
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )
    return dynamodb

def get_table(dynamodb, table_name):
    table = dynamodb.Table(table_name)
    return table

def print_table(table):
    response = table.scan()
    items = response['Items']
    for item in items:
        print(item)

# Usa tus propias credenciales de AWS y el nombre de la tabla
aws_access_key_id = 'ASIA5626W32RU2KYIAAL'
aws_secret_access_key = '4KVCTcPrmerz2kpwFv1ECMWmSy/g4UlrYv+eAZ0v'
region_name = 'us-east-1'  # Cambia a tu región
table_name = 'colecciones'

dynamodb = connect_to_dynamodb(aws_access_key_id, aws_secret_access_key, region_name)
table = get_table(dynamodb, table_name)

# Ahora puedes usar 'table' para interactuar con tu tabla DynamoDB
print_table(table)

