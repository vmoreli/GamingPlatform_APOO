from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from .forms import CadastroForm, LoginForm, AvaliacaoForm, DenunciaForm, RelatarBugsForm
from django.shortcuts import render, get_object_or_404
from .models import Minigame, Jogar, UsuarioNaoAdministrativo, RelatoBugs

def home(request):
    if not request.usuario:  # Verifica se o usuário está autenticado
        return redirect('login')

    # Obtem todos os minigames publicados
    minigames = Minigame.objects.filter(estado='Publicado')

    return render(request, 'gameplatform_app/home.html', {
        'usuario': request.usuario,
        'minigames': minigames,
    })

def detalhes_minigame(request, id):
    minigame = get_object_or_404(Minigame, pk=id)
    info = minigame.carregar_info(id)

    if 'erro' in info:
        return render(request, 'gameplatform_app/erro.html', {'mensagem': info['erro']})
    
    try:
        usuario_nao_adm = UsuarioNaoAdministrativo.objects.get(pk=request.usuario.id)
    except UsuarioNaoAdministrativo.DoesNotExist:
        return render(request, 'gameplatform_app/erro.html', {'mensagem': 'Apenas usuários não administrativos podem jogar.'})
    
    jogar, created = Jogar.objects.get_or_create(usuario=usuario_nao_adm, minigame=minigame)

    avaliacoes = Jogar.objects.filter(minigame_id=id)
    
    return render(request, 'gameplatform_app/detalhes_minigame.html', {
        'minigame': info,
        'jogar': jogar,
        'avaliacoes': avaliacoes,
        'usuario': request.usuario,
    })

def cadastro_view(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('login')
    else:
        form = CadastroForm()
    return render(request, 'gameplatform_app/cadastro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario = form.authenticate()
            if usuario:
                login(request, usuario)
                request.session['usuario_id'] = usuario.id
                messages.success(request, f'Bem-vindo, {usuario.nome}!')
                print(usuario)
                return redirect('home')
            else:
                messages.error(request, 'Email ou senha inválidos.')
    else:
        form = LoginForm()
    return render(request, 'gameplatform_app/login.html', {'form': form})

def logout_view(request):
    if 'usuario_id' in request.session:
        del request.session['usuario_id']
    messages.info(request, 'Você saiu da sua conta.')
    return redirect('login')

def avaliar_minigame(request, id):
    jogo = get_object_or_404(Jogar, usuario=request.usuario, minigame_id=id)

    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            estrelas = form.cleaned_data['estrelas']
            review = form.cleaned_data['review']
            jogo.nova_avaliacao(estrelas, review)
            return redirect('detalhes_minigame', id=id)
    else:
        form = AvaliacaoForm()

    return render(request, 'gameplatform_app/avaliar_minigame.html', {
        'form': form,
        'usuario': request.usuario,
        'id':id,
    })

def denunciar_minigame(request, id):
    jogo = get_object_or_404(Jogar, usuario=request.usuario, minigame_id=id)

    if request.method == 'POST':
        form = DenunciaForm(request.POST)
        if form.is_valid():
            detalhes = form.cleaned_data['detalhes']
            jogo.nova_denuncia(detalhes)
            return redirect('detalhes_minigame', id=id)
    else:
        form = DenunciaForm()

    return render(request, 'gameplatform_app/denunciar_minigame.html', {
        'form': form,
        'usuario': request.usuario,
        'id':id,
    })

def reportar_bug(request, id, alvo):
    """
    View para relatar bugs. O alvo é definido pelo parâmetro 'alvo', que pode ser 'minigame' ou 'plataforma'.
    """
    jogo = None
    if alvo == 'minigame':
        jogo = get_object_or_404(Jogar, usuario=request.usuario, minigame_id=id)

    if request.method == 'POST':
        form = RelatarBugsForm(request.POST)
        
        if form.is_valid():
            detalhes = form.cleaned_data['detalhes']
            
            # Cria o objeto RelatoBugs e define os campos
            bug = RelatoBugs(
                jogar=jogo if alvo == 'minigame' else None,
                alvo=alvo,
                detalhes=detalhes
            )
            bug.save()

            return redirect('home')
    else:
        form = RelatarBugsForm()

    return render(request, 'gameplatform_app/reportar_bug.html', {
        'form': form,
        'usuario': request.usuario,
        'alvo': alvo,
    })
