import tkinter as tk
from tkinter import ttk
import datetime
import time
import re

class HorarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Horario de Clases - 2º ASIR")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Datos del horario
        self.horarios = [
            {"hora": "8:30", "duracion": 55, "lunes": "0376 asir 2", "martes": "0378 asir 2", 
             "miercoles": "0378 asir 2", "jueves": "0375 asir 2", "viernes": "1710 Ipe II"},
            {"hora": "9:25", "duracion": 55, "lunes": "0376 asir 2", "martes": "CM0 II asir 2", 
             "miercoles": "0378 asir 2", "jueves": "0375 asir 2", "viernes": "1665 asir 2"},
            {"hora": "10:20", "duracion": 55, "lunes": "0375 asir 2", "martes": "0376 asir 2", 
             "miercoles": "0179asir 2", "jueves": "0374 asir 2", "viernes": "0374 asir 2"},
            {"hora": "11:15", "duracion": 30, "lunes": "0375 asir 2", "martes": "0377 asir 2", 
             "miercoles": "0374 asir 2", "jueves": "0374 asir 2", "viernes": "0374 asir 2"},
            {"hora": "11:45", "duracion": 55, "lunes": "1710 Ipe II", "martes": "0179asir 2", 
             "miercoles": "1708 asir 2", "jueves": "0378 asir 2", "viernes": "0377 asir 2"},
            {"hora": "12:40", "duracion": 55, "lunes": "CM0 II asir 2", "martes": "0375 asir 2", 
             "miercoles": "CM0 II asir 2", "jueves": "0376 asir 2", "viernes": "0377 asir 2"}
        ]
        
        # Mapeo de códigos a nombres completos
        self.modulos = {
            "0377": "ADMINISTRACIÓN DE SISTEMAS GESTORES DE BASES DE DATOS",
            "0374": "ADMINISTRACIÓN DE SISTEMAS OPERATIVOS",
            "1710": "ITINERARIO PARA LA EMPLEABILIDAD II",
            "0376": "IMPLANTACIÓN DE APLICACIONES WEB",
            "0179": "INGLÉS PROFESIONAL PARA GRADO SUPERIOR",
            "0378": "SEGURIDAD Y ALTA DISPONIBILIDAD",
            "0375": "SERVICIOS DE RED E INTERNET",
            "1665": "DIGITALIZACIÓN APLICADA A LOS SECTORES PRODUCTIVOS GS",
            "1708": "SOSTENIBILIDAD APLICADA AL SISTEMA PRODUCTIVO",
            "CM0 II": "AMPLIACIÓN APLICACIONES WEB"
        }
        
        # Mapeo de profesores
        self.profesores = {
            "0376": "Mr Mar Garcia Pérez",
            "0378": "Mr José Becerril Luj",
            "0375": "Mr José Becerril Luj",
            "1710": "Laura Largo - Coord.",
            "CM0 II": "Mr Mar Garcia Pérez",
            "0179": "Mr Angeles Cabeza",
            "0374": "Miguel A. García Sol",
            "0377": "Mr Vicorda Bullón A",
            "1665": "Miguel A. García Sol",
            "1708": "Mr Nicarona Delgado"
        }
        
        self.setup_ui()
        self.actualizar_tiempo()
        
    def setup_ui(self):
        # Título
        titulo = tk.Label(self.root, text="HORARIO DE CLASES - 2º ASIR", 
                         font=("Arial", 16, "bold"), bg='#2c3e50', fg='white', pady=10)
        titulo.pack(fill=tk.X)
        
        # Frame para el tiempo restante
        self.frame_tiempo = tk.Frame(self.root, bg='#3498db', padx=20, pady=10)
        self.frame_tiempo.pack(fill=tk.X, padx=10, pady=10)
        
        self.label_tiempo = tk.Label(self.frame_tiempo, text="", font=("Arial", 14, "bold"), 
                                    bg='#3498db', fg='white')
        self.label_tiempo.pack()
        
        # Frame para la tabla del horario
        frame_tabla = tk.Frame(self.root, bg='#f0f0f0')
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear tabla
        self.crear_tabla(frame_tabla)
        
        # Información adicional
        frame_info = tk.Frame(self.root, bg='#ecf0f1', padx=10, pady=10)
        frame_info.pack(fill=tk.X, padx=10, pady=10)
        
        info_text = "Haz clic en cualquier clase para ver más detalles"
        tk.Label(frame_info, text=info_text, font=("Arial", 10), 
                bg='#ecf0f1', fg='#7f8c8d').pack()
        
    def crear_tabla(self, parent):
        # Crear Treeview
        columns = ('hora', 'lunes', 'martes', 'miercoles', 'jueves', 'viernes')
        self.tabla = ttk.Treeview(parent, columns=columns, show='headings', height=12)
        
        # Definir encabezados
        self.tabla.heading('hora', text='HORA')
        self.tabla.heading('lunes', text='LUNES')
        self.tabla.heading('martes', text='MARTES')
        self.tabla.heading('miercoles', text='MIÉRCOLES')
        self.tabla.heading('jueves', text='JUEVES')
        self.tabla.heading('viernes', text='VIERNES')
        
        # Ajustar anchos de columna
        self.tabla.column('hora', width=80)
        for col in columns[1:]:
            self.tabla.column(col, width=150)
        
        # Insertar datos
        for horario in self.horarios:
            self.tabla.insert('', tk.END, values=(
                horario['hora'],
                horario['lunes'],
                horario['martes'],
                horario['miercoles'],
                horario['jueves'],
                horario['viernes']
            ))
        
        # Bind para el evento de clic
        self.tabla.bind('<ButtonRelease-1>', self.mostrar_detalles)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar
        self.tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def obtener_clase_actual(self):
        ahora = datetime.datetime.now()
        # Solo días lectivos (0..4)
        dia_semana = ahora.weekday()
        if dia_semana >= 5:
            return None, 0, "", 0

        dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes']
        for horario in self.horarios:
            # parsear hora de inicio (ej. "8:30" o "08:30")
            try:
                h, m = horario['hora'].split(':')
            except ValueError:
                continue
            hora_inicio = ahora.replace(hour=int(h), minute=int(m), second=0, microsecond=0)
            hora_fin = hora_inicio + datetime.timedelta(minutes=horario['duracion'])

            if hora_inicio <= ahora < hora_fin:
                clase_actual = horario[dias[dia_semana]]
                tiempo_restante_segundos = int((hora_fin - ahora).total_seconds())
                return clase_actual, tiempo_restante_segundos, horario['hora'], horario['duracion']

        return None, 0, "", 0
    
    def actualizar_tiempo(self):
        clase_actual, tiempo_restante, hora_inicio, duracion = self.obtener_clase_actual()
        
        if clase_actual:
            # Extraer código del módulo de forma robusta
            codigo = self.obtener_codigo_clase(clase_actual)
            nombre_modulo = self.modulos.get(codigo, "Módulo no identificado")
            profesor = self.profesores.get(codigo, "Profesor no identificado")
            
            # tiempo_restante en segundos -> formatear mm:ss
            minutos = tiempo_restante // 60
            segundos = tiempo_restante % 60
            
            texto = f"CLASE ACTUAL: {nombre_modulo}\n"
            texto += f"Profesor: {profesor} | Hora: {hora_inicio} ({duracion} min)\n"
            texto += f"TIEMPO RESTANTE: {minutos:02d}:{segundos:02d}"
            
            self.label_tiempo.config(text=texto)
            
            # Cambiar color según el tiempo restante (comparar en segundos)
            if tiempo_restante < 5 * 60:
                self.frame_tiempo.configure(bg='#e74c3c')  # Rojo para poco tiempo
            elif tiempo_restante < 15 * 60:
                self.frame_tiempo.configure(bg='#f39c12')  # Naranja para tiempo medio
            else:
                self.frame_tiempo.configure(bg='#3498db')  # Azul para tiempo suficiente
                
            self.label_tiempo.configure(bg=self.frame_tiempo['bg'])
        else:
            self.label_tiempo.config(text="No hay clase en este momento")
            self.frame_tiempo.configure(bg='#95a5a6')  # Gris cuando no hay clase
            self.label_tiempo.configure(bg=self.frame_tiempo['bg'])
        
        # Actualizar cada segundo
        self.root.after(1000, self.actualizar_tiempo)

    def obtener_codigo_clase(self, clase):
        """Buscar la clave del módulo dentro del texto de la clase (respetando 'CM0 II', '0179asir 2', etc.)."""
        texto = clase.upper()
        # Intentar emparejar por coincidencia de clave conocida (prefiriendo claves más largas)
        for key in sorted(self.modulos.keys(), key=len, reverse=True):
            if key.upper() in texto:
                return key
        # Si no coincide, buscar dígitos (0377, 1710...)
        m = re.search(r'\d{3,4}', texto)
        if m:
            return m.group(0)
        # Fallback: primer token
        token = texto.split()[0] if texto.split() else clase
        return token

    def mostrar_detalles(self, event):
        # Obtener elemento seleccionado
        item = self.tabla.selection()
        if item:
            item = item[0]
            valores = self.tabla.item(item, 'values')
            
            # Crear ventana de detalles
            ventana_detalles = tk.Toplevel(self.root)
            ventana_detalles.title("Detalles de la Clase")
            ventana_detalles.geometry("500x400")
            ventana_detalles.configure(bg='#ecf0f1')
            
            # Obtener información de la clase seleccionada
            hora = valores[0]
            columna = self.tabla.identify_column(event.x)
            try:
                idx = int(columna.replace('#', '')) - 1
            except Exception:
                return
            # idx == 0 -> columna HORA -> no mostrar detalles
            if idx <= 0:
                return
            dias = ["Hora", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
            if idx < 0 or idx >= len(valores):
                return
            clase = valores[idx]
            dia = dias[idx]
            
            if clase:
                codigo = self.obtener_codigo_clase(clase)
                nombre_modulo = self.modulos.get(codigo, "Módulo no identificado")
                profesor = self.profesores.get(codigo, "Profesor no identificado")
                
                # Mostrar información
                tk.Label(ventana_detalles, text=f"Día: {dia}", 
                        font=("Arial", 12, "bold"), bg='#ecf0f1').pack(pady=10)
                tk.Label(ventana_detalles, text=f"Hora: {hora}", 
                        font=("Arial", 12), bg='#ecf0f1').pack(pady=5)
                tk.Label(ventana_detalles, text=f"Módulo: {nombre_modulo}", 
                        font=("Arial", 12), bg='#ecf0f1', wraplength=450).pack(pady=10)
                tk.Label(ventana_detalles, text=f"Profesor: {profesor}", 
                        font=("Arial", 12), bg='#ecf0f1').pack(pady=5)
                tk.Label(ventana_detalles, text=f"Código: {codigo}", 
                        font=("Arial", 12), bg='#ecf0f1').pack(pady=10)
                
                # Botón para cerrar
                tk.Button(ventana_detalles, text="Cerrar", 
                         command=ventana_detalles.destroy, 
                         bg='#e74c3c', fg='white', font=("Arial", 10)).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = HorarioApp(root)
    root.mainloop()