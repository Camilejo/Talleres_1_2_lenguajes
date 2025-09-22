import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from collections import defaultdict

class AutomataFinito:
    def __init__(self):
        """
        Inicializa el autómata finito basado en la definición formal
        Q: {q0, q1, q2, q3, q4}
        q₀: q0 (estado inicial)
        Σ: {a, b}
        F: {q4} (estado final)
        δ: función de transición según la definición formal
        """
        self.estados = {'q0', 'q1', 'q2', 'q3', 'q4'}
        self.alfabeto = {'a', 'b'}
        self.estado_inicial = 'q0'
        self.estados_finales = {'q4'}
        
        # Función de transición según la definición formal
        self.transiciones = {
            ('q0', 'a'): 'q1',
            ('q0', 'b'): 'q2',
            ('q1', 'a'): 'q4',
            ('q1', 'b'): 'q2',
            ('q2', 'a'): 'q4',
            ('q2', 'b'): 'q3',
            ('q4', 'a'): 'q4',
            ('q4', 'b'): 'q2'
        }
    
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
        """
        datos_tabla = {}
        
        for estado in sorted(self.estados):
            datos_tabla[estado] = {}
            for simbolo in sorted(self.alfabeto):
                if (estado, simbolo) in self.transiciones:
                    datos_tabla[estado][simbolo] = self.transiciones[(estado, simbolo)]
                else:
                    datos_tabla[estado][simbolo] = '-'
        
        df = pd.DataFrame(datos_tabla).T
        return df
    
    def visualizar(self):
        """
        Crea una representación visual del autómata
        """
        G = nx.DiGraph()
        
        # Agregar nodos
        for estado in self.estados:
            G.add_node(estado)
        
        # Agregar aristas con etiquetas
        etiquetas_aristas = {}
        for (estado_origen, simbolo), estado_destino in self.transiciones.items():
            if G.has_edge(estado_origen, estado_destino):
                # Si la arista ya existe, agregar el símbolo a la etiqueta
                etiqueta_actual = etiquetas_aristas.get((estado_origen, estado_destino), "")
                etiquetas_aristas[(estado_origen, estado_destino)] = f"{etiqueta_actual},{simbolo}" if etiqueta_actual else simbolo
            else:
                G.add_edge(estado_origen, estado_destino)
                etiquetas_aristas[(estado_origen, estado_destino)] = simbolo
        
        # Configurar el gráfico
        plt.figure(figsize=(12, 8))
        
        # Posicionar nodos en un diseño que refleje la estructura del autómata
        pos = {
            'q0': (0, 0),
            'q1': (2, 1),
            'q2': (2, -1),
            'q3': (4, -1),
            'q4': (4, 1)
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
                              arrowsize=20, arrowstyle='->')
        
        # Dibujar etiquetas
        nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
        nx.draw_networkx_edge_labels(G, pos, etiquetas_aristas, font_size=10)
        
        # Agregar leyenda
        plt.figtext(0.02, 0.98, "Leyenda:", fontsize=12, weight='bold', va='top')
        plt.figtext(0.02, 0.94, "• Verde: Estado Inicial (q0)", fontsize=10, va='top')
        plt.figtext(0.02, 0.90, "• Rojo: Estado de aceptación (q4)", fontsize=10, va='top')
        plt.figtext(0.02, 0.86, "• Azul: Estados de no aceptación", fontsize=10, va='top')
        
        plt.title("Autómata Finito - Diagrama de Estados", fontsize=16, weight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.show()

def principal():
    """
    Función principal para demostrar el autómata
    """
    # Crear el autómata
    automata = AutomataFinito()
    
    print("=" * 60)
    print("IMPLEMENTACIÓN DE AUTÓMATA FINITO")
    print("=" * 60)
    print(f"Estados: {sorted(automata.estados)}")
    print(f"Alfabeto: {sorted(automata.alfabeto)}")
    print(f"Estado Inicial: {automata.estado_inicial}")
    print(f"Estados Finales: {sorted(automata.estados_finales)}")
    print()
    
    # Mostrar tabla de transiciones
    print("TABLA DE TRANSICIONES:")
    print("=" * 30)
    tabla = automata.obtener_tabla_transiciones()
    print(tabla)
    print()
    
    # Cadenas de prueba de la interfaz de JFLAP
    cadenas_prueba = [
        "abba",
        "aababaabb", 
        "abaababa",
        "abbabba",
        "abababababab",
        "babbaaaba",
        "bbbbbbb",
        "aaaaaaa",
        "abaababa",
        "ababba",
        "abaaaaabaaaa",
        "aabbbaaa"
    ]
    
    print("RESULTADOS DE PRUEBA DE CADENAS:")
    print("=" * 50)
    print(f"{'Cadena':<15} {'Resultado':<10} {'Ruta'}")
    print("-" * 50)
    
    for cadena_prueba in cadenas_prueba:
        aceptada, ruta, resultado = automata.procesar_cadena(cadena_prueba)
        ruta_str = " → ".join(ruta)
        print(f"{cadena_prueba:<15} {resultado:<10} {ruta_str}")
    
    print()
    print("ANÁLISIS DETALLADO:")
    print("=" * 40)
    print("DEFINICIÓN FORMAL DEL AUTÓMATA:")
    print("Q = {q0, q1, q2, q3, q4}")
    print("q₀ = q0 (estado inicial)")
    print("Σ = {a, b}")
    print("F = {q4} (estado final)")
    print("δ = función de transición:")
    print("   δ(q0,a) = q1    δ(q0,b) = q2")
    print("   δ(q1,a) = q4    δ(q1,b) = q2")
    print("   δ(q2,a) = q4    δ(q2,b) = q3")
    print("   δ(q4,a) = q4    δ(q4,b) = q2")
    print()
    print("ANÁLISIS DEL LENGUAJE:")
    print("Este autómata acepta cadenas que contienen al menos una 'a'")
    print("seguida eventualmente por otra 'a' o que terminan en 'a'.")
    print("L = {w ∈ {a,b}* | w contiene el patrón que lleva al estado q4}")
    print()
    
    # Mostrar el gráfico
    print("Generando diagrama de estados...")
    automata.visualizar()

if __name__ == "__main__":
    principal()
