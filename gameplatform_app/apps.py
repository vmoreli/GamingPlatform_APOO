from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.core.management import call_command


class GameplatformAppConfig(AppConfig):
    name = 'gameplatform_app'

    def ready(self):
        # Conectar o sinal post_migrate apenas uma vez
        post_migrate.connect(self.run_initial_setup, sender=self)

    def run_initial_setup(self, sender, **kwargs):
        """
        Método executado após as migrações. Garante que os dados sejam inseridos
        somente na primeira inicialização do banco de dados.
        """
        # Importar os modelos dentro da função para evitar problemas de inicialização
        from gameplatform_app.models import UsuarioNaoAdministrativo

        try:
            # Verificar se há registros na tabela UsuarioNaoAdministrativo
            if UsuarioNaoAdministrativo.objects.exists():
                print("O banco de dados já está populado. Nenhuma ação necessária.")
            else:
                print("Banco de dados vazio. Populando com dados iniciais...")
                # Executa o comando de população inicial
                call_command('criar_usuarios_e_minigames')
        except Exception as e:
            # Captura e exibe quaisquer erros que ocorram durante a verificação ou execução do comando
            print(f"Erro durante a inicialização dos dados: {e}")
