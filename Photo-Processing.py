# -*- coding: utf-8 -*-
"""
@author: Guillaume Sachet
"""

import tkMessageBox
import unicodedata
from math import sqrt
from tkFileDialog import *
from Tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk


# Classe image
class cImage:
    def __init__(self, coords, nomFichier=""):
        self.coords = coords
        self.nomFichier = nomFichier
        self.imageTK = None
        self.image = None
        self.pixels = None
        self.gris = False
        self.taille = []
        self.ouvert = False
        self.historique = []

    def ouvrir(self, nomFichier):
        self.nomFichier = nomFichier
        self.taille = np.shape(np.array(Image.open(self.nomFichier)))
        if self.taille[0] > 500:
            self.image = Image.open(self.nomFichier).resize(((350,460)))
        else:
            self.image = Image.open(self.nomFichier)
        self.imageTK = ImageTk.PhotoImage(self.image)
        self.pixels = np.array(self.image)
        self.taille = np.shape(self.pixels)
        self.ouvert = True
        self.gris = self.verifGris()
        print self.taille


    def changer(self, newMatrice):
        if self.coords == img1.coords:
            self.historique.append(self.pixels)
        newImage = Image.fromarray(newMatrice)
        self.image = newImage
        self.imageTK = ImageTk.PhotoImage(self.image)
        self.pixels = np.array(self.image)
        self.taille = np.shape(self.pixels)
        zoneDessin.create_image(self.coords[0], self.coords[1], image=self.imageTK)

    def verifGris(self):
        for ligne in range(0, self.taille[0]):
            for i in range(0, self.taille[1]):
                if type(self.pixels[ligne][i]) == np.ndarray:
                    if int(self.pixels[ligne][i][0]) != int(self.pixels[ligne][i][1]) or int(self.pixels[ligne][i][0]) != int(self.pixels[ligne][i][2]):
                        return False
                if type(self.pixels[ligne][i]) == np.uint8 or type(self.pixels[ligne][i]) == np.float32:
                    return True
        self.gris = False
        self.filtreGris()
        return True
    def chargerImage(self):
        filepath = ""
        filepath = askopenfilename(title="Ouvrir une image", filetypes=[("Tout les fichiers images", (".png", ".jpg", ".gif",".bmp", ".tif"))])
        if filepath != "":
            self.ouvrir(filepath)
            zoneDessin.create_image(self.coords[0], self.coords[1], image=self.imageTK)
            if img1.ouvert == False:
                img1.ouvrir(filepath)
                zoneDessin.create_image(img1.coords[0], img1.coords[1], image=img1.imageTK)


    def enregistrerImage(self):
        if self.ouvert == False:
            tkMessageBox.showerror("Erreur", "Erreur : Pas d'image chargée")
        else:
            dossierSauvegarde = ""
            dossierSauvegarde = asksaveasfilename(title="Enregistrer sous", defaultextension=".gif", initialfile="Nouvelle Image", filetypes=[('PNG', '.png'), ('GIF', '.gif'), ('JPEG', '.jpg'), ('Bitmap', '.bmp'), ('TIFF', '.tif')])
            if dossierSauvegarde != "":
                self.image = self.image.convert("RGB")
                self.image.save(dossierSauvegarde)

    def fonctionCopier(self, image):
        if image.ouvert == False:
            tkMessageBox.showerror("Erreur", "Erreur : Pas d'image chargée")
        else:
            self.changer(image.pixels)
            self.gris = image.gris
            self.ouvert = True
            self.nomFichier = image.nomFichier
            zoneDessin.create_image(self.coords[0], self.coords[1], image=self.imageTK)

    def filtres(self):
        if self.ouvert == False:
            tkMessageBox.showerror("Erreur", "Erreur : Pas d'image chargée")
        else:
            valueFiltre = unicodedata.normalize('NFD', unicode(varFiltre.get())).encode('ASCII', 'ignore')
            if valueFiltre == "Filtre Moyen":
                self.filtreMoyen()
            elif valueFiltre == "Filtre Gaussien":
                self.filtreGaussien()
            elif valueFiltre == "Filtre de Prewitt":
                self.filtreDePrewitt()
            elif valueFiltre == "Filtre Laplacien":
                self.filtreLaplacien()
            elif valueFiltre == "Filtre Median":
                self.filtreMedian()
            elif valueFiltre == "Filtre Negatif":
                self.filtreNegatif()
            elif valueFiltre == "Filtre Gris":
                self.filtreGris()

    def filtreGris(self):
        if self.gris == False:
            newMatrice = np.mean(self.pixels, -1)
            self.gris = True
            self.changer(newMatrice)
        else:
            tkMessageBox.showerror("Erreur", "Erreur : Image déjà grise")

    def filtreMoyen(self):
        if self.gris == True:
            newMatrice = np.ones([self.taille[0], self.taille[1]])
            for ligne in range(0, self.taille[0]):
                for i in range(0, self.taille[1]):
                    if (ligne == 0) or (ligne == self.taille[0]-1) or (i == 0) or (i == self.taille[1]-1):
                        newMatrice[ligne][i] *= int(self.pixels[ligne][i])
                    else:
                        newMatrice[ligne][i] = (int(self.pixels[ligne-1][i-1])+int(self.pixels[ligne-1][i])+int(self.pixels[ligne-1][i+1])+int(self.pixels[ligne][i-1])+int(self.pixels[ligne][i])+int(self.pixels[ligne][i+1])+int(self.pixels[ligne+1][i-1])+int(self.pixels[ligne+1][i])+int(self.pixels[ligne+1][i+1]))/9

        else:
            newMatrice = np.ones([self.taille[0], self.taille[1], 3], dtype=np.uint8)
            for ligne in range(0, self.taille[0]):
                for i in range(0, self.taille[1]):
                    if (ligne == 0) or (ligne == self.taille[0]-1) or (i == 0) or (i == self.taille[1]-1):
                        newMatrice[ligne][i][0] *= int(self.pixels[ligne][i][0])
                        newMatrice[ligne][i][1] *= int(self.pixels[ligne][i][1])
                        newMatrice[ligne][i][2] *= int(self.pixels[ligne][i][2])
                    else:
                        newMatrice[ligne][i][0] = (int(self.pixels[ligne-1][i-1][0])+int(self.pixels[ligne-1][i][0])+int(self.pixels[ligne-1][i+1][0])+int(self.pixels[ligne][i-1][0])+int(self.pixels[ligne][i][0])+int(self.pixels[ligne][i+1][0])+int(self.pixels[ligne+1][i-1][0])+int(self.pixels[ligne+1][i][0])+int(self.pixels[ligne+1][i+1][0]))/9
                        newMatrice[ligne][i][1] = (int(self.pixels[ligne-1][i-1][1])+int(self.pixels[ligne-1][i][1])+int(self.pixels[ligne-1][i+1][1])+int(self.pixels[ligne][i-1][1])+int(self.pixels[ligne][i][1])+int(self.pixels[ligne][i+1][1])+int(self.pixels[ligne+1][i-1][1])+int(self.pixels[ligne+1][i][1])+int(self.pixels[ligne+1][i+1][1]))/9
                        newMatrice[ligne][i][2] = (int(self.pixels[ligne-1][i-1][2])+int(self.pixels[ligne-1][i][2])+int(self.pixels[ligne-1][i+1][2])+int(self.pixels[ligne][i-1][2])+int(self.pixels[ligne][i][2])+int(self.pixels[ligne][i+1][2])+int(self.pixels[ligne+1][i-1][2])+int(self.pixels[ligne+1][i][2])+int(self.pixels[ligne+1][i+1][2]))/9
        self.changer(newMatrice)

    def filtreGaussien(self):
        if self.gris == True:
            newMatrice = np.ones([self.taille[0], self.taille[1]])
            for ligne in range(0, self.taille[0]):
                for i in range(0, self.taille[1]):
                    if (ligne == 0) or (ligne == self.taille[0]-1) or (i == 0) or (i == self.taille[1]-1):
                        newMatrice[ligne][i] *= int(self.pixels[ligne][i])
                    else:
                        newMatrice[ligne][i] = (int(self.pixels[ligne-1][i])+int(self.pixels[ligne][i-1])+4*int(self.pixels[ligne][i])+int(self.pixels[ligne][i+1])+int(self.pixels[ligne+1][i]))/8
        else:
            newMatrice = np.ones([self.taille[0], self.taille[1], 3], dtype=np.uint8)
            for ligne in range(0, self.taille[0]):
                for i in range(0, self.taille[1]):
                    if (ligne == 0) or (ligne == self.taille[0]-1) or (i == 0) or (i == self.taille[1]-1):
                        newMatrice[ligne][i][0] *= int(self.pixels[ligne][i][0])
                        newMatrice[ligne][i][1] *= int(self.pixels[ligne][i][1])
                        newMatrice[ligne][i][2] *= int(self.pixels[ligne][i][2])
                    else:
                        newMatrice[ligne][i][0] *= (int(self.pixels[ligne-1][i][0])+int(self.pixels[ligne][i-1][0])+4*int(self.pixels[ligne][i][0])+int(self.pixels[ligne][i+1][0])+int(self.pixels[ligne+1][i][0]))/8
                        newMatrice[ligne][i][1] *= (int(self.pixels[ligne-1][i][1])+int(self.pixels[ligne][i-1][1])+4*int(self.pixels[ligne][i][1])+int(self.pixels[ligne][i+1][1])+int(self.pixels[ligne+1][i][1]))/8
                        newMatrice[ligne][i][2] *= (int(self.pixels[ligne-1][i][2])+int(self.pixels[ligne][i-1][2])+4*int(self.pixels[ligne][i][2])+int(self.pixels[ligne][i+1][2])+int(self.pixels[ligne+1][i][2]))/8
        self.changer(newMatrice)


    def filtreDePrewitt(self):
        if self.gris == True:
            newMatrice = np.ones([self.taille[0], self.taille[1]])
            for ligne in range(0, self.taille[0]):
                for i in range(0, self.taille[1]):
                    if (ligne == 0) or (ligne == self.taille[0]-1) or (i == 0) or (i == self.taille[1]-1):
                        newMatrice[ligne][i] *= int(self.pixels[ligne][i])
                    else:
                        valeurGradientX = -int(self.pixels[ligne-1][i-1])+int(self.pixels[ligne-1][i+1])-int(self.pixels[ligne][i-1])+int(self.pixels[ligne][i+1])-int(self.pixels[ligne+1][i-1])+int(self.pixels[ligne+1][i+1])
                        valeurGradientY = int(self.pixels[ligne-1][i-1])+int(self.pixels[ligne-1][i])+int(self.pixels[ligne-1][i+1])-int(self.pixels[ligne+1][i-1])-int(self.pixels[ligne+1][i])-int(self.pixels[ligne+1][i+1])
                        newMatrice[ligne][i] *= sqrt(valeurGradientX**2+valeurGradientY**2)
        else:
            newMatrice = np.ones([self.taille[0], self.taille[1],3], dtype=np.uint8)
            for ligne in range(0, self.taille[0]):
                for i in range(0, self.taille[1]):
                    if (ligne == 0) or (ligne == self.taille[0]-1) or (i == 0) or (i == self.taille[1]-1):
                        newMatrice[ligne][i][0] *= int(self.pixels[ligne][i][0])
                        newMatrice[ligne][i][1] *= int(self.pixels[ligne][i][1])
                        newMatrice[ligne][i][2] *= int(self.pixels[ligne][i][2])
                    else:
                        valeurGradientXR = -int(self.pixels[ligne-1][i-1][0])+int(self.pixels[ligne-1][i+1][0])-int(self.pixels[ligne][i-1][0])+int(self.pixels[ligne][i+1][0])-int(self.pixels[ligne+1][i-1][0])+int(self.pixels[ligne+1][i+1][0])
                        valeurGradientYR = int(self.pixels[ligne-1][i-1][0])+int(self.pixels[ligne-1][i][0])+int(self.pixels[ligne-1][i+1][0])-int(self.pixels[ligne+1][i-1][0])-int(self.pixels[ligne+1][i][0])-int(self.pixels[ligne+1][i+1][0])
                        newMatrice[ligne][i][0] *= sqrt(valeurGradientXR**2+valeurGradientYR**2)
                        valeurGradientXG = -int(self.pixels[ligne-1][i-1][1])+int(self.pixels[ligne-1][i+1][1])-int(self.pixels[ligne][i-1][1])+int(self.pixels[ligne][i+1][1])-int(self.pixels[ligne+1][i-1][1])+int(self.pixels[ligne+1][i+1][1])
                        valeurGradientYG = int(self.pixels[ligne-1][i-1][1])+int(self.pixels[ligne-1][i][1])+int(self.pixels[ligne-1][i+1][1])-int(self.pixels[ligne+1][i-1][1])-int(self.pixels[ligne+1][i][1])-int(self.pixels[ligne+1][i+1][1])
                        newMatrice[ligne][i][1] *= sqrt(valeurGradientXG**2+valeurGradientYG**2)
                        valeurGradientXB = -int(self.pixels[ligne-1][i-1][2])+int(self.pixels[ligne-1][i+1][2])-int(self.pixels[ligne][i-1][2])+int(self.pixels[ligne][i+1][2])-int(self.pixels[ligne+1][i-1][2])+int(self.pixels[ligne+1][i+1][2])
                        valeurGradientYB = int(self.pixels[ligne-1][i-1][2])+int(self.pixels[ligne-1][i][2])+int(self.pixels[ligne-1][i+1][2])-int(self.pixels[ligne+1][i-1][2])-int(self.pixels[ligne+1][i][2])-int(self.pixels[ligne+1][i+1][2])
                        newMatrice[ligne][i][2] *= sqrt(valeurGradientXB**2+valeurGradientYB**2)
        self.changer(newMatrice)

    def filtreLaplacien(self):
        if self.gris == True:
            newMatrice = np.ones([self.taille[0], self.taille[1]])
            for ligne in range(0, self.taille[0]):
                for i in range(0, self.taille[1]):
                    if (ligne == 0) or (ligne == self.taille[0]-1) or (i == 0) or (i == self.taille[1]-1):
                        newMatrice[ligne][i] *= int(self.pixels[ligne][i])
                    else:
                        valeurPixel = -int(self.pixels[ligne-1][i-1])-int(self.pixels[ligne-1][i])-int(self.pixels[ligne-1][i+1])-int(self.pixels[ligne][i-1])+8*int(self.pixels[ligne][i])-int(self.pixels[ligne][i+1])-int(self.pixels[ligne+1][i-1])-int(self.pixels[ligne+1][i])-int(self.pixels[ligne+1][i+1])
                        newMatrice[ligne][i] *= valeurPixel
            self.changer(newMatrice)
        else:
            tkMessageBox.showerror("Erreur", "Erreur : Image en Couleur")

    def filtreMedian(self):
        if self.gris == True:
            newMatrice = np.ones([self.taille[0], self.taille[1]])
            for ligne in range(0, self.taille[0]):
                for i in range(0, self.taille[1]):
                    if (ligne == 0) or (ligne == self.taille[0]-1) or (i == 0) or (i == self.taille[1]-1):
                        self.pixels[ligne][i] *= int(self.pixels[ligne][i])
                    else:
                        listePixels = [int(self.pixels[ligne-1][i-1]), int(self.pixels[ligne-1][i]), int(self.pixels[ligne-1][i+1]), int(self.pixels[ligne][i-1]), int(self.pixels[ligne][i]), int(self.pixels[ligne][i+1]), int(self.pixels[ligne+1][i-1]), int(self.pixels[ligne+1][i]), int(self.pixels[ligne+1][i+1])]
                        listePixels.sort()
                        newMatrice[ligne][i] *= listePixels[4]
            self.changer(newMatrice)
        else:
            tkMessageBox.showerror("Erreur", "Erreur : Image en Couleur")

    
    def filtreNegatif(self):
        if self.gris == True:
            newMatrice = np.ones([self.taille[0], self.taille[1]])
            for ligne in range(0, self.taille[0]):
                for i in range(0, self.taille[1]):
                    newMatrice[ligne][i] *= (255-int(self.pixels[ligne][i]))
        else:
            newMatrice = np.ones([self.taille[0], self.taille[1], 3], dtype=np.uint8)
            for ligne in range(0, self.taille[0]):
                for i in range(0, self.taille[1]):
                    newMatrice[ligne][i][0] *= 255-int(self.pixels[ligne][i][0])
                    newMatrice[ligne][i][1] *= 255-int(self.pixels[ligne][i][1])
                    newMatrice[ligne][i][2] *= 255-int(self.pixels[ligne][i][2])
        self.changer(newMatrice)
        
    def seuillage(self, var, value=0):
        if self.ouvert == False:
            tkMessageBox.showerror("Erreur", "Erreur : Pas d'image chargée")
        else:
            if self.gris == True:
                if var != 0:
                    value = var.get()
                newMatrice = np.ones([self.taille[0], self.taille[1]])
                for ligne in range(0, self.taille[0]):
                    for i in range(0, self.taille[1]):
                            if self.pixels[ligne][i] <= value:
                                valeurPixel = 0
                            elif self.pixels[ligne][i] > value:
                                valeurPixel = 255
                            newMatrice[ligne][i] *= valeurPixel
                self.changer(newMatrice)
            else:
                tkMessageBox.showerror("Erreur", "Erreur : Image en Couleur")
                
    def seuillageMaxVariance(self):
        if self.ouvert == False:
            tkMessageBox.showerror("Erreur", "Erreur : Pas d'image chargée")
        else:
            if self.gris == True:
                class sAuto:
                    def __init__(self):
                        self.M = 0.0
                        self.N = 0.0

                S0 = sAuto()
                S1 = sAuto()
                S = 128
                Y=[]
                x=0
                Y = [0] * 256
                for ligne in range(0, self.taille[0]):
                    for col in range(0, self.taille[1]):
                        Y[int(self.pixels[ligne][col])] += 1
                it = 2
                while it < 8 :  
                    it *= 2
                    S0.M, S0.N, S1.M, S1.N = 0.0, 0.0, 0.0, 0.0
                    for i in Y[:S]:
                        S0.N += i
                    for y in Y[S+1:]:
                        S1.N += y
                    z = 0
                    while z<=S:
                        S0.M += z*Y[z]
                        z+=1
                    S0.M /= S0.N
                    z=S+1
                    while z<=255:
                        S1.M += z*Y[z]
                        z+=1
                    S1.M /= S1.N
                    if S < (S0.M+S1.M)/2:
                        S += 256//it
                    elif S < (S0.M+S1.M)/2:
                        S -= 256//it
                    print S
                self.seuillage(0,S)
            else:
                tkMessageBox.showerror("Erreur", "Erreur : Image en Couleur")

    def histogramme(self):
        if self.ouvert == False:
            tkMessageBox.showerror("Erreur", "Erreur : Pas d'image chargée")
        else:
            if self.gris == True:
                X=range(256)
                Y=[]
                x=0
                while x < 256:
                    Y.append(0)
                    x+=1
                for ligne in range(0, self.taille[0]):
                    for col in range(0, self.taille[1]):
                        Y[int(self.pixels[ligne][col])] += 1
                plt.plot(X,Y)
            else:
                tkMessageBox.showerror("Erreur", "Erreur : Image en Couleur")
        
    def retourArriere(self):
        if self.historique == []:
            tkMessageBox.showerror("Erreur", "Erreur : Pas d'image précédente")
        else :
            while np.array_equal(self.pixels, self.historique[-1]) :
                    self.historique.pop(-1)
                    if self.historique == []:
                        tkMessageBox.showerror("Erreur", "Erreur : Pas d'image précédente")
                        return
            self.changer(self.historique[-1])
            self.historique.pop(-1)
            print self.pixels[5][5]
            print type(self.pixels[5][5])
            self.gris = self.verifGris()
            print self.gris


# Initialisation de la fenêtre et variables
fenetre = Tk()
h = fenetre.winfo_screenheight()
w = fenetre.winfo_screenwidth()
fenetre.title("Projet Python")
#fenetre.state(newstate = 'zoomed')
border = 4
img0 = cImage([192,250])
img1 = cImage([611,250])
    
# Barre Menu
barreMenu = Menu(fenetre)
menuFichier = Menu(barreMenu, tearoff=0)
barreMenu.add_cascade(label="Fichier", menu=menuFichier)
menuFichier.add_command(label="Ouvrir", command=img0.chargerImage)
menuFichier.add_command(label="Enregistrer sous...", command=img0.enregistrerImage)
menuFichier.add_separator()
menuFichier.add_command(label="Quitter", command=fenetre.destroy)
fenetre.config(menu=barreMenu)

# Canvas + Boutons
zoneDessin = Canvas(fenetre, width=800, height=500, bg="black")
zoneDessin.grid(row=0, column=0, rowspan=4, sticky="w")
zoneDessin.create_text(200,50, text="Image Originale", font='Arial 20')
zoneDessin.create_text(600,50, text="Image Copié", font='Arial 20')
zoneDessin.create_rectangle(100,30,300,70, width=2)
zoneDessin.create_rectangle(510,30,690,70, width=2)
boutonCopierDroite = Button(zoneDessin, text=">>", font="bold", overrelief=RIDGE, borderwidth=border, command=lambda:img1.fonctionCopier(img0))
boutonCopierDroite.pack()
boutonCopierDroite.place(x=383,y=190)
boutonCopierGauche=Button(zoneDessin, text="<<", font="bold", overrelief=RIDGE, borderwidth=border, command=lambda:img0.fonctionCopier(img1))
boutonCopierGauche.pack()
boutonCopierGauche.place(x=383,y=260)

# Filtres
listeFiltre = LabelFrame(fenetre,text="Filtres")
listeFiltre.grid(row=0, column=1)
listeOption = ("Filtre Moyen", "Filtre Gaussien", "Filtre de Prewitt", "Filtre Laplacien", "Filtre Médian", "Filtre Négatif", "Filtre Gris")
varFiltre = StringVar()
varFiltre.set(listeOption[6])
optionMenu = OptionMenu(listeFiltre,varFiltre,*listeOption)
optionMenu.grid(column=0, row=0, padx=20)
boutonAppliquerFiltre = Button(listeFiltre, text="Appliquer Filtre", overrelief=RIDGE, borderwidth=border, command=img1.filtres)
boutonAppliquerFiltre.grid(column=1, row=0, padx=20, pady=20)

# Seuillage
zoneSeuillage = LabelFrame(fenetre, text="Seuillage", height=150, width=400)
zoneSeuillage.grid(row=1, column=1, padx=20, pady=20)
varSeuillage = IntVar(fenetre, 0)
scale = Scale(zoneSeuillage, from_=0, to=255, length=350, orient=HORIZONTAL, resolution=1, tickinterval=20, variable=varSeuillage)
scale.grid(row=0, column=0, columnspan=2)
spinbox = Spinbox(zoneSeuillage, from_=0, to=255, increment=1, textvariable=varSeuillage, width=5)
spinbox.grid(row=0, column=2)
boutonSeuillage = Button(zoneSeuillage, text="Appliquer Seuillage", overrelief=RIDGE, borderwidth=border, command=lambda:img1.seuillage(varSeuillage))
boutonSeuillage.grid(row=1, column=0, pady=10)
boutonHistogramme = Button(zoneSeuillage, text="Histogramme",overrelief=RIDGE, borderwidth=border, command=img1.histogramme)
boutonHistogramme.grid(row=1, column=1)

# Seuillage Automatique
varSeuillageAuto = IntVar(fenetre, 0)
zoneSeuillageAuto = Frame(zoneSeuillage)
zoneSeuillageAuto.grid(row=2, column= 0, columnspan=2)
seuillageMaxVarInterclasse = Radiobutton(zoneSeuillageAuto, text="Par Variance Interclasse", overrelief=RIDGE, borderwidth=border, variable=varSeuillageAuto, value=0)
seuillageMaxVarInterclasse.grid(row=0, column=0)
seuillageMaxEntropie = Radiobutton(zoneSeuillageAuto, text="Par Variance Interclasse", overrelief=RIDGE, borderwidth=border, variable=varSeuillageAuto, value=1)
seuillageMaxEntropie.grid(row=1, column=0)
seuillageClasse = Radiobutton(zoneSeuillageAuto, text="Par Variance Interclasse", overrelief=RIDGE, borderwidth=border, variable=varSeuillageAuto, value=2)
seuillageClasse.grid(row=2, column=0)
boutonSeuillageAuto = Button(zoneSeuillageAuto, text="Seuillage Automatique", overrelief=RIDGE, borderwidth=border, command=img1.seuillageMaxVariance)
boutonSeuillageAuto.grid(row=1, column=1)

# Autres
zoneAutres = LabelFrame(fenetre, text="Autres", height=150, width=400)
zoneAutres.grid(row=2, column=1, padx=20, pady=20)
boutonRetourArriere = Button(zoneAutres, text="Retour Arrière", overrelief=RIDGE, borderwidth=border, command=img1.retourArriere)
boutonRetourArriere.grid(row=0, column=0, padx=20, pady=20)
fenetre.mainloop()

