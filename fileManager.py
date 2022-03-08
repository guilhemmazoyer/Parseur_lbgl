import fitz
import os, shutil, platform

class FileManager:
    OS_NAME = False
    folder = ""
    resFolder = ""
    files = []

    def __init__(self, folder):
        self.folder = folder
        
        # Recuperation du systeme d'exploitation, True si "Windows", False sinon
        self.OS_NAME = (platform.system() == "Windows")

        # Chemin vers le fichier de resultat
        if self.OS_NAME:
            self.resFolder = folder + "\\" + "result"
        else:
            self.resFolder = folder + "/" + "result"

    # Creer un dossier "result" dans le dossier source
    def createResultFolder(self):
        if os.path.exists(self.resFolder):
            shutil.rmtree(self.resFolder)
        os.mkdir(self.resFolder)

    #
    def openFile(self, file):
        if self.OS_NAME:
            return fitz.open(self.folder + "\\" + file)
        else:
            return fitz.open(self.folder + "/" + file)

    def getFileName(self, file):
        if self.OS_NAME:
            file_basename = os.path.basename(self.folder + "\\" + file)
        else:
            file_basename = os.path.basename(self.folder + "/" + file)
        
        return file_basename[0:file_basename.find('.')]

    #
    def writeTxt(self, result):
        # Creation et ouverture du fichier .txt
        txtFileToFill = open(self.resFolder + '/' + txt_basename + ".txt", "w+")

        # Ecriture du nom du fichier, du titre, des auteurs et de l'abstract
        txtFileToFill.write(result)

        # Fermeture du fichier
        txtFileToFill.close()

    #
    def writeXML(self, result):
        # Creation et ouverture du fichier .txt
        txtFileToFill = open(self.resFolder + '/' + txt_basename + ".xml", "w+")

        # Ecriture du nom du fichier, du titre, des auteurs et de l'abstract
        txtFileToFill.write(result)

        # Fermeture du fichier
        txtFileToFill.close()
    
    def pdfFilesProcessing(self):
        # Créer le dossier result
        self.resFolder = self.folder + "/result"
        self.createResultFolder(self)

        # TODO

    def pdfFilesProcessingWindows(self):
         # Créer le dossier result
        self.resFolder = self.folder + "\result"
        self.createResultFolder(self)

        # TODO