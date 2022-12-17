from django.urls import path
from appfarm.views import *
from chatapp.views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", inicio, name="inicio"),
    path("vegetal/buscar/", buscar_vegetal, name="farm-vegetal-buscar"),
    path("vegetal/buscar/resultado", resultado_busqueda_vegetal, name="farm-vegetal-buscar-resultado"),
    path("entregables/", EntregablesList.as_view(), name="farm-entregables"),
    path("entregables/detalle/<pk>/", EntregableDetail.as_view(), name="farm-entregables-detail"),
    path("entregables/crear/", EntregableCreate.as_view(), name="farm-entregables-create"),
    path("entregables/actualizar/<pk>/", EntregableUpdate.as_view(), name="farm-entregables-update"),
    path("entregables/borrar/<pk>/", EntregableDelete.as_view(), name="farm-entregables-delete"),
    path("solo_frutas", solo_frutas, name="farm-solo-frutas"),
    path("solo_verduras", solo_verduras, name="farm-solo-verduras"),

    path("about/", nosotros, name="about"),

    path("accounts/login/", iniciar_sesion, name="auth-login"),
    path("accounts/signup/", registrar_usuario, name="auth-register"),
    path("logout/", LogoutView.as_view(template_name="appfarm/logout.html"), name="auth-logout"),
    path("accounts/profile/", editar_perfil, name="auth-editar-perfil"),
    path("accounts/profile/avatar/", agregar_avatar, name="auth-avatar"),

    path("post/crear/", PostCreate.as_view(), name="farm-post-create"),
    path("post/detalle/<pk>/", PostDetail.as_view(), name="farm-post-detail"),
    path("post/list/", PostList.as_view(), name="farm-post-list"),
    path("post/update/<pk>", PostUpdate.as_view(), name="farm-post-update"),
    path("post/delete/<pk>/", PostDelete.as_view(), name="farm-post-delete"),

    path("messages/", home, name="inicia-chat"),
    path('messages/<str:room>/', room, name='room'),
    path('messages/checkview', checkview, name='checkview'),
    path('messages/send', send, name='send'),
    path('messages/getMessages/<str:room>/', getMessages, name='getMessages'),

]