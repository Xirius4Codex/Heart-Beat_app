import socket
import tkinter as tk
from tkinter import scrolledtext

class EmuladorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cliente de Emulador")

        # Campo de texto desplazable para mostrar los datos recibidos
        self.output_text = scrolledtext.ScrolledText(self.root, width=50, height=15, state='disabled')
        self.output_text.grid(row=0, column=0, padx=10, pady=10)

        # Botón de conexión
        self.connect_button = tk.Button(self.root, text="Conectar", command=self.connect_to_emulator)
        self.connect_button.grid(row=1, column=0, padx=10, pady=10)

        # Configuración del socket
        self.ip_address = 'localhost'
        self.port = 8080
        self.client_socket = None

    def connect_to_emulator(self):
        try:
            # Crear y conectar el socket
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.ip_address, self.port))
            self.update_output("Conexión establecida con el emulador")

            # Comenzar a recibir datos
            self.receive_data()
        except socket.error as e:
            self.update_output(f"Error de conexión: {e}")

    def receive_data(self):
        try:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                self.update_output(f"Datos recibidos: {data.decode('utf-8')}")
        except socket.error as e:
            self.update_output(f"Error al recibir datos: {e}")
        finally:
            self.client_socket.close()

    def update_output(self, message):
        # Habilitar, insertar y deshabilitar el campo de texto para evitar edición
        self.output_text.config(state='normal')
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.config(state='disabled')
        self.output_text.yview(tk.END)  # Desplazarse al final

# Inicializar la GUI
root = tk.Tk()
app = EmuladorGUI(root)
root.mainloop()


