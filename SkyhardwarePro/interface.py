#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *

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

Button(app, text="Enviar Dados").place(x=323, y=260, width=100, height=20)

app.mainloop()