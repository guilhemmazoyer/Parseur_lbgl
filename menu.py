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
    def makeListChosen(self, numbers):
        print(numbers)
        listeIndex = numbers.split()
        liste = []
        for i in listeIndex:
            if re.match(r"\d+-\d+", i):
                #split
                values = i.split("-")
                l = list(self.listPdf[int(values[0])-1:int(values[1])])
                for f in l:
                    liste.append(f)
            elif is_integer(i):
                liste.append(self.listPdf[int(i)-1])
        print(liste)
        return liste
        

    # affiche la liste de tous les pdf
    def lsPdf(self):
        length = len(max(self.listPdf, key=len))
        if length < 35:
            for i in range(0, len(self.listPdf), 3):
                print( "{:<40} {:<40}".format(self.printPdf(i+1, self.listPdf[i]), self.printPdf(i+2, self.listPdf[i+1])), self.printPdf(i+3, self.listPdf[i+2]) )
        else :
            for i in range(0, len(self.listPdf), 2):
                print( "{:<60} {:<60}".format(self.printPdf(i+1, self.listPdf[i]), self.printPdf(i+2, self.listPdf[i+1])) )
        
    # affiche un seul pdf avec son indice
    def printPdf(self, number, nameFile):
        return str(number)+". "+nameFile

def is_integer(n):
    return int(n)