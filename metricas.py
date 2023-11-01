#metricas 4 vela roxa
def get_metrica_3roxo(historico2):
    roxo = 0
    count_ind = 0

    for vela in historico2:
        count_ind += 1
        intvela = float(vela)
        #if intvela >= 2 and intvela < 10:
        #if intvela >= 1.5 and intvela < 10000:
        if intvela >= 2 and intvela < 10:
            roxo += 1
            if roxo == 3:
                print('Entrar')
                return 'Entrar'

        else:
            if roxo == 2:
                return 'atencao'
            elif roxo <=3:
                roxo = 0
                return None 

#metrica 2 rosa + 2 azuis
def get_metrica_2rosa_2azul(historico2):
    rosa = 0
    azul = 0
    roxo = 0

    for vela in historico2:
        intvela = float(vela)

        if intvela < 2:
            azul += 1
        elif intvela >= 10:
            rosa += 1
        elif intvela >= 2 and intvela < 10:
            roxo = 1 
        if azul == 2 and rosa == 2:
            print('Entrar')
            return 'Entrar'
        
        else:
            if azul == 1 and rosa == 2:
                return 'atencao'
            elif azul < 1 or azul > 2 or roxo == 1:
                rosa = 0
                azul = 0
                roxo = 0
                return None