'''
Examen 1era Unidad - Juego en 1D
'''
import tkinter as tk
from tkinter import messagebox
import random

# Clase del juego
class Game:
    def __init__(self):
        self.score = 0  # Puntaje inicial
        self.level = 1  # Nivel inicial

    def mostrar_puntaje_total(self):
        messagebox.showinfo("Puntaje Total", f"Tu puntaje total es: {self.score}")

# Ventana de bienvenida
def mostrar_bienvenida():
    bienvenida = tk.Tk()
    bienvenida.title("Bienvenido a NitoAttack")
    bienvenida.geometry("400x300")

    lbl_bienvenida = tk.Label(bienvenida, text="¡Bienvenido a NitoAttack !", font=("Helvetica", 16))
    lbl_bienvenida.pack(pady=50)

    btn_comenzar = tk.Button(bienvenida, text="Comenzar", command=lambda: iniciar_ventana_principal(bienvenida), width=20)
    btn_comenzar.pack(pady=10)

    btn_instrucciones = tk.Button(bienvenida, text="Instrucciones", command=lambda: [bienvenida.destroy(), mostrar_instrucciones()], width=20)
    btn_instrucciones.pack(pady=10)

    btn_salir = tk.Button(bienvenida, text="Salir", command=bienvenida.quit, width=20)
    btn_salir.pack(pady=10)

    bienvenida.mainloop()

# Ventana de instrucciones
def mostrar_instrucciones():
    instrucciones = tk.Tk()
    instrucciones.title("Instrucciones")
    instrucciones.geometry("800x600")
    instrucciones.resizable(False, False)

    texto_instrucciones = (
        "Instrucciones del juego en 1D:\n\n"
        "1. Selecciona 'Jugar' para iniciar la batalla.\n"
        "2. Mueve a tu jugador a la izquierda o derecha en la línea.\n"
        "3. Ataca o evade a los enemigos que encuentres en tu camino.\n"
        "4. Derrota a todos los enemigos para conseguir la máxima puntuación.\n"
    )

    tk.Label(instrucciones, text=texto_instrucciones, font=("Helvetica", 14), justify="left").pack(pady=20)
    tk.Button(instrucciones, text="Jugar", command=lambda: [instrucciones.destroy(), iniciar_ventana_principal(None)]).pack(pady=10)

    instrucciones.mainloop()

# Ventana principal
def iniciar_ventana_principal(bienvenida):
    if bienvenida:
        bienvenida.destroy()  # Cerrar la ventana de bienvenida
    global root
    root = tk.Tk()
    root.title("NitoAttack en 1D")
    root.geometry("800x600")

    global game
    game = Game()

    btn_play = tk.Button(root, text="Jugar", command=iniciar_juego, width=20)
    btn_play.pack(pady=10)

    btn_exit = tk.Button(root, text="Salir", command=lambda: [game.mostrar_puntaje_total(), root.quit()], width=20)
    btn_exit.pack(pady=10)

    root.mainloop()

# Nueva función para iniciar el juego en una nueva ventana
def iniciar_juego():
    global game_window, board, battling
    root.withdraw()  # Ocultar la ventana principal

    game_window = tk.Tk()
    game_window.title("NitoAttack en 1D - Juego en Progreso")
    game_window.geometry("800x200")

    board = tk.Canvas(game_window, width=400, height=100)
    board.pack()

    control_frame = tk.Frame(game_window)
    control_frame.pack()

    tk.Button(control_frame, text="Izquierda", command=lambda: move_player(-1)).grid(row=0, column=0)
    tk.Button(control_frame, text="Derecha", command=lambda: move_player(1)).grid(row=0, column=2)

    draw_board(board)
    battling = False  # Estado de batalla inicial
    game_window.mainloop()

# Configuración inicial del juego
board_size = 8
player_position = 0
queen_position = board_size-1
enemies = {}
current_level = 1

def init_enemies(level):
    global enemies
    enemy_count = level + 2
    enemies = {
        "pawn": [random.randint(1, board_size-2) for _ in range(enemy_count)],
        "knight": [random.randint(1, board_size-2) for _ in range(level)],
        "rook": [random.randint(1, board_size-2) for _ in range(1)]
    }

init_enemies(current_level)

def draw_board(canvas):
    canvas.delete("all")
    square_size = 50
    # Dibujar las casillas (ahora es una línea)
    for i in range(board_size):
        color = "white" if i % 2 == 0 else "gray"
        canvas.create_rectangle(i*square_size, 0, (i+1)*square_size, square_size, fill=color)

    # Dibujar el jugador (azul)
    px = player_position
    canvas.create_oval(px*square_size+10, 10, (px+1)*square_size-10, square_size-10, fill="blue")

    # Dibujar la reina (rojo)
    qx = queen_position
    canvas.create_oval(qx*square_size+10, 10, (qx+1)*square_size-10, square_size-10, fill="red")

    # Dibujar los enemigos
    for pos in enemies["pawn"]:
        canvas.create_rectangle(pos*square_size+10, 10, (pos+1)*square_size-10, square_size-10, fill="green")
    for pos in enemies["knight"]:
        canvas.create_rectangle(pos*square_size+10, 10, (pos+1)*square_size-10, square_size-10, fill="purple")
    for pos in enemies["rook"]:
        canvas.create_rectangle(pos*square_size+10, 10, (pos+1)*square_size-10, square_size-10, fill="yellow")

def move_player(dx):
    global player_position, battling
    new_pos = player_position + dx

    if 0 <= new_pos < board_size:
        player_position = new_pos
        check_collisions()
        draw_board(board)

def check_collisions():
    global current_level, battling
    if player_position == queen_position:
        tk.messagebox.showinfo("Victoria", f"¡Has derrotado a la Reina en el nivel {current_level}! Avanzas al siguiente nivel.")
        current_level += 1
        if current_level > 3:
            game.mostrar_puntaje_total()  # Mostrar puntaje total
            game_window.quit()  # Cierra la ventana del juego
            root.quit()  # Cierra la ventana de la aplicación principal
            exit()  # Cierra la aplicación completamente
        else:
            reset_game()

    for enemy_type, positions in enemies.items():
        if player_position in positions and not battling:
            battling = True  # Cambia el estado a en batalla
            action = tk.messagebox.askquestion("¡Enemigo!", f"Te has encontrado con un {enemy_type}. ¿Quieres enfrentarlo?")
            if action == 'yes':
                defeat_enemy(enemy_type, player_position)
            else:
                move_player(-1)  # Mueve al jugador hacia atrás si decide no luchar
            battling = False  # Restablece el estado después de la batalla

def defeat_enemy(enemy_type, position):
    if position in enemies[enemy_type]:
        enemies[enemy_type].remove(position)
        tk.messagebox.showinfo("Éxito", f"¡Has derrotado al {enemy_type}!")
        if enemy_type == "pawn":
            game.score += 15
        elif enemy_type == "knight":
            game.score += 25
        elif enemy_type == "rook":
            game.score += 50
        draw_board(board)

def reset_game():
    global player_position, queen_position
    player_position = 0
    queen_position = board_size-1
    init_enemies(current_level)
    draw_board(board)

# Iniciar el juego
if __name__ == "__main__":
    mostrar_bienvenida()
