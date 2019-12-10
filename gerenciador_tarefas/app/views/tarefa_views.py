from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from ..forms import TarefaForm
from ..entidades.tarefa import Tarefa
from ..services import tarefa_service

# Create your views here.
@login_required()
def listar_tarefas(request):
    usuario = request.user
    tarefas = tarefa_service.listar_tarefas(usuario)
    return render(request, 'tarefas/listar_tarefas.html', {'tarefas':tarefas})

@login_required()
def cadastrar_tarefa(request):
    if request.method == "POST":
        form_tarefa = TarefaForm(request.POST)
        if form_tarefa.is_valid():
            titulo = form_tarefa.cleaned_data["titulo"]
            descricao = form_tarefa.cleaned_data["descricao"]
            data_expiracao = form_tarefa.cleaned_data["data_expiracao"]
            prioridade = form_tarefa.cleaned_data["prioridade"]
            usuario = request.user
            tarefa_nova = Tarefa(titulo, descricao, data_expiracao, prioridade, usuario)
            tarefa_service.cadastrar_tarefa(tarefa_nova)
            return redirect('listar_tarefas')
    else:
        form_tarefa = TarefaForm()
    return render(request, 'tarefas/form_tarefa.html', {"form_tarefa": form_tarefa})

@login_required()
def editar_tarefa(request, id):
    tarefa_bd = tarefa_service.listar_tarefa_id(id)

    usuario = request.user
    if tarefa_bd.usuario != usuario:
        return HttpResponse("Não permintido")

    form_tarefa = TarefaForm(request.POST or None, instance=tarefa_bd)
    if form_tarefa.is_valid():
        titulo = form_tarefa.cleaned_data["titulo"]
        descricao = form_tarefa.cleaned_data["descricao"]
        data_expiracao = form_tarefa.cleaned_data["data_expiracao"]
        prioridade = form_tarefa.cleaned_data["prioridade"]

        tarefa_nova = Tarefa(titulo, descricao, data_expiracao, prioridade, usuario)
        tarefa_service.editar_tarefa(tarefa_bd, tarefa_nova)
        return redirect('listar_tarefas')
    return render(request, 'tarefas/form_tarefa.html', {"form_tarefa": form_tarefa})

@login_required()
def remover_tarefa(request, id):
    tarefa_bd = tarefa_service.listar_tarefa_id(id)

    usuario = request.user
    if tarefa_bd.usuario != usuario:
        return HttpResponse("Não permintido")

    if request.method == "POST":
        tarefa_service.remover_tarefa(tarefa_bd)
        return redirect('listar_tarefas')
    return render(request,'tarefas/confirma_exclusao.html',{'tarefa':tarefa_bd})