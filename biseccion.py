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
			fb = fc
		else:
			a = c
			fa = fc
	return c, pasos, f_num

if __name__ == "__main__":
	casos = [
		{
			"expr": "e^x = 1 + x",
			"a": 0.0,
			"b": 1.0,
			"desc": "e^x = 1 + x"
		},
		{
			"expr": "sin(10*x) + cos(3*x)",
			"a": 0.0,
			"b": 0.5,
			"desc": "f(x) = sin(10x) + cos(3x)"
		},
		{
			"expr": "-1/2*x**2 + 5/2*x + 9/2",
			"a": -5.0,
			"b": 5.0,
			"desc": "f(x) = -1/2 x^2 + 5/2 x + 9/2"
		}
	]

	for caso in casos:
		print(f"\n{'='*50}\nCaso: {caso['desc']}")
		try:
			raiz, pasos, f_num = biseccion(caso["expr"], caso["a"], caso["b"])
		except Exception as e:
			print(f"Error: {e}")
			continue

		print("\nIteraciones:")
		print("Iter\ta\tb\tc\tf(c)")
		for it, a, b, c, fc in pasos:
			print(f"{it}\t{a:.8f}\t{b:.8f}\t{c:.8f}\t{fc:.8e}")

		print(f"\nRaíz aproximada (5 cifras significativas): {raiz:.5g}")

		rango = max(5, abs(raiz) + 1)
		x_vals = np.linspace(raiz - rango, raiz + rango, 400)
		y_vals = f_num(x_vals)

		plt.figure()
		plt.axhline(0, color='black', linewidth=0.8)
		plt.plot(x_vals, y_vals, label='f(x)')
		plt.scatter([raiz], [0], color='red', zorder=5,
					label=f'Raíz ≈ {raiz:.5g}')
		plt.title(f'Bisección para: {caso['desc']}')
		plt.xlabel('x')
		plt.ylabel('f(x)')
		plt.legend()
		plt.grid(True)
	plt.show()
