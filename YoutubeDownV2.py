# Librarias que eu usei para esta aplicaçao -------------------------------------------------
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox, Progressbar
from pytube import YouTube
from PIL import Image, ImageTk
import requests
from tkinter import filedialog
import os
import threading
#---------------------------------------------------------------------------------------------------------------
# função para Sair ---------------------------------------------------------------------------------------------
def fechar_aplicacao():
    resposta = messagebox.askyesno("Fechar Aplicação", "Tem certeza de que deseja fechar a aplicação? sim/ nao")
    if resposta:
        Janela.destroy()  # fecha a aplicação se a resposta for afirmativa
#----------------------------------------------------------------------------------------------------------------
# função para Limpar --------------------------------------------------------------------------------------------
def limpar_campos():
    Eurl.delete(0, END)  # Limpa o campo de entrada
    rdmp3.set(0)          # Desmarca o radiobutton de MP3
    rdmp4.set(0)          # Desmarca o radiobutton de MP4
    mp3.set('Qualidade mp3')  # Redefine a combobox de MP3 para o valor padrão
    mp3['values'] = [] 
    mp4.set('Qualidade mp4')  # Redefine a combobox de MP4 para o valor padrão
    mp4['values'] = [] 
    Limagem.config(image='')  # Limpa a imagem exibida
    progresso.stop()  # Para a barra de progresso
    progresso['value'] = 0  # Redefine o valor da barra de progresso para 0
#-------------------------------------------------------------------------------------------
# função Mostrar ----------------------------------------------------------------------------
def mostrar():
    url = Eurl.get()
    try:
        yt = YouTube(url)
        thumbnail_url = yt.thumbnail_url
        imagem = Image.open(requests.get(thumbnail_url, stream=True).raw)
        imagem.thumbnail((2500, 305))
        foto = ImageTk.PhotoImage(imagem)
        Limagem.config(image=foto)
        Limagem.image = foto

        # Obter as opções de qualidade de áudio e vídeo
        video_streams = yt.streams.filter(only_video=True)
        audio_streams = yt.streams.filter(only_audio=True)

        if rdmp3.get() == 1:  # Se selecionou MP3
            # Filtrar apenas as qualidades disponíveis de áudio
            available_audio_streams = [stream.abr for stream in audio_streams if stream.abr]
            # Preencher a combobox de MP3 apenas com as opções de qualidade disponíveis
            mp3['values'] = available_audio_streams
            # Se a qualidade selecionada não estiver disponível, limpar a seleção
            if mp3.get() not in available_audio_streams:
                mp3.set('') 
            mp4.set('')  # Limpa a combobox de MP4
        elif rdmp4.get() == 1:  # Se selecionou MP4
            # Filtrar apenas as qualidades de vídeo disponíveis e eliminar duplicatas
            available_video_streams = list(set([f"{stream.resolution}p" for stream in video_streams if stream.resolution]))
            # Preencher a combobox de MP4 apenas com as opções de qualidade disponíveis
            mp4['values'] = available_video_streams
            # Se a qualidade selecionada não estiver disponível, limpar a seleção
            if mp4.get() not in available_video_streams:
                mp4.set('') 
            mp3.set('')  # Limpa a combobox de MP3

            # Exibir as qualidades disponíveis em uma messagebox
            if available_video_streams:
                messagebox.showinfo("Qualidades Disponíveis", f"Qualidades disponíveis: {', '.join(available_video_streams)}")
            else:
                messagebox.showinfo("Qualidades Disponíveis", "Nenhuma qualidade de vídeo disponível.")
        
    except Exception as e:
        Limagem.config(image='')
        Limagem.image = None
        mp3.set('Qualidade mp3')
        mp4.set('Qualidade mp4')
        messagebox.showinfo('Erro', f"Erro ao processar a URL: {e}")

#---------------------------------------------------------------------------------------------
# função para sacar Musicas em mp3 --------------------------------------------------------------------------------------------------------------------------------------------------------
def download_mp3():
    url = Eurl.get()
    selected_quality = mp3.get()  # Obtém a qualidade selecionada
    try:
        yt = YouTube(url)
        # Encontra a stream de áudio com a qualidade selecionada
        audio_stream = yt.streams.filter(only_audio=True, abr=selected_quality).first()
        
        # Abre uma janela de diálogo para selecionar o local e o nome do arquivo
        file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        
        if file_path:  # Se o usuário selecionou um local e nome de arquivo
            audio_stream.download(output_path=os.path.dirname(file_path), filename=os.path.basename(file_path))  # Faz o download do áudio com o nome especificado
            messagebox.showinfo('Download', 'Download MP3 concluído com sucesso!')
    except Exception as e:
        messagebox.showinfo('Erro', f'Erro ao fazer o download MP3: {e}')
    finally:
        progresso.stop()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------        
# função para iniciar O download Mp4 -----------------------------------------------------------------------------------------------------------------------------------
def download_mp4():
    url = Eurl.get()
    selected_quality = mp4.get()  # Obtém a qualidade selecionada
    try:
        yt = YouTube(url)
        # Encontra todas as streams disponíveis
        all_streams = yt.streams.filter(file_extension='mp4')
        
        # Encontra a melhor opção de vídeo com áudio
        best_option = None
        for stream in all_streams:
            if stream.includes_audio_track:
                best_option = stream
                break
        
        if best_option:
            # Abre uma janela de diálogo para selecionar o local e o nome do arquivo
            file_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
            
            if file_path:  # Se o usuário selecionou um local e nome de arquivo
                best_option.download(output_path=os.path.dirname(file_path), filename=os.path.basename(file_path))  # Faz o download do vídeo com o nome especificado
                messagebox.showinfo('Download', 'Download MP4 concluído com sucesso!')
        else:
            messagebox.showinfo('Erro', 'Não foi possível encontrar uma opção de vídeo com áudio disponível.')
    except Exception as e:
        messagebox.showinfo('Erro', f'Erro ao fazer o download MP4: {e}')
    progresso.stop()
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

# função para Iniciar O download --------------------------------------------------------------------------------------
def iniciar_download():
    progresso.start()
    if rdmp3.get() == 1:
        download_mp3()
    elif rdmp4.get() == 1:
        download_mp4()
#----------------------------------------------------------------------------------------------------------------------
# defenir as Cores a usar ---------------------------------------------------------------------------------------------
co0 ='#ffffff' # cor branca Para O fundo da Janela
co1 ='#ffeee1' # vemelho claro para Os botões 
co2 ='#f6ffe9' # verde claro para a entry 
#----------------------------------------------------------------------------------------------------------------------
# configurar a Nossa Janela-----------------------------------------------------------------
Janela = Tk()
Janela.title('Youtube Download V2 Dev Joel Portugal 2024 ©, Versão Portuguesa')
Janela.geometry('600x540+100+100')
Janela.resizable(0,0)
Janela.config(bg=co0)
Janela.iconbitmap('C:\\Users\\HP\\Desktop\\Projectos\\Download V1\\icon.ico')
#-------------------------------------------------------------------------------------------

# criar o fonte end ------------------------------------------------------------------------
Eurl = Entry(Janela, font=('arial 14'), width=50, bg=co2)
Eurl.place(x=10, y=10)
#-------------------------------------------------------------------------------------------
# criar os Radiobutons----------------------------------------------------------------------
rdmp3 = IntVar()
Radiobutton(Janela, text='Formato Mp3', font=('arial 14'), bg=co0,variable=rdmp3, value=1).place(x=10, y=45)
rdmp4 = IntVar()
Radiobutton(Janela, text='Formato Mp4', font=('arial 14'), bg=co0,variable=rdmp4, value=1).place(x=250, y=45)
#-------------------------------------------------------------------------------------------
# criar as Comboboxes ----------------------------------------------------------------------
mp3 = Combobox (Janela, font=('arial 14'),width=15,)
mp3.place(x=10, y=85)
mp3.set('Qualidade mp3') 
mp4 = Combobox (Janela, font=('arial 14'),width=15,)
mp4.place(x=250, y=85) 
mp4.set('Qualidade mp4') 
#-------------------------------------------------------------------------------------------
# criar os Botões -------------------------------------------------------------------------
BDown = Button(Janela, text='Download', font=('arial 14'), bg=co1,relief=RAISED, overrelief=RIDGE, command=iniciar_download)
BDown.place(x=10, y=130)
BMostrar = Button(Janela, text='Mostrar', font=('arial 14'), bg=co1,relief=RAISED, overrelief=RIDGE, command= mostrar)
BMostrar.place(x=120, y=130)
BLimpar = Button(Janela, text='Limpar', font=('arial 14'), bg=co1,relief=RAISED, overrelief=RIDGE, command=limpar_campos)
BLimpar.place(x=210, y=130)
BSair = Button(Janela, text='Fechar Aplicação', font=('arial 14'),bg=co1,relief=RAISED, overrelief=RIDGE, command=fechar_aplicacao)
BSair.place(x=295, y=130)
#-----------------------------------------------------------------------------------------
# cria a label onde vai ser exbida a capa do video ---------------------------------------
Limagem = Label(Janela, bg='white',)
Limagem.place(x=10, y=180)
#------------------------------------------------------------------------------------------
# criar a Barra de Progresso --------------------------------------------------------------
progresso = Progressbar(Janela,length=545, mode='determinate',)
progresso.place(x=10, y=500)
#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
# Iniciar a Janela ------------------------------------------------------------------------
Janela.mainloop()
#------------------------------------------------------------------------------------------