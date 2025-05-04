from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import  CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm # registro de usuaario
from django.contrib.auth import login # Registro de usuario
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy # direcciona a un sitio especifico
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Tarea

# Create your views here.

class Logueo(LoginView):
    template_name = "base/login.html"
    field ="__all__"
    redirect_authenticated_user = True

    def get_success_url(self):  #Lo redireccciona a la pagina de tareas
        return reverse_lazy('tareas')

class PaginaRegistro(FormView):
    template_name = 'base/registro.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tareas') # redicreccionar

    def form_valid(self, form):
        usuario = form.save()
        if usuario is not None:
            login(self.request, usuario)
        return super(PaginaRegistro, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tareas')
        return super(PaginaRegistro, self).get(*args, **kwargs)
class ListaPendientes(LoginRequiredMixin,ListView):
    model = Tarea
    context_object_name = 'tareas'

    def get_context_data(self, **kwarg): #Se visualizara de acuerdo al contexto,
                                            #kwargs argumentos clave
        context = super().get_context_data(**kwarg)# instancia superior
        context ['tareas'] = context['tareas'].filter(usuario=self.request.user) # usuario requerido
        context['count'] = context['tareas'].filter(completo=False).count()# Para ver todas las tareas no completas

        valor_buscado =self.request.GET.get('area-buscar') or ''
        if valor_buscado:
            context['tareas'] = context['tareas'].filter(titulo__icontains=valor_buscado)
        context['valor_buscado'] = valor_buscado
        return context

class DetalleTarea(LoginRequiredMixin,DetailView):
    model = Tarea
    context_object_name = 'tarea'
    template_name = 'base/tarea.html'


class CrearTarea(LoginRequiredMixin,CreateView):
    model = Tarea
    fields = ['titulo','descripcion', 'completo'] # Campos a llenar para guasrdar la tarea
    success_url = reverse_lazy('tareas')

    def form_valid(self, form):# Asigna la tarea a crear al usuario que esta logueado
        form.instance.usuario = self.request.user
        return super(CrearTarea, self).form_valid(form)

class EditarTarea(LoginRequiredMixin,UpdateView):
    model = Tarea
    fields = ['titulo','descripcion', 'completo']
    success_url = reverse_lazy('tareas')


class EliminarTarea(LoginRequiredMixin, DeleteView):
    model = Tarea
    context_object_name = 'tarea'
    success_url = reverse_lazy('tareas')