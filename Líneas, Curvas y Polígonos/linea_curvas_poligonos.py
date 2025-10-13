import tkinter as tk
from tkinter import ttk

class LineaCurvasPoligonos:
    def __init__(self, master):
        opciones = ["Linea", "Curva", "Polígono"]
        variable = tk.StringVar(value="Polígono")        
        
        self.master = master
        self.master.title("Líneas, Curvas y Polígonos")
        self.master.state('zoomed')
        self.master.configure(bg="white")
        
        self.lienzo = tk.Canvas(master, width=700, height=600, bg="white")
        self.lienzo.pack(pady=20)
        
        label = tk.Label(master, text="Seleccione una opción:")
        label.place(x=50, y=20)
        
        self.button_seleccionar = ttk.Combobox(master, textvariable=variable, values=opciones, state="readonly")
        self.button_seleccionar.place(x=50, y=50)
        
        # Lista para guardar los puntos
        self.puntos = []
        
        # Evento de clic
        self.lienzo.bind("<Button-1>", self.marcar_punto)
        
        # Botón para dibujar el polígono completo
        boton_poligono = tk.Button(master, text="Dibujar polígono", command=self.dibujar_poligono)
        boton_poligono.place(x=50, y=90)
        
        boton_poligono = tk.Button(master, text="Borrar", command=lambda: self.lienzo.delete("all"))
        boton_poligono.place(x=50, y=120)
       
    def marcar_punto(self, event):
        x, y = event.x, event.y
        radio = 2
        
        # Dibuja el punto
        self.lienzo.create_oval(x - radio, y - radio, x + radio, y + radio, fill="red", outline="red")
        self.puntos.append((x, y))
        
        # Dibuja líneas parciales entre los puntos (opcional)
        if len(self.puntos) > 1:
            x1, y1 = self.puntos[-2]
            self.lienzo.create_line(x1, y1, x, y, fill="blue", width=2)
    
    def dibujar_poligono(self):
        """Dibuja el polígono completo uniendo todos los puntos"""
        if len(self.puntos) >= 3:
            # Desempaqueta los puntos como lista plana [x1, y1, x2, y2, ..., xn, yn]
            coords = [coord for punto in self.puntos for coord in punto]
            # Dibuja el polígono cerrado
            self.lienzo.create_polygon(coords, outline="blue", fill="", width=2)
            # Limpia los puntos para una nueva figura
            self.puntos.clear()
        else:
            print("Se necesitan al menos 3 puntos para formar un polígono.")
                 
if __name__ == "__main__":
    root = tk.Tk()
    app = LineaCurvasPoligonos(root)
    root.mainloop()
