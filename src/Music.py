import matplotlib.pyplot as plt
from scipy.signal import spectrogram
import numpy 
from pathlib import Path

class Music:
    def __init__(self, data, sample_rate, name_music):
        """
        Construtor da classe Music
        Args:
            data (_type_): Amostras da música
            sample_rate (_type_): Amostras por segundo da música
            name_music (_type_): Nome da música
        """
        self.name_music = name_music
        self._sample_rate = sample_rate # Amostragem da música
        self._data_music = data / numpy.max(numpy.abs(data)) # Normalização das amostragens para valores no intervalo [-1, 1]
        self._music_duration = len(self._data_music) / self._sample_rate # Duracao da música em segundos
        
        
        # Parametros do grafico fft 
        self.fft_freq = None # Valores de frequencia da transformada de fourier
        self.fft_values = None # Voleres de intensidade da transformada de fourier
        
        # Parametros do espectograma
        self.freq = None # Janelas de frequencias
        self.time = None # Janelas de tempo
        self.freq_time = None # Matriz da frequencia x tempo

    def getDataMusic(self):
        return self._data_music

    def getSampleRateMusic(self):
        return self._sample_rate
    
    def musicDecomposition(self):
        # Transformada rápida de Fourier
        fft_values = numpy.abs(numpy.fft.fft(self._data_music))
        return fft_values
    
    def musicFrequencies(self):
        # Frequências correspondentes
        frequencies = numpy.fft.fftfreq(len(self._data_music), 1 / self._sample_rate)
        return frequencies
    
    
    def spectogram(self, time=30):
        """
        Gera o espectograma da música

        Args:
            time (int): Quantidades em segundos para o espectograma

        Returns:
            path_epec: Caminho onde o arquivo do espectograma foi salvo 
        """

        # Configura o caminho a qual o arquivo vai ser salvo
        path_base = Path(__file__).parent.parent / "graphs"
        path_espec = path_base / f"{self.name_music}_espectrograma.png"

        # Manipula o tamanho da música para o espectograma
        max_duration = max(min(self._music_duration, 240, time), 30) # Garate que o espectograma vai ser gerado para uma quantidade de segundos no intervalo [30, 240]
        max_samples = max_duration * self._sample_rate # Quantidade maxima de amostras
        data = self._data_music[:max_samples] # Fatia a quantidade de amostras, para as primeiras ate max_samples

        if self.freq is None or self.time is None or self.freq_time is None:

            # Gera espectograma
            self.freq, self.time, self.freq_time = spectrogram(
                data, # amostras
                self._sample_rate, # quantidade de amostras por segundos
                nperseg=1024, 
                noverlap=512,
                scaling='density'
            )

            self.freq_time = 10 * numpy.log10(self.freq_time + 1e-10) # Converte para db

        # Configura o plot do espectograma
        plt.figure(figsize=(12, 5))
        plt.pcolormesh(self.time, self.freq, self.freq_time, shading='gouraud')
        plt.title(f"Espectrograma {self.name_music}")
        plt.ylabel("Frequência (Hz)")
        plt.xlabel("Tempo (s)")
        plt.colorbar(label="Intensidade (dB)")
        plt.tight_layout()
        plt.savefig(path_espec, dpi=600, bbox_inches="tight")
        plt.close()

        return path_espec

    # Gera o grafico da frequencia
    def frequenceGraph(self):
        """
        Gera um gráfico da frequência x intensidade da música
        Returns:
            path_fft: Caminho onde o gráfico foi salvo
        """
        
        # Configura o caminho a qual o arquivo vai ser salvo
        path_base = Path(__file__).parent.parent / "graphs"
        path_fft = path_base / f"{self.name_music}_fft.png"
        
        # Garate que as tranformada vão ser calculadas apenas uma vez
        if self.fft_freq is None or self.fft_values is None:
            self.fft_freq = self.musicFrequencies() # Frequencias 
            self.fft_values = self.musicDecomposition() # Intensidades
        
        size = len(self.fft_values)

        # Configuracao para o grafico FFT
        plt.figure(figsize=(12, 5))
        plt.plot(self.fft_freq[:size//2], self.fft_values[:size//2])
        plt.title(f"FFT {self.name_music} (MP3)")
        plt.xlabel("Frequência (Hz)")
        plt.ylabel("Intensidade")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(path_fft, dpi=600, bbox_inches="tight")
        plt.close()
        
        return path_fft