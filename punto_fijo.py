import math
import sympy

# ---------------------------------------------------------------------------
# FUNCIÓN 1: El algoritmo numérico (modificado para modo silencioso)
# ---------------------------------------------------------------------------
def iteracion_punto_fijo(g, x0, es, valor_verdadero=None, max_iter=50, silent=False):
    """
    Encuentra la raíz de una función.
    El parámetro 'silent' permite ejecutarlo sin imprimir la tabla.
    """
    if not silent:
        header = f"{'i':<5}{'x_i':<18}{'ε_a (%)':<15}"
        if valor_verdadero is not None:
            header += f"{'ε_t (%)':<15}"
        print(header)
        print("-" * len(header))

    x_anterior = x0

    if not silent:
        linea_0 = f"{0:<5}{x_anterior:<18.6f}{'---':<15}"
        if valor_verdadero is not None and valor_verdadero != 0:
            error_t = abs((valor_verdadero - x_anterior) / valor_verdadero) * 100
            linea_0 += f"{error_t:<15.4f}"
        print(linea_0)

    for i in range(1, max_iter + 1):
        x_actual = g(x_anterior)
        
        if x_actual != 0:
            error_aprox = abs((x_actual - x_anterior) / x_actual) * 100
        else:
            return None # Divergencia o problema

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
# FUNCIÓN 2: El manejador de la interacción (modificado para pre-cálculo)
# ---------------------------------------------------------------------------
def ejecutar_metodo():
    print("--- Método de Iteración de Punto Fijo ---")
    
    str_f_x = input("Ingrese la función f(x) (ej: exp(-x) - x): ")
    
    es_porcentual = 0.05
    print(f"Criterio de detención (Es) predeterminado: {es_porcentual}%")

    try:
        x = sympy.symbols('x')
        f_expr = sympy.sympify(str_f_x)
        g_expr = x + f_expr
        g = sympy.lambdify(x, g_expr, 'math')
        print(f"Función f(x) ingresada: {f_expr}")
        print(f"Función de iteración g(x) derivada: {g_expr}")
    except (sympy.SympifyError, TypeError):
        print("\nError: La función ingresada no es válida.")
        return

    raices_encontradas = []

    while True:
        try:
            print("\n--- Nueva Búsqueda ---")
            x0 = float(input("Ingrese el valor inicial x_0: "))
        except ValueError:
            print("Error: El valor inicial debe ser un número.")
            continue

        # --- CAMBIO: Pre-cálculo silencioso para obtener el valor verdadero ---
        print("Calculando la mejor aproximación para usarla como valor verdadero...")
        valor_verdadero = iteracion_punto_fijo(g, x0, es=1e-12, max_iter=1000, silent=True)

        if valor_verdadero is None:
            print("No se pudo pre-calcular una raíz convergente desde este punto inicial.")
            continue
        
        print(f"Valor verdadero por defecto (mejor aprox.): {valor_verdadero:.10f}")
        print(f"\nCalculando con x_0 = {x0}...\n")
        
        # --- Se ejecuta la iteración normal, pasándole el valor verdadero calculado ---
        raiz = iteracion_punto_fijo(g, x0, es_porcentual, valor_verdadero=valor_verdadero, silent=False)

        if raiz is not None:
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