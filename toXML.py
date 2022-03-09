import os
import textmanipulation as txtmanip
import progressbar as pbar
from fileManager import FileManager as fM
from PdfToPlainText import PdfToPlainText
from progressbar import ProgressBar as pbar

class ToXML:
    folder = ""
    files = []
    manager = None
    pdfTPT = None

    def __init__(self,folder):
        # Variable instanciee a partir des parametres
        self.folder = folder

        # Initialisations de FileManager et PdfToPlainText
        self.manager = fM(self.folder)
        self.pdfTPT = PdfToPlainText(self.manager)

        # Creer le dossier resultat
        self.manager.createResultFolder()

        # Recuperation des fichiers
        files = os.listdir(self.folder)
        files = filter(lambda f: f.endswith(('.pdf', '.PDF')), files)
        self.files = list(files)

    def allPDF(self, numberTotalFiles):
        progressBar = pbar(numberTotalFiles)
        index = 0
        progressBar.progress(index)
        for file in self.files:
            self.pdfTPT.fileProcessing(file)
            result = txtmanip.arrangeXML(self.pdfTPT)
            self.manager.writeXML(self.pdfTPT, result)
            progressBar.progress(index)
            index += 1
        progressBar.progress(index)
