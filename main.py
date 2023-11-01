from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service


import datetime
from datetime import datetime
from datetime import date
from datetime import timedelta


from configparser import ConfigParser, ExtendedInterpolation


import json
import os
import metricas
import telegram
import functions
import emojis
import importlib
import psutil


def restart():
    # Cria um novo Firefox Profile
    profile = FirefoxProfile()

    # Configurações do Profile para permitir o download automático dos arquivos
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', '/path/to/download/folder')
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream')
   

    # Configurações das opções do Firefox
    #options = Options()
    #options.headless = False
    #options.profile = profile

    # Inicia o driver com as opções e o profile configurados
    s = Service(executable_path='geckodriver.exe')
    driver = webdriver.Firefox(service=s)
    #driver = webdriver.Firefox(options=options, executable_path='geckodriver.exe')
    config = ConfigParser()
    config.read('config.conf')
    usr = config.get('DEFAULT','user_mrjack') 
    pw = config.get('DEFAULT','pws_mrjack')
    # Acessa o site desejado
    driver.get('https://mrjack.bet/aviator')
    time.sleep(5)



    try:
       # Preenche os campos de usuário e senha
        login = driver.find_element(By.ID, 'username')
        login.click()
        login.send_keys(usr)
        time.sleep(1)
        driver.find_element(By.ID, 'password').send_keys(pw)
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[1]/main/header/div[1]/form/div[2]/button").click()
        
        time.sleep(5)

        #Click Aviator
        #driver.get("https://mrjack.bet/aviator")
        #time.sleep(5)

    except Exception as e:
        print(e)
        driver.get("https://mrjack.bet/aviator")
        time.sleep(5)
        

    #try:
    # Pega o XPath do iframe e atribui a uma variável
    iframe = driver.find_element(By.XPATH,"/html/body/div[1]/main/iframe")
                        
    # Muda o foco para o iframe
    driver.switch_to.frame(iframe)
    time.sleep(2)

    historico2 = []

    #Coleta dos Dados
    atencao = False
    entrada = False
    IDSendAlerta = 0

    lista_bots = []

    bots = functions.get_bots(16,67)
    print(bots)

    for bot in bots:
        print(bot)
        lista_bots.append(bot)
    
    IDSendAlerta = 0
    while True:
        #try:
            #verify_fun_mode = driver.find_elements(By.CLASS_NAME, 'fun-mode')
            #if len(verify_fun_mode) != 0:
                #print('Atualizando a página do Aviator')
                #driver.get('https://mrjack.bet/aviator')
        #except:
            #pass
        #Coletando histórico
        numeros = driver.find_elements(By.XPATH,"/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]/div/app-bubble-multiplier")   
        i = 0
        fm = 0
        #idtip = 0
        historico = []

        #Coleta dos vôos do aviator
        for numero in numeros:
            data_hora = datetime.now()
            
            data_hora_str = data_hora.strftime("%d-%m-%Y %H-%M")
            entrada_metrica = 'atencao'
            
            if i < 8:
                try:
                    historico.append(str(numero.find_element(By.XPATH,".//div").text).replace("x", ""))
                    i = i + 1
                except:
                    try:
                        driver.close()
                        print('Fechando navegador!')
                    except:
                        print('Navegador já estava fechado!')
                        continue
                    print('Erro no site. Reiniciando o bot!')
                    time.sleep(3)
                    importlib.reload(restart())
            #if fm == 1:
            
                #set1 = set(historico)
                #set2 = set(historico2)
                #comuns_candles = set1.intersection(set2)
                #if len(comuns_candles) < 5:
                    #importlib.reload(restart())

            else:
            #Comparar se houve atualização no histórico e caso sim, imprimir na tela o histórico atual.
                if historico2 != historico:
                    
                    historico2 = historico.copy()  
                    fm = 1
                    
                    velas4 = []
                    li = 0
                    for l in historico:
                        velas4.append(f'{str(l).replace("[","").replace("]","")}x')
                        li += 1
                        if li == 1:

                            break
                            
                    historico.clear()
                    
                    #try:
                    arquivo = open('velas.txt', 'w')
                    arquivo.write(str(historico2).replace("[","").replace("]",""))
                    arquivo.close()

                    processo = functions.atualiza_data_bot(82)
                    #except FileNotFoundError:
                    #print('impossível criar o arquivo')
                    #velas = dadosteste.get_velas()
                    #print(historico2)
                    #time.sleep(2)
                    
                    """with open("velas.txt", "r") as arquivo:
                        text = arquivo.read()
                    
                    historico2.clear()
                    for vela in text.split(','):
                        historico2.append(vela.lstrip().replace("'",""))"""
                    
                    for bot in lista_bots:
                        #INDECES BOT
                        #ID, Bot, IDEmpresa, IDChat, KeyBotApi, ArquivoTip
                        #0,   1,      2,        3,       4,         5
                        if entrada==False:
                            print(historico2)
                            entrada_metrica = metricas.get_metrica_3roxo(historico2)
                            
                            if entrada_metrica != 'atencao' and entrada_metrica != None:
                                
                                #Preciso apagar o atenção e enviar a entrada.
                                #estou enviando 
                                #try:
                                #Aqui se a variavel for maior que 0 significa que o sistema acabou de iniciar, não preciso mandar entrada.
                                retorno = telegram.delete(bot[4],bot[3],IDSendAlerta)
                                if retorno != None:
                                    gale = 0
                                    path_tip = f'Arquivos\\{bot[2]}\\entrada.tip'
                                    
                                    with open(path_tip, 'r') as arquivo:
                                        tip = arquivo.read()
                                        tip = tip.replace('@SEQ', str(velas4))
                                        #tip = tip.replace('@Sequencia', sequencia)
                                        #tip = tip.replace('@Mercado', mercado_entrada)
                                        #tip = tip.replace('@cod', str(metrica))
                                    for key, value in emojis.emojis.items():
                                        tip = tip.replace(key, value)
                                    
                                    retorno = telegram.send(bot[4],bot[3],tip, telegram.botoes)
                                    #print(retorno)
                                    
                                    idsend = retorno['result']['message_id']
                                    entrada = True
                                    atencao = False

                                    #AQUI SALVO A ENTRADA NO BANCO DE DADOS
                                    SQL = f"""INSERT INTO MR_Entradas (idbot,datahora,vela_saida,idmensage_telegram,finalizada,green)
                                                VALUES ({bot[0]},dateadd(hour, -3, getdate()), 1.50,{idsend},0,0)"""
                                    
                                    print(SQL)

                                    functions.put_save_db(SQL)
                                    
                                    #AQUI SELECIONO O ID DA ÚLTIMA TIP SALVA.
                                    SQL = f"""SELECT MAX(ID) FROM MR_Entradas WHERE idbot={bot[0]} 
                                    """
                                    cursor = functions.get_cursor(SQL)
                                    result_tips = cursor.fetchall()    
                                    for r_tip in result_tips:
                                        idtip = int(r_tip[0])
                                        
                                #except:
                                    #print('erro no processo de entrada...')

                            elif entrada_metrica == 'atencao':
                                #AQUI TENHO QUE ENVIAR UM ALERTA DE ENTRADA NO GRUPO.
                                print('Enviar atenção')
                                
                                path_tip = f'Arquivos\\{bot[2]}\\alerta.tip'
                                with open(path_tip, 'r') as arquivo:
                                    arq_alerta = arquivo.read()
                                    #tip = tip.replace('@cod', str(metrica))
                                for key, value in emojis.emojis.items():
                                    arq_alerta = arq_alerta.replace(key, value)
                                
                                #retorno = telegram.send(bot[4],bot[3],arq_alerta, telegram.botoes)
                                #IDSendAlerta = retorno['result']['message_id']
                                
                                
                                
                                atencao = True
                            
                            if atencao==True and entrada_metrica == None:
                                #não concretizou a entrada então preciso apagar o atenção.
                                retorno = telegram.delete(bot[4],bot[3],IDSendAlerta)
                                intSendGale=0
                                entrada = False
                                atencao = False
                        else:
                            for vela in historico2:
                                gale += 1
                                verify_green = gale -1
                                if verify_green <=2:
                                    if float(vela) >= 1.5:
                                        #FOI GREEN
                                        if gale >=2:
                                            retorno = telegram.delete(bot[4],bot[3],intSendGale)
                                            intSendGale=0
                                        
                                        path_tip = f'Arquivos\\{bot[2]}\\green.tip'
                                        with open(path_tip, 'r') as arquivo:
                                            arq_green = arquivo.read()
                                            arq_green = arq_green.replace('@SEQ', str(velas4))

                                        for key, value in emojis.emojis.items():
                                            arq_green = arq_green.replace(key, value)
                                        
                                        retorno=telegram.edit(bot[4],bot[3], idsend,arq_green, telegram.botoes)
                                        
                                        SQL = f"""UPDATE MR_Entradas SET finalizada=1, green=1 WHERE ID={idtip}
                                        """
                                        functions.put_save_db(SQL)

                                        entrada = False
                                        gale = 0
                                        break
                                    else:
                                        if gale >=2:
                                            print(f'intsendgale codigo delete: {intSendGale}')
                                            telegram.delete(bot[4],bot[3], intSendGale)
                                        
                                        if gale <= 2:
                                            path_tip = f'Arquivos\\{bot[2]}\\gale.tip'
                                            
                                            with open(path_tip, 'r') as arquivo:
                                                arq_gale = arquivo.read()
                                                arq_gale = arq_gale.replace('@gale', str(gale))
                                            for key, value in emojis.emojis.items():
                                                arq_gale = arq_gale.replace(key, value)
                                            
                                            retorno=telegram.send(bot[4],bot[3], arq_gale, telegram.botoes)
                                            intSendGale=retorno['result']['message_id']
                                            print(f'intsendgale: {intSendGale}')
                                            break
                                else:
                                    telegram.delete(bot[4],bot[3], intSendGale)
                                    path_tip = f'Arquivos\\{bot[2]}\\red.tip'
                                    with open(path_tip, 'r') as arquivo:
                                        arq_red = arquivo.read()
                                        arq_red = arq_red.replace('@SEQ', str(velas4))
                                    for key, value in emojis.emojis.items():
                                        arq_red = arq_red.replace(key, value)
                                    retorno=telegram.edit(bot[4],bot[3],idsend, arq_red, telegram.botoes)
                                    
                                    SQL = f"""UPDATE MR_Entradas SET finalizada=1, green=0 WHERE ID={idtip}
                                    """
                                    functions.put_save_db(SQL)

                                    entrada = False
                                    gale = 0
                                    break
                i = 0
                break
            
    #except Exception as e:
        #print(e)
        #Click Aviator
        #driver.find_element(By.XPATH, "/html/body/div[1]/div/main/nav/div/div[2]/div/div[1]/ul[1]/li[8]/div/div[1]/div/a[6]").click()
        #driver.get("https://mrjack.bet/aviator")
        #driver.find_element(By.XPATH, '/html/body/div[1]/div/main/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div[1]/button/img').click()
        #time.sleep(5)

reiniciando = restart()     







