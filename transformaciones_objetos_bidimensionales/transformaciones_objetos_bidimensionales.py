import tkinter as tk
import numpy as np
import math
import time

class Transformaciones2D:
    def __init__(self, master):
        self.master = master
        self.master.title("Transformación de Objetos Bidimensionales")
        self.canvas = tk.Canvas(master, width=600, height=600, bg="white")
        self.canvas.pack()

        # --- Ejes cartesianos ---
        self.centro = np.array([300, 300])
        self.canvas.create_line(0, 300, 600, 300, fill="gray", arrow=tk.LAST)  # Eje X
        self.canvas.create_line(300, 600, 300, 0, fill="gray", arrow=tk.LAST)  # Eje Y

        # --- Objeto inicial (triángulo en el primer cuadrante) ---
        self.objeto_original = np.array([
            [50, 50, 1],
            [100, 50, 1],
            [75, 100, 1]
        ])
        self.objeto = np.copy(self.objeto_original)
        self.angulo = 0
        self.escala = 1.0
        self.tx, self.ty = 0, 0

        self.dibujar_objeto()

        # --- Eventos ---
        self.master.bind("<Right>", self.rotar_derecha)
        self.master.bind("<Left>", self.rotar_izquierda)
        self.master.bind("<Up>", self.escalar_mas)
        self.master.bind("<Down>", self.escalar_menos)
        self.canvas.bind("<Button-1>", self.trasladar)
        
        # --- Botón de secuencia ---
        tk.Button(master, text="Secuencia", command=self.secuencia).pack(pady=10)

    # =====================================================
    # FUNCIONES DE TRANSFORMACIÓN
    # =====================================================

    def matriz_rotacion(self, angulo):
        rad = math.radians(angulo)
        return np.array([
            [math.cos(rad), -math.sin(rad), 0],
            [math.sin(rad),  math.cos(rad), 0],
            [0, 0, 1]
        ])

    def matriz_escala(self, sx, sy):
        return np.array([
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, 1]
        ])

    def matriz_traslacion(self, tx, ty):
        return np.array([
            [1, 0, tx],
            [0, 1, ty],
            [0, 0, 1]
        ])

    # =====================================================
    # APLICACIÓN DE TRANSFORMACIONES
    # =====================================================

    def aplicar_transformacion(self):
        # Orden de transformación: Escala → Rotación → Traslación
        M = self.matriz_traslacion(self.tx, self.ty) @ \
            self.matriz_rotacion(self.angulo) @ \
            self.matriz_escala(self.escala, self.escala)

        self.objeto = (self.objeto_original @ M.T)
        self.dibujar_objeto()

    def dibujar_objeto(self):
        self.canvas.delete("objeto")
        puntos = []
        for x, y, _ in self.objeto:
            px = self.centro[0] + x
            py = self.centro[1] - y
            puntos.extend([px, py])
        self.canvas.create_polygon(puntos, outline="blue", fill="skyblue", tags="objeto")

    # =====================================================
    # CONTROLES INTERACTIVOS
    # =====================================================

    def rotar_derecha(self, event=None):
        self.angulo += 10
        self.aplicar_transformacion()

    def rotar_izquierda(self, event=None):
        self.angulo -= 10
        self.aplicar_transformacion()

    def escalar_mas(self, event=None):
        self.escala *= 1.1
        self.aplicar_transformacion()

    def escalar_menos(self, event=None):
        self.escala *= 0.9
        self.aplicar_transformacion()

    def trasladar(self, event):
        # Convertir coordenadas del clic a sistema cartesiano
        x = event.x - self.centro[0]
        y = -(event.y - self.centro[1])
        self.tx, self.ty = x, y
        self.aplicar_transformacion()

    # =====================================================
    # SECUENCIA AUTOMÁTICA
    # =====================================================

    def secuencia(self):
        for _ in range(18):  # 180 grados (18 pasos de 10°)
            self.angulo += 10
            self.aplicar_transformacion()
            self.master.update()
            time.sleep(0.05)
        for _ in range(5):
            self.escala *= 1.1
            self.aplicar_transformacion()
            self.master.update()
            time.sleep(0.05)
        for t in range(0, 100, 5):
            self.tx = t
            self.ty = t / 2
            self.aplicar_transformacion()
            self.master.update()
            time.sleep(0.05)

# =====================================================
# EJECUCIÓN
# =====================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = Transformaciones2D(root)
    root.mainloop()
