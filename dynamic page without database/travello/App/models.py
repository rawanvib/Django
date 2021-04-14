from django.db import models

# Create your models here.

class Destination:
    id: int
    name:str
    img : str
    descrip:str
    price:int