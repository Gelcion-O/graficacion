import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

#Una lista de colores personalizada
colors = ['b','r','g','y']

TOL = 1.e-8

def newton(z0, f, fprime, MAX_IT=1000):
    """Implementación del método de Newton para encontrar raíces de una función compleja.

    Args:
        z0 (complex): Punto inicial.
        f (function): Función compleja.
        fprime (function): Derivada de la función compleja.
        MAX_IT (int, optional): Número máximo de iteraciones. Por defecto es 1000.
        """
    z = z0
    for i in range(MAX_IT):
        dz = f(z) / fprime(z)
        if abs(dz) < TOL:
            return z
        z -= dz
    return False

def fractal(f, fprime, xlim, ylim, N=500, MAX_IT=1000):
    """Genera un fractal basado en el método de Newton para una función compleja.

    Args:
        f (function): Función compleja.
        fprime (function): Derivada de la función compleja.
        xlim (tuple): Límite en el eje x (mínimo, máximo).
        ylim (tuple): Límite en el eje y (mínimo, máximo).
        N (int, optional): Número de puntos en cada eje. Por defecto es 500.
        MAX_IT (int, optional): Número máximo de iteraciones para el método de Newton. Por defecto es 1000.
    """
    x = np.linspace(xlim[0], xlim[1], N)
    y = np.linspace(ylim[0], ylim[1], N)
    X, Y = np.meshgrid(x, y)
    Z0 = X + 1j * Y
    Z = np.zeros(Z0.shape, dtype=complex)
    img = np.zeros(Z0.shape, dtype=int)


    """
    Aca lo que estamos haciendo es que se vayan generando los fractales con los colores dependiendo
    de la función
    """
    roots = []
    for i in range(N):
        for j in range(N):
            z = newton(Z0[i, j], f, fprime, MAX_IT)
            if z is not False:
                Z[i, j] = z
                if not any(np.isclose(z, r, atol=TOL) for r in roots):
                    roots.append(z)
                img[i, j] = next(k for k, r in enumerate(roots) if np.isclose(z, r, atol=TOL))

    plt.figure(figsize=(8, 8))
    cmap = ListedColormap(colors[:len(roots)])
    plt.imshow(img, extent=(xlim[0], xlim[1], ylim[0], ylim[1]), cmap=cmap)
    plt.colorbar(ticks=range(len(roots)), label='Raíces')
    plt.title('Fractal de Newton')
    plt.xlabel('Re(z)')
    plt.ylabel('Im(z)')
    plt.show()

def main():
    # Ejemplo de uso con la función f(z) = z^3 - 1
    f = lambda z: z**3 - 2*z + 2
    fprime = lambda z: 3*z**2 - 2
    fractal(f, fprime, xlim=(-2, 2), ylim=(-2, 2), N=800, MAX_IT=50)
    
main()