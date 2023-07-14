import pygame
import random
import sys

pygame.init()
pygame.mixer.init() # necessario para carregar sons
pygame.display.set_caption("Jogo do Cabeção")
largura, altura = 1200, 800
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()


cabeca = pygame.image.load('cabeca.png').convert_alpha()
fruta = pygame.image.load('fruta.png').convert_alpha()
corpo = pygame.image.load('corpo.png').convert_alpha()
cauda = pygame.image.load('cauda.png').convert_alpha()
mordida = pygame.mixer.Sound('mordida.wav')

# cores RGB
preta = (0, 0, 0)
branca = (255, 255, 255)
vermelha = (255, 0, 0)
verde = (0, 255, 0)

# parâmetros da cobrinha
tamanho_quadrado = 40
espacamento = 5000  # Espaçamento entre a cabeça e o corpo da cobra
velocidade_jogo = 8

def gerar_comida():
    comida_x = round(random.randrange(0, largura - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)
    comida_y = round(random.randrange(0, altura - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)
    return comida_x, comida_y

def desenhar_comida(tamanho, comida_x, comida_y):
    tela.blit(fruta, (comida_x, comida_y))

def desenhar_cobra(tamanho, pixels):
    for i, pixel in enumerate(pixels):
        if i == 0:
            tela.blit(cabeca, (pixel[0], pixel[1]))
        elif i == len(pixels) - 1:
            tela.blit(cauda, (pixel[0], pixel[1]))
        elif i % espacamento != 0:
            tela.blit(corpo, (pixel[0], pixel[1]))

def desenhar_pontuacao(pontuacao):
    fonte = pygame.font.SysFont("Helvetica", 35)
    texto = fonte.render(f"Pontos: {pontuacao}", True, vermelha)
    tela.blit(texto, (1, 1))

def selecionar_velocidade(tecla, velocidade_x, velocidade_y):
    nova_velocidade_x, nova_velocidade_y = velocidade_x, velocidade_y

    if tecla == pygame.K_DOWN and velocidade_y != -tamanho_quadrado:
        nova_velocidade_x, nova_velocidade_y = 0, tamanho_quadrado
    elif tecla == pygame.K_UP and velocidade_y != tamanho_quadrado:
        nova_velocidade_x, nova_velocidade_y = 0, -tamanho_quadrado
    elif tecla == pygame.K_RIGHT and velocidade_x != -tamanho_quadrado:
        nova_velocidade_x, nova_velocidade_y = tamanho_quadrado, 0
    elif tecla == pygame.K_LEFT and velocidade_x != tamanho_quadrado:
        nova_velocidade_x, nova_velocidade_y = -tamanho_quadrado, 0

    return nova_velocidade_x, nova_velocidade_y

def reiniciar_jogo():
    global tamanho_cobra, pixels, x, y, velocidade_x, velocidade_y, fim_jogo
    tamanho_cobra = 1
    pixels = []
    x = largura / 2
    y = altura / 2
    velocidade_x = 0
    velocidade_y = 0
    fim_jogo = False

def tela_fim_jogo(pontuacao):
    tela.fill(preta)
    fonte_grande = pygame.font.SysFont("Helvetica", 50)
    fonte_pequena = pygame.font.SysFont("Helvetica", 30)

    mensagem = fonte_grande.render("Fim de Jogo", True, vermelha)
    pontuacao_msg = fonte_pequena.render(f"Pontuação: {pontuacao}", True, branca)
    reiniciar_msg = fonte_pequena.render("Pressione R para reiniciar", True, branca)
    sair_msg = fonte_pequena.render("Pressione S para sair", True, branca)
    criadores_msg = fonte_pequena.render("Criado por MariCacau e WillCarvalho", True, branca)

    tela.blit(mensagem, (largura/2 - mensagem.get_width()/2, altura/2 - mensagem.get_height()/2 - 50))
    tela.blit(pontuacao_msg, (largura/2 - pontuacao_msg.get_width()/2, altura/2 - pontuacao_msg.get_height()/2))
    tela.blit(reiniciar_msg, (largura/2 - reiniciar_msg.get_width()/2, altura/2 - reiniciar_msg.get_height()/2 + 50))
    tela.blit(sair_msg, (largura/2 - sair_msg.get_width()/2, altura/2 - sair_msg.get_height()/2 + 100))
    tela.blit(criadores_msg, (largura/2 - criadores_msg.get_width()/2, altura - criadores_msg.get_height() - 20))

    pygame.display.update()

def rodar_jogo():
    fim_jogo = False

    x = largura / 2
    y = altura / 2

    velocidade_x = 0
    velocidade_y = 0

    tamanho_cobra = 1
    pixels = []

    comida_x, comida_y = gerar_comida()

    while not fim_jogo:
        tela.fill(preta)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                velocidade_x, velocidade_y = selecionar_velocidade(evento.key, velocidade_x, velocidade_y)

        # desenhar_comida
        desenhar_comida(tamanho_quadrado, comida_x, comida_y)

        # atualizar a posição da cobra
        x += velocidade_x
        y += velocidade_y

        # atravessar a parede
        x %= largura
        y %= altura

        # desenhar_cobra
        pixels.insert(0, [x, y])
        if len(pixels) > tamanho_cobra:
            del pixels[-1]

        # se a cobrinha bateu no próprio corpo
        if [x, y] in pixels[1:]:
            fim_jogo = True

        desenhar_cobra(tamanho_quadrado, pixels)

        # desenhar_pontos
        desenhar_pontuacao(tamanho_cobra - 1)

        # atualização da tela
        pygame.display.update()

        # criar uma nova comida
        if x == comida_x and y == comida_y:
            tamanho_cobra += 1
            comida_x, comida_y = gerar_comida()
            mordida.play()
        relogio.tick(velocidade_jogo)

    tela_fim_jogo(tamanho_cobra - 1)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    reiniciar_jogo()
                    rodar_jogo()
                elif evento.key == pygame.K_s:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

rodar_jogo()
