import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from collections import defaultdict
import string

class AutomataFinito:
    def __init__(self):
        """
        Inicializa el autómata finito basado en la definición formal
        Q: {q0, q1, q2, q3, q4, q5, q6, q7, q8, q9}
        q₀: q0 (estado inicial)
        Σ: {A-Z, 0-9}
        F: {q9} (estado final)
        δ: función de transición según la definición formal
        """
        self.estados = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9'}
        # Alfabeto: letras mayúsculas A-Z y dígitos 0-9
        self.alfabeto = set(string.ascii_uppercase) | set(string.digits)
        self.estado_inicial = 'q0'
        self.estados_finales = {'q9'}
        
        # Función de transición según la definición formal
        self.transiciones = {}
        
        # δ(q0,A…Z)=q1
        for letra in string.ascii_uppercase:
            self.transiciones[(('q0', letra))] = 'q1'
        
        # δ(q1,A…Z)=q2
        for letra in string.ascii_uppercase:
            self.transiciones[(('q1', letra))] = 'q2'
        
        # δ(q2,1…9)=q3    δ(q2,0)=q4
        for digito in '123456789':
            self.transiciones[(('q2', digito))] = 'q3'
        self.transiciones[(('q2', '0'))] = 'q4'
        
        # δ(q3,1…9)=q6    δ(q3,0)=q7
        for digito in '123456789':
            self.transiciones[(('q3', digito))] = 'q6'
        self.transiciones[(('q3', '0'))] = 'q7'
        
        # δ(q4,0)=q5    δ(q4,1…9)=q6
        self.transiciones[(('q4', '0'))] = 'q5'
        for digito in '123456789':
            self.transiciones[(('q4', digito))] = 'q6'
        
        # δ(q6,0..9)=q8
        for digito in string.digits:
            self.transiciones[(('q6', digito))] = 'q8'
        
        # δ(q7,0)=q5    δ(q7,1…9)=q8
        self.transiciones[(('q7', '0'))] = 'q5'
        for digito in '123456789':
            self.transiciones[(('q7', digito))] = 'q8'
        
        # δ(q8,A…Z)=q9
        for letra in string.ascii_uppercase:
            self.transiciones[(('q8', letra))] = 'q9'
    
    def procesar_cadena(self, cadena_entrada):
        """
        Procesa una cadena a través del autómata y retorna si es aceptada
        """
        estado_actual = self.estado_inicial
        ruta = [estado_actual]
        
        for simbolo in cadena_entrada:
            if simbolo not in self.alfabeto:
                return False, ruta, "Rechazada"
            
            if (estado_actual, simbolo) not in self.transiciones:
                return False, ruta, "Rechazada"
            
            estado_actual = self.transiciones[(estado_actual, simbolo)]
            ruta.append(estado_actual)
        
        aceptada = estado_actual in self.estados_finales
        return aceptada, ruta, "Aceptada" if aceptada else "Rechazada"
    
    def obtener_tabla_transiciones(self):
        """
        Genera la tabla de transiciones como un DataFrame de pandas
        Muestra solo algunos ejemplos por categoría para mayor claridad
        """
        # Crear tabla simplificada para mostrar patrones
        datos_tabla = {}
        simbolos_ejemplo = ['A', 'B', 'Z', '0', '1', '5', '9']
        
        for estado in sorted(self.estados):
            datos_tabla[estado] = {}
            for simbolo in simbolos_ejemplo:
                if (estado, simbolo) in self.transiciones:
                    datos_tabla[estado][simbolo] = self.transiciones[(estado, simbolo)]
                else:
                    datos_tabla[estado][simbolo] = '-'
        
        df = pd.DataFrame(datos_tabla).T
        return df
    
    def obtener_tabla_completa_patrones(self):
        """
        Genera una descripción de patrones de transición
        """
        patrones = {
            'q0': 'A-Z → q1',
            'q1': 'A-Z → q2',
            'q2': '1-9 → q3, 0 → q4',
            'q3': '1-9 → q6, 0 → q7',
            'q4': '0 → q5, 1-9 → q6',
            'q5': 'No tiene transiciones',
            'q6': '0-9 → q8',
            'q7': '0 → q5, 1-9 → q8',
            'q8': 'A-Z → q9',
            'q9': 'No tiene transiciones'
        }
        return patrones
    
    def visualizar(self):
        """
        Crea una representación visual del autómata
        """
        G = nx.DiGraph()
        
        # Agregar nodos
        for estado in self.estados:
            G.add_node(estado)
        
        # Agregar aristas simplificadas con etiquetas de patrones
        etiquetas_aristas = {}
        
        # Agrupar transiciones por patrón
        patrones_transicion = {
            ('q0', 'q1'): 'A-Z',
            ('q1', 'q2'): 'A-Z',
            ('q2', 'q3'): '1-9',
            ('q2', 'q4'): '0',
            ('q3', 'q6'): '1-9',
            ('q3', 'q7'): '0',
            ('q4', 'q5'): '0',
            ('q4', 'q6'): '1-9',
            ('q6', 'q8'): '0-9',
            ('q7', 'q5'): '0',
            ('q7', 'q8'): '1-9',
            ('q8', 'q9'): 'A-Z'
        }
        
        for (origen, destino), etiqueta in patrones_transicion.items():
            G.add_edge(origen, destino)
            etiquetas_aristas[(origen, destino)] = etiqueta
        
        # Configurar el gráfico
        plt.figure(figsize=(15, 10))
        
        # Posicionar nodos en un diseño que refleje la estructura del autómata
        pos = {
            'q0': (0, 0),
            'q1': (2, 0),
            'q2': (4, 0),
            'q3': (6, 1),
            'q4': (6, -1),
            'q5': (8, -2),
            'q6': (8, 1),
            'q7': (8, 0),
            'q8': (10, 0),
            'q9': (12, 0)
        }
        
        # Dibujar el grafo
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                              node_size=1500, alpha=0.7)
        
        # Resaltar estado inicial
        nx.draw_networkx_nodes(G, pos, nodelist=[self.estado_inicial], 
                              node_color='lightgreen', node_size=1500, alpha=0.7)
        
        # Resaltar estados finales
        nx.draw_networkx_nodes(G, pos, nodelist=list(self.estados_finales), 
                              node_color='lightcoral', node_size=1500, alpha=0.7)
        
        # Dibujar aristas
        nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, 
                              arrowsize=20, arrowstyle='->', connectionstyle='arc3,rad=0.1')
        
        # Dibujar etiquetas
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
        nx.draw_networkx_edge_labels(G, pos, etiquetas_aristas, font_size=8)
        
        # Agregar leyenda
        plt.figtext(0.02, 0.98, "Leyenda:", fontsize=12, weight='bold', va='top')
        plt.figtext(0.02, 0.94, "• Verde: Estado Inicial (q0)", fontsize=10, va='top')
        plt.figtext(0.02, 0.90, "• Rojo: Estado Final (q9)", fontsize=10, va='top')
        plt.figtext(0.02, 0.86, "• Azul: Estados Regulares", fontsize=10, va='top')
        
        plt.title("Autómata Finito - Diagrama de Estados\n(Reconocedor de Patrones Alfanuméricos)", 
                 fontsize=16, weight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.show()

def principal():
    """
    Función principal para demostrar el autómata
    """
    # Crear el autómata
    automata = AutomataFinito()
    
    print("=" * 70)
    print("IMPLEMENTACIÓN DE AUTÓMATA FINITO - RECONOCEDOR ALFANUMÉRICO")
    print("=" * 70)
    print(f"Estados: {sorted(automata.estados)}")
    print(f"Alfabeto: A-Z, 0-9 (Total: {len(automata.alfabeto)} símbolos)")
    print(f"Estado Inicial: {automata.estado_inicial}")
    print(f"Estados Finales: {sorted(automata.estados_finales)}")
    print()
    
    # Mostrar tabla de transiciones (ejemplos)
    print("TABLA DE TRANSICIONES (EJEMPLOS):")
    print("=" * 40)
    tabla = automata.obtener_tabla_transiciones()
    print(tabla)
    print()
    
    # Mostrar patrones completos
    print("PATRONES DE TRANSICIÓN COMPLETOS:")
    print("=" * 40)
    patrones = automata.obtener_tabla_completa_patrones()
    for estado, patron in patrones.items():
        print(f"{estado}: {patron}")
    print()
    
    # Cadenas de prueba basadas en la imagen de JFLAP
    cadenas_prueba = [
        "AS345S",    # Accept
        "ASD123S",   # Reject  
        "CV657C",    # Accept
        "HL001V",    # Reject
        "39CVB0",    # Reject
        "Im456c",    # Reject (lowercase)
        "BI645K",    # Reject
        "HJCMB579ZX", # Reject
        "HI890I"     # Accept
    ]
    
    print("RESULTADOS DE PRUEBA DE CADENAS:")
    print("=" * 55)
    print(f"{'Cadena':<15} {'Resultado':<10} {'Ruta'}")
    print("-" * 55)
    
    for cadena_prueba in cadenas_prueba:
        aceptada, ruta, resultado = automata.procesar_cadena(cadena_prueba)
        ruta_str = " → ".join(ruta)
        print(f"{cadena_prueba:<15} {resultado:<10} {ruta_str}")
    
    print()
    print("ANÁLISIS DETALLADO:")
    print("=" * 50)
    print("DEFINICIÓN FORMAL DEL AUTÓMATA:")
    print("Q = {q0, q1, q2, q3, q4, q5, q6, q7, q8, q9}")
    print("q₀ = q0 (estado inicial)")
    print("Σ = {A-Z, 0-9}")
    print("F = {q9} (estado final)")
    print("δ = función de transición:")
    print("   δ(q0,A…Z) = q1    δ(q1,A…Z) = q2")
    print("   δ(q2,1…9) = q3    δ(q2,0) = q4")
    print("   δ(q3,1…9) = q6    δ(q3,0) = q7")
    print("   δ(q4,0) = q5      δ(q4,1…9) = q6")
    print("   δ(q6,0..9) = q8   δ(q7,0) = q5")
    print("   δ(q7,1…9) = q8    δ(q8,A…Z) = q9")
    print()
    print("ANÁLISIS DEL LENGUAJE:")
    print("Este autómata reconoce cadenas con el patrón:")
    print("- Dos letras mayúsculas (A-Z)")
    print("- Tres dígitos con restricciones específicas")
    print("- Una letra mayúscula final")
    print("Ejemplo de cadena válida: AS345S")
    print()
    
    # Mostrar el gráfico
    print("Generando diagrama de estados...")
    automata.visualizar()

if __name__ == "__main__":
    principal()
