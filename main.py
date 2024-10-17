import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

# Inicializa o Pygame
pygame.init()

# Define as dimensões da tela
screen_dimensions = (400, 350)
screen = pygame.display.set_mode(screen_dimensions, DOUBLEBUF | OPENGL)
pygame.display.set_caption('Interactive Drawing with OpenGL')

# Configura a viewport e a matriz de projeção
glViewport(0, 0, screen_dimensions[0], screen_dimensions[1])
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(0, screen_dimensions[0], 0, screen_dimensions[1])
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

# Lista para armazenar os pontos clicados
click_points = []
# Cor inicial dos pontos (vermelho)
point_color = (1.0, 0.0, 0.0)
# Tamanho inicial dos pontos
point_size = 5

# Lista de cores para alternar
colors = [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0), (1.0, 1.0, 0.0), (0.0, 1.0, 1.0), (1.0, 0.0, 1.0)]
color_index = 0

# Modo de desenho inicial (pontos)
draw_mode = 'p'

# Função para renderizar os pontos
def render_points():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(*point_color)
    glPointSize(point_size)
    glBegin(GL_POINTS)
    for point in click_points:
        glVertex2fv(point)
    glEnd()

    if draw_mode == 'l':
        glBegin(GL_LINE_STRIP)
        for point in click_points:
            glVertex2fv(point)
        glEnd()
    elif draw_mode == 't' and len(click_points) >= 3:
        glBegin(GL_TRIANGLES)
        for i in range(0, len(click_points) - 2, 3):
            glVertex2fv(click_points[i])
            glVertex2fv(click_points[i+1])
            glVertex2fv(click_points[i+2])
        glEnd()
    elif draw_mode == 'q' and len(click_points) >= 4:
        glBegin(GL_QUADS)
        for i in range(0, len(click_points) - 3, 4):
            glVertex2fv(click_points[i])
            glVertex2fv(click_points[i+1])
            glVertex2fv(click_points[i+2])
            glVertex2fv(click_points[i+3])
        glEnd()

# Função para desenhar um botão
def draw_button(x, y, width, height, text):
    glColor3f(0.5, 0.5, 1.0)  # Azul claro
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()
    font = pygame.font.SysFont('Helvetica', 18)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(x + width // 2, screen_dimensions[1] - y - height // 2))
    screen.blit(text_surface, text_rect.topleft)

# Função para verificar se um botão foi clicado
def is_button_clicked(x, y, button_x, button_y, button_width, button_height):
    return button_x <= x <= button_x + button_width and button_y <= y <= button_y + button_height

active = True
while active:
    for event in pygame.event.get():
        if event.type == QUIT:
            active = False
        elif event.type == MOUSEBUTTONDOWN:
            x, y = event.pos
            y = screen_dimensions[1] - y  # Inverte a coordenada y
            if is_button_clicked(x, y, 10, 10, 100, 30):
                click_points = []  # Reseta os pontos clicados
            else:
                click_points.append((x, y))
        elif event.type == KEYDOWN:
            if event.key == K_c:
                color_index = (color_index + 1) % len(colors)
                point_color = colors[color_index]  # Muda a cor dos pontos
            elif event.key == K_PLUS or event.key == K_EQUALS:
                point_size = point_size + 1 if point_size < 15 else 15  # Aumenta o tamanho dos pontos
            elif event.key == K_MINUS:
                point_size = point_size - 1 if point_size > 1 else 1  # Diminui o tamanho dos pontos
            elif event.key == K_l:
                draw_mode = 'l'  # Muda para o modo de desenho de linhas
            elif event.key == K_t:
                draw_mode = 't'  # Muda para o modo de desenho de triângulos
            elif event.key == K_q:
                draw_mode = 'q'  # Muda para o modo de desenho de quadrados

    render_points()
    draw_button(10, 10, 100, 30, "Reset")
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()