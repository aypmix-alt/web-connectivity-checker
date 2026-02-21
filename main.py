"""
Web Connectivity Checker PRO
Autor: Damián
Descripción:
Aplicación con interfaz gráfica que verifica si un sitio web está en línea
usando urllib y Tkinter.
"""

import tkinter as tk
from tkinter import messagebox
import urllib.request
import urllib.error


# ==================================================
# LÓGICA DE NEGOCIO (NO depende de la interfaz)
# ==================================================

def verificar_sitio(url: str) -> tuple:
    """
    Verifica si un sitio web responde correctamente.

    Retorna:
        (True, codigo_http) si responde.
        (False, mensaje_error) si falla.
    """

    # Buena práctica: limpiar espacios
    url = url.strip()

    # Si el usuario no escribe http/https, lo agregamos
    if not url.startswith("http"):
        url = "https://" + url

    try:
        respuesta = urllib.request.urlopen(url, timeout=10)
        codigo = respuesta.getcode()

        if codigo == 200:
            return True, codigo
        else:
            return False, f"Código HTTP: {codigo}"

    except urllib.error.HTTPError as e:
        return False, f"Error HTTP: {e.code}"

    except urllib.error.URLError:
        return False, "No se pudo establecer conexión (DNS / Internet)"

    except Exception as e:
        return False, f"Error inesperado: {str(e)}"


# ==================================================
# INTERFAZ GRÁFICA
# ==================================================

class ConnectivityApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Web Connectivity Checker PRO")
        self.root.geometry("450x230")
        self.root.resizable(False, False)

        self.crear_widgets()

    def crear_widgets(self):

        self.label = tk.Label(
            self.root,
            text="Ingresa la URL (ej: google.com):",
            font=("Arial", 11)
        )
        self.label.pack(pady=15)

        self.entry_url = tk.Entry(self.root, width=50)
        self.entry_url.pack(pady=5)
        self.entry_url.focus()

        self.boton = tk.Button(
            self.root,
            text="Verificar Estado",
            command=self.procesar_verificacion,
            bg="#2E8B57",
            fg="white",
            padx=10,
            pady=5
        )
        self.boton.pack(pady=20)

    def procesar_verificacion(self):

        url_usuario = self.entry_url.get()

        if not url_usuario:
            messagebox.showwarning(
                "Atención",
                "Por favor, ingresa una dirección web."
            )
            return

        self.root.config(cursor="watch")
        self.root.update()

        estado, info = verificar_sitio(url_usuario)

        self.root.config(cursor="")

        if estado:
            messagebox.showinfo(
                "Resultado",
                f"✔ El sitio está en línea.\nCódigo HTTP: {info}"
            )
        else:
            messagebox.showerror(
                "Resultado",
                f"✖ No disponible.\nDetalle: {info}"
            )


# ==================================================
# PUNTO DE ENTRADA
# ==================================================

def main():
    root = tk.Tk()
    app = ConnectivityApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()