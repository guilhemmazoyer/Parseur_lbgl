import os
import textmanipulation as txtmanip
import progressbar as pbar
from fileManager import FileManager as fM
from PdfToPlainText import PdfToPlainText

class ToXML:
    folder = ""
    files = []
    manager = None
    pdfTPT = None

    def __init__(self,folder):
        # Variable instanciee a partir des parametres
        self.folder = folder

        # Initialisations de FileManager et PdfToPlainText
        fM.__init__(fM, self.folder)
        self.manager = fM
        PdfToPlainText.__init__(PdfToPlainText, self.manager)
        self.pdfTPT = PdfToPlainText

        # Creer le dossier resultat
        self.manager.createResultFolder(self.manager)

        # Recuperation des fichiers
        files = os.listdir(self.folder)
        files = filter(lambda f: f.endswith(('.pdf', '.PDF')), files)
        self.files = list(files)

    def allPDF(self):
        total_index = len(self.files)
        index = 0
        pbar.progress(index, total_index)
        for file in self.files:
            self.pdfTPT.fileProcessing(self.pdfTPT, file)
            result = txtmanip.arrangeXML(self.pdfTPT)
            self.manager.writeXML(self.manager, self.pdfTPT, result)
        pbar.progress(index, total_index)
