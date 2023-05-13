#este py es responsable de codificar y decodificar el JWT token.
from typing import Mapping
import time
import jwt
from decouple import config

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

#esta funcion regresa los tokens generados
def token_response(token: str):
    return {
        "access token" : token
    }
#Funcion para hacer nuestro token
def signJWT(userID : str):
    payload = {
        "userID" : userID,
        "expiry" : time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)



def decodeJWT(token : str):
    try:  
         decode_token = jwt.decode(token, JWT_SECRET, algorithm=JWT_ALGORITHM)
         return decode_token if decode_token['expires'] >= time.time() else None
    except:
         return {}