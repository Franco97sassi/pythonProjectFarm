from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.
class Entregable(models.Model):

    CATEGORIA = (
        ("fruta", "fruta"),
        ("verdura", "verdura"),
    )

    clasificacion = models.CharField(max_length=100, choices=CATEGORIA)
    nombre = models.CharField(max_length=100, unique=True)
    fecha_de_vto = models.DateField()
    precio = models.IntegerField(null=True, blank=True)
    codigo = models.IntegerField(null=True, blank=True, unique=True, verbose_name="Nº codigo")
    productor = models.CharField(max_length=100, null=True, blank=True, verbose_name="Razon social del productor")
    entregado = models. BooleanField()
    imagen = models.ImageField(upload_to="avatares", default="avatares/default.png", blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.clasificacion} -> {self.nombre}"


       
class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="avatares", null=True, blank=True)

    def __str__(self):
        return f"{self.user}"



class Post(models.Model):
    titulo = models. CharField(max_length=100, verbose_name="Titulo")
    path = models.CharField(max_length=200, verbose_name="Path")
    contenido = RichTextField(verbose_name="Contenido")

    def __str__(self):
        return f"{self.titulo} -> {self.path}"