import boto3


dynamodb = boto3.client('dynamodb')

table_user = 'TableUsers'
table_campa = 'TableCampa'
table_pictures = 'TablePictures'
table_ = 'TableStadistics'


def UpdateTable(Item, TableName=None):
    dynamodb.put_item(
        TableName=TableName,
        Item = Item
    )
    


