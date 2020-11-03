#Pojet Info
"Mesurer les similarités"

from datetime import datetime

def tab_capteurs():
    T1,T2,T3,T4,T5,T6=[],[],[],[],[],[]   #tableaux corespondant aux 6 capteurs
    E=open('EIVP_KM.csv','r')
    next(E)
    for ligne in E:
        l=ligne.split(';')  #l correspond à une ligne du tableau
        l[0]=int(l[0])
        for k in range(1,4):
            l[k]=float(l[k])
        for k in range(4,6):
            l[k]=int(l[k])   
        l[6]=l[6].strip()
        if l[0]==1:
            T1.append(l[1:])
        if l[0]==2:
            T2.append(l[1:])
        if l[0]==3:
            T3.append(l[1:])
        if l[0]==4:
            T4.append(l[1:])
        if l[0]==5:
            T5.append(l[1:])
        else:
            T6.append(l[1:])
    E.close()
    return(T1,T2,T3,T4,T5,T6)
                  
