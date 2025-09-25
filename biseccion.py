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

def biseccion(expr_str, a, b, sigfigs=5, max_iter=50):
	x = sp.Symbol('x')
	f = parse_equation(expr_str)
	f_num = sp.lambdify(x, f, 'numpy')
	tol_abs = 0.5 * 10**(2 - sigfigs)
	pasos = []
	fa = f_num(a)
	fb = f_num(b)
	if fa * fb > 0:
		raise ValueError("f(a) y f(b) deben tener signos opuestos.")
	for i in range(1, max_iter+1):
		c = (a + b) / 2
		fc = f_num(c)
		pasos.append((i, a, b, c, fc))
		if abs(fc) < tol_abs or abs(b - a) < tol_abs:
			break
		if fa * fc < 0:
			b = c
		else:
			a = c
			fa = fc
	return c, pasos, f_num

def ejecutar_biseccion():
    """Función para manejar la interacción del usuario con el método de bisección."""
    print("\n--- Método de Bisección ---")
    expr_str = input("Ingrese la función o ecuación (ej. e^x = 1 + x): ")
    try:
        a = float(input("Ingrese el límite inferior del intervalo (a): "))
        b = float(input("Ingrese el límite superior del intervalo (b): "))
        sigfigs = int(input("Ingrese el número de cifras significativas (ej. 5): "))

        raiz, pasos, f_num = biseccion(expr_str, a, b, sigfigs=sigfigs)

        print("\nIteraciones:")
        print("Iter\ta\tb\tc\tf(c)")
        for it, a_i, b_i, c_i, fc_i in pasos:
            print(f"{it}\t{a_i:.8f}\t{b_i:.8f}\t{c_i:.8f}\t{fc_i:.8e}")

        print(f"\nRaíz aproximada ({sigfigs} cifras significativas): {raiz:.{sigfigs}g}")

        # Graficar
        rango = max(5, abs(raiz) + 1)
        x_vals = np.linspace(raiz - rango, raiz + rango, 400)
        y_vals = f_num(x_vals)

        plt.figure()
        plt.axhline(0, color='black', linewidth=0.8)
        plt.plot(x_vals, y_vals, label='f(x)')
        plt.scatter([raiz], [0], color='red', zorder=5, label=f'Raíz ≈ {raiz:.{sigfigs}g}')
        plt.title(f'Bisección para: {expr_str}')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.legend()
        plt.grid(True)
        plt.show()

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")