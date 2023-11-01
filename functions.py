import json
import time
from datetime import datetime
from configparser import ConfigParser, ExtendedInterpolation
import pyodbc
import functions
import telegram
import emojis
import psutil

config = ConfigParser()
config.read("config.conf")

#defino cores para o terminal
red = '\033[1;31m'
green = '\033[32m'
blue = '\033[94m'
color_off = '\033[0;0m'

#crio a conexão com o banco de dados
try:
    server = config.get('base','server') 
    database = config.get('base','database')
    username = config.get('base','username')
    password = config.get('base','password')
    
    #VOU TENTAR CONECTAR AO BANCO DE DADOS 
    try: 
        string_conection = 'Driver={SQL Server};Server='+server+';Database='+database+';UID='+username+';PWD='+password
        print(string_conection)
        cnn = pyodbc.connect(string_conection)
        cursor = cnn.cursor()
        print(f'{green}conexão estabelecida com sucesso{color_off}')
    except:
        print(f"{red}erro ao conectar na base de dados.{color_off}")

except:
    print(f"{red}Chave de configuração não encontrada{color_off}")


def put_save_db(SQL):
    try:
        cursor.execute(SQL)
        cursor.commit()
    except Exception as e:
        print(e)
        print(SQL)
        return e
    
    return 'done'

def get_cursor(SQL):
    try:
        
        cursor.execute(SQL)
        return cursor
    except Exception as e:
        print(f'{functions.red}{e}{functions.color_off}')
        return None

def get_bots(IDEmpresa,idbot):
    
    SQL = f"""
        select ID, Bot, IDEmpresa, IDChat, KeyBotApi, ArquivoTip 
            from Bots 
                WHERE IDEmpresa={IDEmpresa}
                AND IDMercado=5 
                AND (BotPaused=0 and Ativo=1)
        """
    cursor_bots = functions.get_cursor(SQL)
    
    return cursor_bots

def process_appointments(bot):
    
    #aqui, processo todas as marcaçoes automaticas do bot.
    green = False
    count_gales = 0 
    retorno = ''
    try:
        
        idbot = bot
                
        SQL = f"""SELECT tips.ID, tips.idbot, idmensage_send, minutos,
                cast(datepart(minute, j1.data) as varchar(2)) + '-' + j1.placar_ft as jogo1,  
                cast(datepart(minute, j2.data) as varchar(2)) + '-' + j2.placar_ft as jogo2,  
                cast(datepart(minute, j3.data) as varchar(2)) + '-' + j3.placar_ft as jogo3,
                mercado, idmetrica  
            FROM (
                SELECT idbot, id, IDMensage_send, minutos, 
                    datahora_primeiro_tiro as primeiro_tiro, 
                    dateadd(minute, 3, datahora_primeiro_tiro) as segundo_tiro, 
                    dateadd(minute, 6, datahora_primeiro_tiro) as terceiro_tiro,
                    mercado, idmetrica 
                FROM PX_Tips 
                Where idbot={idbot} AND finalizada = 0) tips
                INNER JOIN PX_jogos j1 on tips.primeiro_tiro = j1.data
                INNER JOIN PX_jogos j2 on tips.segundo_tiro = j2.data
                INNER JOIN PX_jogos j3 on tips.terceiro_tiro = j3.data
            ORDER BY tips.primeiro_tiro"""
        
        #print(SQL)

        cursor = functions.get_cursor(SQL)
        tips = cursor.fetchall()
    
    except Exception as e:
        print(f'Erro...{e}')
        return None
    
    for tip in tips:
        count_gales = 0
        retorno = ''
        str_marcacao = ''
        green = False

        print(tip)
        for i in range(3):
            colum = 4+i
            print(tip[colum])

            if tip[colum] != None:
                minuto_placar = str(tip[colum]).split("-")
                minuto = minuto_placar[0]
                placar = str(minuto_placar[1]).split(':')
                placar_casa = placar[0]
                placar_visitante = placar[1]
                mercado = tip[7]
                
                if mercado == 'ambas':
                    if int(placar_casa) > 0 and int(placar_visitante) > 0:
                        #ambas marcam
                        str_marcacao = str(tip[3]).replace(minuto, minuto + emojis.get_key('@check_green'))
                        green = True
                        break
                    else:
                        green=False
                        str_marcacao = str(tip[3])
                elif mercado == 'o25':
                    #Over 2.5
                    if int(placar_casa) + int(placar_visitante) > 2:
                        str_marcacao = str(tip[3]).replace(minuto, minuto + emojis.get_key('@check_green'))
                        green = True
                        break
                    else:
                        green=False
                        str_marcacao = str(tip[3])
                count_gales += 1
        if green == True:
            retorno = telegram.editMensagem(int(tip[0]), bot, 1, tip[2], str_marcacao,tip[7], bot, tip[8]) 
        elif green == False and count_gales == 3:
            retorno = telegram.editMensagem(int(tip[0]), bot, 0, tip[2], str(tip[3]),tip[7], bot, tip[8])  
      
    return retorno

def verifica_minuto_tip(minuto, idbot, mercado):
    
    try:
        SQL = f"""SELECT replace(minutos,' ',':') as minutos, datahora_primeiro_tiro FROM PX_Tips 
                    WHERE datahora_primeiro_tiro between dateadd(minute, -220, Format(getdate(), N'yyyy-MM-dd HH:mm')) AND getdate()
                        AND idbot={idbot}
                        AND mercado = '{mercado}'
        """
        cursor = functions.get_cursor(SQL)
        tips = cursor.fetchall()
        
        for tip in tips:
            minutos = str(tip[0]).split(":")
            for set_minuto in minutos:
                if int(set_minuto) == minuto:
                    #significa que este minuto já foi usado em uma tip anterior desse bot em menos de uma hora 
                    return False
        
        return True
    except:
        return False

def get_bottuns(idempresa):

    if idempresa == 10:
        #exterminador
        caption_botao2 = "Acesso Playpix"
        url_botao2 = "https://sshortly1.com/kPwZGc"
    elif idempresa == 4: 
        caption_botao2 = "Cadastre-se"
        url_botao2 = "https://playpix.com/affiliates/?btag=987573_l169856"
    elif idempresa == 16:    
        caption_botao2 = "Cadastre-se"
        url_botao2 = "https://sshortly1.com/AOg2Ye"
    else:
        caption_botao2 = "Cadastre-se"
        url_botao2 = "https://playpix.com/affiliates/?btag=987573_l169856"

    emoji_botão = emojis.get_key('@blue_circle')
    
    botaoes = {
        "inline_keyboard":[
        [
        {
        "text": f'{emoji_botão}Fazer entrada',
        "url":"https://www.playpix.com/pt/virtual-sports/betconstruct?game=1"
        },
        {
        "text":caption_botao2,
        "url":url_botao2
        }
        ]
        ]
    }
    
    return botaoes

def verify_browser_open():
    for proc in psutil.process_iter(['pid', 'name']):
        if 'chrome' in proc.info['name'].lower():
            return True
    return False

def atualiza_data_bot(idbot):
    try:
        SQL = f"""
            UPDATE Bots SET Processo=dateadd(hour,-3,getdate()) WHERE ID={idbot}""" 
        put_save_db(SQL)
        return 'done'
    except Exception as e:
        return e