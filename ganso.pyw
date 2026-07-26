import sys
import math
import random
import pygame
import pyautogui
from pynput import mouse, keyboard

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = True

pygame.init()

LARGURA_TELA, ALTURA_TELA = pyautogui.size()

screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA), pygame.NOFRAME)

# Constantes da API Win32
HWND_TOPMOST = -1
SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002
SWP_NOACTIVATE = 0x0010
SWP_SHOWWINDOW = 0x0040
SWP_NOOWNERZORDER = 0x0200
FLAGS_FORCAR_TOPO = SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE | SWP_SHOWWINDOW | SWP_NOOWNERZORDER

# Bandas de Z-Order do DWM (Desktop Window Manager)
# Banda 2 = ZBID_UIACCESS (Elevado acima de quase todas as janelas e sobreposições)
ZBID_UIACCESS = 2

hwnd = None


def fixar_no_topo_absoluto():
    if hwnd:
        try:
            import ctypes
            # Tenta injetar na Banda UIAccess do DWM (Requer Windows 8/10/11)
            try:
                ctypes.windll.user32.SetWindowBand(hwnd, 0, ZBID_UIACCESS)
            except Exception:
                pass

            # Reforça via SetWindowPos tradicional sem tomar foco
            ctypes.windll.user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, FLAGS_FORCAR_TOPO)
        except Exception:
            pass


try:
    import ctypes

    hwnd = pygame.display.get_wm_info()["window"]

    # WS_EX_LAYERED (0x80000) | WS_EX_TRANSPARENT (0x20) | WS_EX_TOPMOST (0x8) | WS_EX_TOOLWINDOW (0x80) | WS_EX_NOACTIVATE (0x08000000)
    style_ex = 0x00080000 | 0x00000020 | 0x00000008 | 0x00000080 | 0x08000000
    ctypes.windll.user32.SetWindowLongW(hwnd, -20, style_ex)

    # Transparência pelo tom de preto (0x000000)
    ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0x000000, 0, 1)

    fixar_no_topo_absoluto()
except Exception:
    pass

relogio = pygame.time.Clock()

PROCURANDO = 0
CAPTURADO = 1

estado = PROCURANDO
ganso_x = -100.0
ganso_y = -100.0
alvo_fuga_x = 0.0
alvo_fuga_y = 0.0

VELOCIDADE_CACA = 5.0
VELOCIDADE_FUGA = 8.0

LARGURA_GANSO = 48
ALTURA_GANSO = 60

rodando = True
distancia_percorrida = 0.0

sequencia_emergencia = ""


def ao_pressionar_tecla(key):
    global sequencia_emergencia, rodando
    try:
        if hasattr(key, 'char') and key.char is not None:
            sequencia_emergencia += key.char.lower()
            sequencia_emergencia = sequencia_emergencia[-4:]
            if sequencia_emergencia == "para":
                rodando = False
    except Exception:
        pass


def ao_clicar(x, y, button, pressed):
    global estado
    if pressed:
        fixar_no_topo_absoluto()
        if estado == CAPTURADO:
            spawn_ganso()


def spawn_ganso():
    global ganso_x, ganso_y, estado
    estado = PROCURANDO
    borda = random.choice(['CIMA', 'BAIXO', 'ESQUERDA', 'DIREITA'])
    if borda == 'CIMA':
        ganso_x, ganso_y = float(random.randint(0, LARGURA_TELA)), -80.0
    elif borda == 'BAIXO':
        ganso_x, ganso_y = float(random.randint(0, LARGURA_TELA)), float(ALTURA_TELA + 80)
    elif borda == 'ESQUERDA':
        ganso_x, ganso_y = -80.0, float(random.randint(0, ALTURA_TELA))
    else:
        ganso_x, ganso_y = float(LARGURA_TELA + 80), float(random.randint(0, ALTURA_TELA))


def definir_destino_fuga():
    global alvo_fuga_x, alvo_fuga_y
    cantos = [
        (-120.0, ganso_y),
        (float(LARGURA_TELA + 120), ganso_y),
        (ganso_x, -120.0),
        (ganso_x, float(ALTURA_TELA + 120))
    ]
    alvo_fuga_x, alvo_fuga_y = random.choice(cantos)


spawn_ganso()

listener_mouse = mouse.Listener(on_click=ao_clicar)
listener_teclado = keyboard.Listener(on_press=ao_pressionar_tecla)

listener_mouse.start()
listener_teclado.start()


def desenhar_ganso(surface, x, y, mirando_esquerda, dist_passo):
    cor_corpo = (255, 220, 0)
    cor_bico = (255, 100, 0)
    cor_pata = (230, 90, 0)
    cor_olho = (10, 10, 10)

    frame_passo = int(dist_passo / 12) % 2

    pata1_x = x + 18
    pata2_x = x + 30
    pata_y = y + 50

    if frame_passo == 0:
        pygame.draw.line(surface, cor_pata, (x + 20, y + 45), (pata1_x - 4, pata_y + 8), 3)
        pygame.draw.line(surface, cor_pata, (x + 28, y + 45), (pata2_x + 4, pata_y + 6), 3)
        pygame.draw.line(surface, cor_pata, (pata1_x - 4, pata_y + 8),
                         (pata1_x - 8 if mirando_esquerda else pata1_x, pata_y + 8), 3)
        pygame.draw.line(surface, cor_pata, (pata2_x + 4, pata_y + 6),
                         (pata2_x if mirando_esquerda else pata2_x + 8, pata_y + 6), 3)
    else:
        pygame.draw.line(surface, cor_pata, (x + 20, y + 45), (pata1_x + 4, pata_y + 6), 3)
        pygame.draw.line(surface, cor_pata, (x + 28, y + 45), (pata2_x - 4, pata_y + 8), 3)
        pygame.draw.line(surface, cor_pata, (pata1_x + 4, pata_y + 6),
                         (pata1_x if mirando_esquerda else pata1_x + 8, pata_y + 6), 3)
        pygame.draw.line(surface, cor_pata, (pata2_x - 4, pata_y + 8),
                         (pata2_x - 8 if mirando_esquerda else pata2_x, pata_y + 8), 3)

    pygame.draw.ellipse(surface, cor_corpo, (x, y + 20, 48, 32))
    offset_cabeca = 5 if mirando_esquerda else 28
    pygame.draw.ellipse(surface, cor_corpo, (x + offset_cabeca, y, 16, 30))
    offset_bico = offset_cabeca - 10 if mirando_esquerda else offset_cabeca + 12
    pygame.draw.polygon(surface, cor_bico, [
        (x + offset_cabeca + 8, y + 12),
        (x + offset_bico, y + 16),
        (x + offset_cabeca + 8, y + 20)
    ])
    offset_olho = offset_cabeca + 4 if mirando_esquerda else offset_cabeca + 10
    pygame.draw.circle(surface, cor_olho, (int(x + offset_olho), int(y + 8)), 2)


while rodando:
    relogio.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            rodando = False

    fixar_no_topo_absoluto()

    cx, cy = pyautogui.position()

    if estado == PROCURANDO:
        dx = cx - (ganso_x + LARGURA_GANSO / 2)
        dy = cy - (ganso_y + ALTURA_GANSO / 2)
        distancia = math.hypot(dx, dy)

        if distancia < 25:
            estado = CAPTURADO
            definir_destino_fuga()
        else:
            pas_x = (dx / distancia) * VELOCIDADE_CACA
            pas_y = (dy / distancia) * VELOCIDADE_CACA
            ganso_x += pas_x
            ganso_y += pas_y
            distancia_percorrida += math.hypot(pas_x, pas_y)

    elif estado == CAPTURADO:
        bico_x = int(ganso_x + (5 if ganso_x > alvo_fuga_x else 38))
        bico_y = int(ganso_y + 16)

        try:
            pyautogui.moveTo(bico_x, bico_y)
        except pyautogui.FailSafeException:
            rodando = False

        dx = alvo_fuga_x - ganso_x
        dy = alvo_fuga_y - ganso_y
        distancia = math.hypot(dx, dy)

        if distancia < 15:
            spawn_ganso()
        else:
            pas_x = (dx / distancia) * VELOCIDADE_FUGA
            pas_y = (dy / distancia) * VELOCIDADE_FUGA
            ganso_x += pas_x
            ganso_y += pas_y
            distancia_percorrida += math.hypot(pas_x, pas_y)

    screen.fill((0, 0, 0))

    olhando_esquerda = (cx < ganso_x) if estado == PROCURANDO else (alvo_fuga_x < ganso_x)
    desenhar_ganso(screen, ganso_x, ganso_y, olhando_esquerda, distancia_percorrida)

    pygame.display.flip()

listener_mouse.stop()
listener_teclado.stop()
pygame.quit()
sys.exit()