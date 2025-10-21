import pygame
import sys

# Inicializar o Pygame
pygame.init()

# Configurações da tela
LARGURA = 800
ALTURA = 600
FUNDO_AMARELO = (255, 255, 0)  # Amarelo

# Cores
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
PRETO = (0, 0, 0)

# Configurações do jogador
LARGURA_JOGADOR = 40
ALTURA_JOGADOR = 30
VELOCIDADE_JOGADOR = 5

# Configurações dos invaders
LARGURA_INVADER = 30
ALTURA_INVADER = 30
VELOCIDADE_INVADERS = 1

class Jogador:
    def __init__(self):
        self.x = LARGURA // 2
        self.y = ALTURA - 50
        self.largura = LARGURA_JOGADOR
        self.altura = ALTURA_JOGADOR
    
    def desenhar(self, tela):
        # Desenhar triângulo azul (apontando para cima)
        pontos = [
            (self.x, self.y - self.altura//2),  # Ponto superior
            (self.x - self.largura//2, self.y + self.altura//2),  # Ponto inferior esquerdo
            (self.x + self.largura//2, self.y + self.altura//2)   # Ponto inferior direito
        ]
        pygame.draw.polygon(tela, AZUL, pontos)
    
    def mover(self, direcao):
        self.x += direcao * VELOCIDADE_JOGADOR
        # Manter o jogador dentro da tela
        self.x = max(self.largura//2, min(LARGURA - self.largura//2, self.x))

class Invader:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largura = LARGURA_INVADER
        self.altura = ALTURA_INVADER
    
    def desenhar(self, tela):
        # Desenhar disco voador (círculo vermelho com detalhes)
        pygame.draw.circle(tela, VERMELHO, (self.x, self.y), self.largura//2)
        
        # Adicionar detalhes para parecer um disco voador
        pygame.draw.circle(tela, PRETO, (self.x, self.y), self.largura//4)
        pygame.draw.rect(tela, PRETO, (self.x - self.largura//2, self.y - 2, self.largura, 4))
    
    def mover(self, direcao):
        self.x += direcao * VELOCIDADE_INVADERS

def criar_invaders():
    invaders = []
    for linha in range(3):
        for coluna in range(8):
            x = 100 + coluna * 80
            y = 100 + linha * 60
            invaders.append(Invader(x, y))
    return invaders

def main():
    # Criar a tela
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Space Invaders - Pygame")
    
    # Criar objetos do jogo
    jogador = Jogador()
    invaders = criar_invaders()
    
    # Clock para controlar FPS
    clock = pygame.time.Clock()
    
    # Variáveis de controle
    direcao_jogador = 0
    tempo_ultimo_movimento = 0
    intervalo_movimento = 500  # ms
    direcao_invaders = 1  # 1 para direita, -1 para esquerda
    
    # Loop principal do jogo
    executando = True
    while executando:
        # Processar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
            
            # Controles do jogador
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    direcao_jogador = -1
                if evento.key == pygame.K_RIGHT:
                    direcao_jogador = 1
            
            if evento.type == pygame.KEYUP:
                if evento.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    direcao_jogador = 0
        
        # Atualizar posição do jogador
        jogador.mover(direcao_jogador)
        
        # Mover invaders periodicamente
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - tempo_ultimo_movimento > intervalo_movimento:
            tempo_ultimo_movimento = tempo_atual
            
            # Verificar se algum invader chegou na borda
            mover_para_baixo = False
            for invader in invaders:
                if (invader.x <= LARGURA_INVADER//2 and direcao_invaders == -1) or \
                   (invader.x >= LARGURA - LARGURA_INVADER//2 and direcao_invaders == 1):
                    mover_para_baixo = True
                    break
            
            if mover_para_baixo:
                # Mudar direção e descer
                direcao_invaders *= -1
                for invader in invaders:
                    invader.y += 20
            else:
                # Continuar na mesma direção
                for invader in invaders:
                    invader.mover(direcao_invaders)
        
        # Desenhar
        tela.fill(FUNDO_AMARELO)  # Fundo amarelo
        
        # Desenhar jogador e invaders
        jogador.desenhar(tela)
        for invader in invaders:
            invader.desenhar(tela)
        
        # Atualizar a tela
        pygame.display.flip()
        
        # Controlar FPS
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()