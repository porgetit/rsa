import pytest
from rsa_keygen import RSAGenerator

def test_es_primo_grande():
    rsa = RSAGenerator(key_size=1024)
    # 7919 es un primo conocido empíricamente
    assert rsa._es_primo_grande(7919) is True
    # 7920 es par, matemáticamente no es primo
    assert rsa._es_primo_grande(7920) is False
    # 91 = 7 * 13, compuesto engañoso en primitivas bajas
    assert rsa._es_primo_grande(91) is False

def test_generar_primo_aleatorio():
    """
    Test individual para _generar_primo_aleatorio usando un
    key_size mucho menor (256 bits) para optimizar el banco de pruebas.
    """
    rsa = RSAGenerator(key_size=256)
    primo = rsa._generar_primo_aleatorio()
    
    # Ineludiblemente debe ser impar
    assert primo % 2 != 0
    
    # Debe pasar la prueba de primalidad de Miller-Rabin de manera exitosa
    assert rsa._es_primo_grande(primo) is True

def test_generate_keys_structure():
    """Valida la integridad y la estructura devuelta (e, n) y (d, n) de genereate_keys"""
    rsa = RSAGenerator(key_size=256)
    pub_key, priv_key = rsa.generate_keys()
    
    # La estructura debe ser imperativamente la misma
    assert len(pub_key) == 2
    assert len(priv_key) == 2
    
    e, n_pub = pub_key
    d, n_priv = priv_key
    
    assert n_pub == n_priv
    assert e >= 65537

def test_rsa_encryption_decryption():
    """
    Prueba que la funcionalidad final de cifrado y descifrado asimétrico 
    matemáticamente se resuelva correctamente aislando un mensaje (m).
    """
    rsa = RSAGenerator(key_size=256)
    pub_key, priv_key = rsa.generate_keys()
    
    e, n = pub_key
    d, _ = priv_key
    
    # 'Mensaje' numérico original a modo sandbox
    m = 42
    
    # Cifrado: c = m^e mod n
    c = pow(m, e, n)
    
    # Asegúrate que el criptograma sea distinto al mensaje original
    assert c != m
    
    # Descifrado: m_descifrado = c^d mod n
    m_descifrado = pow(c, d, n)
    
    # Por el Teorema de Euler el mensaje reconstruido con d debe coincidir
    assert m == m_descifrado
