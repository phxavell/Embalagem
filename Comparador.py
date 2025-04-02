import tkinter as tk
import time
import a_sap_connect23new as sap
import pandas as pd
import os
from datetime import datetime
import winsound

count= 0
a="pass"

# Contador global para numerar as execuções
execution_counter = 1
sound_file = "C:\\Embalagem\\error_sound.wav"
sound_file1 = "C:\\Embalagem\\click.wav"

def play_success_sound():
    sound_file1 = "C:\\Embalagem\\click.wav"  # Certifique-se de usar o formato WAV girlohno
   ## sound_file = "C:\\Embalagem\\girlohno.wav"
    
    if os.path.exists(sound_file1):
        # Reproduzir o som
        winsound.PlaySound(sound_file1, winsound.SND_FILENAME)
        time.sleep(0.5)  # Pausa de 0,5 segundos entre as execuções
        winsound.PlaySound(sound_file1, winsound.SND_FILENAME)
        time.sleep(0.5) 
        winsound.PlaySound(sound_file1, winsound.SND_FILENAME)
        time.sleep(0.5) 
        winsound.PlaySound(sound_file1, winsound.SND_FILENAME)
        
    else:
        print("Erro: Arquivo de som não encontrado!")

# Função para criar ou abrir o arquivo de log e registrar a mensagem
def logstep(stepinfo):
    global execution_counter
    
    # Obter o horário exato
    current_time = time.time() - start_time
    log_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")  # Formato: dia/mês/ano hora:minuto:segundo
    
    # Criar a mensagem do log com o horário exato
    log_message = (
        f"==================================================\n"
        f"### Início da Execução {execution_counter} - {log_time} ###\n"
        f"==================================================\n"
        f"LOG: {stepinfo}. Time: {current_time:.2f}s\n"
        f"Log Time: {log_time}\n"
        f"==================================================\n"
    )
    
    # Imprimir no console (se necessário)
    print(log_message)
    
    # Defina o caminho absoluto do arquivo de log
    log_filename = "C:\\Embalagem\\log.txt"
    
    # Verificar se o diretório existe, caso contrário, criar o diretório
    if not os.path.exists(os.path.dirname(log_filename)):
        try:
            os.makedirs(os.path.dirname(log_filename))
            print(f"Diretório {os.path.dirname(log_filename)} criado com sucesso.")
        except Exception as e:
            print(f"Erro ao criar diretório: {e}")
    
    # Verificar se o arquivo de log existe, caso contrário, criar
    if not os.path.exists(log_filename):
        with open(log_filename, 'w', encoding='utf-8') as log_file:
         log_file.write("Log file created\n")

# Abrir o arquivo de log em modo 'append' para adicionar novas entradas
    with open(log_filename, 'a', encoding='utf-8') as log_file:
     log_file.write(log_message)
    
    # Incrementar o contador de execução após registrar o log
    execution_counter += 1
    
    time.sleep(0.5)

def color(colorname):
    colorcode = 0

    if colorname == 'green':
        colorcode = '02'
    elif colorname == 'yellow':
        colorcode = '06'
    elif colorname == 'red':
        colorcode = '04'
    elif colorname == 'red-reverse':
        colorcode = '40'
    elif colorname == 'red-white':
        colorcode = 'F4'    
    else:
        colorcode = '07'

    colorful = lambda: os.system(
        'color ' + str(colorcode)
    )  # on Windows System

def verify_model(var_so, arquivo):
    # Carregar a planilha do Excel
    df = pd.read_excel(arquivo)
    
    # Normalizar as descrições para facilitar a comparação (remover espaços extras, converter para minúsculas)
    var_so = var_so.lower().strip()
    
    # Iterar sobre as linhas do DataFrame
    for index, row in df.iterrows():
        modelo_resumido = row['MODELO'].lower().strip()
        
        # Verificar se o modelo resumido está contido na descrição completa
        if modelo_resumido in var_so:
            sn_fonte = row['SN FONTE']
            sn_cabo = row['SN CABO']
            return sn_fonte, sn_cabo
      

# Função que será chamada quando o botão "Buscar" for pressionado
def on_button_click(entry_serial, entry_cabo, entry_fonte, result_label, status_label,connection_status_label,status_code,root):
    # Obter o número de série digitado
    global execution_counter
    serial_number = entry_serial.get()
    cabo = entry_cabo.get()
    fonte = entry_fonte.get()
    
    if status_code == 200:
        connection_status_label.config(bg="green") 
    
    status_label.config(text="login realizado com sucesso")
    logstep("00800- login realizado com sucesso")
    if entry_serial.get().startswith("AVNB"):
  
    # Chamada para obter o serial_number
     var_sn = sap.serial_chave2(serial_number)
     status_label.config(text=f"realizando consulta com o numero de serie..{serial_number}")
     logstep("00900- Consulta realizada com o numero de serie..")

     logstep(serial_number)
     logstep(serial_number)
    # Chamada para obter a descrição com base no serial_number
     var_so = sap.description(var_sn)
     status_label.config(text=f"ordem de producao:{var_sn}")
     logstep("001000- Ordem de Producao...")
     logstep(var_sn)
     logstep(var_sn)

    # Defina o caminho do arquivo CSV com os dados dos modelos
     arquivo_csv = 'C:\\Embalagem\\models.xlsx'  # Ajuste o caminho conforme necessário
    
   ##  pdb.set_trace()
    # Chamar a função para verificar o modelo no CSV
     sn_fonte, sn_cabo = verify_model(var_so, arquivo_csv)
    
    # Atualizar o rótulo de resultado com os números de série encontrados
     result_label.config(text=f"SN FONTE: {sn_fonte}, SN CABO: {sn_cabo}")
     
     value = assure_string(sn_fonte)
    # Verificar a comparação entre os números de série e os valores inseridos
     cabo_ok = cabo.startswith(sn_cabo) if sn_cabo else False
     fonte_ok = fonte.startswith(value) if sn_fonte else False

     root.config(bg="green")

     if cabo_ok and fonte_ok:
        # Se ambos os números de série forem prefixos dos valores inseridos
        status_label.config(text="Validação obteve sucesso")
        root.config(bg="green") 
       # winsound.PlaySound(sound_file1, winsound.SND_FILENAME)
      #  root.after(50, lambda: root.config(bg='green'))  # Cor padrão da janela
       # winsound.PlaySound(sound_file1, winsound.SND_FILENAME)
        root.after(20200, lambda: root.config(bg='SystemButtonFace'))  # Cor padrão da janela
        winsound.PlaySound(sound_file1, winsound.SND_FILENAME)
        winsound.PlaySound(sound_file1, winsound.SND_FILENAME)
        
        
        result_label.config(text=f"")
        logstep("01100 - Operation successfully")

       
        logstep("═══════════════════════════════════════════════════════════")
        logstep("✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅")
        logstep("✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅")
        logstep("═══════════════════════════════════════════════════════════")
        execution_counter=1
        
        
     else:
        # Caso contrário, verifica se algum não está correto
        if not cabo_ok:
            status_label.config(text="Cabo não encontrado ou não corresponde")
            connection_status_label.config(bg="red") 
            # Alterar a cor de fundo da janela para vermelho
            root.config(bg="red")
           
            winsound.PlaySound(sound_file, winsound.SND_FILENAME)
            root.after(100, lambda: root.config(bg='red'))  # Cor padrão da janela
            winsound.PlaySound(sound_file, winsound.SND_FILENAME)
            root.after(22100, lambda: root.config(bg='SystemButtonFace'))  # Cor padrão da janela
                # Após 2 segundos, retornar à cor original
            logstep(f"SN CABO: {sn_cabo} nao encontrado")
            
            logstep("═══════════════════════════════════════════════════════════")
            logstep("❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌")
            logstep("❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌")
            logstep("═══════════════════════════════════════════════════════════")
            execution_counter=1
            
            

        elif not fonte_ok:
            status_label.config(text="Fonte não encontrada ou não corresponde")
            connection_status_label.config(bg="red") 
            root.config(bg="red")
           
            winsound.PlaySound(sound_file, winsound.SND_FILENAME)
            root.after(100, lambda: root.config(bg='red'))  # Cor padrão da janela
            winsound.PlaySound(sound_file, winsound.SND_FILENAME)
            root.after(22100, lambda: root.config(bg='SystemButtonFace'))  # Cor padrão da janela

            logstep(f"SN FONTE: {sn_fonte} nao encontrado")
            
            logstep("═══════════════════════════════════════════════════════════")
            logstep("⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️")
            logstep("⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️")        
            logstep("═══════════════════════════════════════════════════════════")
            execution_counter=1
            
        else:
            status_label.config(text="Não encontrado")
    else:
       status_label.config(text="Por favor, preencha um serial valido") 
              
    
    # Atualizar o status (pode ser uma mensagem de sucesso ou erro)
    

# Função principal que inicia a interface gráfica
def main(status_code):
    # Criando a interface gráfica
    root = tk.Tk()
    root.title("Final Inspection")

    # Tornar a janela em tela cheia
    root.attributes('-fullscreen', True)
    root.bind("<F11>", lambda event: toggle_fullscreen(root))  # Permite alternar entre tela cheia e janela normal
    root.bind("<Escape>", lambda event: exit_fullscreen(root))  # Sair da tela cheia ao pressionar Esc

    # Carregar a imagem da logo usando tkinter.PhotoImage
    logo_path = "avell.png"  # Use .png ou .gif, pois PhotoImage não suporta .jpeg diretamente
    logo_photo = tk.PhotoImage(file=logo_path)

    # Criar o label para a logo
    logo_label = tk.Label(root, image=logo_photo, bg="#f4f4f4")
    logo_label.image = logo_photo  # Isso é necessário para evitar que a imagem seja descartada
    logo_label.place(x=10, y=10)  # Posicionar no canto superior esquerdo

    # Centralizar os componentes
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=1)
    root.grid_rowconfigure(4, weight=1)
    root.grid_rowconfigure(5, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # Estilos modernos
    font_style = ("Segoe UI", 18)  # Aumentando o tamanho da fonte para as labels
    bg_color = "#f4f4f4"
    entry_bg = "#ffffff"
    button_color = "#31C394"
    button_hover = "#45a049"
    border_color = "#ccc"
    
    # Alterando a cor de fundo da janela
    root.config(bg=bg_color)

    # Labels e campos de entrada
    label_serial = tk.Label(root, text="Serial:", font=font_style, bg=bg_color)
    label_serial.grid(row=2, column=0, padx=20, pady=20, sticky="e")

    entry_serial = tk.Entry(root, width=30, font=font_style, bg=entry_bg, relief="solid", bd=2)
    entry_serial.grid(row=2, column=1, padx=20, pady=20, sticky="ew")
    
    label_cabo = tk.Label(root, text="Cabo:", font=font_style, bg=bg_color)
    label_cabo.grid(row=1, column=0, padx=20, pady=20, sticky="e")

    entry_cabo = tk.Entry(root, width=30, font=font_style, bg=entry_bg, relief="solid", bd=2)
    entry_cabo.grid(row=1, column=1, padx=20, pady=20, sticky="ew")

    label_fonte = tk.Label(root, text="Fonte:", font=font_style, bg=bg_color)
    label_fonte.grid(row=0, column=0, padx=20, pady=20, sticky="e")

    entry_fonte = tk.Entry(root, width=30, font=font_style, bg=entry_bg, relief="solid", bd=2)
    entry_fonte.grid(row=0, column=1, padx=20, pady=20, sticky="ew")

    # Definir o foco no campo de entrada ao iniciar
    entry_fonte.focus_set()

    # Nova label para "Status:" com maior fonte
    label_status = tk.Label(root, text="Status:", font=font_style, bg=bg_color)
    label_status.grid(row=3, column=0, padx=20, pady=20, sticky="e")

    status_label = tk.Label(root, text="", font=font_style, bg=bg_color)
    status_label.grid(row=3, column=1, padx=20, pady=20, sticky="ew")

    result_label = tk.Label(root, text="", font=font_style, bg=bg_color)
    result_label.grid(row=4, column=0, columnspan=2, padx=20, pady=40, sticky="ew")

    # Botão de busca
    button_search = tk.Button(root, text="Buscar", command=lambda: on_button_click(entry_serial, entry_cabo, entry_fonte, result_label, status_label, connection_status_label, status_code, root), font=font_style, bg=button_color, activebackground=button_hover, relief="flat")
    button_search.grid(row=5, column=0, columnspan=2, pady=20, sticky="ew")

    # Bolinha verde ou vermelha no canto superior direito para indicar o status da conexão
    connection_status_label = tk.Label(root, width=2, height=1, bg="red", relief="solid", bd=2)
    connection_status_label.place(x=root.winfo_width() - 30, y=10)

    # Iniciar a verificação para mover o foco após a interface ser iniciada
    entry_serial.after(100, check_and_move, entry_fonte, entry_cabo, button_search, "fonte", entry_fonte)
    entry_cabo.after(100, check_and_move, entry_cabo, entry_serial, button_search, "cabo", entry_fonte)

    # Iniciar a interface gráfica
    root.mainloop()


def toggle_fullscreen(root, event=None):
    """ Alterna entre o modo tela cheia e o modo janela normal """
    is_fullscreen = root.attributes('-fullscreen')
    root.attributes('-fullscreen', not is_fullscreen)

def exit_fullscreen(root, event=None):
    """ Sai do modo tela cheia """
    root.attributes('-fullscreen', False)

def move_to_next(entry_current, entry_next, button):
    """Move o foco para o próximo campo"""
    entry_next.focus_set()

def assure_string(valor):
    if isinstance(valor, (int, float)):  # Verifica se é um número
        valor = str(valor)  # Converte para string
    return valor
   


def check_and_move(entry_current, entry_next, button, ts , entry_serial):
    """Verifica se o campo atual foi preenchido e move o foco se necessário"""
    dicionario = {
    "240301F04": "Valor 1",
    "180308F00": "Valor 2",
    "230505F01": "Valor 3",
    "0453C": "Valor 4",
    "180304F05": "Valor 5",
    "280500W00": "Valor 6",
    "2303023": "Valor 7",
    "1503C1": "Valor 8",
    "F2A18": "Valor 9",
    "POWR": "Valor 10", 
    "F2A81": "Valor 11"  
}
    global a
#   pdb.set_trace()
    if isinstance(entry_next.get(), str) and entry_next.get().startswith("AVNB") and len(entry_next.get()) >= 12 and ts == "cabo": 
        button.invoke()
        entry_current.delete(0, tk.END)
        entry_next.delete(0, tk.END)
        entry_serial.delete(0, tk.END)
        print("deletando tudo")
        print(ts)
        entry_serial.focus_set()
        a="pass"
        

    if (entry_current.get().startswith("POWR")  and len(entry_current.get()) >= 22 and ts == "cabo") or entry_current.get().startswith("POWR")  and len(entry_current.get()) >= 10 and ts == "cabo" : 
        entry_value = entry_current.get()  # Obtém o valor da entrada
        entry_current.delete(0, "end")  # Limpa o campo de entrada
        entry_current.insert(0, entry_value[:12])
        move_to_next(entry_current, entry_next, button)   
        a="next"

    if (any(entry_current.get().startswith(key) for key in dicionario) and len(entry_current.get()) >= 19 and ts == "fonte" and a == "pass") or  (any(entry_current.get().startswith(key) for key in dicionario) and len(entry_current.get()) >= 16 and ts == "fonte" and a == "pass") or  (any(entry_current.get().startswith(key) for key in dicionario) and len(entry_current.get()) >= 10 and ts == "fonte" and a == "pass"):
        entry_value = entry_current.get()  # Obtém o valor da entrada
        entry_current.delete(0, "end")  # Limpa o campo de entrada
        entry_current.insert(0, entry_value[:12])  # Insere os primeiros 12 caracteres  
        move_to_next(entry_current, entry_next, button)
 
     
      #  pdb.set_trace() 
 
    # Agenda a próxima verificação para 500ms
    print(a)
    print("campo1")
   ## len(entry_current.get() >= 12)
    print(entry_current.get())
    entry_current.after(300, check_and_move, entry_current, entry_next, button,ts, entry_serial)    




# Função principal de execução
if __name__ == "__main__":
    start_time = time.time()

    logstep("00600 - Connect to Avell's SAP API")

    result = sap.connect()
    status_code = result.status_code

# Dicionário de interpretação de códigos de status
    status_messages = {
    200: "Conexão bem-sucedida.",
    400: "Requisição inválida.",
    401: "Não autorizado.",
    404: "Não encontrado.",
    500: "Erro no servidor.",
}

# Retorna a mensagem correspondente ao código de status
    status_message = status_messages.get(status_code, "Status desconhecido.")
    print(f"Status da conexão: {status_message} (Código: {status_code})")
    logstep("00700 - SAP Inventory & manufacturing handle")
    main(status_code)


