import socket
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import webbrowser
import threading

# Variables globales
data_values = []
time_values = []
client_socket = None
pacemaker_location = None
start_time = None

# Función para simular una pantalla de carga
def loading_screen():
    progress_window = tk.Toplevel(root)
    progress_window.title("Cargando...")

    loading_label = tk.Label(progress_window, text="Cargando, por favor espera...")
    loading_label.pack(pady=20)

    progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=20)

    def update_progress(value=0):
        progress_bar['value'] = value
        if value < 100:
            root.after(100, update_progress, value + 10)
        else:
            progress_window.destroy()
            connect_to_pacemaker()

    update_progress()

# Función para conectarse al marcapasos
def connect_to_pacemaker():
    global client_socket, start_time
    ip_address = 'localhost'
    port = 3128

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip_address, port))
        messagebox.showinfo("Conexión", "Conexión exitosa al marcapasos")
        ip_label.config(text=f"IP del Marcapasos: {ip_address}")
        start_time = time.time()
        receive_data()
    except socket.error as e:
        messagebox.showerror("Error", f"No se pudo conectar: {e}")
        if client_socket:
            client_socket.close()

# Función para recibir datos del marcapasos
def receive_data():
    def receive_thread():
        global data_values, time_values, pacemaker_location
        while True:
            try:
                data = client_socket.recv(1024)
                if data:
                    received_data = data.decode('utf-8').split(',')
                    tension_value = float(received_data[0])
                    latitude = float(received_data[1])
                    longitude = float(received_data[2])

                    data_values.append(tension_value)
                    current_time = time.time() - start_time
                    time_values.append(current_time)

                    root.after(0, lambda: data_label.config(text=f"Tensión: {tension_value} mmHg"))
                    root.after(0, lambda: plot_data())

                    pacemaker_location = (latitude, longitude)
            except Exception as e:
                messagebox.showerror("Error", f"Error al recibir datos: {e}")
                break

    threading.Thread(target=receive_thread, daemon=True).start()

# Función para actualizar la gráfica
def plot_data():
    if not data_values or not time_values:
        return

    ax.clear()
    ax.plot(time_values, data_values, marker='o')
    ax.set_title("Tensión del Marcapasos vs Tiempo")
    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel("Tensión (mmHg)")
    ax.set_ylim(min(data_values) - 5, max(data_values) + 5)
    ax.set_xlim(0, max(time_values))
    plt.xticks(rotation=45)
    plt.tight_layout()
    canvas.draw()

# Función para refrescar los datos
def refresh_data():
    global data_values, time_values
    data_values.clear()
    time_values.clear()
    data_label.config(text="Tensión: Esperando...")
    plot_data()

# Función para abrir Google Maps
def open_map():
    if pacemaker_location:
        lat, lon = pacemaker_location
        url = f"https://www.google.com/maps?q={lat},{lon}"
        webbrowser.open(url)
    else:
        messagebox.showwarning("Ubicación no disponible", "No se ha recibido la ubicación del marcapasos.")

# Función para manejar el cierre de la ventana
def on_closing():
    if client_socket:
        client_socket.close()
    root.destroy()

# Crear la ventana principal
root = tk.Tk()
root.title("Heart Beat")

data_label = tk.Label(root, text="Esperando datos...")
data_label.pack(pady=20)

ip_label = tk.Label(root, text="IP del Marcapasos: Desconocida")
ip_label.pack(pady=20)

fig, ax = plt.subplots(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(pady=20)

button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

connect_button = tk.Button(button_frame, text="Iniciar", command=loading_screen)
connect_button.pack(side=tk.LEFT, padx=10)

refresh_button = tk.Button(button_frame, text="Refrescar Datos", command=refresh_data)
refresh_button.pack(side=tk.LEFT, padx=10)

map_button = tk.Button(button_frame, text="Ver en Google Maps", command=open_map)
map_button.pack(side=tk.RIGHT, padx=10)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
