import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import re

def parse_equation(expr_str):
    """
    Convierte cadenas como 'e^x = 1 + x' en una expresión sympy igualada a 0.
    """
    x = sp.Symbol('x')

    # Si hay igualdad, pasamos todo al lado izquierdo
    if '=' in expr_str:
        left, right = expr_str.split('=')
        expr_str = f"({left}) - ({right})"

    # Reemplazar notaciones comunes
    # 1. e^x -> exp(x)
    expr_str = re.sub(r'e\^(\w+)', r'exp(\1)', expr_str)
    # 2. potencia ^ -> ** para Python
    expr_str = expr_str.replace('^', '**')

    return sp.sympify(expr_str)

def newton_raphson(expr_str, x0, sigfigs=5):
    x = sp.Symbol('x')
    f = parse_equation(expr_str)
    fprime = sp.diff(f, x)

    f_num = sp.lambdify(x, f, 'numpy')
    fprime_num = sp.lambdify(x, fprime, 'numpy')

    # tolerancia para 5 cifras significativas
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

if __name__ == "__main__":
    casos = [
        {
            "expr": "e^x = 1 + x",
            "x0": 0.5,
            "desc": "e^x = 1 + x"
        },
        {
            "expr": "sin(10*x) + cos(3*x)",
            "x0": 0.1,
            "desc": "f(x) = sin(10x) + cos(3x)"
        },
        {
            "expr": "-1/2*x**2 + 5/2*x + 9/2",
            "x0": 0.0,
            "desc": "f(x) = -1/2 x^2 + 5/2 x + 9/2"
        }
    ]

    for caso in casos:
        print(f"\n{'='*50}\nCaso: {caso['desc']}")
        try:
            raiz, pasos, f_num = newton_raphson(caso["expr"], caso["x0"])
        except Exception as e:
            print(f"Error: {e}")
            continue

        print("\nIteraciones:")
        print("Iter\t   x\t\t    f(x)")
        for it, xi, fxi in pasos:
            print(f"{it}\t{xi:.8f}\t{fxi:.8e}")

        print(f"\nRaíz aproximada (5 cifras significativas): {raiz:.5g}")

        # Graficar
        rango = max(5, abs(raiz) + 1)
        x_vals = np.linspace(raiz - rango, raiz + rango, 400)
        y_vals = f_num(x_vals)

        plt.figure()
        plt.axhline(0, color='black', linewidth=0.8)
        plt.plot(x_vals, y_vals, label='f(x)')
        plt.scatter([raiz], [0], color='red', zorder=5,
                    label=f'Raíz ≈ {raiz:.5g}')
        plt.title(f'Newton-Raphson para: {caso['desc']}')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.legend()
        plt.grid(True)
    plt.show()
