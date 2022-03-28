import os

class Menu:

    # constructeur
    def __init__(self, path):
        self.listPdf = self.makeList(path)

    
    # créer la liste des pdf
    def makeList(self, path):
        return sorted([_ for _ in os.listdir(path) if _.endswith(r".pdf")])
        

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

