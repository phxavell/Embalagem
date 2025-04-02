import a_sap_config23new as sap
import time
import requests
#from urllib3.exceptions import InsecureRequestWarning
import urllib3
import json

global session
session = requests.Session()
session.verify = False

def connect(retry_delay=3):  # Adiciona um parâmetro para o tempo de espera entre as tentativas
    data = '''{"CompanyDB": "%s", "UserName": "%s", "Password": "%s"}''' % (sap.COMPANYDB, sap.USERNAME, sap.PASSWORD)
    url = sap.URL
    urllib3.disable_warnings()  # Desabilita os avisos de permissão HTTPS

    attempts = 0  # Inicializa o contador de tentativas

    while True:
        attempts += 1  # Incrementa o contador a cada tentativa
        try:
            aaa = session.post(url, data)
            aaa.raise_for_status()  # Levanta um erro para códigos de status HTTP não 200
            return aaa  # Retorna a resposta da conexão se for bem-sucedida
        
        except requests.exceptions.RequestException as e:
            print(f"Erro na conexão: {e}. Tentativa #{attempts}. Código de status: {aaa.status_code if 'aaa' in locals() else 'N/A'}. Resposta: {aaa.text if 'aaa' in locals() else 'N/A'}")
            time.sleep(retry_delay)  # Espera o tempo especificado antes de tentar novamente


def description(var_os):
    pd = pedido(var_os) # Adiciona o numero do pedido a uma variavel
    coditem = cod_item(var_os)
    url2 = "https://avell.ramo.com.br:50000/b1s/v1/Orders(%s)?$select=DocumentLines" % pd # Passa por parametros a ordem de venda para buscar a descrição do computador. Usar a mesma para tirar o sistema e o modelo do notebook
    bbb = session.get(url2) # Dá um get para buscar as informações solicitadas na URL
    bbb_dic = bbb.json()
    i=0
    for n in bbb_dic['DocumentLines']:
        if (bbb_dic['DocumentLines'][i]['ItemCode'] == coditem):
            return bbb_dic['DocumentLines'][i]['ItemDescription']
        i+=1
    
 #usando o cod_item para retornar a NB e gravar na BIOS como SKU   
def cod_item(var_ped, retry_delay=3):  # Adiciona um parâmetro para o tempo de espera entre as tentativas
    url2 = "https://avell.ramo.com.br:50000/b1s/v1/ProductionOrders?$filter=DocumentNumber eq %s" % var_ped  # Passa o número da OS como parâmetro para retornar o número do pedido

    attempts = 0  # Inicializa o contador de tentativas

    while True:
        attempts += 1  # Incrementa o contador a cada tentativa
        try:
            bbb = session.get(url2)
            bbb.raise_for_status()  # Levanta um erro para códigos de status HTTP não 200
            db = json.loads(bbb.text)

            # Verifique se a lista não está vazia
            if 'value' in db and len(db['value']) > 0:
                return db['value'][0]['ItemNo']  # Retorna o código do ITEM
            else:
                return "Nenhum resultado encontrado para o Número do Pedido fornecido."
        
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}. Tentativa #{attempts}. Tentando novamente...")
            time.sleep(retry_delay)  # Espera o tempo especificado antes de tentar novamente
    
    
    
    
def serial_chave():
    sn_chave = input("Digite o Número de Série:")
    url2 = f"https://avell.ramo.com.br:50000/b1s/v1/ProductionOrders?$filter=U_AV_NR_SERIE eq '{sn_chave}'"
    bbb = session.get(url2)
    db = json.loads(bbb.text)
    
    # Verifique se a lista não está vazia
    if 'value' in db and len(db['value']) > 0:
        return db['value'][0]['DocumentNumber']
    else:
        return "Nenhum resultado encontrado para o Número de Série fornecido."

def serial_chave1(retry_delay=3):  # Adiciona um parâmetro para o tempo de espera entre as tentativas
    sn_chave = input('\nFAÇA A LEITURA DO NUMERO DE SERIE: ')
    url2 = f"https://avell.ramo.com.br:50000/b1s/v1/ProductionOrders?$filter=U_AV_NR_SERIE eq '{sn_chave}'"
    
    attempts = 0  # Inicializa o contador de tentativas

    while True:
        attempts += 1  # Incrementa o contador a cada tentativa
        try:
            bbb = session.get(url2)
            bbb.raise_for_status()  # Levanta um erro para códigos de status HTTP não 200
            db = json.loads(bbb.text)

            # Verifique se a lista não está vazia
            if 'value' in db and len(db['value']) > 0:
                return db['value'][0]['DocumentNumber']
            else:
                return "Nenhum resultado encontrado para o Número de Série fornecido."
        
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}. Tentativa #{attempts}. Tentando novamente...")
            time.sleep(retry_delay)  # Espera o tempo especificado antes de tentar novamente

def serial_chave2(sn_chave):  # Adiciona um parâmetro para o tempo de espera entre as tentativas
 #   sn_chave = input('\nFAÇA A LEITURA DO NUMERO DE SERIE: ')
    url2 = f"https://avell.ramo.com.br:50000/b1s/v1/ProductionOrders?$filter=U_AV_NR_SERIE eq '{sn_chave}'"
    
    attempts = 0  # Inicializa o contador de tentativas

    while True:
        attempts += 1  # Incrementa o contador a cada tentativa
        try:
            bbb = session.get(url2)
            bbb.raise_for_status()  # Levanta um erro para códigos de status HTTP não 200
            db = json.loads(bbb.text)

            # Verifique se a lista não está vazia
            if 'value' in db and len(db['value']) > 0:
                return db['value'][0]['DocumentNumber']
            else:
                return "Nenhum resultado encontrado para o Número de Série fornecido."
        
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}. Tentativa #{attempts}. Tentando novamente...")
            time.sleep(3)  # Espera o tempo especificado antes de tentar novamente
'''
def sn_chave():
    # Solicite ao usuário que insira o valor de U_AV_NR_SERIE
    u_av_nr_serie = input("Digite o número de Série: ")

    # Defina a URL base e o filtro
    base_url = "https://avell.ramo.com.br:50000/b1s/v1/ProductionOrders"
    query = f"?$filter=U_AV_NR_SERIE eq '{u_av_nr_serie}'"
    url = base_url + query

    # Faça a solicitação GET à API
    response = session.get(url)

    # Verifique a resposta
    if response.status_code == 200:
        data = response.json()
        
        # Filtrar e exibir apenas os campos desejados
        filtered_data = [
            {
                "DocumentNumber": item["DocumentNumber"],
                "ItemNo": item["ItemNo"],
                "ProductDescription": item["ProductDescription"]
            } 
            for item in data.get("value", [])
        ]
        
        print(json.dumps(filtered_data, indent=4))
    else:
        print(f"Erro: {response.status_code}")
        print(response.text)

'''
def pedido(var_ped, retry_delay=3):  # Adiciona um parâmetro para o tempo de espera entre as tentativas
    url2 = f"https://avell.ramo.com.br:50000/b1s/v1/ProductionOrders?$filter=DocumentNumber eq {var_ped}"

    attempts = 0  # Inicializa o contador de tentativas

    while True:
        attempts += 1  # Incrementa o contador a cada tentativa
        try:
            bbb = session.get(url2)
            bbb.raise_for_status()  # Levanta um erro para códigos de status HTTP não 200
            db = json.loads(bbb.text)

            # Verifique se a lista não está vazia
            if 'value' in db and len(db['value']) > 0:
                return db['value'][0]['ProductionOrderOriginEntry']
            else:
                return "Nenhum resultado encontrado para o Número do Pedido fornecido."
        
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}. Tentativa #{attempts}. Tentando novamente...")
            time.sleep(retry_delay)  # Espera o tempo especificado antes de tentar novamente

    
def sis(var_os):
    #if (var_os[:4] == 'INTR'):
    #    return 'Windows 10 Pro'
    pd = pedido(var_os) # Adiciona o numero do pedido a uma variavel
    coditem = cod_item(var_os)
    url2 = "https://avell.ramo.com.br:50000/b1s/v1/Orders(%s)?$select=DocumentLines" % pd # Passa por parametros a ordem de venda para buscar a descrição do computador. Usar a mesma para tirar o sistema e o modelo do notebook
    bbb = session.get(url2)
    bbb_dic = bbb.json()
    i=0
    for n in bbb_dic['DocumentLines']:
        if (bbb_dic['DocumentLines'][i]['ItemCode'] == coditem):
            return bbb_dic['DocumentLines'][i]['U_AVELL_SO'] # Retorna o sistema
        i+=1



def virtuo(var_os):

    pd = pedido(var_os) # Adiciona o numero do pedido a uma variavel
    coditem = cod_item(var_os)
    url2 = "https://avell.ramo.com.br:50000/b1s/v1/Orders(%s)?$select=DocumentLines" % pd # Passa por parametros a ordem de venda para buscar a descrição do computador. Usar a mesma para tirar o sistema e o modelo do notebook
    bbb = session.get(url2)
    bbb_dic = bbb.json()
    i=0
    for n in bbb_dic['DocumentLines']:
        if (bbb_dic['DocumentLines'][i]['ItemCode'] == coditem):
            return bbb_dic['DocumentLines'][i]['U_AVELL_SIS_Virtuo'] # Retorna se o sistema é Virtuo ou não
        i+=1
    

def dexis(var_os):

    pd = pedido(var_os) # Adiciona o numero do pedido a uma variavel
    coditem = cod_item(var_os)
    url2 = "https://avell.ramo.com.br:50000/b1s/v1/Orders(%s)?$select=DocumentLines" % pd # Passa por parametros a ordem de venda para buscar a descrição do computador. Usar a mesma para tirar o sistema e o modelo do notebook
    bbb = session.get(url2)
    bbb_dic = bbb.json()
    i=0
    for n in bbb_dic['DocumentLines']:
        if (bbb_dic['DocumentLines'][i]['ItemCode'] == coditem):
            return bbb_dic['DocumentLines'][i]['U_AVELL_SIS_Dexis'] # Retorna se o sistema é DEXIS ou não
    

def serial(var_os):
    url2 = "https://avell.ramo.com.br:50000/b1s/v1/ProductionOrders?$filter=DocumentNumber eq %s" % var_os # Passa por parametros a ordem de venda para buscar o Numero de série na tabela OBJ_SERVICO
    bbb = session.get(url2)
    db = json.loads(bbb.text)
    return (db['value'][0]['U_AV_NR_SERIE'])
    
### TENTATIVA PARA ADICIONAR A NB NA BIOS ### inacio - 15/04/2024
'''
def nbsku(var_os):
    url2 = "https://avell.ramo.com.br:50000/b1s/v1/ProductionOrders?$filter=DocumentNumber eq %s" % var_os # Passa por parametros a ordem de venda para buscar o Numero de série na tabela OBJ_SERVICO
    bbb = session.get(url2)
    db = json.loads(bbb.text)
    return (db['value'][0]['ItemCode'])    
'''

def sistema(var_os):                            #necessário atenção para verificar se com windows ou não para pedidos com mais de 1 máquina.
    #if (var_os[:4] == 'INTR'):
    #    return 'Windows 10 PRO'
    pd = pedido(var_os)
    url2 = "https://avell.ramo.com.br:50000/b1s/v1/Orders(%s)?$select=DocumentLines" % pd # Passa por parametros a ordem de venda para buscar a descrição do computador. Usar a mesma para tirar o sistema e o modelo do notebook
    bbb = session.get(url2)
    bbb_dic = bbb.json()
    var_sis = sis(var_os)
    if var_sis is None:
        return ("SEM SO")
    #Faz a verificação de qual sistema será instalado
    var_10h = ['Windows 10 Home Single Language', 'Windows 10 HSL']
    var_10p = ['Windows 10 Professional', 'Windows 10 PRO','Windows 10 Pro']
    var_11h = ['Windows 11 Home Single Language', 'Windows 11 HSL']
    var_11p = ['Windows 11 Professional', 'Windows 11 PRO','Windows 11 Pro']
    vir = virtuo(var_os)
    dex = dexis(var_os)
    if vir:
        return("Virtuo") # Se for um virtuo, é feito o retorno antecipado, não indo para as proximas linhas
    
    if dex:
        return("Dexis")
    for n in var_10h:
        if n in var_sis:
            return ("Windows 10 HSL")
    for n in var_10p:
        if n in var_sis:
            return ("Windows 10 PRO")
    for n in var_11h:
        if n in var_sis:
            return ("Windows 11 HSL")
    for n in var_11p:
        if n in var_sis:
            return ("Windows 11 PRO")
    
    else: return ("SEM SO")
    
    