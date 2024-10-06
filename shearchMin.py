import pygame
import random

pygame.init()

ANCHO = 600
ALTO = 600
TAMAÑO_CELDA = 0
FILAS = 0
COLUMNAS = 0
MINAS = 0

BLANCO = (255, 255, 255)
GRIS = (200, 200, 200)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)

ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Buscaminas")

def generar_tablero(filas, columnas, minas):
    tablero = [[0 for _ in range(columnas)] for _ in range(filas)]
    minas_colocadas = 0
    while minas_colocadas < minas:
        fila = random.randint(0, filas - 1)
        columna = random.randint(0, columnas - 1)
        if tablero[fila][columna] == 0:
            tablero[fila][columna] = -1
            minas_colocadas += 1
    return tablero

def contar_minas_adyacentes(tablero, fila, columna):
    minas_adyacentes = 0
    for i in range(fila - 1, fila + 2):
        for j in range(columna - 1, columna + 2):
            if 0 <= i < FILAS and 0 <= j < COLUMNAS and tablero[i][j] == -1:
                minas_adyacentes += 1
    return minas_adyacentes

def dibujar_tablero(tablero, celdas_descubiertas, juego_terminado):
    for fila in range(len(tablero)):
        for columna in range(len(tablero[0])):
            x = columna * TAMAÑO_CELDA
            y = fila * TAMAÑO_CELDA
            rect = pygame.Rect(x, y, TAMAÑO_CELDA, TAMAÑO_CELDA)
            if (fila, columna) in celdas_descubiertas or juego_terminado:
                if tablero[fila][columna] == -1:
                    pygame.draw.rect(ventana, ROJO, rect)  # Mostrar mina
                else:
                    pygame.draw.rect(ventana, BLANCO, rect)  # Mostrar celda segura
                    minas_adyacentes = contar_minas_adyacentes(tablero, fila, columna)
                    if minas_adyacentes > 0:
                        fuente = pygame.font.SysFont(None, 36)
                        texto = fuente.render(str(minas_adyacentes), True, AZUL)
                        ventana.blit(texto, (x + TAMAÑO_CELDA // 3, y + TAMAÑO_CELDA // 3))
            else:
                pygame.draw.rect(ventana, GRIS, rect)
            pygame.draw.rect(ventana, NEGRO, rect, 2)

def mostrar_mensaje(ventana, mensaje):
    fuente = pygame.font.SysFont(None, 75)
    texto = fuente.render(mensaje, True, ROJO)
    ventana.blit(texto, (ANCHO // 4, ALTO // 3))

def dibujar_boton_reiniciar():
    fuente = pygame.font.SysFont(None, 50)
    texto = fuente.render("Reiniciar", True, NEGRO)
    boton_rect = pygame.Rect(ANCHO // 4, ALTO - 100, ANCHO // 4, 60)
    pygame.draw.rect(ventana, VERDE, boton_rect)
    ventana.blit(texto, (ANCHO // 4 + 10, ALTO - 90))
    return boton_rect

def dibujar_boton_menu():
    fuente = pygame.font.SysFont(None, 50)
    texto = fuente.render("Menú", True, NEGRO)
    boton_rect = pygame.Rect(ANCHO // 2, ALTO - 100, ANCHO // 4, 60)
    pygame.draw.rect(ventana, VERDE, boton_rect)
    ventana.blit(texto, (ANCHO // 2 + 30, ALTO - 90))
    return boton_rect

def dibujar_boton_resolver():
    fuente = pygame.font.SysFont(None, 50)
    texto = fuente.render("Resolver", True, NEGRO)
    boton_rect = pygame.Rect(ANCHO // 2, ALTO - 200, ANCHO // 4, 60)
    pygame.draw.rect(ventana, VERDE, boton_rect)
    ventana.blit(texto, (ANCHO // 2 + 30, ALTO - 190))
    return boton_rect

def resolver_buscaminas(tablero):
    celdas_por_descubrir = [(fila, columna) for fila in range(FILAS) for columna in range(COLUMNAS)]
    random.shuffle(celdas_por_descubrir)
    for fila, columna in celdas_por_descubrir:
        if tablero[fila][columna] == -1:
            continue
        else:
            yield (fila, columna)

def dibujar_menu_dificultad():
    ventana.fill(BLANCO)
    fuente = pygame.font.SysFont(None, 50)
    facil_texto = fuente.render("Fácil", True, NEGRO)
    medio_texto = fuente.render("Medio", True, NEGRO)
    dificil_texto = fuente.render("Difícil", True, NEGRO)

    facil_boton = pygame.Rect(ANCHO // 3, 200, ANCHO // 3, 60)
    medio_boton = pygame.Rect(ANCHO // 3, 300, ANCHO // 3, 60)
    dificil_boton = pygame.Rect(ANCHO // 3, 400, ANCHO // 3, 60)

    pygame.draw.rect(ventana, VERDE, facil_boton)
    pygame.draw.rect(ventana, VERDE, medio_boton)
    pygame.draw.rect(ventana, VERDE, dificil_boton)

    ventana.blit(facil_texto, (ANCHO // 3 + 30, 210))
    ventana.blit(medio_texto, (ANCHO // 3 + 30, 310))
    ventana.blit(dificil_texto, (ANCHO // 3 + 30, 410))

    return facil_boton, medio_boton, dificil_boton

def configurar_dificultad(dificultad):
    global FILAS, COLUMNAS, MINAS, TAMAÑO_CELDA
    if dificultad == "facil":
        FILAS, COLUMNAS, MINAS = 8, 8, 10
    elif dificultad == "medio":
        FILAS, COLUMNAS, MINAS = 12, 12, 20
    elif dificultad == "dificil":
        FILAS, COLUMNAS, MINAS = 16, 16, 40
    TAMAÑO_CELDA = ANCHO // COLUMNAS

# Main loop
def main():
    global FILAS, COLUMNAS, MINAS, TAMAÑO_CELDA
    corriendo = True
    juego_terminado = False
    en_menu = True
    perdio = False
    tablero = []
    celdas_descubiertas = set()
    resolver = False
    resolver_generator = None

    while corriendo:
        if en_menu:
            facil_boton, medio_boton, dificil_boton = dibujar_menu_dificultad()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if facil_boton.collidepoint(x, y):
                        configurar_dificultad("facil")
                        tablero = generar_tablero(FILAS, COLUMNAS, MINAS)
                        celdas_descubiertas = set()
                        juego_terminado = False
                        en_menu = False
                    elif medio_boton.collidepoint(x, y):
                        configurar_dificultad("medio")
                        tablero = generar_tablero(FILAS, COLUMNAS, MINAS)
                        celdas_descubiertas = set()
                        juego_terminado = False
                        en_menu = False
                    elif dificil_boton.collidepoint(x, y):
                        configurar_dificultad("dificil")
                        tablero = generar_tablero(FILAS, COLUMNAS, MINAS)
                        celdas_descubiertas = set()
                        juego_terminado = False
                        en_menu = False

        else:
            ventana.fill(BLANCO)
            dibujar_tablero(tablero, celdas_descubiertas, juego_terminado)
            boton_reiniciar = dibujar_boton_reiniciar()
            boton_menu = dibujar_boton_menu()
            boton_resolver = dibujar_boton_resolver()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    columna = x // TAMAÑO_CELDA
                    fila = y // TAMAÑO_CELDA
                    if (fila, columna) not in celdas_descubiertas:
                        celdas_descubiertas.add((fila, columna))
                        if tablero[fila][columna] == -1:
                            perdio = True
                            juego_terminado = True
                    elif boton_reiniciar.collidepoint(x, y):
                        tablero = generar_tablero(FILAS, COLUMNAS, MINAS)
                        celdas_descubiertas = set()
                        juego_terminado = False
                        resolver = False
                    elif boton_menu.collidepoint(x, y):
                        en_menu = True
                    if boton_resolver.collidepoint(x, y):
                        resolver = not resolver
                        if resolver:
                            resolver_generator = resolver_buscaminas(tablero)

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE and not juego_terminado:
                        fila, columna = pygame.mouse.get_pos()
                        fila //= TAMAÑO_CELDA
                        columna //= TAMAÑO_CELDA
                        if (fila, columna) not in celdas_descubiertas:
                            celdas_descubiertas.add((fila, columna))
                            if tablero[fila][columna] == -1:
                                juego_terminado = True
                                perdio = True
                            if len(celdas_descubiertas) == (FILAS * COLUMNAS) - MINAS:
                                juego_terminado = True

            if resolver and resolver_generator:
                try:
                    fila, columna = next(resolver_generator)
                    celdas_descubiertas.add((fila, columna))
                    if tablero[fila][columna] == -1:
                        juego_terminado = True
                        perdio = True
                    if len(celdas_descubiertas) == (FILAS * COLUMNAS) - MINAS:
                        juego_terminado = True
                except StopIteration:
                    resolver = False

            if juego_terminado:
                mensaje = "Perdiste!" if perdio else "¡Ganaste!"
                mostrar_mensaje(ventana, mensaje)

        pygame.display.flip()

    pygame.quit()

main()
