import socket
import time
import random
import tkinter as tk
from threading import Thread

# Configuración de GUI
root = tk.Tk()
root.title("Servidor de Tensión Arterial y Ubicación")

# Área de texto para mostrar logs
log_text = tk.Text(root, height=15, width=50, state="disabled")
log_text.pack(padx=10, pady=10)

# Botón de inicio de servidor
start_button = tk.Button(root, text="Iniciar Servidor", state="normal")
start_button.pack(pady=5)

# Variables de control
server_socket = None
is_server_running = False

# Función para loguear mensajes en la GUI
def log_message(message):
    log_text.config(state="normal")
    log_text.insert("end", f"{message}\n")
    log_text.config(state="disabled")
    log_text.see("end")

# Función del servidor
def start_server():
    global server_socket, is_server_running
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 3128))
    server_socket.listen(1)
    is_server_running = True
    log_message("Servidor en espera de conexión en el puerto 3128")

    while is_server_running:
        try:
            client_socket, addr = server_socket.accept()
            log_message(f"Conexión establecida con {addr}")
            while is_server_running:
                # Generar valores de tensión y ubicación aleatorios
                tension = round(random.uniform(60, 180), 1)
                latitude = 40.7128 + random.uniform(-0.01, 0.01)
                longitude = -74.0060 + random.uniform(-0.01, 0.01)

                # Enviar datos formateados al cliente
                data = f"{tension},{latitude},{longitude}"
                client_socket.sendall(data.encode('utf-8'))
                log_message(f"Datos enviados: {data}")

                # Espera de 3 segundo
                time.sleep(3)
        except (ConnectionResetError, BrokenPipeError):
            log_message("Cliente desconectado.")
        except Exception as e:
            log_message(f"Error del servidor: {e}")
        finally:
            client_socket.close()

# Función para iniciar el servidor en un hilo separado
def start_server_thread():
    global server_thread
    server_thread = Thread(target=start_server, daemon=True)
    server_thread.start()
    start_button.config(state="disabled")

# Asociar la función de inicio al botón
start_button.config(command=start_server_thread)

root.mainloop()

