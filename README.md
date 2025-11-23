# Espectograma com Base na Transforma de Fourier 
# 1. Representação Matemática do Áudio
Uma música digital é um sinal discreto representado como um vetor:

$$x[n], \; n = 0, 1, 2, \ldots, N-1$$

A taxa de amostragem define quantas amostras existem por segundo:

$$
f_s = \text{sample rate}
$$

A duração do áudio é:

$$
\text{Duração da música} = 
\frac{\text{Número de amostras}}{\text{Taxa de amostragem}}
$$

Mesmo que:

$$
T = \frac{N} {f_s}
$$

---

# 2. Normalização do Sinal
Para evitar estouros nos cálculos é adequado realizar uma normalização da amostragem.
A normalização foi realiza no intervalo [-1, 1]. Usando:

$$
x_{\text{norm}}[n] = \frac{x[n]}{\max |x[n]|}
$$

Isso evita distorções e saturação numérica.

# 3. Transformada Rápida de Fourier (FFT)
A FFT converte o sinal do domínio do tempo para o domínio da frequência.
Transformada Discreta de Fourier (DFT):

$$
X[k] = \sum_{n=0}^{N-1} x[n] \, e^{-j \frac{2\pi kn}{N}}
$$


Cada $X[k]$ indica a quantidade de energia presente na frequência  $f_k$.


As frequências associadas aos índices:

$$
f[k] = \frac{k}{N} f_s
$$

# 4. Espectograma - STFT (Short-Time Fourier Transform)
O espectrograma aplica a FFT em janelas ao longo do tempo:

$$
X_m[k] = \sum_{n=0}^{L-1} x[n + mH]\; w[n]\; e^{-j \frac{2\pi kn}{L}}
$$

Onde:
 - L = Tamanho da janela
 - H = Salto entre janela
 - $w[n]$ é uma função janela (Hann, por padrão).


A matriz resultante:

$$
S(k,m) = |X_m[k]|^2
$$

Depois convertida para decibéis:

$$
S_{\mathrm{dB}} = 10 \log_{10}(S)
$$
