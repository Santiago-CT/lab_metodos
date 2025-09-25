from punto_fijo import ejecutar_punto_fijo
from biseccion import ejecutar_biseccion
from newton import ejecutar_newton

def mostrar_menu():
    """Muestra el menú de opciones al usuario."""
    print("\n--- Calculadora de Raíces de Funciones ---")
    print("Seleccione el método que desea utilizar:")
    print("1. Método de Bisección")
    print("2. Método de Newton-Raphson")
    print("3. Método de Iteración de Punto Fijo")
    print("4. Salir")

if __name__ == "__main__":
    while True:
        mostrar_menu()
        opcion = input("Ingrese el número de su opción: ")

        if opcion == '1':
            ejecutar_biseccion()
        elif opcion == '2':
            ejecutar_newton()
        elif opcion == '3':
            ejecutar_punto_fijo()
        elif opcion == '4':
            print("Programa finalizado.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")