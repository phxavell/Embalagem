import time
import av_art
import a_sap_connect23new as sap
import pandas as pd
import os

def logstep(stepinfo):
    print("LOG: %s. Time: %2.fs" % (stepinfo, time.time() - start_time))
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

# Função que realiza o batimento entre o nome completo e o nome resumido

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
    
    # Caso não encontre nenhum modelo correspondente
    return None, None

def main():
    '''Main function to install and activate Windows'''

    # av_art.screen_clear()
    av_art.art_avell_notebooks()
    logstep("00600 - Connect to Avell's SAP API")

    sap.connect()
    
    logstep("00700 - SAP Inventory & manufacturing handle")
    av_art.art_serial()
    var_sn = sap.serial_chave1()
    logstep(var_sn)
    logstep(var_sn)
    logstep(var_sn)
    
    # Obter a descrição completa do produto
    var_so = sap.description(var_sn)
    logstep(var_so)
    logstep(var_so)
    logstep(var_so)

    # Defina o caminho do arquivo CSV com os dados dos modelos
    arquivo_csv = 'C:\Embalagem\models.xlsx'  # Ajuste o caminho conforme necessário
    
    # Chamar a função para verificar o modelo no CSV
    sn_fonte, sn_cabo = verify_model(var_so, arquivo_csv)
    

    if sn_fonte and sn_cabo:
     print(f"SN FONTE: {sn_fonte}, SN CABO: {sn_cabo}")
    else:
     print("Modelo não encontrado")

    # # Exibir os resultados, caso o modelo tenha sido encontrado
    # if sn_fonte and sn_cabo:
    #     logstep(f"Modelo encontrado! SN FONTE: {sn_fonte}, SN CABO: {sn_cabo}")
    # else:
    #     logstep("Modelo não encontrado no CSV.")

if __name__ == "__main__":
    start_time = time.time()
    main()
