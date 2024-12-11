from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from .forms import CadastroForm, LoginForm, AvaliacaoForm, DenunciaForm, RelatarBugsForm
from django.shortcuts import render, get_object_or_404
from .models import Minigame, Jogar, UsuarioNaoAdministrativo, RelatoBugs

# View da tela inicial
def home(request):
    if not request.usuario:  # Verifica se o usuário nao esta autenticado
        return redirect('login')

    # Obtem todos os minigames publicados
    minigames = Minigame.objects.filter(estado='Publicado')

    return render(request, 'gameplatform_app/home.html', {
        'usuario': request.usuario,
        'minigames': minigames,
    })

# View que traz os detalhes do minigame selecionado
def detalhes_minigame(request, id):
    minigame = get_object_or_404(Minigame, pk=id)   # pega o minigame pela pk
    info = minigame.carregar_info(id)   # retorna dict com info do minigame

    if 'erro' in info:  # se o minigame nao foi encontrado
        return render(request, 'gameplatform_app/erro.html', {'mensagem': info['erro']})
    
    try:
        usuario_nao_adm = UsuarioNaoAdministrativo.objects.get(pk=request.usuario.id)   # pega usuario nao adm logado
    except UsuarioNaoAdministrativo.DoesNotExist:
        return render(request, 'gameplatform_app/erro.html', {'mensagem': 'Apenas usuários não administrativos podem jogar.'})
    
    # seleciona do DB ou cria se nao existir classe jogar entre usuario nao adm e minigame
    jogar, created = Jogar.objects.get_or_create(usuario=usuario_nao_adm, minigame=minigame)

    # pega avaliacoes do minigame para mostrar na tela
    avaliacoes = Jogar.objects.filter(minigame_id=id)
    
    return render(request, 'gameplatform_app/detalhes_minigame.html', {
        'minigame': info,
        'jogar': jogar,
        'avaliacoes': avaliacoes,
        'usuario': request.usuario,
    })

# View para cadastro de usuarios
def cadastro_view(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST, request.FILES)    # pega info digitada
        if form.is_valid(): # valida forms
            form.save() # salva no DB novo usuario
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('login')    # redireciona para login
    else:
        form = CadastroForm()   # forms para ser impresso na tela
    return render(request, 'gameplatform_app/cadastro.html', {'form': form})

# View para login de usuários
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)  # pega info digitada
        if form.is_valid(): # valida forms
            usuario = form.authenticate()   # tenta autenticar usuario
            if usuario: # info correta, usuario autenticado
                login(request, usuario) #realiza login
                request.session['usuario_id'] = usuario.id  # salva id do usuario na sessao
                messages.success(request, f'Bem-vindo, {usuario.nome}!')
                return redirect('home') # redireciona para tela inicial
            else:
                messages.error(request, 'Email ou senha inválidos.')    # se autenticacao deu errado
    else:
        form = LoginForm()
    return render(request, 'gameplatform_app/login.html', {'form': form})

# View para logout
def logout_view(request):
    if 'usuario_id' in request.session:
        del request.session['usuario_id']   # retira id do usuario da sessao
    messages.info(request, 'Você saiu da sua conta.')
    return redirect('login')    # redireciona para tela de login

# View paa avaliar o minigame
def avaliar_minigame(request, id):
    jogo = get_object_or_404(Jogar, usuario=request.usuario, minigame_id=id)    # pega classe jogar relativa ao usuario e jogo

    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)  # pega info digitada
        if form.is_valid(): # valida forms
            estrelas = form.cleaned_data['estrelas']
            review = form.cleaned_data['review']
            jogo.nova_avaliacao(estrelas, review)   # preenche campos de avaliacao: estrelas e review no DB
            return redirect('detalhes_minigame', id=id) # redireciona para tela de detalhes do minigame
    else:
        form = AvaliacaoForm()  # forms para ser impresso na tela

    return render(request, 'gameplatform_app/avaliar_minigame.html', {
        'form': form,
        'usuario': request.usuario,
        'id':id,
    })

# View para denunciar minigame
def denunciar_minigame(request, id):
    jogo = get_object_or_404(Jogar, usuario=request.usuario, minigame_id=id)    # pega classe jogar relativa ao usuario e jogo

    if request.method == 'POST':
        form = DenunciaForm(request.POST)   # pega info digitada
        if form.is_valid(): # valida forms
            detalhes = form.cleaned_data['detalhes']
            jogo.nova_denuncia(detalhes)    # preenche campos de denuncia: bool denuncia e detalhes no DB
            return redirect('detalhes_minigame', id=id) # redireciona para tela de detalhes do minigame
    else:
        form = DenunciaForm()   # forms para ser impresso na tela

    return render(request, 'gameplatform_app/denunciar_minigame.html', {
        'form': form,
        'usuario': request.usuario,
        'id':id,
    })

# View para reportar bugs
def reportar_bug(request, id, alvo):
    jogo = None
    if alvo == 'minigame':  # se o bug eh de um minigame, encontra a classe jogar relativa
        jogo = get_object_or_404(Jogar, usuario=request.usuario, minigame_id=id)

    if request.method == 'POST':
        form = RelatarBugsForm(request.POST)    # pega info digitada
        
        if form.is_valid(): # valida forms
            detalhes = form.cleaned_data['detalhes']
            
            # Cria o objeto RelatoBugs e define os campos
            bug = RelatoBugs(
                jogar=jogo if alvo == 'minigame' else None,
                alvo=alvo,
                detalhes=detalhes
            )
            bug.save()  # salva o relato de bugs no DB

            return redirect('home')
    else:
        form = RelatarBugsForm()

    return render(request, 'gameplatform_app/reportar_bug.html', {
        'form': form,
        'usuario': request.usuario,
        'alvo': alvo,
    })
