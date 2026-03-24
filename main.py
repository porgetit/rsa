from math import gcd
import random

def rsa(p: int, q: int):
    """
    Genera las claves publica y privada para el algoritmo RSA
    con primos p y q de 1024 bits
    """
    n = p * q
    phi = (p-1) * (q-1)
    e = 65537
    while gcd(e, phi) != 1:
        e += 2
    d = pow(e, -1, phi)
    return (e, n), (d, n)

def es_primo_grande(n, k=5): # k es el número de pruebas
    if n < 2: return False
    for _ in range(k):
        a = random.randint(2, n - 1)
        if pow(a, n - 1, n) != 1:
            return False
    return True

def generar_primo_aleatorio(bits=1024):
    while True:
        # Generar un número impar aleatorio
        n = random.getrandbits(bits) | 1
        if es_primo_grande(n):
            return n
