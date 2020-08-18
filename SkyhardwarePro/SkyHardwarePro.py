#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tabulate import tabulate
import numpy as np
import pandas as pd
from pathlib import Path
import codecs
import urllib
import webbrowser


def caminho(nome):
    #Encontra o caminho do arquivo html
    diretorio = Path().absolute()
    cam = "file://" + str(diretorio) + "/" + nome
    
    caminho = cam

    return caminho


def readcsvAndSelect():
    #Essa funcao le os arquivos csv necessarios

    #Motores E Helicess

    df_mp = pd.read_csv('motoresEpropellers.csv')
    #print(df_mp.head())
    mp_data = df_mp.iloc[:,[0,5,6,7,10,11,12,13,14,15]].values
    # 0-Conjunto-0/5-PesoMotor-1/6-n_cell-2/7-propDiam-3/10-imin-4/11-imax-5/12-Empmin-6/13-Empmax-7/14-coef_ang-8/15-coef_lin-9
    #print(mp_data)
    mp_geral = df_mp.iloc[:,:].values

    #Baterias

    df_bat = pd.read_csv('BateriasLipoGrafenoCelulas34.csv')
    #print(df_bat.head())
    bat_data = df_bat.iloc[:,[0,2,3,4,5,9]].values
    # 0-Numeracao-0/2-TipoBat(0->lipo,1->graf)-1/3-mAh-2/4-Ncell-3/5-Crating-4/9-peso-5
    #print(bat_data)
    bat_geral = df_bat.iloc[:,:].values

    return mp_data , bat_data , mp_geral , bat_geral


def TEmedmax():
    #Essa funcao calcula a o percentual do empuxo máximo usado num voo padrão em média

    #Drone Padrão
    E_max = 850*4
    i_med_log = 10.179451722343641
    a = 138
    b = 0
    E_med_log = a*i_med_log + b
    TEmedmax = E_med_log/E_max
    return TEmedmax
   

def ordena_lista_pelo_tempo(lista_final):
    #ind=np.sort(lista_final[:,-1])
    ind=np.argsort(lista_final[:,-1])
    lista_ordenada =lista_final[ind]
    return lista_ordenada


def resultados(i_MH,j_Bat, mp_geral , bat_geral):
    #Essa funcao devolve uma lista dos parâmetros de interesse referentes a bateria, helice e motor para mostrar ao usuário final
    #Motores: Tipo , Nome_motor , Marca, kv ,n_celuas , peso
    motorSel  = [mp_geral[i_MH][1],mp_geral[i_MH][2],mp_geral[i_MH][3],mp_geral[i_MH][4],mp_geral[i_MH][6],mp_geral[i_MH][5]]

    def propeller(i_MH,mp_geral):
        #Essa funcao retorna o nome do propeller
        #Diametro da helice
        if mp_geral[i_MH][7] < 10:
           prop_diam = str(int(mp_geral[i_MH][7]*10))
        else:
           prop_diam = str(int(mp_geral[i_MH][7]))
        prop_diam = prop_diam[0] + prop_diam[1]
        #Pitch da helice
        if int(mp_geral[i_MH][8][0]) < 10:
           prop_pitch = str(int(mp_geral[i_MH][8][0])*10)
        else:
           prop_pitch = str(int(mp_geral[i_MH][8][0]))
        prop_pitch = prop_pitch[0] + prop_pitch[1]

        prop_name = prop_diam + prop_pitch
        return prop_name

    propSel = [propeller(i_MH,mp_geral)]
    
    def type_bat(j_Bat,bat_geral):

        if bat_geral[j_Bat][2] == 0:
            tipo = 'Lipo'
        else:
            tipo = 'Grafeno'

        return tipo


    #Bateria: Marca,Lipo/grafeno,mAh,n_celulas,C,Peso
    batSel = [bat_geral[j_Bat][1] , type_bat(j_Bat,bat_geral) , bat_geral[j_Bat][3] , bat_geral[j_Bat][4] , bat_geral[j_Bat][5] , bat_geral[j_Bat][6]]

    resultado = [motorSel[0],motorSel[1],motorSel[2],motorSel[3],motorSel[4],motorSel[5],propSel[0],batSel[0],batSel[1],batSel[2],batSel[3],batSel[4],batSel[5]]
    return resultado


def Tempo_de_voo():
    #Constantes
    Phelicepadrao = 12 #peso médio de uma helice em g
    
    #Dados do Usuário
    Pframe = vpeso.get()
    Tep = vempuxo.get()
    prop_diam_max = vtamanho.get()

    #Casting
    Pframe = float(Pframe)
    Tep = float(Tep)
    prop_diam_max = float(prop_diam_max)

    #Dados arquivos CSV
    mp_data , bat_data , mp_geral , bat_geral = readcsvAndSelect()

    #Contas
    list_bat_mot_prop = []
    for i in range(len(mp_data)):
        for j in range(len(bat_data)):
            if int(mp_data[i][2]) == int(bat_data[j][3]): #Se o numero de celulas da bateria for compatível com aquele motor
                if mp_data[i][3] <= prop_diam_max : #Se o prop_diam <= prop_diam_maximo
                    Pdrone = Pframe + 4*(mp_data[i][1]+Phelicepadrao) + bat_data[j][5] 
                    E_maxN = Pdrone*Tep
                    if E_maxN <= 4*mp_data[i][7] : #Se o empuxo maximo calculado for menor do que aquele que so 4 motores podm fornecer
                        E_medN = TEmedmax()*E_maxN

                        i_medN = (1/mp_data[i][8])*E_medN - (mp_data[i][9]/mp_data[i][8])
                        #O calculo da corrnete maxima da bateria esta certo
                        if (i_medN/4 <= mp_data[i][5]) and (i_medN <= bat_data[j][2]*bat_data[j][4]/1000) : 
                            #Se a corrente media for menor que a maxima corrente que o motor fornece e que a bateria fornece
                            # i_max_bateria = mAh*C/1000
                            T_voo = ((bat_data[j][2]/1000)/i_medN)*60 #tempo de voo em (60min/1h)*(mAh/1000)/A [minutos]
                            #Lista com o conjunto a ser comprado e autonomia associada [(num_motor&prop),num_bateria,Tempo_de_voo]
                            r = resultados(int(mp_data[i][0])-1,int(bat_data[j][0])-1, mp_geral , bat_geral)

                            list_bat_mot_prop.append([r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9],r[10],r[11],r[12],T_voo]) 
    if len(list_bat_mot_prop) != 0:
        lista_final = np.array(list_bat_mot_prop)
        lista_fina_ordenada = ordena_lista_pelo_tempo(lista_final)

        df = pd.DataFrame(data=lista_fina_ordenada, columns=["MotorType","MotorName","Company","KV","N_cells","MotorWeight","Propeller","BatteryCompany","BatteryType","Charge[mAh]","N_cells","C","BatteryWeight","Autonomy[min]"])
        with pd.option_context('display.max_rows', None, 'display.max_columns', None): 
            pd.options.display.width=None # more options can be specified also
            pdtabulate=lambda df:tabulate(df,headers='keys',tablefmt='psql')
            #print(pdtabulate(df))

            #render dataframe as html
            html = df.to_html()

            #write html to file
            text_file = open("SkyHardwarePro_results.html", "w")
            text_file.write(html)
        

            #file = codecs.open("SkyHardwarePro_results.html", "r", "utf-8")
            #print(file.read())

            #page =  urllib.urlopen('SkyHardwarePro_results.html').read()
            #print(page)
            caminho1 = caminho("SkyHardwarePro_results.html")
            url = caminho1
            webbrowser.open(url, new=2)

            text_file.close()
    else:
        #write html msg in html language
        html1_str = """
        <html>
            <body>
                <p> Suas especificações Não Geraram nenhum resultado possíve considerando-se motores, helices e Baterias disponíveis. <p>
                <p> Possíveis Causas: <p>
                <p> 1) Peso do Frame muito elevado <p>
                <p> 2) Peso de eletrônicos muito elevado (embutido no peso do frame escolhido) <p>
                <p> 3) Escolha de tamanho máximo da helice muito pequeno <p>
                <p> 4) Escolha de um Trhust-to-weight_ratio muito elevado <p>
            </body>
        </html>
        """
        


        html_file = open("ErrorMsg.html", "w")
        html_file.write(html1_str)
        html_file.close()
    

        #file = codecs.open("SkyHardwarePro_results.html", "r", "utf-8")
        #print(file.read())

        #page =  urllib.urlopen('SkyHardwarePro_results.html').read()
        #print(page)
        caminho2 = caminho("ErrorMsg.html")
        urlERROR = caminho2
        webbrowser.open(urlERROR, new=2)

        html_file.close()   

app= Tk()
app.title("SkyHardwarePro")
app.geometry("800x300")
app.configure(background="#dde")

img = PhotoImage(file="Logo.png")
imagem = Label(app, image=img, background="#dde").place(x=565, y=-19)

Label(app, text="SkyHardwarePro", background="#dde", foreground="black", font="impact 20 bold", anchor=W).place(x=10, y=60)

Label(app, text="By Skyrats Autonomous Drone Team ", background="#dde", foreground="black", anchor=W).place(x=10, y=98)

Label(app, text="Peso do frame e componentes eletrônicos (exceto Motor,Helice e Bateira) em gramas: ", background="#dde", foreground="black", anchor=W).place(x=10, y=160)
vpeso=Entry(app)
vpeso.place(x=583, y=160, width=200, height=20)

Label(app, text="Ensira o Thrust to weight ratio (Taxa empuxo peso) desejada: ", background="#dde", foreground="black", anchor=W).place(x=10, y=190)
vempuxo=Entry(app)
vempuxo.place(x=420, y=190, width=200, height=20)

Label(app, text="Tamanho maximo do diâmetro do propeller em polegadas: ", background="#dde", foreground="black", anchor=W).place(x=10, y=220)
vtamanho=Entry(app)
vtamanho.place(x=405, y=220, width=200, height=20)

Button(app, text="Enviar Dados", command=Tempo_de_voo).place(x=323, y=260, width=100, height=20)

app.mainloop()

