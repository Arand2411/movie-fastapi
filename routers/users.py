from fastapi.responses import HTMLResponse, JSONResponse  # Tipos de respuesta
from pydantic import BaseModel  # Validación de datos con Pydantic
from user_jwt import createToken   # Funciones personalizadas para JWT
from fastapi import APIRouter


routerUsers = APIRouter()



# Modelo de usuario para login
class User(BaseModel):
    email: str
    password: str

# Endpoint para login y creación de token
@routerUsers.post('/login', tags=['Autentication'])
def login(user: User):
    if user.email == 'equesadaarand@gmail.com' and user.password == 'contra123':
        token: str = createToken(user.dict())
        print(token)
        return JSONResponse(content=token)

# Página raíz (GET)
@routerUsers.get('/', tags=['Inicio'])
def read_root():
    return HTMLResponse('<h2>Hola mundo!<h2>')

