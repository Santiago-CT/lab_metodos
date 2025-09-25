

from newton import NewtonRaphson
from biseccion import Biseccion
from punto_fijo import PuntoFijo

if __name__ == "__main__":
    # Newton-Raphson
    newton = NewtonRaphson("e^x = 1 + x", 0.5, desc="e^x = 1 + x")
    newton.mostrar_resultados()
    newton.graficar()

    # Bisección
    biseccion = Biseccion("sin(10*x) + cos(3*x)", 0.0, 0.5, desc="f(x) = sin(10x) + cos(3x)")
    biseccion.mostrar_resultados()
    biseccion.graficar()

    # Punto Fijo con función contractiva g(x)
    # g(x) = (1/2)*x**2 - (5/2)*x - (9/2)
    punto_fijo = PuntoFijo("-1/2*x**2 + 5/2*x + 9/2", 0.0, desc="f(x) = -1/2 x^2 + 5/2 x + 9/2", g_expr="(1/2)*x**2 - (5/2)*x - (9/2)")
    punto_fijo.mostrar_resultados()
    punto_fijo.graficar()

    import matplotlib.pyplot as plt
    plt.show()