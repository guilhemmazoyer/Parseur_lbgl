import re, sys, os
import textmanipulation as txtmanip
from fileManager import fileManager
from textmanipulation import REGEX_ABSTRACT, REGEX_AUTHORS, REGEX_NO_ABSTRACT, REGEX_TITLE

class pdfToXML:
    folder = ""
    resFolder = ""
    manager = None


    def __init__(self,folder):
        self.folder = folder
        self.resFolder = self.folder + "/result"
        self.manager = fileManager(folder)
        self.getParts()


    def getParts(self):
        texts = self.manager.getTextFirstPage()
        metadatas = self.manager.getMetadatas()
        files = self.manager.getFiles()
        index = 0

        for text in texts:
            ### PARTIE NOM FICHIER ###
            # recuperation du nom du fichier pdf
            file_basename = os.path.basename(sys.argv[1] + '/' + files[index])
            filename_display = file_basename + '\n'

            # transformation du nom pour le futur fichier texte
            txt_basename = file_basename[0:file_basename.find('.')]

            ### PARTIE TITRE ###
            titleDisplay = self.__getTitle(metadatas, text, index)

            ### PARTIE AUTEURS ###
            authorDisplay = self.__getAuthors(metadatas, text, index)

            ### PARTIE ABSTRACT ###
            abstractDisplay = self.__getAbstract(text)

            ### PARTIE ECRITURE ###
            self.manager.writeTxt(txt_basename, filename_display, titleDisplay, authorDisplay, abstractDisplay)
            index += 1


    def __getTitle(self, metadatas, text, index):
        title = metadatas[index]["title"]
        patternCorrectTitle = r"/|\\"
        patternTitle = REGEX_TITLE
        titleDisplay = "Titre non trouvé !\n"

        # Si les metadata sont incoherentes
        if re.search(patternCorrectTitle, title) is not None:
            
            # On recupere le titre avec regex (premiere ligne)
            if re.search(patternTitle, text) is not None:
                title = re.search(patternTitle, text).group(0)
                title = txtmanip.cleanText(title)
                titleDisplay = title + '\n'
                
        else:
            titleDisplay = title + '\n'

        return titleDisplay


    def __getAuthors(self, metadatas,text, index):
        authorDisplay = ""
        author = metadatas[index]["author"]
        patternAuthors = REGEX_AUTHORS

        if author is None or author == "":
            

            if re.search(patternAuthors, text) is not None:
                authorsEmail = re.findall(patternAuthors, text)
                for author in authorsEmail:
                    email_decompose = author[0:author.find('@')]

                    if email_decompose.find('.') != -1:
                        nom = email_decompose[0:email_decompose.find('.')]
                        prenom = email_decompose[email_decompose.find('.') + 1:]
                        authorDisplay += nom + prenom + "; "
                    else:
                        authorDisplay += email_decompose + "; "

            else:
                if re.search(patternAuthors, text, re.MULTILINE) is not None:
                    authorsEmail = re.findall(patternAuthors, text, re.MULTILINE)

                    for author in authorsEmail:
                        email_decompose = author[author.find('{') + 1:author.find('}')]
                        names = re.findall("[\w]+", email_decompose)

                        for name in names:
                            authorDisplay += name + "; "
                else:
                    authorDisplay += "Auteurs non trouvés"
        else:
            author = txtmanip.cleanText(author)
            authorDisplay += author

        authorDisplay += "\n"
        return authorDisplay

    def __getAbstract(self, text):
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