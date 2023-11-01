from pyrogram import Client
import json

class set_client:
    def __init__(self, token, chat_id, api_hash, api_id):
        self.token = token
        self.chat_id = chat_id
        self.api_hash = api_hash
        self.api_id = api_id
    
    def send(self, chat_id, text):
        with Client('SUPORTE', self.api_id, self.api_hash, self.token) as app:
            retorno = app.send_message(chat_id, text, disable_web_page_preview=True)
            # Acessa o ID da mensagem enviada
            conteudo = json.loads(str(retorno))
            return conteudo
 
    def edit(self, chat_id, message_id, new_text):
        with Client('SUPORTE', self.api_id, self.api_hash, self.token) as app:
            app.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=new_text
            )

    def delete(self, chat_id, message_id):
        with Client('SUPORTE', self.api_id, self.api_hash, self.token) as app:
            app.delete_messages(chat_id, message_id)


