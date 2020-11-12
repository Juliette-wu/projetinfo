#Pojet Info
"Mesurer les similarités"

from math import *
from matplotlib.pyplot import *
from numpy import *

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

def test():
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
    return((E-E_L*E_P)/(O_L*O_P))

#faire les fonctions humidex, finales, bonus
