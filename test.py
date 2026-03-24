import time
from datetime import datetime
from main import generar_primo_aleatorio, rsa

def run_test():
    print("Iniciando prueba de rendimiento RSA...")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    total_start_time = time.time()
    
    bit_size = 1024
    
    # generar dos primos random
    print(f"Generando primo p de {bit_size} bits...")
    p_start_time = time.time()
    p = generar_primo_aleatorio(bit_size)
    p_end_time = time.time()
    p_time = p_end_time - p_start_time
    
    print(f"Generando primo q de {bit_size} bits...")
    q_start_time = time.time()
    q = generar_primo_aleatorio(bit_size)
    q_end_time = time.time()
    q_time = q_end_time - q_start_time
    
    print("Calculando claves publica y privada...")
    rsa_start_time = time.time()
    public_key, private_key = rsa(p, q)
    rsa_end_time = time.time()
    rsa_time = rsa_end_time - rsa_start_time
    
    total_end_time = time.time()
    total_time = total_end_time - total_start_time
    
    print("Public key (e, n):", public_key)
    print("Private key (d, n):", private_key)
    print(f"Tiempo total de ejecución: {total_time:.4f} segundos")
    
    # Escribir los resultados en log.txt
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] Prueba RSA - Tamaño de primos: {bit_size} bits\n")
        f.write(f"Tiempo generación primo p: {p_time:.4f} segundos\n")
        f.write(f"Tiempo generación primo q: {q_time:.4f} segundos\n")
        f.write(f"Tiempo algoritmo RSA:      {rsa_time:.4f} segundos\n")
        f.write(f"Tiempo total de ejecución: {total_time:.4f} segundos\n")
        f.write("-" * 50 + "\n")
        
if __name__ == "__main__":
    run_test()
