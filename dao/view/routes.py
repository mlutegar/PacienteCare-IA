from fastapi import APIRouter
from dao.control.controller import root_controller, say_hello_controller, predict_controller
from dao.model.models import PatientData

router = APIRouter()

@router.get("/")
async def root():
    return root_controller()

@router.get("/hello/{name}")
async def say_hello(name: str):
    return say_hello_controller(name)

@router.post("/predict/")
async def predict(data: PatientData):
    return predict_controller(data)
