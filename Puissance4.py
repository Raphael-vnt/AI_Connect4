
import time
import numpy as np

nbColumns=12
nbLines=6
tailleGrille=nbLines*nbColumns
grille=['-']*tailleGrille
row=4

heuri=np.array([[0,1,5,50,40000],
               [-1,0,0,0,0],
               [-5,0,0,0,0],
               [-50,0,0,0,0],
               [-40000,0,0,0,0]])


# Return la liste des actions possibles
def Actions(s):
    ac=[]
    for i in range(nbColumns):
        if(s[i]=='-'): ac.append(i)
    return ac

# Return le plateau update après le coup d'un joueur 
def Result(s,coup,joueur):
    newS=s[:]
    for i in range(coup+(nbLines-1)*nbColumns,coup-1,-nbColumns):
        if(newS[i]=='-'):
            #print('Coup : ', i)
            newS[i]=joueur
            break  
    return newS


def AllSolutions():
    # Alignements horizontaux
    solutions_lignes = []
    for i in range(nbLines):
        for j in range(nbColumns - 3):
            start = i * nbColumns + j
            solutions_lignes.append([start, start + 1, start + 2, start + 3])

    # Alignements verticaux
    solutions_colonnes = []
    for i in range(nbColumns):
        for j in range(nbLines - 3):
            start = i + j * nbColumns
            solutions_colonnes.append([start, start + nbColumns, start + 2 * nbColumns, start + 3 * nbColumns])

    # Alignements diagonaux montants 
    solutions_diag_montantes = []
    for i in range(nbLines - 3):
        for j in range(nbColumns - 3):
            start = i * nbColumns + j
            solutions_diag_montantes.append([start, start + nbColumns + 1, start + 2 * (nbColumns + 1), start + 3 * (nbColumns + 1)])

    # Alignements diagonaux descendants 
    solutions_diag_descendantes = []
    for i in range(3, nbLines):
        for j in range(nbColumns - 3):
            start = i * nbColumns + j
            solutions_diag_descendantes.append([start, start - nbColumns + 1, start - 2 * (nbColumns - 1), start - 3 * (nbColumns - 1)])

    solutions = solutions_lignes + solutions_colonnes + solutions_diag_montantes + solutions_diag_descendantes

    return solutions

# Condition d'arrêt : joueur gagne ou égalité (plateau rempli)
def TerminalTest(s):
    for i in solutions:
        if s[i[0]]!='-' and all(s[j]==s[i[0]] for j in i): return True    
    if('-' in s): return False  
    return True



def peut_jouer(s, pos):
    if pos < 0 or pos >= nbColumns * nbLines:
        return False
    
    if s[pos] != '-':
        return False
    
    if pos >= nbColumns * (nbLines - 1):
        return True
    
    position_below = pos + nbColumns
    if s[position_below] != '-':
        return True
    
    return False


def Heuristic2(s,d):
    score=0
    menacesj1=[]
    menacesj2=[]
    m=None
    for i in solutions:   
        j1=0
        j2=0
        for case in i:
            if(s[case]=='X'):
                j1+=1
            if(s[case]=='O'):
                j2+=1  
            if(s[case]=='-'):
                m=case
                
        if(j1==3 and j2==0):
            if m not in menacesj1: 
                menacesj1.append(m)  
            else : 
                score -= 50
                 
        if(j2==3 and j1==0):
            if m not in menacesj2: 
                menacesj2.append(m)
            else : 
                score += 50

        if(j1==4): return 40000+d
        if(j2==4): return -40000-d
        
        score+=heuri[j2,j1] 

    ultra_menaces_j1 = 0
    ultra_menaces_j2 = 0

    for m1 in menacesj1:
        if peut_jouer(s, m1): 
            ultra_menaces_j1 +=1
            #print('ultra menace j1 : ', m1)
        if((m1+nbColumns in menacesj1) or (m1-nbColumns in menacesj1)): 
                score+=1000
        if(m1+nbColumns in menacesj2):
                score-=40

    for m2 in menacesj2:
        if peut_jouer(s, m2): 
            #print('ultra menace j2 : ', m2)
            ultra_menaces_j2 +=1
        if((m2+nbColumns in menacesj2) or (m2-nbColumns in menacesj2)): 
                score-=1000
        if(m2+nbColumns in menacesj1):
                score+=40  

    if ultra_menaces_j1 > 1 : 
        score += 5000

    if ultra_menaces_j2 > 1 : 
        score -= 5000

    return score


# Etalage alpha beta
def maxValue(s,α,β,depth): 
    if(depth== 0 or TerminalTest(s)):
        return [Heuristic2(s,depth)]
    v=-100000 
    move=None
    for a in Actions(s):
        utilAdve=minValue(Result(s,a,'X'),α,β,depth-1)[0]
        if(utilAdve>v): 
            move=a
            v=utilAdve
        if(v>=β): return (v,move)
        α=max(α,v)
    return (v,move)

def minValue(s,α,β,depth):
    if(depth== 0 or TerminalTest(s)):
        return [Heuristic2(s,depth)]
    v=100000
    move=None
    for a in Actions(s):
        utilAdve=maxValue(Result(s,a,'O'),α,β,depth-1)[0]
        if(utilAdve<v):
            move=a
            v=utilAdve            
        if(v<=α): return (v,move)
        β=min(β,v)
    return (v,move)         
 

def AfficherGrille(grille):
    for i in range(len(grille)):
        print(grille[i]," ",end='') if (i+1)%nbColumns!=0 else print(grille[i]) 
    for i in range(nbColumns):
        print(i+1," ",end='')

def commentaire(score):
    av_joueur = "Vous avez " if score<0 else "L'ia a "
    phrase = av_joueur
    if np.abs(score)>2000:
        return phrase + "un énorme avantage"
    if np.abs(score)>200:
        return phrase + "un gros avantage"
    if np.abs(score)>80:
        return phrase + "l'avantage"
    if np.abs(score)>40:
        return phrase + "un léger avantage"

    return "La partie est équilibré"



def Play():
    n=0
    s=grille[:]
    premierJoueur=eval(input("Qui est le 1er joueur ? 0 pour vous et 1 pour l'IA : "))
    difficulté=eval(input("Quel niveau de difficulté ? De 1 à 6 (5 conseillé pour le challenge, 6 temps de calcul long, de 30 à 7O secondes par coup) : "))
    if(premierJoueur==1): n=1
    while(TerminalTest(s)==False and n<42):        
        AfficherGrille(s)    
        print("\n")
        if(n%2==0):      
            move=eval(input("A votre tour de jouer (entre 1 et 12): "))-1
            while(move<0 or move>11):
                print("coup non valide")
                move=eval(input("A votre tour de jouer(entre 1 et 12): "))-1
            s=Result(s,move,'O')



        else:
            debut=time.time()
            print( "Calcul de l'ia ...")
            move=maxValue(s,-100000,100000,difficulté)
            fin=time.time()
            print(fin-debut,"secondes ; L'ia vient de jouer sur la colonne ",move[1]+1)
            print(commentaire(move[0]))
            s=Result(s,move[1],'X')
                   
        n=n+1 

    AfficherGrille(s)
    print("fin : ",n)


solutions=AllSolutions()
Play()
