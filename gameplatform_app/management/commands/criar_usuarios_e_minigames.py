from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from gameplatform_app.models import UsuarioNaoAdministrativo, Minigame


class Command(BaseCommand):
    help = 'Cria 3 usuários não administrativos e 10 minigames com desenvolvedores válidos.'

    def handle(self, *args, **kwargs):
        # Criar 3 usuários não administrativos
        usuarios = []
        for i in range(3):
            usuario = UsuarioNaoAdministrativo.objects.create(
                nome=f'UsuarioTeste{i + 1}',
                enderecoEmail=f'usuario{i + 1}@example.com',
                senha=make_password('senha123'),  # Usando make_password para hash seguro
                desenvolvedor=True
            )
            usuarios.append(usuario)
            self.stdout.write(self.style.SUCCESS(f'Usuário "{usuario.nome}" criado com sucesso.'))

        # Criar 10 minigames associados a desenvolvedores válidos
        for i in range(10):
            desenvolvedor = usuarios[i % len(usuarios)]  # Garantir que todos os minigames tenham desenvolvedores
            minigame = Minigame.objects.create(
                nome=f'Minigame Teste {i + 1}',
                descricao=f'Descrição do Minigame Teste {i + 1}',
                estado=Minigame.EstadoChoices.PUBLICADO,
                codigo=f'print("Minigame {i + 1}")',
                url=f'https://example.com/minigame-{i + 1}',
                desenvolvedor=desenvolvedor  # Atribuir um desenvolvedor válido
            )
            self.stdout.write(self.style.SUCCESS(f'Minigame "{minigame.nome}" criado com sucesso.'))

        self.stdout.write(self.style.SUCCESS('Processo concluído com sucesso.'))
