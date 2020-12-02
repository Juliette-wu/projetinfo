#!/usr/bin/env python

#Pojet Info
"Mesurer les similarités"

from math import *
from matplotlib.pyplot import *
from numpy import *
from datetime import datetime
from sys import argv

def tab_capteurs():
    T1,T2,T3,T4,T5,T6=[],[],[],[],[],[]   #tableaux corespondant aux 6 capteurs
    E=open('EIVP_KM.csv','r')
    next(E)
    for ligne in E:
        l=ligne.split(';')  #l correspond à une ligne du tableau
        l[1]=int(l[1])
        for k in range(2,5):
            l[k]=float(l[k])
        for k in range(5,7):
            l[k]=int(l[k])   
        l[7]=l[7].strip()
        if l[1]==1:
            T1.append(l[2:])
        if l[1]==2:
            T2.append(l[2:])
        if l[1]==3:
            T3.append(l[2:])
        if l[1]==4:
            T4.append(l[2:])
        if l[1]==5:
            T5.append(l[2:])
        else:
            T6.append(l[2:])
    E.close()
    return(T1,T2,T3,T4,T5,T6)

def courbe_simple(X,Y,a,b):
    f=figure()
    ax = f.add_subplot(111)
    plot(X,Y)
    xlabel(a)
    ylabel(b)
    xticks(X[::50],rotation=-85)
    show()

def tri(L): #tri rapide
    if len(L)<=1:
        return(L)
    p=L[0]
    A,B=[],[]
    for i in range(1,len(L)):
        if L[i]<p:
            A.append(L[i])
        else:
            B.append(L[i])
    return(tri(A)+[p]+tri(B))
                          
def valeurs_stats(L):
    n=len(L)
    m,M,S,D=L[0],L[0],L[0],L[0]**2
    for k in range(1,n):
        if L[k]<m:
            m=L[k]
        if L[k]>M:
            M=L[k]
        S=S+L[k]
        D=D+L[k]**2
    E=S/n
    V=D/n-E**2
    O=sqrt(V)
    X=tri(L)
    if n%2==0:
        Z=(X[int(n/2)-1]+X[int(n/2)])/2
    else:
        Z=X[int(n/2)]
    E=round(E,2)
    O=round(O,2)
    return(m,M,E,O,Z)
    print('minimum :',m)
    print('maximum :',M)
    print('moyenne :',E)
    print('écart-type :',O)
    print('médiane :',Z)
    
def courbe_simple_stats(X,Y,a,b):
    m,M,E,O,Z=valeurs_stats(Y)
    m,M,E,O,Z=str(m),str(M),str(E),str(O),str(Z)
    f=figure()
    ax = f.add_subplot(111)
    text(0.87,0.87,'minimum : '+m+'\n'+'maximum : '+M+'\n'+'moyenne : '+E+'\n'+'écart-type : '+O+'\n'+'médiane : '+Z,horizontalalignment='center',verticalalignment='center',transform=ax.transAxes)
    plot(X,Y)
    xlabel(a)
    ylabel(b)
    xticks(X[::50],rotation=-85)
    show()
   
def corrélation(L,P):
    n,S,S_L,S_P,D_L,D_P=len(L),0,0,0,0,0
    for k in range(n):
        S=S+L[k]*P[k]
        S_L=S_L+L[k]
        D_L=D_L+L[k]**2
        S_P=S_P+P[k]
        D_P=D_P+P[k]**2
    E=S/n
    E_L=S_L/n
    O_L=sqrt(D_L/n-E_L**2)
    E_P=S_P/n
    O_P=sqrt(D_P/n-E_P**2)
    return(round((E-(E_L*E_P))/(O_L*O_P),2))

def humidex(T,H):
    n=len(T)
    h=[]
    for i in range(n):
        h.append(round(T[i]+(5/9)*(6.112*10**(7.5*(T[i]/(237.7+T[i])))*(H[i]/100)-10)))
    return(h)    

def graph_corrélation(X,L,P,a,l,p):
    c=corrélation(L,P)
    c=str(c)
    f=figure()
    ax = f.add_subplot(111)
    text(0.75,0.95,'corrélation : '+c,transform=ax.transAxes)
    plot(X,L,label=l)
    plot(X,P,label=p)
    legend(loc = 'upper left')
    xlabel(a)
    title('Corrélation')
    xticks(X[::50],rotation=-85)
    show()

def dt(t): #extrait la date sous format utilisable pour faire des comparaisons
    a,m,j=int(t[0:4]),int(t[5:7]),int(t[8:10])
    h,mi,s=int(t[11:13]),int(t[14:16]),int(t[17:19])
    return(datetime(a,m,j,h,mi,s))

def limitation_temps(C,td,tf):
    T,i=[],0
    while dt(C[i][5])<tf:
        while dt(C[i][5])<=td:
            i=i+1
        T.append(C[i])
        i=i+1
    return(T)

def limitation_temps_totale(td,tf): #td : date du début / tf : date de fin
    C1,C2,C3,C4,C5,C6=tab_capteurs()
    return(limitation_temps(C1,td,tf),limitation_temps(C2,td,tf),limitation_temps(C3,td,tf),limitation_temps(C4,td,tf),limitation_temps(C5,td,tf),limitation_temps(C6,td,tf))    

def séparation(C,n):
    B,T,H,L,D=[],[],[],[],[]
    for i in range(n):
        B.append(C[i][0])
        T.append(C[i][1])
        H.append(C[i][2])
        L.append(C[i][3])
        D.append(C[i][4])
    return(B,T,H,L,D)

def graph(X,L,titre):
    c12=corrélation(L[0],L[1])
    c12=str(c12)
    c13=corrélation(L[0],L[2])
    c13=str(c13)
    c14=corrélation(L[0],L[3])
    c14=str(c14)
    c15=corrélation(L[0],L[4])
    c15=str(c15)
    c16=corrélation(L[0],L[5])
    c16=str(c16)
    c23=corrélation(L[1],L[2])
    c23=str(c23)
    c24=corrélation(L[1],L[3])
    c24=str(c24)
    c25=corrélation(L[1],L[4])
    c25=str(c25)
    c26=corrélation(L[1],L[5])
    c26=str(c26)
    c34=corrélation(L[2],L[3])
    c34=str(c34)
    c35=corrélation(L[2],L[4])
    c35=str(c35)
    c36=corrélation(L[2],L[5])
    c36=str(c36)
    c45=corrélation(L[3],L[4])
    c45=str(c45)
    c46=corrélation(L[3],L[5])
    c46=str(c46)
    c56=corrélation(L[4],L[5])
    c56=str(c56)
    f=figure(figsize=(20,6), dpi=80)
    ax = f.add_subplot(111)
    text(0.22,0.97,'c12 : '+c12+'; c13 : '+c13+'; c14 : '+c14+'; c15 : '+c15+'; c16 : '+c16+'; c23 : '+c23+'; c24 : '+c24+'; c25 : '+c25+'; c26 : '+c26+'; c34 : '+c34+'; c35 : '+c35+'; c36 : '+c36+'; c45 : '+c45+'; c46 : '+c46+'; c56 : '+c56,transform=ax.transAxes)
    plot(X,L[0],label='Capteur 1')
    plot(X,L[1],label='Capteur 2')
    plot(X,L[2],label='Capteur 3')
    plot(X,L[3],label='Capteur 4')
    plot(X,L[4],label='Capteur 5')
    plot(X,L[5],label='Capteur 6')
    legend(loc = 'upper left')
    xlabel('temps')
    title('Similarité '+titre)
    xticks(X[::50],rotation=-85)

def mesure_similarités(td,tf):
    C1,C2,C3,C4,C5,C6=limitation_temps_totale(td,tf)
    n1=len(C1)
    n2=len(C2)
    n3=len(C3)
    n4=len(C4)
    n5=len(C5)
    n6=len(C6)
    print('nombre de valeurs pour chaque capteur entre '+str(td)+' et '+str(tf)+' :')
    print('Capteur 1 : '+str(n1))
    print('Capteur 2 : '+str(n2))
    print('Capteur 3 : '+str(n3))
    print('Capteur 4 : '+str(n4))
    print('Capteur 5 : '+str(n5))
    print('Capteur 6 : '+str(n6))
    n=min([n1,n2,n3,n4,n5,n6])
    X=[]
    for i in range(n):
        x=C1[i][5] #choix arbitraire de C1
        X.append(x[5:19])
    B1,T1,H1,L1,D1=séparation(C1,n)
    B2,T2,H2,L2,D2=séparation(C2,n)
    B3,T3,H3,L3,D3=séparation(C3,n)
    B4,T4,H4,L4,D4=séparation(C4,n)
    B5,T5,H5,L5,D5=séparation(C5,n)
    B6,T6,H6,L6,D6=séparation(C6,n)
    # Bruit :
    graph(X,[B1,B2,B3,B4,B5,B6],'du niveau sonore en dBA')
    # Température :
    graph(X,[T1,T2,T3,T4,T5,T6],'de la température en °C')
    #Humidité :
    graph(X,[H1,H2,H3,H4,H5,H6],"de l'humidité relative en %")
    #Humidex ;
    U=[humidex(T1,H1),humidex(T2,H2),humidex(T3,H3),humidex(T4,H4),humidex(T5,H5),humidex(T6,H6)]
    graph(X,U,"de l'indice humidex")
    #Luminosité :
    graph(X,[L1,L2,L3,L4,L5,L6],'du niveau lumineux en lux')
    #CO2 :
    graph(X,[D1,D2,D3,D4,D5,D6],'de la quantité de CO2 en ppm')
    show()

if argv[1]=='display':
    C1,C2,C3,C4,C5,C6=limitation_temps_totale(dt(argv[4]),dt(argv[5]))
    X,Y=[],[]
    if argv[2]=='capteur1':
        n=len(C1)
        for k in range(n):
            X.append(C1[k][5])
        B,T,H,L,D=séparation(C1,n)
        if argv[3]=='noise':
            Y=B
            y='noise'
        if argv[3]=='temp':
            Y=T
            y='temp'
        if argv[3]=='humidity':
            Y=H
            y='humidity'
        if argv[3]=='lum':
            Y=L
            y='lum'
        if argv[3]=='co2':
            Y=D
            y='co2'
        if argv[3]=='humidex':
            Y=humidex(T,H)
            y='humidex'
    if argv[2]=='capteur2':
        n=len(C2)
        for k in range(n):
            X.append(C2[k][5])
        B,T,H,L,D=séparation(C2,n)
        if argv[3]=='noise':
            Y=B
            y='noise'
        if argv[3]=='temp':
            Y=T
            y='temp'
        if argv[3]=='humidity':
            Y=H
            y='humidity'
        if argv[3]=='lum':
            Y=L
            y='lum'
        if argv[3]=='co2':
            Y=D
            y='co2'
        if argv[3]=='humidex':
            Y=humidex(T,H)
            y='humidex'
    if argv[2]=='capteur3':
        n=len(C3)
        for k in range(n):
            X.append(C3[k][5])
        B,T,H,L,D=séparation(C3,n)
        if argv[3]=='noise':
            Y=B
            y='noise'
        if argv[3]=='temp':
            Y=T
            y='temp'
        if argv[3]=='humidity':
            Y=H
            y='humidity'
        if argv[3]=='lum':
            Y=L
            y='lum'
        if argv[3]=='co2':
            Y=D
            y='co2'
        if argv[3]=='humidex':
            Y=humidex(T,H)
            y='humidex'
    if argv[2]=='capteur4':
        n=len(C4)
        for k in range(n):
            X.append(C4[k][5])
        B,T,H,L,D=séparation(C4,n)
        if argv[3]=='noise':
            Y=B
            y='noise'
        if argv[3]=='temp':
            Y=T
            y='temp'
        if argv[3]=='humidity':
            Y=H
            y='humidity'
        if argv[3]=='lum':
            Y=L
            y='lum'
        if argv[3]=='co2':
            Y=D
            y='co2'
        if argv[3]=='humidex':
            Y=humidex(T,H)
            y='humidex'
    if argv[2]=='capteur5':
        n=len(C5)
        for k in range(n):
            X.append(C5[k][5])
        B,T,H,L,D=séparation(C5,n)
        if argv[3]=='noise':
            Y=B
            y='noise'
        if argv[3]=='temp':
            Y=T
            y='temp'
        if argv[3]=='humidity':
            Y=H
            y='humidity'
        if argv[3]=='lum':
            Y=L
            y='lum'
        if argv[3]=='co2':
            Y=D
            y='co2'
        if argv[3]=='humidex':
            Y=humidex(T,H)
            y='humidex'
    if argv[2]=='capteur6':
        n=len(C6)
        for k in range(n):
            X.append(C6[k][5])
        B,T,H,L,D=séparation(C6,n)
        if argv[3]=='noise':
            Y=B
            y='noise'
        if argv[3]=='temp':
            Y=T
            y='temp'
        if argv[3]=='humidity':
            Y=H
            y='humidity'
        if argv[3]=='lum':
            Y=L
            y='lum'
        if argv[3]=='co2':
            Y=D
            y='co2'
        if argv[3]=='humidex':
            Y=humidex(T,H)
            y='humidex'
    courbe_simple(X,Y,'temps',y)

if argv[1]=='displayStat':
    C1,C2,C3,C4,C5,C6=limitation_temps_totale(dt(argv[4]),dt(argv[5]))
    X,Y=[],[]
    if argv[2]=='capteur1':
        n=len(C1)
        for k in range(n):
            X.append(C1[k][5])
        B,T,H,L,D=séparation(C1,n)
        if argv[3]=='noise':
            Y=B
            y='noise'
        if argv[3]=='temp':
            Y=T
            y='temp'
        if argv[3]=='humidity':
            Y=H
            y='humidity'
        if argv[3]=='lum':
            Y=L
            y='lum'
        if argv[3]=='co2':
            Y=D
            y='co2'
        if argv[3]=='humidex':
            Y=humidex(T,H)
            y='humidex'
    if argv[2]=='capteur2':
        n=len(C2)
        for k in range(n):
            X.append(C2[k][5])
        B,T,H,L,D=séparation(C2,n)
        if argv[3]=='noise':
            Y=B
            y='noise'
        if argv[3]=='temp':
            Y=T
            y='temp'
        if argv[3]=='humidity':
            Y=H
            y='humidity'
        if argv[3]=='lum':
            Y=L
            y='lum'
        if argv[3]=='co2':
            Y=D
            y='co2'
        if argv[3]=='humidex':
            Y=humidex(T,H)
            y='humidex'
    if argv[2]=='capteur3':
        n=len(C3)
        for k in range(n):
            X.append(C3[k][5])
        B,T,H,L,D=séparation(C3,n)
        if argv[3]=='noise':
            Y=B
            y='noise'
        if argv[3]=='temp':
            Y=T
            y='temp'
        if argv[3]=='humidity':
            Y=H
            y='humidity'
        if argv[3]=='lum':
            Y=L
            y='lum'
        if argv[3]=='co2':
            Y=D
            y='co2'
        if argv[3]=='humidex':
            Y=humidex(T,H)
            y='humidex'
    if argv[2]=='capteur4':
        n=len(C4)
        for k in range(n):
            X.append(C4[k][5])
        B,T,H,L,D=séparation(C4,n)
        if argv[3]=='noise':
            Y=B
            y='noise'
        if argv[3]=='temp':
            Y=T
            y='temp'
        if argv[3]=='humidity':
            Y=H
            y='humidity'
        if argv[3]=='lum':
            Y=L
            y='lum'
        if argv[3]=='co2':
            Y=D
            y='co2'
        if argv[3]=='humidex':
            Y=humidex(T,H)
            y='humidex'
    if argv[2]=='capteur5':
        n=len(C5)
        for k in range(n):
            X.append(C5[k][5])
        B,T,H,L,D=séparation(C5,n)
        if argv[3]=='noise':
            Y=B
            y='noise'
        if argv[3]=='temp':
            Y=T
            y='temp'
        if argv[3]=='humidity':
            Y=H
            y='humidity'
        if argv[3]=='lum':
            Y=L
            y='lum'
        if argv[3]=='co2':
            Y=D
            y='co2'
        if argv[3]=='humidex':
            Y=humidex(T,H)
            y='humidex'
    if argv[2]=='capteur6':
        n=len(C6)
        for k in range(n):
            X.append(C6[k][5])
        B,T,H,L,D=séparation(C6,n)
        if argv[3]=='noise':
            Y=B
            y='noise'
        if argv[3]=='temp':
            Y=T
            y='temp'
        if argv[3]=='humidity':
            Y=H
            y='humidity'
        if argv[3]=='lum':
            Y=L
            y='lum'
        if argv[3]=='co2':
            Y=D
            y='co2'
        if argv[3]=='humidex':
            Y=humidex(T,H)
            y='humidex'
    courbe_simple_stats(X,Y,'temps',y)

if argv[1]=='corrélation':
    C1,C2,C3,C4,C5,C6=limitation_temps_totale(dt(argv[5]),dt(argv[6]))
    X=[]
    n1=len(C1)
    n2=len(C2)
    n3=len(C3)
    n4=len(C4)
    n5=len(C5)
    n6=len(C6)
    n=min([n1,n2,n3,n4,n5,n6])
    for i in range(n):
        x=C1[i][5] #choix arbitraire de C1
        X.append(x[5:19])
    B1,T1,H1,L1,D1=séparation(C1,n)
    B2,T2,H2,L2,D2=séparation(C2,n)
    B3,T3,H3,L3,D3=séparation(C3,n)
    B4,T4,H4,L4,D4=séparation(C4,n)
    B5,T5,H5,L5,D5=séparation(C5,n)
    B6,T6,H6,L6,D6=séparation(C6,n)
    B=[B1,B2,B3,B4,B5,B6]
    T=[T1,T2,T3,T4,T5,T6]
    H=[H1,H2,H3,H4,H5,H6]
    L=[L1,L2,L3,L4,L5,L6]
    D=[D1,D2,D3,D4,D5,D6]
    U=[humidex(T1,H1),humidex(T2,H2),humidex(T3,H3),humidex(T4,H4),humidex(T5,H5),humidex(T6,H6)]
    if argv[4]=='noise':
       graph_corrélation(X,B[int(argv[2][7])-1],B[int(argv[3][7])-1],'temps',argv[4]+' '+argv[2],argv[4]+' '+argv[3]) 
    if argv[4]=='temp':
       graph_corrélation(X,T[int(argv[2][7])-1],T[int(argv[3][7])-1],'temps',argv[4]+' '+argv[2],argv[4]+' '+argv[3])
    if argv[4]=='humidity':
       graph_corrélation(X,H[int(argv[2][7])-1],H[int(argv[3][7])-1],'temps',argv[4]+' '+argv[2],argv[4]+' '+argv[3])    
    if argv[4]=='lum':
       graph_corrélation(X,L[int(argv[2][7])-1],L[int(argv[3][7])-1],'temps',argv[4]+' '+argv[2],argv[4]+' '+argv[3]) 
    if argv[4]=='co2':
       graph_corrélation(X,D[int(argv[2][7])-1],D[int(argv[3][7])-1],'temps',argv[4]+' '+argv[2],argv[4]+' '+argv[3])  
    if argv[4]=='humidex':
       graph_corrélation(X,U[int(argv[2][7])-1],U[int(argv[3][7])-1],'temps',argv[4]+' '+argv[2],argv[4]+' '+argv[3]) 

if argv[1]=='auto':
    mesure_similarités(datetime(2019,8,12,12,0,0),datetime(2019,8,24,12,0,0))
