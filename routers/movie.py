from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends  # Importa utilidades de FastAPI
from fastapi.responses import HTMLResponse, JSONResponse  # Tipos de respuesta
from fastapi.security import HTTPBearer  # Manejo de tokens tipo Bearer
from pydantic import BaseModel, Field  # Validación de datos con Pydantic
from typing import Optional  # Para definir campos opcionales
from user_jwt import createToken , validateToken  # Funciones personalizadas para JWT
from bd.database import Session
from models.movie import Movie as ModelMovie
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter


routerMovie = APIRouter()

# Autenticación personalizada con token JWT
class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validateToken(auth.credentials)
        if data['email'] != 'equesadaarand@gmail.com':
            raise HTTPException(status_code=403, detail='Credenciales Incorrectas')
        
# Modelo de película con validaciones
class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default="Titulo de la peli", min_length=5, max_length=60)
    overview: str = Field(default="Descripcion de la peli", min_length=15, max_length=60)
    year: int = Field(default=2023)
    rating: float = Field(ge=1, le=10)  # ge = mínimo, le = máximo
    category: str = Field(default="Categoria de la peli", min_length=3, max_length=100)
    
    
# Listar todas las películas (requiere token)
@routerMovie.get('/movies', tags=['Movies'], dependencies=[Depends(BearerJWT())])
def get_movies():
    db = Session()
    data = db.query(ModelMovie).all()
    return JSONResponse(content=jsonable_encoder(data))

# Buscar película por ID con validación del rango
@routerMovie.get('/movies/{id}', tags=['Movies'])
def get_movie(id: int = Path(ge=1, le=100)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message':'Recurso no encontrado'})
    return JSONResponse(status_code=200, content=jsonable_encoder(data))

# Buscar películas por categoría (por query param)
@routerMovie.get('/movies/', tags=['Movies'], status_code=200)
def get_movies_by_category(category: str = Query(min_length=3, max_length=100)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.category == category).all()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'No se encontro la categoria'})
    return JSONResponse(status_code=200, content=jsonable_encoder(data))
    

# Crear una nueva película
@routerMovie.post('/movies', tags=['Movies'], status_code=201)
def create_movie(movie: Movie):
    db = Session()
    newMovie = ModelMovie(**movie.dict())
    db.add(newMovie)
    db.commit()
    return JSONResponse(content={'message': 'Se ha cargado una nueva pelicula'})


# Actualizar una película por ID
@routerMovie.put('/movies/{id}', tags=['Movies'])
def update_movie(id: int, movie: Movie):  
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'No se encontro el recurso'})
        
    data.title = movie.title
    data.overview = movie.overview
    data.year = movie.year
    data.rating = movie.rating
    data.category = movie.category
    db.commit()
    return JSONResponse(content={'message': 'Se ha actualizado la pelicula', 'data': jsonable_encoder(data)})


# Eliminar película por ID
@routerMovie.delete('/movies/{id}', tags=['Movies'], status_code=200)
def delete_movie(id: int):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'No se encontro el recurso','data': jsonable_encoder(data)})
    db.delete(data)
    db.commit()
    return JSONResponse(content={'message': 'Se ha eliminado la pelicula', 'data': jsonable_encoder(data)})


