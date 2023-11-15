from boto3 import resource, Session
from boto3.dynamodb.conditions import Attr, Key
from datetime import datetime

demo_table = resource('dynamodb').Table('brand_user')
"""
{
    user_id:'',
    data:{
        name:
        lastname:
        img:s
    }
}
"""

def new_user(id,name,lastname,email,img):
    response=demo_table.put_item(
        Item={
            'user_id':id,
            'name':name,
            'lastname':lastname,
            'email':email,
            'img':img
        }
    )
    print(f'Insert response: {response}')
   


def get_user(id):
    response={}
    response=demo_table.get_item(
        Key={
            'user_id':id
        }
    )
    item=response['Item']
    if(item):
        print('Existe usuario')
        return item
    else:
        print('No existe usuario')
        
def update_user(cambio,id,update_item):
    demo_table.update_item(
        Key={
            'user_id':id,
        },
        UpdateExpression=f'set #{cambio} =:val1',
        ExpressionAttributeValues={
            ':val1':update_item
        },
        ExpressionAttributeNames={
            f'#{cambio}':f'{cambio}'
        },
        ReturnValues='UPDATED_NEW'
    )

#print(demo_table.creation_date_time)
update_user('email','105772693367918719219','ronaldo.flores@utec.edu.pe')



