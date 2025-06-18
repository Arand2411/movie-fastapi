from fastapi import FastAPI # Importa utilidades de FastAPI
from fastapi.responses import HTMLResponse, JSONResponse  # Tipos de respuesta
from pydantic import BaseModel  # Validación de datos con Pydantic
from user_jwt import createToken , validateToken  # Funciones personalizadas para JWT
from bd.database import engine, Base
from routers.movie import routerMovie
from routers.users import routerUsers
import os

# Instancia principal de la app
app = FastAPI(
    title='Aprendiendo FastAPI',
    description='Una api en los primeros pasos',
    version= '0.0.1'
)


app.include_router(routerMovie)
app.include_router(routerUsers)

Base.metadata.create_all(bind=engine)


# Página raíz (GET)
@app.get('/', tags=['Inicio'])
def read_root():
    return HTMLResponse('<h2>Hola mundo!<h2>')

if __name__ == '__main__':
    port = int(os.environ.get("PORT",8000))
    uvicorn.run("main:app", host= "0.0.0.0", port=port)