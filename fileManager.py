import fitz
import os, sys, shutil, platform

class FileManager:
    OS_NAME = False
    folder = ""
    resFolder = ""
    option = ""
    index = 0
    files = []

    def __init__(self, folder, option):
        self.folder = folder
        self.option = option
        
        # Recuperation du systeme d'exploitation, True si "Windows", False sinon
        self.OS_NAME = (platform.system() == "Windows")

    # Creer un dossier "result" dans le dossier source
    def createResultFolder(self):
        if os.path.exist(self.resFolder):
            shutil.rmtree(self.resFolder)
        os.mkdir(self.resFolder)

    # 
    def createResultFileTXT(self):
        # TODO
        print("")
    
    #
    def createResultFileXML(self):
        # TODO
        print("")

    #
    def writeTxt(self, txt_basename, filename_display, title_display , author_display, abstract_display):
        # Creation et ouverture du fichier .txt
        txtFileToFill = open(self.resFolder + '/' + txt_basename + ".txt", "w+")

        # Ecriture du nom du fichier, du titre, des auteurs et de l'abstract
        txtFileToFill.write(filename_display)
        txtFileToFill.write(title_display)
        txtFileToFill.write(author_display)
        txtFileToFill.write(abstract_display)

        # Fermeture du fichier
        txtFileToFill.close()

    #
    def writeXML(self, txt_basename, filename_display, title_display , author_display, abstract_display):
        # Creation et ouverture du fichier .xml
        txtFileToFill = open(self.resFolder + '/' + txt_basename + ".xml", "w+")

        # TODO

        # Fermeture du fichier
        txtFileToFill.close()

    def getTextFirstPage(self):
        texts = []

        for file in self.files:

            # Ouverture du fichier .pdf
            doc = fitz.open(sys.argv[1] + '/' + file)
            page = doc.load_page(0)
            dl = page.get_displaylist()
            tp = dl.get_textpage()
            texts.append(tp.extractText())
        
        return texts
    
    def getMetadatas(self):
        metadatas = []
        index = 0
        for file in self.files:
            doc = fitz.open(sys.argv[1] + '/' + file)
            metadatas.append(doc.metadata)
            self.index += 1

        return metadatas

    def getFiles(self):
        return self.files
    
    def getIndex(self):
        return self.index
    
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