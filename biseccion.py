
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import re

class Biseccion:
    def __init__(self, expr_str, a, b, sigfigs=5, max_iter=50, desc=None):
        self.expr_str = expr_str
        self.a = a
        self.b = b
        self.sigfigs = sigfigs
        self.max_iter = max_iter
        self.desc = desc or expr_str
        self.x = sp.Symbol('x')
        self.f = self.parse_equation(expr_str)
        self.f_num = sp.lambdify(self.x, self.f, 'numpy')

    def parse_equation(self, expr_str):
        x = self.x
        if '=' in expr_str:
            left, right = expr_str.split('=')
            expr_str = f"({left}) - ({right})"
        expr_str = re.sub(r'e\^(\w+)', r'exp(\1)', expr_str)
        expr_str = expr_str.replace('^', '**')
        return sp.sympify(expr_str)

    def solve(self):
        tol_abs = 0.5 * 10**(2 - self.sigfigs)
        a = self.a
        b = self.b
        pasos = []
        fa = self.f_num(a)
        fb = self.f_num(b)
        if fa * fb > 0:
            raise ValueError("f(a) y f(b) deben tener signos opuestos.")
        for i in range(1, self.max_iter+1):
            c = (a + b) / 2
            fc = self.f_num(c)
            pasos.append((i, a, b, c, fc))
            if abs(fc) < tol_abs or abs(b - a) < tol_abs:
                break
            if fa * fc < 0:
                b = c
                fb = fc
            else:
                a = c
                fa = fc
        self.raiz = c
        self.pasos = pasos
        return c, pasos

    def mostrar_resultados(self):
        raiz, pasos = self.solve()
        print(f"\n{'='*50}\nBisección: {self.desc}")
        print("\nIteraciones:")
        print("Iter\ta\tb\tc\tf(c)")
        for it, a, b, c, fc in pasos:
            print(f"{it}\t{a:.8f}\t{b:.8f}\t{c:.8f}\t{fc:.8e}")
        print(f"\nRaíz aproximada (5 cifras significativas): {raiz:.5g}")

    def graficar(self):
        raiz = getattr(self, 'raiz', None)
        if raiz is None:
            self.solve()
            raiz = self.raiz
        rango = max(5, abs(raiz) + 1)
        x_vals = np.linspace(raiz - rango, raiz + rango, 400)
        y_vals = self.f_num(x_vals)
        plt.figure()
        plt.axhline(0, color='black', linewidth=0.8)
        plt.plot(x_vals, y_vals, label='f(x)')
        plt.scatter([raiz], [0], color='red', zorder=5,
                    label=f'Raíz ≈ {raiz:.5g}')
        plt.title(f'Bisección para: {self.desc}')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.legend()
        plt.grid(True)


    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")