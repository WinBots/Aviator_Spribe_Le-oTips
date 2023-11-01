def get_key(getkey):
    for key, value in emojis.items():
        if key == getkey:
            return value
    
    return "key doesn't exist"

emojis = {
    "@robo":"\U0001F916", #🤖
    "@trofeu":"\U0001f3c6", #🏆
    "@red_exclamacao":"\U00002757", #❗
    "@atencao":"\U000026a0\U0000fe0f", #⚠️
    "@medalha_militar":"\U0001f396\U0000fe0f", #🎖️
    "@bola_futebol":"\U000026bd", #⚽ 
    "@relogio_alarme":"\U000023f0", #⏰
    "@alvo":"\U0001f3af", #🎯
    "@bolsa_dinheiro":"\U0001f4b0", #💰
    "@notebook":"\U0001f4bb", #💻
    "@cemaforo_vertical":"\U0001f6a6", #🚦
    "@check_green":"\U00002705", #✅
    "@x_red":"\U0000274c", #❌
    "@umaemeia":"\U0001f55c", #🕜
    "@abobora":"\U0001f383", #🎃
    "@coroa":"\U0001f451", #👑
    "@blue_circle":"\U0001f535", #🔵
    "@aviao":"\U00002708\U0000fe0f", #✈️
    "@right":"\U000027a1\U0000fe0f" #➡️
}