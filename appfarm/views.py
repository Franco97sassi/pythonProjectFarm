from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from appfarm.forms import *
from appfarm.models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import CreateView
from proyectfarm.settings import BASE_DIR
import os

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.contrib import messages

# Create your views here.
class StaffRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect(settings.LOGIN_URL)
        return super(StaffRequiredMixin, self).dispatch(request,
            *args, **kwargs)



def inicio(request):
    if request.user.is_authenticated:
        
        try:
            imagen_model = Avatar.objects.filter(user = request.user.id).order_by("-id")[0]
            imagen_url = imagen_model.imagen.url

        except:
            return redirect("auth-avatar")
        
    else:
        imagen_url = ""
    return render(request, "appfarm/base.html", {"imagen_url": imagen_url})
# @login_required
# @login_required
# def inicio(request):

#       avatares = Avatar.objects.filter(user=request.user.id)
      
#       return render(request, "appfarm/base.html", {"url":avatares[0].imagen.url})


def entregables(request):
    return render(request, "appfarm/entregables.html")



class EntregablesList(StaffRequiredMixin, ListView):

    model = Entregable
    template_name = "appfarm/list_entregables.html"



class EntregableDetail(StaffRequiredMixin, DetailView):

    model = Entregable
    template_name = "appfarm/detail_entregable.html"



class EntregableCreate(StaffRequiredMixin, CreateView):

    model = Entregable
    success_url = "/farm/entregables/"
    fields = ["clasificacion", "nombre", "fecha_de_vto", "precio", "codigo", "productor", "entregado", "imagen"]
    template_name = "appfarm/entregable_form.html"

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)



class EntregableUpdate(StaffRequiredMixin, UpdateView):

    model = Entregable
    success_url = "/farm/entregables/"
    fields = ["nombre", "fecha_de_vto", "precio", "codigo", "productor", "entregado", "imagen"]



class EntregableDelete(StaffRequiredMixin, DeleteView):

    model = Entregable
    success_url = "/farm/entregables/"



def buscar_vegetal(request):

    return render(request, "appfarm/busqueda_vegetal.html")

    

def resultado_busqueda_vegetal(request):

    nombre_vegetal = request.GET["nombre_vegetal"] 
                
    vegetales = Entregable.objects.filter(nombre__icontains=nombre_vegetal)

    return render(request, "appfarm/resultado_busqueda_vegetal.html", {"vegetales": vegetales})



def solo_frutas(request):

    vegetales = Entregable.objects.filter(clasificacion="fruta")

    return render(request, "appfarm/solo_frutas.html", {"vegetales": vegetales})



def solo_verduras(request):

    vegetales = Entregable.objects.filter(clasificacion="verdura")

    return render(request, "appfarm/solo_frutas.html", {"vegetales": vegetales})



def iniciar_sesion(request):

    errors = ""

    if request.method == "POST":

        formulario = AuthenticationForm(request, data=request.POST)

        if formulario.is_valid():
            data = formulario.cleaned_data

            user = authenticate(username=data["username"], password=data["password"])

            if user is not None:
                login(request, user)
                return redirect("inicio")

            else:
                return render(request, "appfarm/login.html", {"form": formulario, "errors": "Credenciales invalidas"})
    
        else:
            return render(request, "appfarm/login.html", {"form": formulario, "errors": formulario.errors})    

    formulario = AuthenticationForm()
    return render(request, "appfarm/login.html", {"form": formulario, "errors": errors})



def registrar_usuario(request):

    if request.method == "POST":
        formulario = UserRegisterForm(request.POST)

        if formulario.is_valid():

            formulario.save()
            return redirect("inicio")

        else:
            return render(request, "appfarm/register.html", { "form": formulario, "errors": formulario.errors})

    formulario = UserRegisterForm()
    return render(request, "appfarm/register.html", { "form": formulario})



@login_required
def editar_perfil(request):

    usuario = request.user

    if request.method == "POST":

        formulario = UserEditForm(request.POST)

        if formulario.is_valid():
            data = formulario.cleaned_data

            usuario.email = data["email"]
            usuario.first_name = data["first_name"]
            usuario.last_name = data["last_name"]

            usuario.save()  
            return redirect("inicio")

        else:
            return render(request, "appfarm/editar_perfil.html", {"form": formulario, "errors": formulario.errors})    

    else:
        formulario = UserEditForm(initial = {"email": usuario.email, "first_name": usuario.first_name, "last_name": usuario.last_name})

    return render(request, "appfarm/editar_perfil.html", {"form": formulario})



@login_required
def agregar_avatar(request):

    if request.method == "POST":
        formulario = AvatarForm(request.POST, request.FILES)

        if formulario.is_valid():
            data = formulario.cleaned_data

            usuario = request.user

            avatar = Avatar(user=usuario, imagen=data["imagen"])
            avatar.save()

            return redirect("inicio")

        else:
            return render(request, "appfarm/agregar_avatar.html", {"form": formulario, "errors": formulario.errors})
    
    formulario = AvatarForm()

    return render(request, "appfarm/agregar_avatar.html", {"form": formulario})



########## POST ##########

class PostCreate(StaffRequiredMixin, CreateView):

    model = Post
    success_url = "/farm/post/list/"
    fields = ["titulo", "path", "contenido"]
    template_name = "appfarm/post_form.html"



class PostDetail(DetailView):

    model = Post
    template_name = "appfarm/detail_post.html"



class PostList(ListView):

    model = Post
    template_name = "appfarm/list_post.html"



class PostUpdate(StaffRequiredMixin, UpdateView):

    model = Post
    success_url = "/farm/post/list/"
    fields = ["titulo", "path", "contenido"]



class PostDelete(StaffRequiredMixin, DeleteView):

    model = Post
    success_url = "/farm/post/list/"



########## ABOUT ##########

def nosotros(request):
    return render(request, "appfarm/about.html")