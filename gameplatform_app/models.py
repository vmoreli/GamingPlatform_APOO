from django.db import models
from django.utils import timezone

# Create your models here.

class Usuario(models.Model):
    # id é automaticamente adicionado pelo Django como chave primária
    nome = models.CharField(max_length=100)
    enderecoEmail = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='usuarios/fotos/', null=True, blank=True)
    senha = models.CharField(max_length=128)
    # is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nome


class UsuarioNaoAdministrativo(Usuario):
    desenvolvedor = models.BooleanField(default=True)   # indica se o usuario pode desenvolver ou nao, por padrao eh true

class Minigame(models.Model):
    class EstadoChoices(models.TextChoices):
        PUBLICADO = 'Publicado', 'Publicado'
        PRIVADO = 'Privado', 'Privado'

    nome = models.CharField(max_length=100)
    desenvolvedor = models.ForeignKey(UsuarioNaoAdministrativo, on_delete=models.CASCADE, related_name='minigames')
    descricao = models.CharField(max_length=250)
    estado = models.CharField(max_length=10, choices=EstadoChoices.choices, default=EstadoChoices.PRIVADO)
    codigo = models.TextField()
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.nome

    def carregar_info(self, id):
        """Retorna informações do minigame com base no ID"""

        try:
            minigame = Minigame.objects.get(pk=id)
            return {
                'id': minigame.id,
                'nome': minigame.nome,
                'descricao': minigame.descricao,
                'estado': minigame.estado,
                'url': minigame.url,
            }
        except Minigame.DoesNotExist:
            return {'erro': 'Minigame não encontrado.'}
        
class Jogar(models.Model):
    usuario = models.ForeignKey(UsuarioNaoAdministrativo, on_delete=models.CASCADE, related_name='jogos')
    minigame = models.ForeignKey(Minigame, on_delete=models.CASCADE, related_name='jogadores')
    pontuacao = models.IntegerField(default=None, null=True, blank=True)
    estrelas = models.IntegerField(default=None, null=True, blank=True)
    review = models.TextField(null=True, blank=True)
    denunciar = models.BooleanField(default=False)
    denunciar_detalhes = models.TextField(null=True, blank=True)

    def nova_avaliacao(self, estrelas, review):
        self.estrelas = estrelas
        self.review = review
        self.save()

    def nova_denuncia(self, detalhes):
        self.denunciar = True
        self.denunciar_detalhes = detalhes
        self.save()

    def __str__(self):
        return f'{self.usuario.nome} jogou {self.minigame.nome}'
    
class RelatoBugs(models.Model):
    ALVO_CHOICES = [
        ('minigame', 'Minigame'),
        ('plataforma', 'Plataforma'),
    ]
    
    jogar = models.ForeignKey(Jogar, on_delete=models.CASCADE, related_name="bugs", null=True, blank=True)
    alvo = models.CharField(max_length=20, choices=ALVO_CHOICES)
    detalhes = models.TextField()

    def __str__(self):
        return f"Bug relatado ({self.alvo}): {self.detalhes[:30]}"
    
    def set_detalhes(self, detalhes):
        self.detalhes = detalhes
        self.save()
