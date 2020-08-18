#Esse script devolve a corrente média de um csv gerado a apartir do log de voo gerado pela pixhawk e obtido pela qGroundControl
def corrente_media_de_um_logPX4_csv(nome_do_arquivo_ponto_csv):
    import pandas as pd
    import numpy as np
    df = pd.read_csv(nome_do_arquivo_ponto_csv)
    print(df.head())
    correntes = df.iloc[:, 3].values
    print(correntes)
    #print(type(correntes))

    print("Corrente_media = " + str(np.mean(correntes))+ " A")


    
corrente_media_de_um_logPX4_csv('bateria.csv')
