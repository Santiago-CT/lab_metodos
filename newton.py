import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import re

def parse_equation(expr_str):
    x = sp.Symbol('x')
    if '=' in expr_str:
        left, right = expr_str.split('=')
        expr_str = f"({left}) - ({right})"
    expr_str = re.sub(r'e\^(\w+)', r'exp(\1)', expr_str)
    expr_str = expr_str.replace('^', '**')
    return sp.sympify(expr_str)

def newton_raphson(expr_str, x0, sigfigs=5):
    x = sp.Symbol('x')
    f = parse_equation(expr_str)
    fprime = sp.diff(f, x)

    f_num = sp.lambdify(x, f, 'numpy')
    fprime_num = sp.lambdify(x, fprime, 'numpy')

    tol_abs = 0.5 * 10**(2 - sigfigs)
    x_n = x0
    pasos = []

    for i in range(50):
        fx = f_num(x_n)
        dfx = fprime_num(x_n)
        if dfx == 0:
            raise ValueError("La derivada se anuló, prueba otro x0.")
        x_next = x_n - fx/dfx
        pasos.append((i+1, x_n, fx))
        if abs(x_next - x_n) < tol_abs:
            x_n = x_next
            break
        x_n = x_next
    return x_n, pasos, f_num

def ejecutar_newton():
    """Función para manejar la interacción del usuario con el método de Newton-Raphson."""
    print("\n--- Método de Newton-Raphson ---")
    expr_str = input("Ingrese la función o ecuación (ej. e^x = 1 + x): ")
    try:
        x0 = float(input("Ingrese el valor inicial (x0): "))
        sigfigs = int(input("Ingrese el número de cifras significativas (ej. 5): "))

        raiz, pasos, f_num = newton_raphson(expr_str, x0, sigfigs=sigfigs)

        print("\nIteraciones:")
        print("Iter\t   x\t\t    f(x)")
        for it, xi, fxi in pasos:
            print(f"{it}\t{xi:.8f}\t{fxi:.8e}")

        print(f"\nRaíz aproximada ({sigfigs} cifras significativas): {raiz:.{sigfigs}g}")

        # Graficar
        rango = max(5, abs(raiz) + 1)
        x_vals = np.linspace(raiz - rango, raiz + rango, 400)
        y_vals = f_num(x_vals)

        plt.figure()
        plt.axhline(0, color='black', linewidth=0.8)
        plt.plot(x_vals, y_vals, label='f(x)')
        plt.scatter([raiz], [0], color='red', zorder=5, label=f'Raíz ≈ {raiz:.{sigfigs}g}')
        plt.title(f'Newton-Raphson para: {expr_str}')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.legend()
        plt.grid(True)
        plt.show()

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")