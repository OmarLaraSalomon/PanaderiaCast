from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .models import Post
from .models import Correo
from .models import Productos
from .models import Servicios
from .carro import Carro
from .models import Pedido
from .models import LineaPedido
from .models import Noticias
from .models import Profile
from .models import Comentario
from .forms import UserRegisterForm,ComForm

from .forms import UserRegisterForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template.loader import render_to_string

from django.utils.html import strip_tags

from django.core.mail import send_mail

# django nos permite tener forms#


# Create your views here.
# el context es para pedir datos a base

def layout(request):

    return render(request, 'social/layout.html')


def feed(request):

    coments = Comentario.objects.all()
    context = {'coments': coments}

    return render(request, 'social/feed.html', context)


def coment(request):
        current_user = get_object_or_404(User, pk=request.user.pk)
        if request.method == 'POST':
            form = ComForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = current_user
                post.save()
                messages.success(request, 'Post enviado')
                return redirect('feed')
        else:
            form = ComForm()
        return render(request, 'social/comentario.html', {'form': form })


def perfil(request):

    return render(request, 'social/perfil.html')


def registro(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Usuario {username} creado')
            return redirect('logout')
    else:
        form = UserRegisterForm()

    context = {'form' : form }
    return render(request, 'social/registro.html', context)


def login(request):

    return render(request, 'social/login.html')


@login_required
def retorno(request):

    return render(request, 'social/pruebita.html')


def contactosregistro(request):
    if request.method == 'POST':

        datos = Post.objects.create(

                user_id=request.POST['user'],
                first_name=request.POST['nombre'],
                last_name=request.POST['apellidos'],
                telefono=request.POST['telefono'],
                telefono_casa=request.POST['telefono_casa'],
                nacimiento=request.POST['nacimiento'],
                direccion=request.POST['direccion'],
                contacto_emergencia=request.POST['contacto_emergencia'],
                telefono_emergencia=request.POST['telefono_emergencia'],
            puesto=request.POST['puesto'],
            departamento=request.POST['departamento'],
            is_leader=request.POST['lider'],

            )
        datos.save()
    return render(request, 'social/contacto.html')


def consultar(request):
    info = Post.objects.all()

    context = {'posts': info}

    #correo = Correo.objects.all()

    #context= {'datos': correo}
    return render(request, 'social/consulta.html', context)


def carrusel(request):

    return render(request, 'social/carru.html')


def mandarcorreo(request):
    if request.method == 'POST':
        correoPru = request.POST['correo_electronico']
        asunto = request.POST['nombre'] + ' ' + request.POST['apellidos'] +  ' con correo ' + request.POST['correo_electronico'] + ' \n ' + 'Envio su informacion para una consulta con respecto al asunto: ' + request.POST['comentarios'] + ' \n ' + 'En breve sera contactado al numero ' + request.POST['telefono'] 
        datos = Correo.objects.create(
            nombre=request.POST['nombre'],
            apellidos=request.POST['apellidos'],
            correo_electronico=request.POST['correo_electronico'],
            telefono=request.POST['telefono'],
            comentarios=request.POST['comentarios']
        )
        datos.save()

        send_mail(
            'Correo de Confirmacion',
            asunto,
            'Hola buen dia .',
    [correoPru, 'panaderiaCastillos01.com'],
            fail_silently=False
            )
    context = {}
    return render(request, 'social/correo.html')


def consultarc(request):
    correo = Correo.objects.all()

    context = {'datos': correo}
    return render(request, 'social/consultarc.html', context)


def tiendita(request):

    return render(request, 'social/tienda.html')


def home(request):
    noticias = Noticias.objects.all()

    return render(request, 'social/home.html', {"noticias": noticias})





def cate(request):

    return render(request, 'social/categoria.html')





def lista(request):
    productos = Productos.objects.all()

    return render(request, 'social/lista.html', {"productos": productos})





def produ(request):


    productos = Productos.objects.all()

    return render(request, 'social/productos.html', {"productos": productos})


def agregar_producto(request, producto_id=None):
    carro = Carro(request)
    producto = Productos.objects.get(id=producto_id)
    carro.agregar(producto=producto)
    return redirect("productos")


def eliminar_producto(request, producto_id=None):
    carro = Carro(request)
    producto = Productos.objects.get(id=producto_id)
    carro.eliminar(producto=producto)
    return redirect("productos")


def restar_producto(request, producto_id=None):
    carro = Carro(request)
    producto = Productos.objects.get(id=producto_id)
    carro.restar_producto(producto=producto)
    return redirect("productos")


def limpiar_carro(request):

    carro = Carro(request)

    carro.limpiar_carro()

    return redirect("productos")


def reiniciar(request):

    carro = Carro(request)

    carro.reiniciar()

    return redirect("home")


def procesar_pedido(request):
    pedido = Pedido.objects.create(user=request.user) # damos de alta un pedido
    carro = Carro(request)  # cogemos el carro
    lineas_pedido = list()  # lista con los pedidos para recorrer los elementos del carro
    for key, value in carro.carro.items():  # recorremos el carro con sus items
        lineas_pedido.append(LineaPedido(
            producto_id=key,
            cantidad=value['cantidad'],
            precio=value['precio'],
            user=request.user,
            pedido=pedido
           
        ))

    LineaPedido.objects.bulk_create(lineas_pedido)  # crea registros en BBDD en paquete
    # enviamos mail al cliente
    enviar_mail(
        pedido=pedido,
        lineas_pedido=lineas_pedido,
        nombreusuario=request.user.username,
        email_usuario=request.user.email


    )

    reiniciar(request)


    # mensaje para el futuro
    messages.success(request, "El pedido se ha creado correctamente")

    return redirect('home')
    # return redirect('listado_productos')
    # return render(request, "tienda/tienda.html",{"productos":productos})


def enviar_mail(**kwargs):
    asunto = "Gracias por el pedido"
    mensaje =render_to_string("social/pedidos.html", {
        "pedido": kwargs.get("pedido"),
        "lineas_pedido": kwargs.get("lineas_pedido"),
        "nombreusuario": kwargs.get("nombreusuario"),
        "email_usuario": kwargs.get("email_usuario")  

    })

    mensaje_texto = strip_tags(mensaje)
    from_email = "weskermexx@gmail.com"
    to = kwargs.get("email_usuario")
    send_mail(asunto, mensaje_texto,from_email,[to], html_message=mensaje)
