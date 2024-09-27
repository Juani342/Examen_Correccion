'''
Examen_Correcion
'''
import tkinter as tk
from tkinter import messagebox
import random
import sys  # Añadimos sys para cerrar el programa al final

# Clase del juego
class Game:
    def __init__(self):
        self.score = 0  # Puntaje inicial
        self.level = 1  # Nivel inicial
        self.intentos = 10  # Máximo de intentos

    def mostrar_puntaje_total(self):
        messagebox.showinfo("Puntaje Total", f"Tu puntaje total es: {self.score}")

# Ventana de bienvenida
def mostrar_bienvenida():
    bienvenida = tk.Tk()
    bienvenida.title("Bienvenido a Adivina la Moneda")
    bienvenida.geometry("400x300")

    lbl_bienvenida = tk.Label(bienvenida, text="¡Bienvenido a Adivina la Moneda!", font=("Helvetica", 16))
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
    instrucciones.geometry("800x500")

    texto_instrucciones = (
        "Instrucciones del juego:\n\n"
        "1. Selecciona 'Jugar' para iniciar.\n"
        "2. Adivina si la moneda caerá en cara o cruz.\n"
        "3. Si aciertas, ganas 350 puntos. Si fallas, pierdes 150 puntos.\n"
        "4. Tienes un máximo de 10 intentos para conseguir la mayor cantidad de puntos."
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
    root.title("Adivina la Moneda")
    root.geometry("400x300")

    global game
    game = Game()

    btn_play = tk.Button(root, text="Jugar", command=iniciar_juego, width=20)
    btn_play.pack(pady=10)

    btn_exit = tk.Button(root, text="Salir", command=lambda: [game.mostrar_puntaje_total(), root.quit()], width=20)
    btn_exit.pack(pady=10)

    root.mainloop()

# Nueva ventana o cuadro para jugar
def iniciar_juego():
    global game_window, lbl_resultado, lbl_intentos, lbl_puntaje

    root.withdraw()  # Ocultamos la ventana principal al comenzar el juego

    if 'game_window' not in globals():  # Si la ventana no existe, la creamos
        game_window = tk.Toplevel(root)
        game_window.title("Adivina la Moneda")
        game_window.geometry("400x250")

        lbl_instruccion = tk.Label(game_window, text="Elige: ¿Cara o Cruz?", font=("Helvetica", 14))
        lbl_instruccion.pack(pady=10)

        control_frame = tk.Frame(game_window)
        control_frame.pack()

        tk.Button(control_frame, text="Cara", command=lambda: adivinar_moneda("cara")).grid(row=0, column=0, padx=20)
        tk.Button(control_frame, text="Cruz", command=lambda: adivinar_moneda("cruz")).grid(row=0, column=1, padx=20)

        lbl_resultado = tk.Label(game_window, text="", font=("Helvetica", 14))
        lbl_resultado.pack(pady=10)

        lbl_intentos = tk.Label(game_window, text=f"Intentos restantes: {game.intentos}", font=("Helvetica", 12))
        lbl_intentos.pack()

        lbl_puntaje = tk.Label(game_window, text=f"Puntaje: {game.score}", font=("Helvetica", 12))
        lbl_puntaje.pack(pady=10)
    else:
        game_window.deiconify()  # Reutilizamos la misma ventana y solo la mostramos de nuevo

def adivinar_moneda(eleccion):
    if game.intentos > 0:
        resultado = random.choice(["cara", "cruz"])
        if eleccion == resultado:
            game.score += 350  # Sumar puntos si acierta
            lbl_resultado.config(text=f"¡Acertaste! La moneda cayó en {resultado}.")
        else:
            game.score -= 150  # Restar puntos si falla
            lbl_resultado.config(text=f"Fallaste. La moneda cayó en {resultado}.")

        game.intentos -= 1
        lbl_intentos.config(text=f"Intentos restantes: {game.intentos}")
        lbl_puntaje.config(text=f"Puntaje: {game.score}")

        if game.intentos == 0:
            finalizar_juego()
    else:
        finalizar_juego()

# Función para cerrar el programa al finalizar el juego
def finalizar_juego():
    game.mostrar_puntaje_total()  # Mostramos el puntaje total
    print("El juego ha terminado.")  # Mensaje opcional en consola
    sys.exit()  # Cierra el programa

# Iniciar el juego
if __name__ == "__main__":
    mostrar_bienvenida()
