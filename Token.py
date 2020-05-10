import requests
# DB
import pymysql

import json
import os

UserId = 1

def TokenData(UserId):

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
            sql = "SELECT `grant_type`, `client_id`, `client_secret`, `Environment` FROM `User` WHERE `Id`=%s"
            cursor.execute(sql, (UserId))
            result = cursor.fetchone()

            grant_type = str(result.get('grant_type'))
            client_id = str(result.get('client_id'))
            client_secret = str(result.get('client_secret'))
            Environment = str(result.get('Environment'))

            result = [grant_type, client_id, client_secret, Environment]

    finally:
        connection.close()
    return result

# Datos para el Token Funcion TokenData
Data  = TokenData (UserId)
#
grant_type = Data[0]
client_id = Data[1]
client_secret = Data[2]
Environment_Url = Data[3] + "/token"

#Realizamos peticion Http
pload = {'grant_type':grant_type,'client_id':client_id,'client_secret':client_secret}
r = requests.post(Environment_Url, data = pload)

#encoded respuesta
data_string = json.dumps(r.json())

#Decoded respuesta
decoded = json.loads(data_string)

# capturamos Variables
Token = str(decoded["access_token"])
Generado = str(decoded[".issued"])
Expira = str(decoded[".expires"])


def AddToken (User, Token, Generado, Expira):

    #print (EndpointId)
    connection = pymysql.connect(host='192.168.100.51',
        user='Qatest',
        password='Quito.2019',
        db='External-Api',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)


    try:
        with connection.cursor() as cursor:
        # Create a new record
            User = int(User)
            
            # Actualizar todos los registos del Usuario
            sql_update_query = """UPDATE Token set IsActive = %s where User_Id = %s"""
            data_tuple = (0, User)

            cursor.execute(sql_update_query, data_tuple)
            connection.commit()

            # Insertar \             
            sql = "INSERT INTO `Token` (`User_Id`, `Token`, `Toke_Generated`, `Token_Expiration`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (User, Token, Generado, Expira))
            
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

            

    finally:
        connection.close()

# Agregar Token Funcion AddToken
AddToken (UserId, Token, Generado, Expira)

