import pygame
import math
import random

# Dimensões da tela
LARGURA = 800
ALTURA = 600

# Paleta de Cores Retrô
PRETO = (15, 15, 25)
BRANCO = (245, 245, 250)
VERDE_GRAMA = (68, 168, 72)
VERDE_ESCURO = (34, 102, 46)
VERDE_FLORESTA = (42, 115, 58)
TERRA_CAMINHO = (210, 175, 125)
TERRA_BORDA = (175, 138, 90)
AGUA = (52, 135, 215)
AGUA_BRILHO = (120, 195, 255)
ROXO_MAGO = (125, 55, 185)
DOURADO = (250, 205, 45)
MARROM_MADEIRA = (135, 80, 40)
TELHADO_VERMELHO = (195, 65, 55)


class Mapa:
    """Gerencia o cenário, obstáculos e portal de cada fase do RPG."""

    def __init__(self):
        self.fase = 1
        self.obstaculos = []
        self.arvores = []
        self.portal_ativo = False
        self.portal_rect = pygame.Rect(710, 290, 48, 64)
        self.mago_rect = pygame.Rect(460, 220, 36, 40)

    def carregar_fase(self, numero_fase):
        """Monta os obstáculos e árvores da fase escolhida."""
        self.fase = numero_fase
        self.obstaculos = []
        self.arvores = []
        self.portal_ativo = False

        if numero_fase == 1:
            # FASE 1: A VILA DO MAGO
            self.obstaculos.append(pygame.Rect(270, 120, 100, 65))   # Casa
            self.obstaculos.append(pygame.Rect(520, 420, 170, 110))  # Lago
            self.obstaculos.append(pygame.Rect(110, 440, 120, 20))   # Cerca
            self.obstaculos.append(self.mago_rect)                   # Mago

            posicoes_arvores = [
                (40, 80), (140, 75), (620, 85), (710, 110),
                (35, 260), (40, 480), (710, 470)
            ]
        else:
            # FASE 2: FLORESTA SOMBRIA DO CHEFÃO
            posicoes_arvores = [
                (140, 90), (320, 85), (520, 90), (690, 95),
                (150, 480), (350, 490), (560, 480), (700, 470)
            ]

        for ax, ay in posicoes_arvores:
            self.arvores.append((ax, ay))
            self.obstaculos.append(pygame.Rect(ax + 12, ay + 24, 24, 20))

    def desenhar_arvore(self, tela, x, y):
        """Desenha uma árvore em estilo pixel art."""
        pygame.draw.ellipse(tela, (25, 65, 30), (x + 6, y + 36, 36, 10))
        pygame.draw.rect(tela, MARROM_MADEIRA, (x + 18, y + 24, 12, 18))
        pygame.draw.circle(tela, VERDE_ESCURO, (x + 24, y + 18), 20)
        pygame.draw.circle(tela, VERDE_FLORESTA, (x + 16, y + 14), 14)
        pygame.draw.circle(tela, VERDE_FLORESTA, (x + 32, y + 14), 14)
        pygame.draw.circle(tela, VERDE_GRAMA, (x + 24, y + 8), 14)

    def desenhar_casa(self, tela, x, y):
        """Desenha a casa de telhado vermelho da vila."""
        pygame.draw.rect(tela, (235, 220, 190), (x + 10, y + 40, 100, 60))
        pygame.draw.rect(tela, MARROM_MADEIRA, (x + 10, y + 40, 100, 60), 3)
        pygame.draw.polygon(tela, TELHADO_VERMELHO, [(x, y + 42), (x + 120, y + 42), (x + 60, y + 5)])
        pygame.draw.polygon(tela, PRETO, [(x, y + 42), (x + 120, y + 42), (x + 60, y + 5)], 3)
        pygame.draw.rect(tela, MARROM_MADEIRA, (x + 48, y + 65, 24, 35))
        pygame.draw.circle(tela, DOURADO, (x + 67, y + 84), 3)
        pygame.draw.rect(tela, AGUA_BRILHO, (x + 22, y + 58, 18, 18))
        pygame.draw.rect(tela, MARROM_MADEIRA, (x + 22, y + 58, 18, 18), 2)

    def desenhar(self, tela):
        """Desenha todo o cenário da fase atual na tela."""
        if self.fase == 1:
            tela.fill(VERDE_GRAMA)

            # Caminhos de terra
            pygame.draw.rect(tela, TERRA_BORDA, (150, 295, 580, 62), border_radius=12)
            pygame.draw.rect(tela, TERRA_CAMINHO, (154, 299, 572, 54), border_radius=10)
            pygame.draw.rect(tela, TERRA_CAMINHO, (305, 180, 36, 130))

            # Lago animado
            pygame.draw.ellipse(tela, (35, 95, 165), (515, 415, 180, 120))
            pygame.draw.ellipse(tela, AGUA, (520, 420, 170, 110))
            onda = int(math.sin(pygame.time.get_ticks() * 0.005) * 6)
            pygame.draw.line(tela, AGUA_BRILHO, (555 + onda, 455), (595 + onda, 455), 3)
            pygame.draw.line(tela, AGUA_BRILHO, (585 - onda, 485), (630 - onda, 485), 3)

            # Cerca de madeira
            for cx in range(110, 230, 24):
                pygame.draw.rect(tela, MARROM_MADEIRA, (cx, 435, 8, 26))
            pygame.draw.rect(tela, MARROM_MADEIRA, (110, 442, 120, 5))
            pygame.draw.rect(tela, MARROM_MADEIRA, (110, 452, 120, 5))

            # Casa
            self.desenhar_casa(tela, 260, 85)

            # Portal Mágico para a Fase 2 (aparece ao derrotar os slimes)
            if self.portal_ativo:
                raio = 24 + int(math.sin(pygame.time.get_ticks() * 0.01) * 4)
                pygame.draw.ellipse(tela, ROXO_MAGO, self.portal_rect)
                pygame.draw.circle(tela, AGUA_BRILHO, self.portal_rect.center, raio)
                pygame.draw.circle(tela, BRANCO, self.portal_rect.center, raio // 2)

        elif self.fase == 2:
            # Floresta Sombria do Chefão
            tela.fill((36, 92, 48))
            pygame.draw.rect(tela, (95, 85, 75), (60, 285, 680, 70), border_radius=16)

        # Detalhes de grama
        random.seed(self.fase * 42)
import pygame
import math
import random

# Dimensões da tela
LARGURA = 800
ALTURA = 600

…            # Floresta Sombria do Chefão
            tela.fill((36, 92, 48))
            pygame.draw.rect(tela, (95, 85, 75), (60, 285, 680, 70), border_radius=16)

        # Detalhes de grama
        random.seed(self.fase * 42)
        for _ in range(35):
            fx = random.randint(30, LARGURA - 30)
            fy = random.randint(70, ALTURA - 30)
            pygame.draw.circle(tela, VERDE_ESCURO, (fx, fy), 2)

        # Árvores da fase
        for ax, ay in self.arvores:
            self.desenhar_arvore(tela, ax, ay)