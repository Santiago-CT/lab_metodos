import math
import sympy

# ---------------------------------------------------------------------------
# FUNCIÓN DE AYUDA: Muestra la guía de sintaxis
# ---------------------------------------------------------------------------
def mostrar_guia_sintaxis():
    """Imprime una tabla con ejemplos de cómo escribir funciones."""
    print("--- Guía Rápida de Sintaxis ---")
    print("Operación          | Notación Matemática | Cómo Escribirlo en el Programa")
    print("-------------------|---------------------|--------------------------------")
    print("Multiplicación     | 5x, (x+1)(x-2)      | 5*x, (x+1)*(x-2)")
    print("Potencia           | x², x^3             | x**2, x**3")
    print("Seno               | sen(x)              | sin(1*x)")
    print("Coseno             | cos(x)              | cos(1*x)")
    print("Exponencial (e)    | e^x                 | exp(x)")
    print("Raíz Cuadrada      | √x                  | sqrt(x)")
    print("Logaritmo Natural  | ln(x)               | log(x)")
    print("Constante Pi (π)   | π                   | pi")
    print("------------------------------------------------------------------")

# ---------------------------------------------------------------------------
# FUNCIÓN 1: El algoritmo numérico
# ---------------------------------------------------------------------------
def iteracion_punto_fijo(g, x0, es, valor_verdadero=None, max_iter=50, silent=False):
    """
    Encuentra la raíz de una función.
    El parámetro 'silent' permite ejecutarlo sin imprimir la tabla para el pre-cálculo.
    """
    if not silent:
        # Construye el encabezado de la tabla
        header = f"{'i':<5}{'x_i':<18}{'ε_a (%)':<15}"
        if valor_verdadero is not None:
            header += f"{'ε_t (%)':<15}"
        print(header)
        print("-" * len(header))

    x_anterior = x0

    if not silent:
        # Imprime la primera línea (iteración 0)
        linea_0 = f"{0:<5}{x_anterior:<18.6f}{'---':<15}"
        if valor_verdadero is not None and valor_verdadero != 0:
            error_t = abs((valor_verdadero - x_anterior) / valor_verdadero) * 100
            linea_0 += f"{error_t:<15.4f}"
        print(linea_0)

    for i in range(1, max_iter + 1):
        x_actual = g(x_anterior)
        
        if x_actual == 0 and x_anterior != 0: return None
        
        error_aprox = abs((x_actual - x_anterior) / x_actual) * 100 if x_actual != 0 else 0

        if not silent:
            linea_actual = f"{i:<5}{x_actual:<18.6f}{error_aprox:<15.4f}"
            if valor_verdadero is not None and valor_verdadero != 0:
                error_t = abs((valor_verdadero - x_actual) / valor_verdadero) * 100
                linea_actual += f"{error_t:<15.4f}"
            print(linea_actual)

        if error_aprox < es:
            if not silent:
                print(f"\nCriterio de detención |ε_a| < {es}% alcanzado.")
            return x_actual
            
        x_anterior = x_actual
        
    if not silent:
        print(f"\nEl método no convergió después de {max_iter} iteraciones.")
    return x_actual

# ---------------------------------------------------------------------------
# FUNCIÓN 2: El manejador de la interacción con el usuario
# ---------------------------------------------------------------------------
def ejecutar_metodo():
    """
    Función principal que maneja la entrada del usuario, el pre-cálculo del valor
    verdadero y el bucle principal del programa.
    """
    print("--- Método de Iteración de Punto Fijo ---")
    
    # Se muestra la guía al iniciar
    mostrar_guia_sintaxis()
    
    str_f_x = input("Ingrese la función f(x): ")
    
    es_porcentual = 0.05
    print(f"Criterio de detención (Es) predeterminado: {es_porcentual}%")

    try:
        x = sympy.symbols('x')
        f_expr = sympy.sympify(str_f_x)
        # Se deriva g(x) automáticamente usando la transformación g(x) = x + f(x)
        g_expr = x + f_expr
        g = sympy.lambdify(x, g_expr, 'math')
        print(f"Función f(x) ingresada: {f_expr}")
        print(f"Función de iteración g(x) derivada: {g_expr}")
    except (sympy.SympifyError, TypeError):
        print("\n❌ Error: La función ingresada no es válida. Revisa la guía de sintaxis.")
        return

    raices_encontradas = []

    while True:
        try:
            print("\n--- Nueva Búsqueda ---")
            x0 = float(input("Ingrese el valor inicial x_0: "))
        except ValueError:
            print("Error: El valor inicial debe ser un número.")
            continue

        print("Calculando la mejor aproximación para usarla como valor verdadero...")
        # Se ejecuta el método en "modo silencioso" con alta precisión
        valor_verdadero = iteracion_punto_fijo(g, x0, es=1e-12, max_iter=1000, silent=True)

        if valor_verdadero is None:
            print("No se pudo pre-calcular una raíz convergente desde este punto inicial.")
            continue
        
        print(f"Valor verdadero por defecto (mejor aprox.): {valor_verdadero:.10f}")
        print(f"\nCalculando con x_0 = {x0}...\n")
        
        # Se ejecuta la iteración normal, mostrando la tabla y usando el valor verdadero
        raiz = iteracion_punto_fijo(g, x0, es_porcentual, valor_verdadero=valor_verdadero, silent=False)

        if raiz is not None:
            # Agrega la raíz a la lista si no es un duplicado cercano
            if not any(math.isclose(raiz, r) for r in raices_encontradas):
                 raices_encontradas.append(raiz)
        
        print("\n" + "="*55)
        if not raices_encontradas:
            print(" Raíces encontradas hasta ahora: Ninguna")
        else:
            print(f" Raíces encontradas hasta ahora ({len(raices_encontradas)}):")
            for i, r in enumerate(raices_encontradas):
                print(f"  {i+1}.  Raíz ≈ {r:.7f}")
        print("="*55)
        
        continuar = input("\n¿Desea buscar otra raíz con un punto inicial diferente? (s/n): ").lower()
        if continuar != 's':
            break

    print("\nPrograma finalizado.")