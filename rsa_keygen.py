"""Módulo para la generación de claves criptográficas RSA.

Este módulo provee una implementación orientada a objetos para generar
claves públicas y privadas utilizando el algoritmo RSA, con soporte para
pruebas de primalidad de Miller-Rabin.
"""

import random
from math import gcd
from typing import Tuple


class RSAGenerator:
    """Generador de claves RSA utilizando primos de gran tamaño.

    Attributes:
        key_size (int): Tamaño en bits para la generación de cada número
            primo (P y Q). El tamaño total del módulo N será aproximadamente
            el doble de este valor.
    """

    def __init__(self, key_size: int = 1024) -> None:
        """Inicializa el generador RSA.

        Args:
            key_size: Cantidad de bits para cada número primo generado.
                Típicamente 1024 o 2048. Por defecto es 1024.
        """
        self.key_size = key_size

    def _es_primo_grande(self, n: int, k: int = 5) -> bool:
        """Verifica la primalidad de un número mediante un test de Miller-Rabin simplificado.

        Args:
            n: El número entero positivo a evaluar.
            k: El número de iteraciones (pruebas) a realizar. Mayor cantidad
                aumenta la fiabilidad de la prueba. Por defecto es 5.

        Returns:
            bool: True si el número es un probable primo, False si es compuesto.
        """
        if n < 2:
            return False

        for _ in range(k):
            a = random.randint(2, n - 1)
            if pow(a, n - 1, n) != 1:
                return False

        return True

    def _generar_primo_aleatorio(self) -> int:
        """Genera un número primo aleatorio del tamaño especificado.

        Returns:
            int: Un número entero que ha pasado exitosamente las pruebas de primalidad.
        """
        while True:
            # Seleccionamos números con el último bit en 1 (número impar)
            n = random.getrandbits(self.key_size) | 1
            if self._es_primo_grande(n):
                return n

    def generate_keys(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Genera un par de claves RSA (pública y privada).

        El par de claves matemáticas garantiza la posibilidad del
        cifrado asimétrico estandarizado para la transferencia segura de la información.

        Returns:
            Tuple[Tuple[int, int], Tuple[int, int]]: Tupla principal que agrupa:
                - Clave pública formateada como la tupla (e, n).
                - Clave privada formateada como la tupla (d, n).
        """
        p = self._generar_primo_aleatorio()
        q = self._generar_primo_aleatorio()

        n = p * q
        phi = (p - 1) * (q - 1)

        # 65537 (F4) es el estándar comúnmente usado como exponente público e
        e = 65537
        while gcd(e, phi) != 1:
            e += 2

        # d se calcula mediante el inverso multiplicativo de e módulo phi
        d = pow(e, -1, phi)

        return ((e, n), (d, n))


if __name__ == "__main__":
    rsa_gen = RSAGenerator(key_size=1024)
    print("Generando claves RSA... (Tamaño de primos: 1024 bits)")
    pub_key, priv_key = rsa_gen.generate_keys()
    
    print(f"Clave pública (e, n): {pub_key}")
    print(f"Clave privada (d, n): {priv_key}")
