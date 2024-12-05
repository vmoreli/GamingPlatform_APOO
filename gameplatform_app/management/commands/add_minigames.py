from django.core.management.base import BaseCommand, CommandError
from gameplatform_app.models import UsuarioNaoAdministrativo, Minigame

class Command(BaseCommand):
    help = 'Adiciona minigames a um usuário específico para testes'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help='ID do usuário ao qual os minigames serão adicionados')
        parser.add_argument('--quantidade', type=int, default=3, help='Quantidade de minigames a serem criados (padrão: 3)')

    def handle(self, *args, **options):
        user_id = options['user_id']
        quantidade = options['quantidade']

        try:
            usuario = UsuarioNaoAdministrativo.objects.get(pk=user_id)
        except UsuarioNaoAdministrativo.DoesNotExist:
            raise CommandError(f'Usuário com ID {user_id} não encontrado.')

        for i in range(quantidade):
            nome = f'Minigame Teste {i + 1}'
            descricao = f'Descrição do Minigame Teste {i + 1}'
            minigame = Minigame.objects.create(
                nome=nome,
                desenvolvedor=usuario,
                descricao=descricao,
                estado='Publicado',
                codigo=f'print("Minigame {i + 1}")',
                url=f'https://example.com/minigame-{i + 1}'
            )
            self.stdout.write(self.style.SUCCESS(f'Minigame "{nome}" criado com sucesso para o usuário {usuario.nome}'))

        self.stdout.write(self.style.SUCCESS(f'{quantidade} minigames adicionados ao usuário {usuario.nome}.'))
