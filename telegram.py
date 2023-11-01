import json
import requests
import emojis

import asyncio


parse_mode='Markdown'
def send(api_key, id_chat, texto, botoes):
    data = {
            "chat_id": id_chat,
            "text": f'{str(texto)}',
            "parse_mode": parse_mode,
            "reply_markup": json.dumps(botoes)
        }
    retorno = requests.get(url="https://api.telegram.org/bot"+api_key+"/sendMessage",data=data).json()
    return retorno

def edit(api_key, id_chat, id_mensage, texto, botoes):
        
    data = {
            "chat_id": id_chat,
            "message_id": id_mensage,
            "text": f'{str(texto)}',
            "parse_mode": parse_mode,
            "reply_markup": json.dumps(botoes)
        }
    retorno = requests.post(url="https://api.telegram.org/bot"+api_key+"/editMessageText",data=data).json()
    return retorno

def delete(api_key, id_chat, id_mensage):
    try:
        data = {
                "message_id": id_mensage,
                "chat_id": id_chat
            }
        
        retorno = requests.post(url="https://api.telegram.org/bot"+api_key+"/deleteMessage",data=data).json()
        return retorno
    except:
        return None
    
    
emoji_aviao = emojis.get_key('@aviao')

botoes = {
        'inline_keyboard':[
        [
        {
        "text":f"{emoji_aviao}Fazer entrada",
        "url":"https://mrjack.bet?p=leaotips"
        }
        ]
        ]
    }