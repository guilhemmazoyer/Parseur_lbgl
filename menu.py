# -*- coding : utf-8 -*-

import os, re

class Menu:

    # constructeur
    def __init__(self, path):
        self.listPdf = self.makeListAll(path)

    
    # créer la liste des pdf
    def makeListAll(self, path):
        return sorted([_ for _ in os.listdir(path) if _.endswith(r".pdf")])

    # retourne la liste des pfd choisis par l'utilisateur
    # IL N'Y A PAS DE VERIFICATION (a utiliser après la méthode checkInputList)
    def makeListChosen(self, filesNumbers):
        if filesNumbers == "*": # tous les fichiers
            return self.listPdf
        listeIndex = filesNumbers.split()
        liste = [] # liste des fichiers selectionnés
        for i in listeIndex:
            if re.match(r"\d+-\d+", i): # on trouve un tiret (bornes)
                values = i.split("-")
                v0, v1 = int(values[0]), int(values[1])
                temp = list(self.listPdf[v0-1:v1])
                for file in temp:
                    liste.append(file)
            else: # on trouve un simple numéro
                liste.append(self.listPdf[int(i)-1])
        # suppression de doublon
        return list(set(liste)) # suppression de doublons eventuels

    # vérifie la validité de l'input de l'utilisateur
    def checkInputList(self, filesNumbers):
        if filesNumbers == "*": # tous les fichiers
            return True
        listeIndex = filesNumbers.split()
        for i in listeIndex:
            if re.match(r"\d+-\d+", i): # on trouve un tiret (bornes)
                values = i.split("-")
                try:
                    v0, v1 = int(values[0]), int(values[1]) # verification conversion
                    if v0 > v1: # verification ordre
                        return False
                except ValueError:
                    return False
            else: # on trouve un simple numéro
                try:
                    i = int(i)
                    if i < 0 or i > len(self.listPdf): # verification validité de l'index
                        return False
                except ValueError:
                    return False
        return True
        

    # affiche la liste de tous les pdf
    def lsPdf(self):
        #length = len(max(self.listPdf, key=len))
        cptLine = 1
        for i in range(len(self.listPdf)):
            if cptLine < 3:
                print( "{:<40}".format(self.printPdf(i+1, self.listPdf[i])), end="")
                cptLine+=1
                if i == len(self.listPdf)-1:
                    print("\n")
            else:
                print( "{:<40}".format(self.printPdf(i+1, self.listPdf[i])))
                cptLine = 1
                



        
    # affiche un seul pdf avec son indice
    def printPdf(self, number, nameFile):
        return str(number)+". "+nameFile

