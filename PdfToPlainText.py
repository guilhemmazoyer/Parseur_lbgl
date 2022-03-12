# -*- coding : utf-8 -*-

import re
import textmanipulation as txtmanip
from textmanipulation import (
    REGEX_TABREFERENCES, REGEX_TITLE, REGEX_INCORRECT_TITLE, REGEX_EMAILS,
    REGEX_MULTI_EMAILS, REGEX_ABSTRACT, REGEX_NO_ABSTRACT,
    REGEX_REFERENCES)

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

    # Recupere la derniere page de l'article
    def getTextLastPage(self):
        # Ouverture de la premiere page du fichier .pdf
        page = self.doc.load_page(self.getNbPages()-1)
        dl = page.get_displaylist()
        tp = dl.get_textpage()
        rawText = tp.extractText()

        return txtmanip.cleanText(rawText)

    def getTextAnyPage(self, nb):
        # Ouverture de la nb page du fichier .pdf
        try:
            page = self.doc.load_page(nb)
            dl = page.get_displaylist()
            tp = dl.get_textpage()
            rawText = tp.extractText()

            return txtmanip.cleanText(rawText)
        except IndexError:
            print("erreur de numéro de numéro de page")

    
    # retourn le nombre de page dans le document
    def getNbPages(self):
        return self.doc.page_count


    # Recupere les metadonnees du fichier courant
    def getMetadata(self):
        return self.doc.metadata

    # Definit le nom du fichier
    def __setFilename(self):
        file_basename = self.manager.getFileName(self.currentFile)
        self.filename = file_basename[0:file_basename.find('.')]

    # Definit le titre de l'article
    def __setTitle(self, metadatas, text):
        title = metadatas["title"]

        # Si metadata vide ou incorrect
        if title is None or title == "" or re.search(REGEX_INCORRECT_TITLE, title) is not None:
            # On recupere le titre avec regex (premiere ligne)
            if re.search(REGEX_TITLE, text) is not None:
                title = re.search(REGEX_TITLE, text).group(0)
                title = txtmanip.cleanText(title)
            else:
                title = "Titre non trouvé"

        self.title = title

    # Definit les auteurs et leurs emails
    def __setAuthorsAndEmails(self, metadatas, text):
        meta_author = metadatas["author"]
        type_email = self.findEmails(text)

        if meta_author is None or meta_author == "":
            if type_email == 0:
                self.authors.append("Auteur non trouvé")

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
            
            self.authors = txtmanip.authorFormat(self.authors)

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
            self.emails.append("Email non trouvé")
            return 0

    # Definit la partie Abstract de l'article
    def __setAbstract(self, text):
        if re.search(REGEX_ABSTRACT, text) is not None:
            abstract = re.search(REGEX_ABSTRACT, text).group(3)
            abstract = txtmanip.cleanText(abstract)

        elif re.search(REGEX_NO_ABSTRACT, text) is not None :
            abstract = re.search(REGEX_NO_ABSTRACT, text).group(0)
            abstract = txtmanip.cleanText(abstract)
            
        else:
            abstract = "Abstract non trouvé"

        self.abstract = abstract

    # Definit les references de l'article
    def __setReferences(self):
        text = ""
        textTest = ""
        # On part de la derniere page
        for pages in range(self.getNbPages()-1, 0, -1):
            textTest = self.getTextAnyPage(pages)
            if re.search(REGEX_REFERENCES, textTest) is not None: # trouve le mot references
                text = re.search(REGEX_REFERENCES, textTest).group(1) + ' ' + text + ' ' # on ajoute au début a partir du mot references
                text = txtmanip.cleanText(text)
                if re.search(REGEX_TABREFERENCES, text) is not None: # verification de crochets
                    tab_ref = re.split(REGEX_TABREFERENCES, text)
                    if tab_ref[0] == '':
                        del tab_ref[0]
                    self.references = tab_ref
                else: # ajout d'une simple chaine de caractere
                    self.references.append(text)
                break # on stop le parcours de pagess
            else: # mot references non trouve, on ajout le texte au debut
                text = textTest+' '+text+' '
        

