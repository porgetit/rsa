import time
import pandas as pd
from main import generar_primo_aleatorio, rsa

def run_benchmark(iterations=30, bit_size=1024):
    print(f"Iniciando banco de pruebas de {iterations} iteraciones para claves RSA de {bit_size} bits.")
    
    results = []
    
    for i in range(1, iterations + 1):
        print(f"Iteración {i:02d}/{iterations}...", end="", flush=True)
        
        iter_start = time.time()
        
        # Etapa 1: Primo P
        p_start = time.time()
        p = generar_primo_aleatorio(bit_size)
        p_end = time.time()
        
        # Etapa 2: Primo Q
        q_start = time.time()
        q = generar_primo_aleatorio(bit_size)
        q_end = time.time()
        
        # Etapa 3: Claves RSA
        rsa_start = time.time()
        public_key, private_key = rsa(p, q)
        rsa_end = time.time()
        
        iter_end = time.time()
        
        time_p = p_end - p_start
        time_q = q_end - q_start
        time_rsa = rsa_end - rsa_start
        time_total = iter_end - iter_start
        
        results.append({
            "Iteracion": i,
            "Bits": bit_size,
            "Tiempo_P_s": time_p,
            "Tiempo_Q_s": time_q,
            "Tiempo_RSA_s": time_rsa,
            "Tiempo_Total_s": time_total
        })
        print(f" Completada en {time_total:.4f}s")
        
    # Guardar datos sin procesar a CSV
    df = pd.DataFrame(results)
    csv_filename = "resultados_benchmark.csv"
    df.to_csv(csv_filename, index=False)
    print(f"\nDatos crudos guardados en {csv_filename}")
    
    # Análisis estadístico usando pandas
    print("Calculando estadísticas descriptivas...")
    # Solo tomamos las columnas de tiempo para el análisis
    cols_tiempo = ["Tiempo_P_s", "Tiempo_Q_s", "Tiempo_RSA_s", "Tiempo_Total_s"]
    stats = df[cols_tiempo].describe()
    
    # Persistir análisis
    analysis_filename = "analisis_estadistico.txt"
    with open(analysis_filename, "w", encoding="utf-8") as f:
        f.write(f"=== Análisis Estadístico de {iterations} Iteraciones (Distribución RSA {bit_size} bits) ===\n\n")
        f.write(stats.to_string())
        f.write("\n\n=== Resumen Descriptivo ===\n")
        f.write(f"- Promedio de ejecución total: {stats.loc['mean', 'Tiempo_Total_s']:.4f} s\n")
        f.write(f"- Desviación estándar total:   {stats.loc['std', 'Tiempo_Total_s']:.4f} s\n")
        f.write(f"- Tiempo máximo en 1 prueba:   {stats.loc['max', 'Tiempo_Total_s']:.4f} s\n")
        f.write(f"- Tiempo mínimo en 1 prueba:   {stats.loc['min', 'Tiempo_Total_s']:.4f} s\n")
        
    print(f"Análisis descriptivo guardado en {analysis_filename}")

if __name__ == "__main__":
    run_benchmark(30, 1024)
