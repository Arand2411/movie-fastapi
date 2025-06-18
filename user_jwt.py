import jwt  # Importa la biblioteca PyJWT para crear y verificar tokens JWT :contentReference[oaicite:0]{index=0}

def createToken(data: dict) -> str:
    # Crea un token JWT firmado con HS256. 'data' es el payload que quieres incluir,
    # 'misecret' es la clave secreta (solo para pruebas; en producción, gestiona esto de forma segura).
    token: str = jwt.encode(payload=data, key='misecret', algorithm='HS256')
    return token

def validateToken(token: str) -> dict:
    # Decodifica y valida el token JWT usando la misma clave y algoritmo.
    # Si el token es inválido o ha expirado, lanzará una excepción.
    data: dict = jwt.decode(token, key='misecret', algorithms=['HS256'])
    return data
