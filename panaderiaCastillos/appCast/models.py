from distutils.command.upload import upload
from email.policy import default
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from importlib.resources import contents
from sqlite3 import Timestamp
from django.utils import timezone
from time import time, timezone
from django.db.models import DateTimeField
from django.contrib.auth import get_user_model #devuelve el usuario activo actual
from django.db.models import F,Sum, FloatField  # para calcular el total de una orden de pedido



# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='logo_perfil.png')

	def __str__(self):
		return f'Perfil de {self.user.username}'



class Comentario(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentarios')
	timestamp = models.DateTimeField(auto_now_add=True)
	content = models.TextField()

	class Meta:
		ordering = ['-timestamp']


	def __str__(self):
		return f'{self.user.username}: {self.content}'






class Post (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, null=True)
    first_name = models.CharField(max_length=250, null=True)
    last_name = models.CharField(max_length=250, null=True)
    telefono = models.CharField(max_length=250, null=True, unique=False)
    telefono_casa = models.CharField(max_length=250, null=True,  unique=False)
    nacimiento = models.CharField(max_length=250, null=True)
    direccion = models.CharField(max_length=300, null=True)
    contacto_emergencia = models.CharField(max_length=250, null=True)
    telefono_emergencia = models.CharField(max_length=250, null=True)
    puesto = models.CharField(max_length=250, null=True)
    departamento = models.CharField(max_length=250, null=True)
    is_leader = models.BooleanField(default=False,null=True)


class Correo (models.Model):
    nombre = models.CharField(max_length=90)
    apellidos = models.CharField(max_length=30)
    correo_electronico = models. EmailField(max_length=254)
    telefono = models.CharField(max_length=100)
    comentarios = models.TextField()



class CategoriaProd(models.Model):
    
    nombre = models.CharField(max_length=90)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name= "categoriaProd"
        verbose_name_plural= "categoriasProd"

  #salida 
    def __str__(self):
        return self.nombre




class Productos (models.Model):
  
    nombre = models.CharField(max_length=90)
    categoria = models.ForeignKey(CategoriaProd,on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="productos", null=True, blank=True)
    precio= models.FloatField()
    disponibilidad=models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now_add=True)


    class Meta:
       
        verbose_name= "Producto"



class Servicios  (models.Model):
    
    titulo = models.CharField(max_length=90)
    contenido = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to="servicios", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now_add=True)


    class Meta:
       
        verbose_name= "servicio"
        verbose_name_plural= "servicios"
    
    
  #salida 
    def __str__(self):
        return self.titulo





class Noticias  (models.Model):
    
    titulo = models.CharField(max_length=90)
    contenido = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to="noticias", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now_add=True)


    class Meta:
       
        verbose_name= "noticia"
        verbose_name_plural= "noticias"
    
    
  #salida 
    def __str__(self):
        return self.titulo



get_user_model()

class Pedido (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
 #salida 
    def __str__(self):
        return self.id
#la propiedad seria el total, que devuelva el total del pedido que ha hecho el usuario
    @property
    def total(self):
        return self.lineapedido_set.aggregate(

            total=Sum(F("precio")*F("cantidad"), output_field=FloatField())

        )["total"]


    class Meta:
     db_table="pedidos"
     verbose_name= "pedido"
     verbose_name_plural= "pedidos"
     ordering=["id"]


class LineaPedido(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    producto=models.ForeignKey(Productos, on_delete=models.CASCADE)
    pedido= models.ForeignKey(Pedido, on_delete=models.CASCADE)
    cantidad=models.IntegerField(default=1)
    precio=models.FloatField(default=1)
    created_at=models.DateTimeField(auto_now_add=True)


     #salida 
    def __str__(self):
        return f'{self.cantidad} unidades de {self.producto.nombre} con costo de ${self.producto.precio}0'

 

    class Meta:
      db_table="lineapedidos"
      verbose_name= "Linea Pedido"
      verbose_name_plural= "Lineas Pedidos"
      ordering=["id"]


