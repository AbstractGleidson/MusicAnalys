from Music import Music
from pathlib import Path
import sys
import os 
import platform
import librosa

try:
    music_name = sys.argv[1]
except IndexError:
    print("Música não informada!")
    music_name = None
    
    
command = "cls" if platform.platform() == "Windows-11-10.0.26100-SP0" else "clear"

if __name__ == "__main__" and music_name is not None:
        
    path_music = Path(__file__).parent.parent / "assets" / music_name # path da musica
    
    try:
        data_music, sample_rate = librosa.load(path_music, sr=None)
        os.system(command)
        isMusicLoad = True
    except FileNotFoundError:  
        os.system(command)
        print("Não foi possível carregar a música da pasta assets!")
        isMusicLoad = False
    
    
    if isMusicLoad:
        
        # tratamento do name da musica
        music_name = music_name.split(".")[0] # Pega apenas a musica sem a extensao
        music_name = "_".join(music_name.split(" ")) # Tira os espacos e substitui por "_"
        music = Music(data_music, sample_rate, music_name)

        plot_response = "" # Resposta do plot 
        while(True):
            os.system(command)
            
            print(plot_response)
            print("============== Menu =============")
            print("1 - Gerar grafico da frenquencia")
            print("2 - Gerar espectograma")
            print("3 - Sair")
            response = int(input(": "))
            
            if response == 1:
                print("\nGerando gráfico...")
                
                path = music.frequenceGraph()
        
                plot_response = f"Gráfico gerado com suscesso. Salvo em: {path}"
            
            elif response == 2:
                time = int(input("Quantidade de segundos: "))
                
                print("\nGerando espectograma...")
                #Cria o spectograma da musica
                path = music.spectogram(time)
                
                plot_response = f"Espectograma gerado com suscesso. Salvo em: {path}"
                
            elif response == 3:
                break
        
            else:
                plot_response = "Escolha uma opção válida!"
