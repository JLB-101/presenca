from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.mail import send_mail

class User(AbstractUser):
    pass

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    docente = models.ForeignKey('controle.Docente', on_delete=models.CASCADE, related_name='turmas_criadas')
    ano = models.PositiveIntegerField()
    cadeira = models.CharField(max_length=100)
    total_estudantes = models.PositiveIntegerField(default=0)
    evento_presenca = models.BooleanField(default=False)

    def atualizar_total_estudantes(self):
        self.total_estudantes = self.estudante_set.count()
        self.save()

    def iniciar_evento_presenca(self):
        if not self.evento_presenca:
            self.evento_presenca = True
            self.save()
            self.enviar_notificacoes_email()

    def enviar_notificacoes_email(self):
        estudantes = self.estudante_set.all()
        subject = 'Evento de Presença Iniciado'
        message = 'Um evento de presença foi iniciado para a turma {}. Compareça à aula e marque sua presença.'.format(
            self.nome
        )
        from_email = 'seu-email@example.com'
        recipient_list = [estudante.email for estudante in estudantes]
        send_mail(subject, message, from_email, recipient_list)

class Estudante(models.Model):
    nome = models.CharField(max_length=100)
    codigo_estudante = models.CharField(max_length=10)
    email = models.EmailField()
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Docente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='docente')
    disciplina = models.CharField(max_length=100)
    groups = models.ManyToManyField(Group, blank=True, related_name='docentes')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='docentes')

    def __str__(self):
        return self.user.username

    def criar_turma(self, nome, ano, cadeira):
        turma = Turma(nome=nome, docente=self, ano=ano, cadeira=cadeira)
        turma.save()
        return turma

    def adicionar_estudante(self, turma, nome, codigo_estudante, email):
        estudante = Estudante(nome=nome, codigo_estudante=codigo_estudante, email=email, turma=turma)
        estudante.save()
        return estudante

    def iniciar_evento_presenca(self, turma):
        turma.iniciar_evento_presenca()

    def marcar_presenca(self, estudante, presente):
        presenca = Presenca(estudante=estudante, presente=presente)
        presenca.save()
        return presenca

class Presenca(models.Model):
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    presente = models.BooleanField(default=False)
