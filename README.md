# Implementación del Generador de Claves RSA

### Autor: [Kevin Esguerra Cardona](mailto:kevin.esguerra@utp.edu.co)

Este repositorio contiene una implementación en Python para la generación de pares de claves del criptosistema RSA. El diseño emplea el paradigma de orientación a objetos e implementa pruebas de primalidad probabilísticas para la obtención eficiente de los parámetros estocásticos del sistema.

## 1. Fundamentos del Criptosistema RSA

RSA es un criptosistema de clave asimétrica cuya seguridad computacional se fundamenta en la intratabilidad del problema de factorización de números enteros compuestos por el producto de dos números primos grandes (problema RSA o _integer factorization problem_).

Un esquema RSA estandarizado define dos claves matemáticamente dependientes:

- **Clave Pública:** Abierta para el dominio público. Utilizada para el cifrado de datos y verificación de firmas.
- **Clave Privada:** Mantenida como secreto cristográfico estricto. Permite el descifrado de datos y la generación de firmas.

## 2. Modelo Matemático de RSA

El algoritmo algebraico opera en el anillo de enteros módulo $n$ ($\mathbb{Z}_n$) y se estructura en tres fases fundamentales:

### 2.1. Generación de Claves

1.  **Selección de primos:** Se generan de manera aleatoria e independiente dos números enteros primos de gran magnitud, $p$ y $q$, tales que $p \neq q$. La longitud de bits de dichos términos define empíricamente el nivel de seguridad algorítmico del sistema.
2.  **Cálculo del módulo $n$:** Se define el módulo del criptosistema como el producto natural $n = p \cdot q$.
3.  **Cálculo de la función indicatriz de Euler $\phi(n)$:** Puesto que $p$ y $q$ son primos por definición, la cardinalidad de los coprimos positivos de $n$ se obtiene con $\phi(n) = (p - 1)(q - 1)$. _Nota: Operacionalmente es viable sustituir por la función de Carmichael $\lambda(n) = \text{mcm}(p-1, q-1)$ para minimizar las operaciones ulteriores_.
4.  **Selección del exponente público $e$:** Se determina un entero escalar $e$ tal que $1 < e < \phi(n)$ sujeto a que $\gcd(e, \phi(n)) = 1$. Se acostumbra emplear números primos de Fermat regulares (particularmente $F_4 = 65537$) por su convergencia óptima en aceleración de hardware y bajo peso de Hamming en su representación binaria.
5.  **Cálculo del exponente privado $d$:** Se halla geométricamente $d$ mediante el inverso multiplicativo modular de $e$ módulo $\phi(n)$. Analíticamente, corresponde a solucionar la relación de congruencia lineal $e \cdot d \equiv 1 \pmod{\phi(n)}$.

La asignación de variables es como se denota a continuación:

- **Clave pública:** Definida por el par codificado $(e, n)$
- **Clave privada:** Definida por el par codificado $(d, n)$

### 2.2. Procedimientos de Cifrado y Descifrado

Dado un mensaje original $M$ arbitrario, este debe ser secuenciado numéricamente mediante relleno polinomial (_padding_ normativo, ej. OAEP) y expresado formalmente como un entero de clase $m \in \{0, 1, \dots, n-1\}$.

- **Cifrado (Transformación forward):** Para obtener el texto cifrado $c$, se eleva la expresión a la potencia del exponente público aplicando congruencia modular base $n$:
  $$c \equiv m^e \pmod n$$
- **Descifrado (Transformación backward):** Teniendo dominio algebraico sobre la constante privada y secreta $d$, el extremo receptor computa a la inversa la correspondencia del criptograma $c$:
  $$m \equiv c^d \pmod n$$

La validez matemática del proceso de descifrado simétrico se ratifica y deriva genéricamente como corolario del teorema de Euler.

## 3. Arquitectura de la Implementación (`rsa_keygen.py`)

La clase `RSAGenerator` encapsula algorítmicamente la fase de inicialización descrita en la sección 2.1. El peso de complejidad computacional ($\mathcal{O}$) en la implementación subyace directamente sobre el bloque de generación iterativa de primos (paso 1). Por lo demás, el cálculo del reverso de variable $d$ es asimilado sin colisión a través del algoritmo de Euclides Extendido, implementado nativamente en C-Python con la llamada built-in de triple variable `pow(e, -1, phi)`.

### 3.1. Análisis Algorítmico y Optimizaciones en la Generación de Primos

La derivación y factoraje numérico factible para parámetros de entropía real $p$ y $q$ (ej. espacio vectorial de orden $2^{1024}$ en bits) exige una transición obligatoria de esquemas de pruebas de primalidad deterministas convencionales, inherentemente de escala $\mathcal{O}(\sqrt{n})$, a favor de topologías probabilísticas optimizadas. Este repositorio implementa las directivas de heurística a continuación:

#### A. Poda Computacional Discreta sobre el Espacio Muestral (Forzamiento de Paridad)

La inicialización de un candidato impar variable $\mathbf{n}$ en el método pseudoaleatorio `_generar_primo_aleatorio` recurre a operadores algebraicos de bajo nivel:

```python
n = random.getrandbits(self.key_size) | 1
```

La aplicación del operador relacional _OR bit a bit_ (disyunción lógica unaria incluyente) transfiere permanentemente bajo máscara un `1` escalar al bit menos significativo (LSB) del número pseudoaleatorio $n$.

Teóricamente, suprime del árbol de procesamiento el subconjunto íntegro de paridad par ($\{x \in \mathbb{N} \mid x \equiv 0 \pmod 2\}$). Al excluir todos los múltiplos directos base 2, se logra reducir estáticamente en un 50% la densidad de evaluaciones nulas en las rutinas predictivas de primalidad, una mitigación axiomática de alta criticidad en latencia temporal.

#### B. Modelo de Test Probabilístico (Derivación de Fermat)

La instancia de subrutina `_es_primo_grande` implementa una verificación probabilística subyacida en la definición axiomática del **Pequeño Teorema de Fermat**.

Para un número candidato global $n$ y de variable iterada $a$ (una "base" arbitrariamente extraída del rando uniforme cerrado $[2, n-1]$).
Si el factor base $n$ obedece a un número primo estricto, la congruencia descrita a continuación es obligatoriamente satisfecha bajo un factor de probabilidad $P=1$:

$$a^{n-1} \equiv 1 \pmod n$$

- Si la operación modular colisiona con el axioma ($a^{n-1} \not\equiv 1 \pmod n$), la función emite en tiempo real $\mathcal{O}(1)$ un veredicto `False`, infiriendo inexorablemente al candidato $\mathbf{n}$ como un número atómicamente **compuesto**.
- Si la congruencia retorna verdadera, el candidato es tipificado algebraicamente como _pseudoprimo respecto a la base_ $a$.

La subrutina expande recursión lineal de esta validación a razón de $k$ épocas (constante interna $k=5$). El cruce correlacionado de distintas bases $a$, dictamina asintóticamente la minimización acelerada de falsos positivos en el espectro. (La varianza de disidencia principal radica acotada en los casos aislados de números compuestos de Carmichael).

#### C. Exponenciación Modular Binaria Eficiente

El orden volumétrico intrínseco de matrices modulares trabajando con dimensiones exponenciales binarias $\ge 1024$ condiciona el espacio finito en hardware para operaciones en coma flotante o registros del modelo $a^{n-1}$ referida en párrafos superiores.

Previendo el umbral de limitación, Python encapsula a nivel compilador C la rutina bajo la función pre-construida de aridad ternaria: `pow(a, n - 1, n)`. Este puente expone el cálculo interno modelado como un proceso iterado transitorio de **exponenciación binaria (método de derecha a izquierda o sustrato análogo)**. La reducción modular por inducción se impone secuencialmente al término local de la variable en vez de al gran total, resolviendo la conmutación general con una cota asintótica óptima de retardo temporal $\mathcal{O}(\log n)$, proveyendo desvinculación efectiva a cuellos de botella por escasez de RAM a medida de cálculos astronómicos.
