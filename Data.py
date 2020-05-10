import requests

import json
import os

# DB
import pymysql
# GUID
import uuid 

UserId = 1

#///////////////////////////////////////////
# Generamos Un GUID 
#///////////////////////////////////////////
IdUnico = uuid.uuid4()
Guid = str(IdUnico)

def GetToken(UserId):

    #print (EndpointId)
    connection = pymysql.connect(host='192.168.100.51',
        user='Qatest',
        password='Quito.2019',
        db='External-Api',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `Token` FROM `Token` WHERE `User_Id`=%s AND IsActive=%s "
            cursor.execute(sql, (UserId, 1))
            result = cursor.fetchone()
            Token = str(result.get('Token'))
    finally:
        connection.close()
    return Token

# Armamos el Token
Token = 'Bearer ' + GetToken(UserId)

headers = {'Authorization' :  Token  }

#pload = {'Authorization' : 'Bearer' + 'Token 90JATsV1lIYYXuH44jyfwkrpTiPv0eGxo_2FD4aqgKyiNUjzA56D7vXZG25tvV6jFjhoCF8NuoG0SgwzL3PVSPTcRCRT3PbWqULOhpl8FtVfe1whTjolBM-1iafgRiQKaRAO85CfO0x1Mwh9G8HtXZjzTfvylx4ajkzZ8upCD_dXrSXCQg8MHH_nHYDu47-DZ9XyzFOIAt9qJQjHf3jpUiPQNjKHmVwAQy17u3wENUVS4g8VrL0nBo76XEGshVyp7zXR428KnuMgjb4HjP_F1g'}
r = requests.post('https://vsblty-apiv2-qa.azurewebsites.net/api/LiveEndpointData/0d5a36c8-2fa2-4488-9076-ad24dfed9759', headers=headers)
print(r.text)

dir = 'C:/Pruebas'  # También es válido 'C:\\Pruebas' o r'C:\Pruebas'
file_name = Guid +".json"

with open(os.path.join(dir, file_name), 'w') as file:
    json.dump(r.json(), file)