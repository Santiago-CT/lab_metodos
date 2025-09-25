
import math
import sympy
import numpy as np
import matplotlib.pyplot as plt

class PuntoFijo:
    def __init__(self, str_f_x, x0, es_porcentual=0.05, max_iter=50, desc=None, g_expr=None):
        self.str_f_x = str_f_x
        self.x0 = x0
        self.es_porcentual = es_porcentual
        self.max_iter = max_iter
        self.desc = desc or str_f_x
        self.x = sympy.symbols('x')
        self.f_expr = sympy.sympify(str_f_x)
        if g_expr is not None:
            self.g_expr = sympy.sympify(g_expr)
        else:
            self.g_expr = self.x + self.f_expr
        self.g = sympy.lambdify(self.x, self.g_expr, 'math')
        self.pasos = []

    def solve(self):
        x_anterior = self.x0
        pasos = [(0, x_anterior, None)]
        x_actual = None
        for i in range(1, self.max_iter + 1):
            try:
                x_actual = self.g(x_anterior)
            except OverflowError:
                print("Advertencia: Divergencia detectada (OverflowError). El método no converge con esta función g(x) y x0.")
                self.raiz = None
                self.pasos = pasos
                return None, pasos
            if x_actual == 0:
                self.raiz = None
                self.pasos = pasos
                return None, pasos
            error_aprox = abs((x_actual - x_anterior) / x_actual) * 100
            pasos.append((i, x_actual, error_aprox))
            if error_aprox < self.es_porcentual:
                self.raiz = x_actual
                self.pasos = pasos
                return x_actual, pasos
            x_anterior = x_actual
        self.raiz = x_actual
        self.pasos = pasos
        return x_actual, pasos

    def mostrar_resultados(self):
        raiz, pasos = self.solve()
        print(f"\n{'='*50}\nPunto Fijo: {self.desc}")
        print("\nIteraciones:")
        print("Iter\tx\t\t   ε_a (%)")
        for it, xi, ea in pasos:
            if ea is None:
                # Muestra x con máximo 5 cifras significativas
                print(f"{it}\t{xi:.5g}\t   ---")
            else:
                print(f"{it}\t{xi:.5g}\t   {ea:.4f}")
        if raiz is not None:
            print(f"\nRaíz aproximada (criterio {self.es_porcentual}%): {raiz:.5g}")
        else:
            print("\nNo se encontró raíz (divergencia o x_actual=0)")

    def graficar(self):
        raiz = getattr(self, 'raiz', None)
        if raiz is None:
            # Intentar resolver si no se ha hecho
            self.solve()
            raiz = self.raiz

        if raiz is None:
            # No hay raíz: graficar un rango fijo o avisar
            print("No se puede graficar con raíz nula: el método no convergió.")
            return  # <---- Salir limpio

        rango = max(5, abs(raiz) + 1)
        x_vals = np.linspace(raiz - rango, raiz + rango, 400)
        f_num = sympy.lambdify(self.x, self.f_expr, 'numpy')
        y_vals = f_num(x_vals)
        plt.figure()
        plt.axhline(0, color='black', linewidth=0.8)
        plt.plot(x_vals, y_vals, label='f(x)')
        plt.scatter([raiz], [0], color='red', zorder=5, label=f'Raíz ≈ {raiz:.5g}')
        plt.title(f'Punto Fijo para: {self.desc}')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.legend()
        plt.grid(True)
