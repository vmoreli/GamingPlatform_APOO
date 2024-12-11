# GamingPlatform_APOO - Plataforma para Criação e Compartilhamento de Minigames

Este projeto foi desenvolvido como parte da disciplina **SSC0124 - Análise e Projeto Orientados a Objetos**, ministrada pela professora **Lina María Garcés Rodríguez** no Instituto de Ciências Matemáticas e de Computação da Universidade de São Paulo (ICMC-USP).  

## Objetivo do Projeto

O objetivo deste projeto é implementar uma plataforma para a criação e o compartilhamento de minigames, projetada para atender diferentes tipos de usuários: **jogadores**, **desenvolvedores** e **administradores**. A plataforma busca fornecer um ambiente interativo e colaborativo, permitindo:  

- **Jogadores:** Acessar, jogar, avaliar e denunciar minigames, além de reportar bugs.  
- **Desenvolvedores:** Criar, testar, publicar e gerenciar seus próprios minigames, utilizando ferramentas de edição e acesso a estatísticas.  
- **Administradores:** Moderar a plataforma, gerenciar permissões, analisar denúncias e manter a segurança e qualidade do ambiente.  

## Funcionalidades Implementadas  

- Cadastro e login de usuários não administradores estão funcionais

### Para Jogadores  
- Selecionar minigame e visualizar detalhes
- Avaliar
- Denunciar
- Visualizar avaliações de outros usuários
- Reportar bugs da plataforma

## Para Executar

A plataforma pode ser acessada por meio dos segunintes passos:

No diretório raiz:

```bash
  python manage.py makemigrations
  python manage.py migrate
  python manage.py runserver    
```

O comando makemigrations configura o DB com as tabelas especificadas em models.py, enquanto o migrate concluí essa configuração e, caso o DB estiver vazio (primeira execução), dispara um script que popula o DB com usuários e minigames. Isso foi necessário para poder implementar o que foi apresentado acima sem implementar a funcionalidade "Criar minigame". Por fim, o último comando inicializa o server de desenvolvimento, que pode ser acessado no endereço padrão http://127.0.0.1:8000/.

Usuários criados automaticamente:

| Email                   | Senha        |
|-------------------------|--------------|
| usuario1@example.com    | senha123     |
| usuario2@example.com    | senha123     |
| usuario3@example.com    | senha123     |

Esses usuários podem ser utilizados para fins de teste, ou outros podem ser criados.
