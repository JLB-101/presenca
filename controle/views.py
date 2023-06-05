from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Docente, Turma, Estudante
from .forms import TurmaForm, EstudanteForm

# página index
def index(request):
    return render(request, 'index.html')

def login_docente(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            docente = Docente.objects.get(user=user)
            login(request, user)
            request.session['docente_id'] = docente.id
            return redirect('dashboard')
        else:
            error_message = 'Credenciais inválidas. Por favor, tente novamente.'
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def logout_docente(request):
    request.session.pop('docente_id', None)
    return redirect('login')

def dashboard(request):
    docente_id = request.session.get('docente_id')
    if not docente_id:
        return redirect('login')

    docente = Docente.objects.get(id=docente_id)
    turmas = docente.turmas_criadas_controle.all()

    return render(request, 'dashboard.html', {'docente': docente, 'turmas': turmas})

def criar_turma(request):
    docente_id = request.session.get('docente_id')
    if not docente_id:
        return redirect('login')

    docente = Docente.objects.get(id=docente_id)

    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            ano = form.cleaned_data['ano']
            cadeira = form.cleaned_data['cadeira']
            turma = Turma(nome=nome, docente=docente, ano=ano, cadeira=cadeira)
            turma.save()
            return redirect('dashboard')
    else:
        form = TurmaForm()

    return render(request, 'criar_turma.html', {'form': form})
