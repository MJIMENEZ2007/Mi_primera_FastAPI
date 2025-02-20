from fastapi import FastAPI , HTTPException , Depends , status
from pydantic import BaseModel
from typing import Annotated
import models 
from database import engine , SessionLocal
from sqlalchemy.orm import Session 

app = FastAPI()

class IngresoBase(BaseModel):
    documentoingreso:str
    nombrepersona:str

class IngresoBase2(BaseModel):
    idregistro:str
    documentoingreso:str
    nombrepersona:str

def get_db():
    db= SessionLocal()
    try:
        yield db 
    finally:
        db.close()

db_dependency= Annotated[Session, Depends(get_db)]

@app.post("/registro/", status_code=status.HTTP_201_CREATED)
async def crear_registro(registro:IngresoBase, db:db_dependency):
    db_registro = models.Ingreso(**registro.dict())
    db.add(db_registro)
    db.commit()
    return "El registro se realizo exitosamente"

@app.get("/listaregistros/", status_code = status.HTTP_200_OK)
async def consultar_registros(db:db_dependency):
    registros = db.query(models.Ingreso).all()
    return registros

@app.get("/consultaregistro/{documento_ingreso}", status_code = status.HTTP_200_OK)
async def consultar_registros_por_documento(documento_ingreso, db:db_dependency):
    registro = db.query(models.Ingreso).filter(models.Ingreso.documentoingreso==documento_ingreso).first()
    if registro is None:
        HTTPException(status_code=404, detail="Registro no encontrado o registro no existente")
    return registro

@app.delete("/eliminarregistro/{id_registro}", status_code=status.HTTP_200_OK)
async def eliminar_registro(id_registro , db:db_dependency):
    registroborrar = db.query(models.Ingreso).filter(models.Ingreso.idregistro == id_registro).first()
    if registroborrar is None:
        HTTPException(status_code=404 , detail="No se puso borrar no existe ese registro")
    db.delete(registroborrar)
    db.commit()
    return "El registro ah sido eliminado de correctamente"

@app.post("/actualizarregistro/", status_code=status.HTTP_200_OK)
async def actualizar_registro(registro:IngresoBase2, db:db_dependency):
    registroactualizar = db.query(models.Ingreso).filter(models.Ingreso.idregistro==registro.idregistro).first()
    if registroactualizar is None:
        HTTPException(status_code=404 , detail="No se a encontrado al registro que quieres actualizar")
    registroactualizar.documentoingreso = registro.documentoingreso
    registroactualizar.nombrepersona = registro.nombrepersona
    db.commit()
    return "Registro actualizado exitosamente"






