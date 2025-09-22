import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from collections import defaultdict
import string

class AutomataFinito:
    def __init__(self):
        """
        Inicializa el autómata finito para validar correos electrónicos
        Basado en el patrón: [a-z][0-9]*@uptc.edu.co
        Q: {q0, q1, q2}
        q₀: q0 (estado inicial)
        Σ: {a-z, 0-9, @, u, p, t, c, ., e, d, o}
        F: {q2} (estado final)
        """
        self.estados = {'q0', 'q1', 'q2'}
        # Alfabeto específico para correos electrónicos
        self.alfabeto = set(string.ascii_lowercase) | set(string.digits) | {'@', '.'}
        self.estado_inicial = 'q0'
        self.estados_finales = {'q2'}
        
        # Función de transición según el diagrama
        self.transiciones = {}
        
        # δ(q0, a-z) = q1 (primera letra minúscula)
        for letra in string.ascii_lowercase:
            self.transiciones[(('q0', letra))] = 'q1'
        
        # δ(q1, 0-9) = q1 (bucle para dígitos)
        for digito in string.digits:
            self.transiciones[(('q1', digito))] = 'q1'
        
        # δ(q1, a-z) = q1 (bucle para más letras minúsculas)
        for letra in string.ascii_lowercase:
            self.transiciones[(('q1', letra))] = 'q1'
        
        # δ(q1, @) = q2 (transición al estado final con @)
        self.transiciones[(('q1', '@'))] = 'q2'
        
        # En q2, validamos la cadena exacta "uptc.edu.co"
        # Esto se manejará de forma especial en el procesamiento
    
    def procesar_cadena(self, cadena_entrada):
        """
        Procesa una cadena a través del autómata y retorna si es aceptada
        Valida específicamente el patrón: [a-z][a-z0-9]*@uptc.edu.co
        """
        if not cadena_entrada:
            return False, ['q0'], "Rechazada"
        
        estado_actual = self.estado_inicial
        ruta = [estado_actual]
        
        # Buscar la posición del @
        if '@' not in cadena_entrada:
            return False, ruta, "Rechazada"
        
        partes = cadena_entrada.split('@')
        if len(partes) != 2:
            return False, ruta, "Rechazada"
        
        usuario, dominio = partes
        
        # Validar parte del usuario
        if not usuario:
            return False, ruta, "Rechazada"
        
        # Primera letra debe ser minúscula
        if not usuario[0].islower() or not usuario[0].isalpha():
            return False, ruta, "Rechazada"
        
        # Procesar caracteres del usuario
        for char in usuario:
            if char not in self.alfabeto:
                return False, ruta, "Rechazada"
            
            if (estado_actual, char) not in self.transiciones:
                return False, ruta, "Rechazada"
            
            estado_actual = self.transiciones[(estado_actual, char)]
            ruta.append(estado_actual)
        
        # Procesar el @
        if (estado_actual, '@') not in self.transiciones:
            return False, ruta, "Rechazada"
        
        estado_actual = self.transiciones[(estado_actual, '@')]
        ruta.append(estado_actual)
        
        # Validar que el dominio sea exactamente "uptc.edu.co"
        if dominio == "uptc.edu.co":
            return True, ruta, "Aceptada"
        else:
            return False, ruta, "Rechazada"
    
    def obtener_tabla_transiciones(self):
        """
        Genera la tabla de transiciones como un DataFrame de pandas
        """
        datos_tabla = {}
        simbolos_ejemplo = ['a', 'b', 'z', '0', '1', '9', '@']
        
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
            'q0': 'a-z → q1 (primera letra minúscula)',
            'q1': 'a-z,0-9 → q1 (bucle), @ → q2',
            'q2': 'Estado final (requiere "uptc.edu.co")'
        }
        return patrones
    
    def visualizar(self):
        """
        Crea una representación visual del autómata
        """
        # Configurar el gráfico
        plt.figure(figsize=(12, 6))
        
        # Posicionar nodos
        pos = {
            'q0': (0, 0),
            'q1': (3, 0),
            'q2': (6, 0)
        }
        
        # Dibujar nodos
        for estado in self.estados:
            if estado == self.estado_inicial:
                color = 'lightgreen'
            elif estado in self.estados_finales:
                color = 'lightcoral'
            else:
                color = 'lightblue'
            
            circle = plt.Circle(pos[estado], 0.3, color=color, alpha=0.8)
            plt.gca().add_patch(circle)
            plt.text(pos[estado][0], pos[estado][1], estado, 
                    ha='center', va='center', fontsize=14, weight='bold', color='white')
        
        # Dibujar aristas
        # q0 -> q1
        plt.annotate('', xy=(2.7, 0), xytext=(0.3, 0),
                    arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        plt.text(1.5, 0.4, '[a-z]', fontsize=12, ha='center', weight='bold',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='yellow', alpha=0.9))
        
        # q1 -> q2
        plt.annotate('', xy=(5.7, 0), xytext=(3.3, 0),
                    arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        plt.text(4.5, 0.4, '@uptc.edu.co', fontsize=12, ha='center', weight='bold',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='yellow', alpha=0.9))
        
        # Bucle en q1
        circle_bucle = plt.Circle((3, 0.8), 0.25, fill=False, color='red', linewidth=3)
        plt.gca().add_patch(circle_bucle)
        plt.annotate('', xy=(2.75, 0.8), xytext=(3.25, 0.8),
                    arrowprops=dict(arrowstyle='->', lw=3, color='red'))
        plt.text(3, 1.2, '[0-9]\n[a-z]', fontsize=11, ha='center', weight='bold',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='orange', alpha=0.9))
        
        # Configurar límites
        plt.xlim(-1, 7)
        plt.ylim(-1, 1.8)
        
        # Agregar leyenda
        plt.figtext(0.02, 0.95, "Leyenda:", fontsize=12, weight='bold', va='top')
        plt.figtext(0.02, 0.90, "• Verde: Estado Inicial (q0)", fontsize=10, va='top')
        plt.figtext(0.02, 0.85, "• Rojo: Estado Final (q2)", fontsize=10, va='top')
        plt.figtext(0.02, 0.80, "• Azul: Estados Regulares", fontsize=10, va='top')
        plt.figtext(0.02, 0.75, "• Círculo Rojo: Bucle", fontsize=10, va='top')
        
        # Agregar título
        plt.suptitle("Autómata Finito - Validador de Correos UPTC", 
                    fontsize=16, weight='bold', y=0.95)
        plt.title("Patrón: [a-z][a-z0-9]*@uptc.edu.co", 
                 fontsize=12, style='italic', pad=10)
        
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
    print("IMPLEMENTACIÓN DE AUTÓMATA FINITO - VALIDADOR DE CORREOS UPTC")
    print("=" * 75)
    print(f"Estados: {sorted(automata.estados)}")
    print(f"Alfabeto: a-z, 0-9, @, . (símbolos específicos)")
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
    
    # Casos de prueba específicos del ejercicio
    correos_prueba = [
        "juan3@uptc.edu.co",      # Aceptado
        "maria@uptc.edu.co",      # Aceptado
        "abc123@uptc.edu.co",     # Aceptado
        "123juan@uptc.edu.co",    # Rechazado (empieza con número)
        "juan@uptc.com",          # Rechazado (dominio incorrecto)
        "MARIA@uptc.edu.co"       # Rechazado (mayúsculas)
    ]
    
    print("RESULTADOS DE PRUEBA DE CORREOS:")
    print("=" * 60)
    print(f"{'Correo':<25} {'Resultado':<10} {'Ruta'}")
    print("-" * 60)
    
    for correo in correos_prueba:
        aceptada, ruta, resultado = automata.procesar_cadena(correo)
        ruta_str = " → ".join(ruta)
        print(f"{correo:<25} {resultado:<10} {ruta_str}")
    
    print()
    print("ANÁLISIS DETALLADO:")
    print("=" * 50)
    print("DEFINICIÓN FORMAL DEL AUTÓMATA:")
    print("Q = {q0, q1, q2}")
    print("q₀ = q0 (estado inicial)")
    print("Σ = {a-z, 0-9, @, .}")
    print("F = {q2} (estado final)")
    print("δ = función de transición:")
    print("   δ(q0, a-z) = q1")
    print("   δ(q1, a-z) = q1    (bucle)")
    print("   δ(q1, 0-9) = q1    (bucle)")
    print("   δ(q1, @) = q2")
    print()
    print("ANÁLISIS DEL LENGUAJE:")
    print("Este autómata valida correos electrónicos de UPTC con el patrón:")
    print("- Comienza con una letra minúscula (a-z)")
    print("- Seguida de cero o más letras minúsculas o dígitos")
    print("- Símbolo @ obligatorio")
    print("- Dominio fijo: uptc.edu.co")
    print("Expresión regular: [a-z][a-z0-9]*@uptc\\.edu\\.co")
    print()
    print("CASOS DE PRUEBA:")
    print("✓ juan3@uptc.edu.co    - Aceptado (patrón correcto)")
    print("✓ maria@uptc.edu.co    - Aceptado (solo letras)")
    print("✓ abc123@uptc.edu.co   - Aceptado (letras + números)")
    print("✗ 123juan@uptc.edu.co  - Rechazado (empieza con número)")
    print("✗ juan@uptc.com        - Rechazado (dominio incorrecto)")
    print("✗ MARIA@uptc.edu.co    - Rechazado (letras mayúsculas)")
    print()
    
    # Mostrar el gráfico
    print("Generando diagrama de estados...")
    automata.visualizar()

if __name__ == "__main__":
    principal()
