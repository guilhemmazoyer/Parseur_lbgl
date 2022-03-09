import re
import textmanipulation as txtmanip
from textmanipulation import (
    REGEX_TITLE, REGEX_CORRECT_TITLE, REGEX_EMAILS,
    REGEX_MULTI_EMAILS, REGEX_ABSTRACT, REGEX_NO_ABSTRACT)

class PdfToPlainText:
    # variables utiles pour les operations
    currentFile = ""
    manager = None
    doc = []

    # variables a recuperer
    filename = ""
    title = ""
    authors = []
    emails = []
    abstract = ""
    references = []

    # Initialise le manager passe en parametre
    def __init__(self, manager):
        self.manager = manager
    
    # Processus majeur, determine tous les attributs a partir d'un fichier
    def fileProcessing(self, file):

        self.resetCoreVariables()

        self.currentFile = file
        self.doc = self.manager.openFile(self.currentFile)

        # Recupere la premiere page et les metadonnees
        text = self.getTextFirstPage()
        metadata = self.getMetadata()

        self.__setFilename()
        self.__setTitle(metadata, text)
        self.__setAuthorsAndEmails(metadata, text)
        self.__setAbstract(text)
        self.__setReferences()

    def resetCoreVariables(self):
        self.doc = []
        self.authors = []
        self.emails = []
        self.references = []

    # Recupere la page de garde de l'article
    def getTextFirstPage(self):
        # Ouverture de la premiere page du fichier .pdf
        page = self.doc.load_page(0)
        dl = page.get_displaylist()
        tp = dl.get_textpage()
        rawText = tp.extractText()

        return txtmanip.cleanText(rawText)

    # Recupere les metadonnees du fichier courant
    def getMetadata(self):
        return self.doc.metadata

    # Definit le nom du fichier
    def __setFilename(self):
        self.filename = self.manager.getFileName(self.currentFile)

    # Definit le titre de l'article
    def __setTitle(self, metadatas, text):
        title = metadatas["title"]

        if title is None or title == "":
            # On recupere le titre avec regex (premiere ligne)
            if re.search(REGEX_TITLE, text) is not None:
                title = re.search(REGEX_TITLE, text).group(0)
                title = txtmanip.cleanText(title)

        # Si les metadata sont incoherentes
        elif re.search(REGEX_CORRECT_TITLE, title) is not None:
            
            # On recupere le titre avec regex (premiere ligne)
            if re.search(REGEX_TITLE, text) is not None:
                title = re.search(REGEX_TITLE, text).group(0)
                title = txtmanip.cleanText(title)
                
        else:
            title = "Titre non trouvé !"

        self.title = title

    # Definit les auteurs et leurs emails
    def __setAuthorsAndEmails(self, metadatas, text):
        meta_author = metadatas["author"]
        type_email = self.findEmails(text)

        if meta_author is None or meta_author == "":
            if type_email == 0:
                self.authors.append("Auteurs non trouvés")

            elif type_email == 1:
                for email in self.emails:
                    email_decompose = email[0:email.find('@')]

                    if email_decompose.find('.') != -1:
                        nom = email_decompose[0:email_decompose.find('.')]
                        prenom = email_decompose[email_decompose.find('.') + 1:]
                        self.authors.append(nom + " " + prenom)
                        
                    else:
                        self.authors.append(email_decompose)

            else:
                for email in self.emails:
                    email_decompose = email[email.find('{') + 1:email.find('}')]
                    names = re.findall("[\w]+", email_decompose)

                    for name in names:
                        self.authors.append(name)
    
        else:
            meta_author = txtmanip.cleanText(meta_author)
            self.authors.append(meta_author)

    # Trouve les emails et renvoie le type de formulation de celle-ci
    def findEmails(self, text):
        if re.search(REGEX_EMAILS, text) is not None:
            self.emails = re.findall(REGEX_EMAILS, text)
            return 1

        elif re.search(REGEX_MULTI_EMAILS, text, re.MULTILINE) is not None:
            self.emails = re.search(REGEX_MULTI_EMAILS, text, re.MULTILINE)
            return 2
        
        else:
            self.emails = "Emails introuvables"
            return 0

    # Definit la partie Abstract de l'article
    def __setAbstract(self, text):
        patternAbstract = REGEX_ABSTRACT
        patternWithoutAbstract = REGEX_NO_ABSTRACT

        if re.search(patternAbstract, text) is not None:
            abstract = re.search(patternAbstract, text).group(3)
            abstractDisplay = txtmanip.cleanText(abstract)

        elif re.search(patternWithoutAbstract, text) is not None :
            abstract = re.search(patternWithoutAbstract, text).group(0)
            abstractDisplay = txtmanip.cleanText(abstract)
            
        else:
            abstractDisplay = "Abstract non trouvé !"

        return abstractDisplay

    # Definit les references de l'article
    def __setReferences(self):
        # TODO
        self.references.append("test")
