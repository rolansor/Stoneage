#modulos
import sys, pygame, random, speech

from pygame.locals import *


#constantes
WIDTH = 400
HEIGHT = 400
FILAS = 10
COLUMNAS = 10
BARRANCO = 0
CAMINO = 1
META = 2
COMPLETO = 8
PIEDRA = 3
JUGADOR = 4
SUBE = 4
BAJA = 7
IZQUIERDA = 8
DERECHA = 9

#clases
#----------------------------------
#clase casillero: el tablero tendra una matriz de casilleros
class Casillero(pygame.sprite.Sprite):
    #ocnstructor que ubica el casillero en la pantalla
    def __init__(self,tipo,x,y,screen):
        pygame.sprite.Sprite.__init__(self)
        self.tipo = tipo
        self.imagen = load_image('images/camino.png',False)
        if self.tipo == BARRANCO:
            self.imagen = load_image('images/obstaculo.png',True)
        if self.tipo == CAMINO:
            self.imagen = load_image('images/camino.png',False)
        if self.tipo == COMPLETO:
            self.imagen = load_image('images/done.png',False)
        if self.tipo == JUGADOR:
            self.imagen = load_image('images/jugador.png',False)
        if self.tipo == META:
            self.imagen = load_image('images/meta.png',False)
        if self.tipo == PIEDRA:
            self.imagen = load_image('images/piedra.png',True)
        self.rect = self.imagen.get_rect()
        self.rect.centerx = x*40 - 20
        self.rect.centery = y*40 - 20
        screen.blit(self.imagen, self.rect)
    
    def get_tipo(self):
        return self.tipo

#clase tablero, hereda de sprite
class Tablero(pygame.sprite.Sprite):
    def __init__(self,screen):
        pygame.sprite.Sprite.__init__(self)
        self.puntos = 0
        self.screen = screen
        self.pantalla_inicio()
        #inicializacion de la matriz
        self.matriz = [ [ Casillero(CAMINO,i,j,screen) for i in range(FILAS+1) ] for j in range(COLUMNAS+1) ]
        #colocar 20 celdas barranco
        for i in range(7):
            fila = random.randrange(1,FILAS)
            columna = random.randrange(1,COLUMNAS)
            if fila==5 and columna==5:
                fila = random.randrange(1,FILAS)
                columna = random.randrange(1,COLUMNAS)
            self.matriz[fila][columna] = Casillero(BARRANCO,fila,columna,screen)
        #colocar 3 piedras en el tablero
        cont = 0
        while cont < 3:
            fila = random.randrange(1,FILAS)
            columna = random.randrange(1,COLUMNAS)
            if self.matriz[fila][columna].get_tipo() == CAMINO:
                if fila != 1 and fila != FILAS and columna != 1 and columna != COLUMNAS:
                    cont += 1
                    self.matriz[fila][columna] = Casillero(PIEDRA,fila,columna,screen)
        #colocar 3 metas en el tablero
        cont = 0
        while cont < 3:
            fila = random.randrange(1,FILAS)
            columna = random.randrange(1,COLUMNAS)
            if self.matriz[fila][columna].get_tipo() == CAMINO:
                cont += 1
                self.matriz[fila][columna] = Casillero(META,fila,columna,screen)
        #colocar jugador en la pantalla
        self.matriz[5][5] = Casillero(JUGADOR,5,5,screen)
        #actualizar la pantalla
        pygame.display.flip()
    #obtener las celdas que estan inmediatamente arriba, abajo, a la izquierda o derecha
    def get_superior(self,x,y):
        if y-1 >= 1:
            return self.matriz[x][y-1]
        return Casillero(BARRANCO,x,y-1,self.screen)
    
    def get_inferior(self,x,y):
        if y+1 <= COLUMNAS:
            return self.matriz[x][y+1]
        return Casillero(BARRANCO,x,y+1,self.screen)
    
    def get_izquierda(self,x,y):
        if x-1 >= 1:
            return self.matriz[x-1][y]
        return Casillero(BARRANCO,x-1,y,self.screen)
    
    def get_derecha(self,x,y):
        if x+1 <= FILAS:
            return self.matriz[x+1][y]
        return Casillero(BARRANCO,x+1,y,self.screen)
    
    #obtener las celdas que estan en cada direccion a dos espacios del jugador
    def get_superior2(self,x,y):
        if y-2 >= 1:
            return self.matriz[x][y-2]
        return Casillero(BARRANCO,x,y-2,self.screen)
    
    def get_inferior2(self,x,y):
        if y+2 <= COLUMNAS:
            return self.matriz[x][y+2]
        return Casillero(BARRANCO,x,y+2,self.screen)
    
    def get_izquierda2(self,x,y):
        if x-2 >= 1:
            return self.matriz[x-2][y]
        return Casillero(BARRANCO,x-2,y,self.screen)
    
    def get_derecha2(self,x,y):
        if x+2 <= FILAS:
            return self.matriz[x+2][y]
        return Casillero(BARRANCO,x+2,y,self.screen)

    def pantalla_inicio(self):
            imagen = load_image('images/inicio_juego.png',False)
            rect = imagen.get_rect()
            rect.centerx = 200 #la mitad horizontal de la pantalla
            rect.centery = 200 #la mitad vertical de la pantalla
            self.screen.blit(imagen, rect)
            pygame.display.flip()
            pygame.mixer.music.load("sounds/mario.mid")
            pygame.mixer.music.play()
            pygame.mixer.music.fadeout(20)
            pygame.time.delay(4000)
            
    def pantalla_fin(self):
            imagen = load_image('images/winner.jpg',False)
            rect = imagen.get_rect()
            rect.centerx = 200 #la mitad horizontal de la pantalla
            rect.centery = 200 #la mitad vertical de la pantalla
            self.screen.blit(imagen, rect)
            pygame.display.flip()
            pygame.time.delay(5000)
        
        
#Clase jugador, representa el jugador y sus movimientos 
class Jugador(pygame.sprite.Sprite):
    def __init__(self,screen):
        self.posicionx = 5
        self.posiciony = 5
        self.restantes = 3
        self.speed = 1
        self.movimiento = 0
        self.screen = screen
        
    
    #mover el jugador en el tablero 
    #OJO SE RECIBE SOLO LA MATRIZ Y NO TODO EL OBJETO TIPO TABLERO          
    def mover(self,tablero,screen):
        #declaracion del reloj que controla la velocidad del juego
        tablero_juego = tablero.matriz #saco la matriz del objeto tablero
        arriba = tablero.get_superior(self.posicionx,self.posiciony)
        abajo = tablero.get_inferior(self.posicionx,self.posiciony)
        izquierda = tablero.get_izquierda(self.posicionx,self.posiciony)
        derecha = tablero.get_derecha(self.posicionx,self.posiciony)
        arriba2 = tablero.get_superior2(self.posicionx,self.posiciony)
        abajo2 = tablero.get_inferior2(self.posicionx,self.posiciony)
        izquierda2 = tablero.get_izquierda2(self.posicionx,self.posiciony)
        derecha2 = tablero.get_derecha2(self.posicionx,self.posiciony)
        if self.movimiento == SUBE: #presiona arriba
            pygame.time.delay(100)
            if arriba.get_tipo() == CAMINO: #arriba hay camino
                tablero_juego[self.posicionx][self.posiciony-1] = Casillero(JUGADOR,self.posicionx,self.posiciony-1,self.screen)
                tablero_juego[self.posicionx][self.posiciony] = Casillero(CAMINO,self.posicionx,self.posiciony,self.screen)
                self.posiciony -= 1 #subir la posicion interna del jugador
                self.movimiento = 0 #para que se detenga inmediatamente 
                pygame.mixer.init()
                pygame.mixer.music.load("sounds/move.mp3")
                pygame.mixer.music.play()
            if arriba.get_tipo() == PIEDRA: #arriba hay una piedra
                if arriba2.get_tipo() == CAMINO: #arriba hay piedra, y mas arriba hay camino
                    tablero_juego[self.posicionx][self.posiciony-2] = Casillero(PIEDRA,self.posicionx,self.posiciony-2,self.screen)
                    tablero_juego[self.posicionx][self.posiciony-1] = Casillero(JUGADOR,self.posicionx,self.posiciony-1,self.screen)
                    tablero_juego[self.posicionx][self.posiciony] = Casillero(CAMINO,self.posicionx,self.posiciony,self.screen)
                    self.posiciony -= 1
                    self.movimiento = 0 #para que se detenga inmediatamente
                if arriba2.get_tipo() == META: #arriba hay piedra, y mas arriba hay meta
                    tablero_juego[self.posicionx][self.posiciony-2] = Casillero(COMPLETO,self.posicionx,self.posiciony-2,self.screen)
                    tablero_juego[self.posicionx][self.posiciony-1] = Casillero(JUGADOR,self.posicionx,self.posiciony-1,self.screen)
                    tablero_juego[self.posicionx][self.posiciony] = Casillero(CAMINO,self.posicionx,self.posiciony,self.screen)
                    self.posiciony -= 1
                    self.restantes -= 1
                    self.movimiento = 0 #para que se detenga inmediatamente
        if self.movimiento == BAJA: #presiona abajo
            pygame.time.delay(100)
            if abajo.get_tipo() == CAMINO: #abajo hay camino
                tablero_juego[self.posicionx][self.posiciony+1] = Casillero(JUGADOR,self.posicionx,self.posiciony+1,self.screen)
                tablero_juego[self.posicionx][self.posiciony] = Casillero(CAMINO,self.posicionx,self.posiciony,self.screen)
                self.posiciony += 1
                self.movimiento = 0 #para que se detenga inmediatamente
            if abajo.get_tipo() == PIEDRA: #abajo hay una piedra
                if abajo2.get_tipo() == CAMINO: #abajo hay piedra, y mas abajo hay camino
                    tablero_juego[self.posicionx][self.posiciony+2] = Casillero(PIEDRA,self.posicionx,self.posiciony+2,self.screen)
                    tablero_juego[self.posicionx][self.posiciony+1] = Casillero(JUGADOR,self.posicionx,self.posiciony+1,self.screen)
                    tablero_juego[self.posicionx][self.posiciony] = Casillero(CAMINO,self.posicionx,self.posiciony,self.screen)
                    self.posiciony += 1
                    self.movimiento = 0 #para que se detenga inmediatamente
                if abajo2.get_tipo() == META: #abajo hay piedra, y mas abajo hay meta
                    tablero_juego[self.posicionx][self.posiciony+2] = Casillero(COMPLETO,self.posicionx,self.posiciony+2,self.screen)
                    tablero_juego[self.posicionx][self.posiciony+1] = Casillero(JUGADOR,self.posicionx,self.posiciony+1,self.screen)
                    tablero_juego[self.posicionx][self.posiciony] = Casillero(CAMINO,self.posicionx,self.posiciony,self.screen)
                    self.posiciony += 1
                    self.restantes -= 1
                    self.movimiento = 0 #para que se detenga inmediatamente
        if self.movimiento == IZQUIERDA: #presiona izquierda
            pygame.time.delay(100)
            if izquierda.get_tipo() == CAMINO: #izquierda hay camino
                tablero_juego[self.posicionx-1][self.posiciony] = Casillero(JUGADOR,self.posicionx-1,self.posiciony,self.screen)
                tablero_juego[self.posicionx][self.posiciony] = Casillero(CAMINO,self.posicionx,self.posiciony,self.screen)
                self.posicionx -= 1
                self.movimiento = 0 #para que se detenga inmediatamente
            if izquierda.get_tipo() == PIEDRA: #izquierda hay una piedra
                if izquierda2.get_tipo() == CAMINO: #izquierda hay piedra, y mas izquierda hay camino
                    tablero_juego[self.posicionx-2][self.posiciony] = Casillero(PIEDRA,self.posicionx-2,self.posiciony,self.screen)
                    tablero_juego[self.posicionx-1][self.posiciony] = Casillero(JUGADOR,self.posicionx-1,self.posiciony,self.screen)
                    tablero_juego[self.posicionx][self.posiciony] = Casillero(CAMINO,self.posicionx,self.posiciony,self.screen)
                    self.posicionx -= 1
                    self.movimiento = 0 #para que se detenga inmediatamente
                if izquierda2.get_tipo() == META: #izquierda hay piedra, y mas izquierda hay meta
                    tablero_juego[self.posicionx-2][self.posiciony] = Casillero(COMPLETO,self.posicionx-2,self.posiciony,self.screen)
                    tablero_juego[self.posicionx-1][self.posiciony] = Casillero(JUGADOR,self.posicionx-1,self.posiciony,self.screen)
                    tablero_juego[self.posicionx][self.posiciony] = Casillero(CAMINO,self.posicionx,self.posiciony,self.screen)
                    self.posicionx -= 1
                    self.restantes -= 1
                    self.movimiento = 0 #para que se detenga inmediatamente
        if self.movimiento == DERECHA: #presiona derecha
            pygame.time.delay(100)
            if derecha.get_tipo() == CAMINO: #derecha hay camino
                tablero_juego[self.posicionx+1][self.posiciony] = Casillero(JUGADOR,self.posicionx+1,self.posiciony,self.screen)
                tablero_juego[self.posicionx][self.posiciony] = Casillero(CAMINO,self.posicionx,self.posiciony,self.screen)
                self.posicionx += 1
                self.movimiento = 0 #para que se detenga inmediatamente
            if derecha.get_tipo() == PIEDRA: #derecha hay una piedra
                if derecha2.get_tipo() == CAMINO: #derecha hay piedra, y mas derecha hay camino
                    tablero_juego[self.posicionx+2][self.posiciony] = Casillero(PIEDRA,self.posicionx+2,self.posiciony,self.screen)
                    tablero_juego[self.posicionx+1][self.posiciony] = Casillero(JUGADOR,self.posicionx+1,self.posiciony,self.screen)
                    tablero_juego[self.posicionx][self.posiciony] = Casillero(CAMINO,self.posicionx,self.posiciony,self.screen)
                    self.posicionx += 1
                    self.movimiento = 0 #para que se detenga inmediatamente
                if derecha2.get_tipo() == META: #derecha hay piedra, y mas derecha hay meta
                    tablero_juego[self.posicionx+2][self.posiciony] = Casillero(COMPLETO,self.posicionx+2,self.posiciony,self.screen)
                    tablero_juego[self.posicionx+1][self.posiciony] = Casillero(JUGADOR,self.posicionx+1,self.posiciony,self.screen)
                    tablero_juego[self.posicionx][self.posiciony] = Casillero(CAMINO,self.posicionx,self.posiciony,self.screen)
                    self.posicionx += 1
                    self.restantes -= 1
                    self.movimiento = 0 #para que se detenga inmediatamente
        #actualizar la pantalla
        pygame.display.flip()
    
    def callback(self,phrase,listener):
        if phrase == "uno":
            self.movimiento = SUBE
            print "sube"
        if phrase == "ocho":
            self.movimiento = BAJA
            print "baja"
        if phrase == "izquierda":
            self.movimiento = IZQUIERDA
            print "izquierda"
        if phrase == "derecha":
            self.movimiento = DERECHA
            print "derecha"
        if phrase == "salir":
            listener.stoplistening()
            sys.exit(0)
    
    def ganador(self):
        return self.restantes == 0
#-----------------------------------
#funciones
#-----------------------------------
def load_image(filename, transparent):
    try: image = pygame.image.load(filename)
    except pygame.error, message:
        raise SystemExit, message
    if transparent:
        color = image.get_at((0,0))
        image.set_colorkey(color, RLEACCEL)
    return image

def texto(texto, posx, posy, color=(255, 255, 255)):
    fuente = pygame.font.Font("images/DroidSans.ttf", 25)
    salida = pygame.font.Font.render(fuente, texto, 1, color)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Stoneage Game")
    tablero = Tablero(screen)
    jugador = Jugador(screen)
    listener = speech.listenforanything(jugador.callback)
    pygame.mixer.init()    

    while not jugador.ganador() or listener.listening():
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)
            jugador.mover(tablero, screen)
    tablero.pantalla_fin()
    return 0
#-----------------------------------

if __name__ == '__main__':
    pygame.init()
    main()