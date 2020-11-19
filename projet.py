#Pojet Info
"Mesurer les similarités"

from math import *
from matplotlib.pyplot import *
from numpy import *
from datetime import datetime

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
    E=round(E,1)
    O=round(O,1)
    return(m,M,E,O,Z)
    print('minimum :',m)
    print('maximum :',M)
    print('espérance :',E)
    print('écart-type :',O)
    print('médiane :',Z)
    
def courbe_simple(X,Y,a,b,c):
    m,M,E,O,Z=valeurs_stats(Y)
    m,M,E,O,Z=str(m),str(M),str(E),str(O),str(Z)
    f=figure()
    ax = f.add_subplot(111)
    text(0.87,0.87,'minimum : '+m+'\n'+'maximum : '+M+'\n'+'espérance : '+E+'\n'+'écart-type : '+O+'\n'+'médiane : '+Z,horizontalalignment='center',verticalalignment='center',transform=ax.transAxes)
    plot(X,Y)
    xlabel(a)
    ylabel(b)
    title(c)
    xticks(X[::50],rotation=-90)
    show()

def test(): #test de la fonction courbe_simple avec des valeurs du fichier csv
    C1,C2,C3,C4,C5,C6=tab_capteurs()
    X,Y=[],[]
    n=len(C1)
    for k in range(n):
        Y.append(C1[k][1])
        X.append(C1[k][5])
    return(courbe_simple(X,Y,'temps','température','courbe'))
    
def corrélation(L,P):
    n,S=len(L),0
    for k in range(n):
        S=S+L[k]*P[k]
    E=S/n
    m_L,M_L,E_L,O_L,Z_L=valeurs_stats(L)
    m_P,M_P,E_P,O_P,Z_P=valeurs_stats(P)
    return(round((E-E_L*E_P)/(O_L*O_P),3))

def humidex(T,H):
    n=len(T)
    h=[]
    for i in range(n):
        h.append(round(T[i]+(5/9)*(6.112*10**(7.5*(T[i]/(237.7+T[i])))*(H[i]/100)-10)))
    return(h)    

def graph_corrélation(X,L,P,a,l,p,t):
    c=corrélation(L,P)
    c=str(c)
    f=figure()
    ax = f.add_subplot(111)
    text(0.7,0.77,'corrélation : '+c,transform=ax.transAxes)
    plot(X,L,label=l)
    plot(X,P,label=p)
    legend()
    xlabel(a)
    title(t)
    xticks(X[::50],rotation=-85)
    show()

def dt(t):
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

def test2(td,tf): #test de la fonction graph_corrélation avec des valeurs du fichier csv entre deux instants
    C1,C2,C3,C4,C5,C6=limitation_temps_totale(td,tf)
    X,L,P=[],[],[]
    n=len(C1)
    for k in range(n):
        L.append(C1[k][1])
        T=C1[k][5]
        X.append(T[5:19])
        P.append(C2[k][1])
    return(graph_corrélation(X,L,P,'temps','température C1','température C2','corrélation température entre C1 et C2'))

def séparation(C,n):
    B,T,H,L,D=[],[],[],[],[]
    for i in range(n):
        B.append(C[i][0])
        T.append(C[i][1])
        H.append(C[i][2])
        L.append(C[i][3])
        D.append(C[i][4])
    return(B,T,H,L,D)

def mesure_similarités(td,tf):
    C1,C2,C3,C4,C5,C6=limitation_temps_totale(td,tf)
    n=min([len(C1),len(C2),len(C3),len(C4),len(C5),len(C6)])
    X=[]
    for i in range(n):
        x=C6[i][5]
        X.append(x[5:19])
    B1,T1,H1,L1,D1=séparation(C1,n)
    B2,T2,H2,L2,D2=séparation(C2,n)
    B3,T3,H3,L3,D3=séparation(C3,n)
    B4,T4,H4,L4,D4=séparation(C4,n)
    B5,T5,H5,L5,D5=séparation(C5,n)
    B6,T6,H6,L6,D6=séparation(C6,n)
    # Bruit :
    c12=corrélation(B1,B2)
    c12=str(c12)
    c13=corrélation(B1,B3)
    c13=str(c13)
    c14=corrélation(B1,B4)
    c14=str(c14)
    c15=corrélation(B1,B5)
    c15=str(c15)
    c16=corrélation(B1,B6)
    c16=str(c16)
    c23=corrélation(B2,B3)
    c23=str(c23)
    c24=corrélation(B2,B4)
    c24=str(c24)
    c25=corrélation(B2,B5)
    c25=str(c25)
    c26=corrélation(B2,B6)
    c26=str(c26)
    c34=corrélation(B3,B4)
    c34=str(c34)
    c35=corrélation(B3,B5)
    c35=str(c35)
    c36=corrélation(B3,B6)
    c36=str(c36)
    c45=corrélation(B4,B5)
    c45=str(c45)
    c46=corrélation(B4,B6)
    c46=str(c46)
    c56=corrélation(B5,B6)
    c56=str(c56)
    f=figure(figsize=(20,6), dpi=80)
    ax = f.add_subplot(111)
    text(0.15,0.95,'c12 : '+c12+'; c13 : '+c13+'; c14 : '+c14+'; c15 : '+c15+'; c16 : '+c16+'; c23 : '+c23+'; c24 : '+c24+'; c25 : '+c25+'; c26 : '+c26+'; c34 : '+c34+'; c35 : '+c35+'; c36 : '+c36+'; c45 : '+c45+'; c46 : '+c46+'; c56 : '+c56,transform=ax.transAxes)
    plot(X,B1,label='Capteur 1')
    plot(X,B2,label='Capteur 2')
    plot(X,B3,label='Capteur 3')
    plot(X,B4,label='Capteur 4')
    plot(X,B5,label='Capteur 5')
    plot(X,B6,label='Capteur 6')
    legend()
    xlabel('temps')
    title('Similarité du Bruit')
    xticks(X[::50],rotation=-85)
    # Température :
    c12=corrélation(T1,T2)
    c12=str(c12)
    c13=corrélation(T1,T3)
    c13=str(c13)
    c14=corrélation(T1,T4)
    c14=str(c14)
    c15=corrélation(T1,T5)
    c15=str(c15)
    c16=corrélation(T1,T6)
    c16=str(c16)
    c23=corrélation(T2,T3)
    c23=str(c23)
    c24=corrélation(T2,T4)
    c24=str(c24)
    c25=corrélation(T2,T5)
    c25=str(c25)
    c26=corrélation(T2,T6)
    c26=str(c26)
    c34=corrélation(T3,T4)
    c34=str(c34)
    c35=corrélation(T3,T5)
    c35=str(c35)
    c36=corrélation(T3,T6)
    c36=str(c36)
    c45=corrélation(T4,T5)
    c45=str(c45)
    c46=corrélation(T4,T6)
    c46=str(c46)
    c56=corrélation(T5,T6)
    c56=str(c56)
    f=figure(figsize=(20,6), dpi=80)
    ax = f.add_subplot(111)
    text(0.15,0.95,'c12 : '+c12+'; c13 : '+c13+'; c14 : '+c14+'; c15 : '+c15+'; c16 : '+c16+'; c23 : '+c23+'; c24 : '+c24+'; c25 : '+c25+'; c26 : '+c26+'; c34 : '+c34+'; c35 : '+c35+'; c36 : '+c36+'; c45 : '+c45+'; c46 : '+c46+'; c56 : '+c56,transform=ax.transAxes)
    plot(X,T1,label='Capteur 1')
    plot(X,T2,label='Capteur 2')
    plot(X,T3,label='Capteur 3')
    plot(X,T4,label='Capteur 4')
    plot(X,T5,label='Capteur 5')
    plot(X,T6,label='Capteur 6')
    legend()
    xlabel('temps')
    title('Similarité du température')
    xticks(X[::50],rotation=-85)
    show()
