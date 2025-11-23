import matplotlib.pyplot as plt
from scipy.signal import spectrogram
import numpy 
from pathlib import Path

class Music:
    def __init__(self, data, sample_rate):
        self._sample_rate = sample_rate # Amostragem da música
        self._data_music = data / numpy.max(numpy.abs(data)) # Normalização das amostragens para valores no intervalo [-1, 1]
        self._fft_values = self.musicDecomposition() # Calcula a FFT da música 
        self._frequencies = self.musicFrequencies() # Calcula a FFT da frequência da música
        self._music_duration = len(self._data_music) / self._sample_rate # Duracao da música em segundos
        
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
    
    
    def spectogram(self, name_music: str, time):

        path_base = Path(__file__).parent.parent / "graphs"
        path_espec = path_base / f"{name_music}_espectrograma.png"

        # Manipula o tamanho da música para o espectograma
        max_duration = min(min(self._music_duration, 240), time) # Permite gerar apenas o espectograma dos primeiro 4 minutos da musica
        max_samples = max_duration * self._sample_rate # Quantidade maxima de amostras
        data = self._data_music[:max_samples] # Fatia a quantidade de amostras, para as primeiras ate max_samples

        if self.freq is None:

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
        plt.title(f"Espectrograma {name_music}")
        plt.ylabel("Frequência (Hz)")
        plt.xlabel("Tempo (s)")
        plt.colorbar(label="Intensidade (dB)")
        plt.tight_layout()
        plt.savefig(path_espec, dpi=600, bbox_inches="tight")
        plt.close()

        return path_espec

    # Gera o grafico da frequencia
    def frequenceGraph(self, name_music: str):
        
        path_base = Path(__file__).parent.parent / "graphs"
        path_fft = path_base / f"{name_music}_fft.png"
        
        size = len(self._fft_values)

        #  Grafico FFT 
        plt.figure(figsize=(12, 5))
        plt.plot(self._frequencies[:size//2], self._fft_values[:size//2])
        plt.title(f"FFT {name_music} (MP3)")
        plt.xlabel("Frequência (Hz)")
        plt.ylabel("Intensidade")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(path_fft, dpi=600, bbox_inches="tight")
        plt.close()
        
        return path_fft