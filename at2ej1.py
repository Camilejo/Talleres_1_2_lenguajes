import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from collections import defaultdict
import string

class AutomataFinito:
    def __init__(self):
        """
        Inicializa el autómata finito basado en la definición formal
        Q: {q0, q1, q2}
        q₀: q0 (estado inicial)
        Σ: {A-Z, a-z, 0-9}
        F: {q2} (estado final)
        δ: función de transición según la definición formal
        """
        self.estados = {'q0', 'q1', 'q2'}
        # Alfabeto: letras mayúsculas, minúsculas y dígitos
        self.alfabeto = set(string.ascii_uppercase) | set(string.ascii_lowercase) | set(string.digits)
        self.estado_inicial = 'q0'
        self.estados_finales = {'q2'}
        
        # Función de transición según la definición formal
        self.transiciones = {}
        
        # δ(q0,A…Z)=q1
        for letra in string.ascii_uppercase:
            self.transiciones[(('q0', letra))] = 'q1'
        
        # δ(q1,a…z)=q1 (bucle en q1)
        for letra in string.ascii_lowercase:
            self.transiciones[(('q1', letra))] = 'q1'
        
        # δ(q1,0…9)=q2
        for digito in string.digits:
            self.transiciones[(('q1', digito))] = 'q2'
        
        # δ(q2,0…9)=q2 (bucle en q2)
        for digito in string.digits:
            self.transiciones[(('q2', digito))] = 'q2'
    
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
        Muestra ejemplos representativos para mayor claridad
        """
        # Crear tabla con ejemplos representativos
        datos_tabla = {}
        simbolos_ejemplo = ['A', 'B', 'Z', 'a', 'b', 'z', '0', '1', '9']
        
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
            'q1': 'a-z → q1 (bucle), 0-9 → q2',
            'q2': '0-9 → q2 (bucle)'
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
        
        # Configurar el gráfico
        plt.figure(figsize=(10, 6))
        
        # Posicionar nodos mucho más juntos
        pos = {
            'q0': (0, 0),
            'q1': (2, 0),    # Más cerca
            'q2': (4, 0)     # Más cerca
        }
        
        # Dibujar nodos
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                              node_size=1800, alpha=0.8)
        
        # Resaltar estado inicial
        nx.draw_networkx_nodes(G, pos, nodelist=[self.estado_inicial], 
                              node_color='lightgreen', node_size=1800, alpha=0.8)
        
        # Resaltar estados finales
        nx.draw_networkx_nodes(G, pos, nodelist=list(self.estados_finales), 
                              node_color='lightcoral', node_size=1800, alpha=0.8)
        
        # Dibujar etiquetas de nodos
        nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold', font_color='white')
        
        # Dibujar aristas manualmente para mejor control
        # Arista q0 -> q1
        plt.annotate('', xy=(1.7, 0), xytext=(0.3, 0),
                    arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        plt.text(1, 0.3, 'A-Z', fontsize=12, ha='center', weight='bold',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='yellow', alpha=0.9))
        
        # Arista q1 -> q2
        plt.annotate('', xy=(3.7, 0), xytext=(2.3, 0),
                    arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        plt.text(3, 0.3, '0-9', fontsize=12, ha='center', weight='bold',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='yellow', alpha=0.9))
        
        # Bucle en q1 (a-z)
        circle1 = plt.Circle((2, 0.8), 0.3, fill=False, color='red', linewidth=3)
        plt.gca().add_patch(circle1)
        plt.annotate('', xy=(1.7, 0.8), xytext=(2.3, 0.8),
                    arrowprops=dict(arrowstyle='->', lw=3, color='red'))
        plt.text(2, 1.3, 'a-z', fontsize=12, ha='center', weight='bold',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='orange', alpha=0.9))
        
        # Bucle en q2 (0-9)
        circle2 = plt.Circle((4, 0.8), 0.3, fill=False, color='red', linewidth=3)
        plt.gca().add_patch(circle2)
        plt.annotate('', xy=(3.7, 0.8), xytext=(4.3, 0.8),
                    arrowprops=dict(arrowstyle='->', lw=3, color='red'))
        plt.text(4, 1.3, '0-9', fontsize=12, ha='center', weight='bold',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='orange', alpha=0.9))
        
        # Configurar límites del gráfico
        plt.xlim(-0.8, 4.8)
        plt.ylim(-0.8, 1.8)
        
        # Agregar leyenda
        plt.figtext(0.02, 0.95, "Leyenda:", fontsize=12, weight='bold', va='top')
        plt.figtext(0.02, 0.90, "• Verde: Estado Inicial (q0)", fontsize=10, va='top')
        plt.figtext(0.02, 0.85, "• Rojo: Estado Final (q2)", fontsize=10, va='top')
        plt.figtext(0.02, 0.80, "• Azul: Estados Regulares", fontsize=10, va='top')
        plt.figtext(0.02, 0.75, "• Círculos Rojos: Bucles", fontsize=10, va='top')
        plt.figtext(0.02, 0.70, "• Etiquetas Naranjas: Bucles", fontsize=10, va='top')
        
        # Agregar título
        plt.suptitle("Autómata Finito - Reconocedor de Identificadores", 
                    fontsize=14, weight='bold', y=0.95)
        plt.title("Patrón: Mayúscula + minúsculas* + dígitos+", 
                 fontsize=11, style='italic', pad=10)
        
        plt.axis('off')
        plt.gca().set_aspect('equal')
        plt.tight_layout()
        plt.subplots_adjust(top=0.82)
        plt.show()

def principal():
    """
    Función principal para demostrar el autómata
    """
    # Crear el autómata
    automata = AutomataFinito()
    
    print("=" * 75)
    print("IMPLEMENTACIÓN DE AUTÓMATA FINITO - RECONOCEDOR DE IDENTIFICADORES")
    print("=" * 75)
    print(f"Estados: {sorted(automata.estados)}")
    print(f"Alfabeto: A-Z, a-z, 0-9 (Total: {len(automata.alfabeto)} símbolos)")
    print(f"Estado Inicial: {automata.estado_inicial}")
    print(f"Estados Finales: {sorted(automata.estados_finales)}")
    print()
    
    # Mostrar tabla de transiciones (ejemplos)
    print("TABLA DE TRANSICIONES (EJEMPLOS):")
    print("=" * 45)
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
        "A123",          # Accept
        "Sogamoso2025",  # Accept
        "Uptc9",         # Accept
        "X0",            # Accept
        "Z99",           # Accept
        "1234",          # Reject (no empieza con mayúscula)
        "soga2025",      # Reject (no empieza con mayúscula)
        "UPTC",          # Reject (no tiene dígitos)
        "aa99",          # Reject (no empieza con mayúscula)
        "AAT"            # Reject (no tiene dígitos)
    ]
    
    print("RESULTADOS DE PRUEBA DE CADENAS:")
    print("=" * 60)
    print(f"{'Cadena':<15} {'Resultado':<10} {'Ruta'}")
    print("-" * 60)
    
    for cadena_prueba in cadenas_prueba:
        aceptada, ruta, resultado = automata.procesar_cadena(cadena_prueba)
        ruta_str = " → ".join(ruta)
        print(f"{cadena_prueba:<15} {resultado:<10} {ruta_str}")
    
    print()
    print("ANÁLISIS DETALLADO:")
    print("=" * 50)
    print("DEFINICIÓN FORMAL DEL AUTÓMATA:")
    print("Q = {q0, q1, q2}")
    print("q₀ = q0 (estado inicial)")
    print("Σ = {A-Z, a-z, 0-9}")
    print("F = {q2} (estado final)")
    print("δ = función de transición:")
    print("   δ(q0,A…Z) = q1")
    print("   δ(q1,a…z) = q1    (bucle)")
    print("   δ(q1,0…9) = q2")
    print("   δ(q2,0…9) = q2    (bucle)")
    print()
    print("ANÁLISIS DEL LENGUAJE:")
    print("Este autómata reconoce identificadores con el patrón:")
    print("- Una letra mayúscula inicial (A-Z)")
    print("- Cero o más letras minúsculas (a-z)")
    print("- Uno o más dígitos (0-9)")
    print("Ejemplo de cadenas válidas: A123, Sogamoso2025, X0")
    print("L = {w ∈ Σ* | w = A-Z(a-z)*(0-9)+}")
    print()
    
    # Mostrar el gráfico
    print("Generando diagrama de estados...")
    automata.visualizar()

if __name__ == "__main__":
    principal()
