
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import re

class NewtonRaphson:
    def __init__(self, expr_str, x0, sigfigs=5, desc=None):
        self.expr_str = expr_str
        self.x0 = x0
        self.sigfigs = sigfigs
        self.desc = desc or expr_str
        self.x = sp.Symbol('x')
        self.f = self.parse_equation(expr_str)
        self.fprime = sp.diff(self.f, self.x)
        self.f_num = sp.lambdify(self.x, self.f, 'numpy')
        self.fprime_num = sp.lambdify(self.x, self.fprime, 'numpy')

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
        x_n = self.x0
        pasos = []
        for i in range(50):
            fx = self.f_num(x_n)
            dfx = self.fprime_num(x_n)
            if dfx == 0:
                raise ValueError("La derivada se anuló, prueba otro x0.")
            x_next = x_n - fx/dfx
            pasos.append((i+1, x_n, fx))
            if abs(x_next - x_n) < tol_abs:
                x_n = x_next
                break
            x_n = x_next
        self.raiz = x_n
        self.pasos = pasos
        return x_n, pasos

    def mostrar_resultados(self):
        raiz, pasos = self.solve()
        print(f"\n{'='*50}\nNewton-Raphson: {self.desc}")
        print("\nIteraciones:")
        print("Iter\t   x\t\t    f(x)")
        for it, xi, fxi in pasos:
            print(f"{it}\t{xi:.8f}\t{fxi:.8e}")
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
        plt.title(f'Newton-Raphson para: {self.desc}')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.legend()
        plt.grid(True)


    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")