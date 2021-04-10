# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 16:43:55 2019

@author: AUR.WILKOSZ
"""
from tkinter import *
from tkinter.filedialog import *
from PIL import Image, ImageTk
from timeit import default_timer
import random
import numpy as np

def generationMatrice():
    """Génère une matrice 18x18 délimitée par la valeur -8 (qui servent de limites), la matrice est ensuite remplie avec 40 bombes placées aléatoirement"""
    #création de la matrice 18x18 remplie de -8
    matrix=np.full((18, 18), -8)
    
    #remplacement du carré interne a1,1-a16,16 par des 0
    for i in range (1,17):
        for j in range (1,17):
            matrix[i][j]=0
    
    #mise en place des 40 bombes
    bomb=40
    while bomb>0:
        m=random.randint(1,16)
        n=random.randint(1,16)
        if matrix[m][n]==0:
            matrix[m][n]=9 #Le 9 est la valeur utilisée pour représenter une bombe
            bomb-=1
    return matrix

def compteurVoisin(m,n,matriceLecture):
    """Pour chaque cases de la matrice, on compte les bombes adjacentes et on met les valeurs dans la matrice"""
    voisin=0

    #On compte les voisins uniquement si la case n'est pas une bombe
    if matriceLecture[m][n] != 9:
        for i in range(m-1,m+2):
            for j in range(n-1,n+2):
                if matriceLecture[i][j]==9:
                    voisin+=1
    else:
        voisin = 9
    matrice[m][n] = voisin
    return voisin

def affichageGraphique(tab, bout, matrBout, boutBomb):
    """Cette fonction génère un objet va remplir Frame3 (Frame contenant l'affichage) avec des canvas, les canvas auront un label avec le nombre de bombes adjacentes à la case ou alors ils auront une image de bombe. Sur chaque canvas, on affiche ensuite des boutons auquel on assigne les fonctions pour l'utilisateur"""
    count = 0 #Le compteur sert à référencer le bouton

    #Création de l'image des bombes
    image = Image.open("images/bombmini.png")
    ph = ImageTk.PhotoImage(image)
    photo = PhotoImage(file="images/bombmini.png")
    can = Canvas(fenetre, width=photo.width(), height=photo.height())
    can.create_image(10, 10, image=ph)
    can.image = ph
    
    for ligne in range(18):
        ligneB = [] #Pour chaque lignes, on créée un tableau de boutons (ligneB est une  ligne de boutons)
        for colonne in range(18):
            if tab[ligne][colonne]!=-8: #Si la case n'est pas un mur
                couleur="Grey"
                valeurCase = Canvas(Frame3, width=20, height=30) #Création d'un canvas
                valeurCase.grid(row=ligne, column=colonne, padx = 2, pady = 2)
                if tab[ligne][colonne] != 9 and tab[ligne][colonne] != 0:
                    Label(valeurCase, text=tab[ligne][colonne],width=2, height=2).pack() #Si la valeur de la case n'est ni 0, ni une bombe(9), on ajoute un label auquel on assigne le nombre de voisins
                elif tab[ligne][colonne] == 0:
                    Label(valeurCase, text='',width=2, height=2).pack() #Si la case n'a pas de bombe autour d'elle on affiche rien dans le label
                else:
                    valeurCase.config(width=photo.width(), height=photo.height(),bg='white')
                    valeurCase.create_image(10,10, image=ph) #Si la case est une bombe, on affiche une bombe dans le canvas
#                    valeurCase['bg'] = "Red"
#                    valeurCase.create_oval(22,22,5,5, outline="#f11", fill="#444", width=1)
                    
                case = Button(Frame3, width=2, height=2, bg=couleur) #Création d'un bouton de la matrice
#                case['text'] = tab[ligne][colonne] #Affichage des valeurs des cases sur les boutons pour tester le code

                bout.append(case) 
                bout[count].grid(row=ligne, column=colonne, padx = 2, pady = 2) #On place le bouton sur le canvas
                bout[count].bind("<Button-1>",lambda i,ref=count,li=ligne,co=colonne: click(ref,li,co)) #On assigne le clic gauche à la fonction clic qui traite les événements lorsque l'utilisateur clique sur une case, li et co sont les coordonnées du bouton !
                bout[count].bind("<Button-3>",lambda i,ref=count,li=ligne,co=colonne: drapeau(ref,li,co)) #Assignation de la fonction qui traite les événements au clic droit de l'utilisateur
                bout[count].config(relief=RAISED)
                tabNbBombe.append(tab[ligne][colonne]) #On stocke le nombre de bombes adjacent à un bouton dans un tableau, on reconnaitra son bouton assigné grace à sa référence
                ligneB.append(bout[count]) #On met le bouton dans le tableau ligneB
                if matrice[ligne][colonne] == 9: #Si la case est une bombe, on stocke la case dans un tableau contenant toutes les références des bombes
                    boutBomb.append(case)
                count+=1
            else:
                couleur="white"
                ligneB.append(Button(Frame1, width=1, height=1, bg=couleur))
                z = Canvas(Frame3, width=10, height=20, bg=couleur)
                z.grid(row=ligne+1, column=colonne, padx = 2, pady = 2)
                z.grid_forget()
        matrBout.append(ligneB) #On insère le tableau ligneB dans une matrice, on pourra ainsi repérer les boutons avec leurs coordonnées


def enleveRangee(ref,li,co):
    """A partir d'une case 0, enlève tous les boutons d'une rangée jusqu'à tomber sur une valeur différente de 0"""
    base = co #Position de base, on enlève une rangée, donc on se déplace de colonnes en colonnes
    #Traitement vers la gauche tant que la case vaut 0 et tant que co > 0 (la position 0 est un mur)
    while co > 0 and matrice[li][co] == 0: 
        if matrice[li][co] == 0:
            enleveDiagonales(li,co)
        co = co - 1
        lesBoutons[li][co].grid_forget() #On enlève le bouton
        matrice2[li][co] = -1
        if lesBoutons[li][co]['state']!="disabled": #Si le bouton n'est pas désactivé
            lesBoutons[li][co]['state'] = "disabled" #On désactive la case pour ne pas avoir de récursion à partir de cette case plus tard
            enleveColonne(ref,li,co)

    co = base #Retour à la valeur de base
    #Traitement vers la droite tant que la case vaut 0 et tant que co < 17 (la position 17 est un mur)
    while co < 17 and matrice[li][co] == 0: 
        if matrice[li][co] == 0: #Si la case vaut 0, on enlève les diagonales
            enleveDiagonales(li,co)
        co = co + 1
        lesBoutons[li][co].grid_forget() #On enlève le bouton
        matrice2[li][co] = -1
        if lesBoutons[li][co]['state']!="disabled": #Si le bouton n'est pas désactivé
            lesBoutons[li][co]['state'] = "disabled" #On désactive la case pour ne pas avoir de récursion à partir de cette case plus tard
            enleveColonne(ref,li,co)
        


def enleveColonne(ref,li,co):
    """A partir d'une case 0, enlève tous les boutons d'une colonne jusqu'à tomber sur une valeur différente de 0"""
    base = li #Position de base, on enlève une colonne, donc on se déplace de lignes en lignes
    #Traitement vers le haut tant que la case vaut 0 et tant que li > 0 (la position 0 est un mur)
    while li > 0 and matrice[li][co] == 0:
        if matrice[li][co] == 0: #Si la case vaut 0, on enlève les diagonales
            enleveDiagonales(li,co) 
        li = li - 1
        lesBoutons[li][co].grid_forget() #On enlève le bouton
        matrice2[li][co] = -1
        if lesBoutons[li][co]['state']!="disabled": #Si le bouton n'est pas désactivé
            lesBoutons[li][co]['state'] = "disabled" #On désactive la case pour ne pas avoir de récursion à partir de cette case plus tard
            enleveRangee(ref,li,co)

    li = base
    #Traitement vers le bas tant que la case vaut 0 et tant que li < 17 (la position 17 est un mur)
    while li < 17 and matrice[li][co]  == 0: 
        if matrice[li][co] == 0:
            enleveDiagonales(li,co)
        li = li + 1
        lesBoutons[li][co].grid_forget() #On enlève le bouton
        matrice2[li][co] = -1
        if lesBoutons[li][co]['state']!="disabled": #Si le bouton n'est pas désactivé
            lesBoutons[li][co]['state'] = "disabled" #On désactive la case pour ne pas avoir de récursion à partir de cette case plus tard
            enleveRangee(ref,li,co)

def enleveDiagonales(li,co):
    """Dévoile les cases en diagonale d'une case dont les coordonnées sont passées en paramètre"""
    for li2 in range(li-1,li+2):
        for co2 in range(co-1,co+2):
            lesBoutons[li2][co2].grid_forget()
            matrice2[li2][co2] = -1
            if matrice[li2][co2] == 0 and lesBoutons[li2][co2]['state'] != 'disabled': #Si le bouton n'est pas désactivé et que la case vaut 0
                lesBoutons[li2][co2]['state'] = "disabled" #On désactive la case 
                enleveColonne(0,li2,co2) #On enlève la rangée
                enleveRangee(0,li2,co2) #On enlève la colonne
    


def drapeau(ref,li,co):
    """Affiche ou enlève un drapeau lorsque l'utilisateur clique droit sur une case"""
# Commenté car l'affichage du drapeau ne fonctionne pas
#    image = Image.open("images/Flag.png")
#    drapeau = ImageTk.PhotoImage(image)
    
    nb = int(compteurBombe['text'])
    
    if bouttons[ref]['text'] == "?": #Si un point d'interrogation est affiché, on l'enlève
            bouttons[ref].config(state="normal", text='')
    elif bouttons[ref]['state'] == "normal": #Si le bouton a un état normal
        nb = nb - 1
        bouttons[ref]['state'] = "disabled"
        bouttons[ref].config(text='X', foreground='green') #On affiche une croix (A défaut d'afficher le drapeau)
        bouttons[ref].unbind("<Button-1>") #On désactive la fonction liée au clic gauche
    else: #Si la case est déjà marquée
        nb = nb + 1
        bouttons[ref].config(state="normal", text="?",foreground='black') #On affiche un point d'interrogation
        bouttons[ref].bind("<Button-1>",lambda i, li=li,co=co: click(ref,li,co)) #On lie la fonction click() au clic gauche
    compteurBombe['text'] = str(nb)

def click(ref,li,co):
    """Vérifie les conditions de jeu"""
    global continuePartie
    
    lesBoutons[li][co].grid_forget() #On enlève le bouton de la grille
    if tabNbBombe[ref] != 9: #Si la case n'est pas une bomne
        matrice2[li][co] = -1 #On remplzce la valeur de la matrice jumelle par -1
        
    if perdu(li,co) == True: #Si la partie est perdue, appelle la fonction finDePartie()
        finDePartie()
        statut.config(text = 'Perdu :(')
    elif tabNbBombe[ref] == 0: #Si la case est un 0, on appelle  les fonctions enleveRangee() et enleveColonne()
        enleveRangee(ref,li,co)
        enleveColonne(ref,li,co)
        
    if gagne() == True: #Si la partie est gagnée
        continuePartie = False #Partie terminée
        statut.config(text = 'Gagné :D')
        for bombe in boutonsBombe: #On désactive les fonctionalités des boutons des cases bomnes
            bombe.unbind("<Button-1>")
            bombe.unbind("<Button-3>")
    

def perdu(li,co):
    """Renvoie True si le joueur a cliqué sur une bombe"""
    print(matrice[li][co])
    if matrice[li][co] == 9:
        return True
    else:
        return False

def finDePartie():
    """Lorsque le joueur clique sur une bombe, les cases bombes sont dévoilées et le jeu s'arrête"""
    global continuePartie
    for button in boutonsBombe:
        button.grid_forget()
    
    for boutton in bouttons: #On désactive les événements de tous les boutons
        boutton.config(state='disabled')
        boutton.unbind("<Button-1>")
        boutton.unbind("<Button-3>")
        continuePartie = False
        

def gagne():
    """Lorsqu'une case est ouverte, la valeur est remplacée par -1 sur la copie de la matrice, la fonction compte les -1"""
    count = 0 
    for i in range(1,17):
        for j in range(1,17):
            if matrice2[i][j] == -1:
                count = count + 1
    print(count)
    if count == 216: #216 correspond aux nombre de cases n'ayant pas de bombes
        return True
    else:
        return False
    

def updateTime():
    """Cette fonction gère le chronomètre"""
    global continuePartie
    now = default_timer() - start
    seconds = now
    str_time = "%02d" % (seconds)
    lbl['text'] = str_time
    if continuePartie == True:
        fenetre.after(1000, updateTime) #Actualisation toutes les secondes

def reset():
    """Cette fonction réinitialise le jeu"""
    global matrice, matrice2, continuePartie, start, lesBoutons, bouttons, boutonsBombe, tabNbBombe
    #On enlève les Frames3 et 4 et on les remet après
    Frame4.grid_forget() 
    Frame3.grid_forget()
    Frame3.grid(padx=10, pady=10)
    Frame4.grid(row=1, column=2)
    matrice = generationMatrice() #On génère une nouvelle matrice
    
    #On compte les voisins
    for ligne in range(18):
        for colonne in range(18):
            if matrice[ligne][colonne]!=-8:
                compteurVoisin(ligne,colonne,matrice)
    
    #On détruit tous les boutons de la Frame3
    for w in Frame3.grid_slaves():
        w.destroy()
    
    statut.config(text = 'Partie en cours')
    bouttons = []
    tabNbBombe = []
    lesBoutons = []
    boutonsBombe = []
    compteurBombe['text'] = '40' #Le compteur revient à 40
    continuePartie = True #La partie est de nouveau en cours
    start = default_timer() #Réinitialisation du timer
    matrice2 = matrice.copy() #On copie la matrice
    affichageGraphique(matrice,bouttons, lesBoutons,boutonsBombe) #On effectue un nouvel affichage graphique
    updateTime() #On redémare le chrono
    
#Initialisation TKinter
fenetre = Tk() #fenetre
fenetre.title("Démineur")
tableau_aleatoire = [] #tableau qui reçoit les aléatoires
matrice = np.zeros(shape=(12, 12), dtype=int) #matrice du tableau
matrice2 = [] #tableau qui permettra d'afficher la matrice après nouvelle génération

fenetre.geometry("750x830")
fenetre['bg'] = 'white';

Frame1 = Frame(fenetre, borderwidth=2, relief=GROOVE, bg="grey") #Frame principale
Frame1.pack(side=LEFT, padx=10, pady=10)

#Frame contenant le chrono, l'état de la partie, le compteur et le bouton reset
Frame2 = Frame(Frame1, borderwidth=2, relief=GROOVE, bg="grey") 
Frame2.grid( padx=10, pady=10)

#La grille de démineur
Frame3 = Frame(Frame1, borderwidth=2, relief=GROOVE, bg="grey")
Frame3.grid(padx=10, pady=10)

#Cette frame contient la légende
Frame4 = Frame(Frame1, borderwidth=2, relief=GROOVE, bg="white")
Frame4.grid(row=1, column=2)

#Affiche le chronomètre
lbl = Label(Frame2, padx='40')
lbl.grid(row=1, column=1)

lblLegendeBombe = Label(Frame4, text='Bombe', bg='white')
lblLegendeBombe.grid(row=1,column=2)

lblMarqueur = Label(Frame4, padx='20', text='X', foreground='green', bg='white')
lblMarqueur.grid(row=2,column=1)

lblLegendeMarqueur = Label(Frame4, text='Clic droit pour \n marquer la case', bg='white')
lblLegendeMarqueur.grid(row=2,column=2)

lblInterrog = Label(Frame4, text='?', bg='white')
lblInterrog.grid(row=3,column=1)

lblInterrogLegende = Label(Frame4, text='Clic droit sur une case marquée\n si vous n\'êtes pas sur de la \n présence de la bombe', bg='white')
lblInterrogLegende.grid(row=3,column=2)

lblVoisin = Label(Frame4, text='1', bg='white')
lblVoisin.grid(row=4,column=1)

lblVoisinLegende = Label(Frame4, text='Indique la présence d\'une bombe \n autour de la case \n (clic gauche pour révéler la case)', bg='white')
lblVoisinLegende.grid(row=4,column=2)

#Label qui affiche l'état de la partie
statut = Label(Frame2,text="Partie en cours", padx='40')
statut.grid(row=1, column=2)

#Label du compteur, reçooit le nombre de bombes et se décrémente à chaque fois que l'utilisateur marque une case
compteurBombe = Label(Frame2, text="40", padx='40')
compteurBombe.grid(row=1, column=3)

#Bouton de réinitialisation
resetBout = Button(Frame2, text='reset')
resetBout.bind("<Button-1>",lambda i: reset())
resetBout.grid(row=1, column=4)

#Chronomètre 
start = default_timer()
continuePartie = True 
updateTime()    
   
#Test des fonctions
matrice = generationMatrice()  #Matrice contenant les valeurs numériques  
print("Compte bombe voisines")
for ligne in range(18):
    for colonne in range(18):
        if matrice[ligne][colonne]!=-8:
            compteurVoisin(ligne,colonne,matrice)

print(matrice)
bouttons = [] #Contient tous les boutons (Trouvables par référence)
tabNbBombe = [] #Contient les valeurs de chaque cases
lesBoutons = [] #Matrice des boutons (Trouvables par coordonnées)
boutonsBombe = [] #Contient tous les boutons des bombes
affichageGraphique(matrice,bouttons, lesBoutons,boutonsBombe) #Initialisation de l'affichage graphique
print(tabNbBombe)

#Image bombe affichée dans la légende
image = Image.open("images/bombmini.png")
ph = ImageTk.PhotoImage(image)
photo = PhotoImage(file="images/bombmini.png")


legendeBombe = Canvas(Frame4, width=20, height=30)
legendeBombe.config(width=photo.width(), height=photo.height(),bg='white')
legendeBombe.create_image(10,10, image=ph)
legendeBombe.grid(row=1,column=1)


matrice2 = matrice.copy() #Matrice qui se videra au fur et à mesure, clé pour la fonction gagne !
    
fenetre.mainloop()