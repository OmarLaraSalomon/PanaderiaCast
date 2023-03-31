from django.contrib import admin
from .models import CategoriaProd, Productos, Servicios, Pedido, LineaPedido, Noticias, Profile, Comentario
# Register your models here.

class CategoriaProdAdmin(admin.ModelAdmin):

    readonly_fields=("created","update")


class ProductoAdmin(admin.ModelAdmin):

    readonly_fields=("created","update")

   

class ServicioAdmin(admin.ModelAdmin):

    readonly_fields=("created","update")



class NoticiaAdmin(admin.ModelAdmin):

    readonly_fields=("created","update")



admin.site.register(Profile)

admin.site.register(Comentario)

admin.site.register(CategoriaProd, CategoriaProdAdmin)

admin.site.register(Productos, ProductoAdmin)

admin.site.register(Noticias, NoticiaAdmin)

admin.site.register(Servicios, ServicioAdmin)

admin.site.register([Pedido,LineaPedido])
