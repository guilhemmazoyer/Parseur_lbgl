# -*- coding : utf-8 -*-

from toTXT import ToTXT
from toXML import ToXML
import sys, time, os
from progressbar import ProgressBar as pbar
import multiprocessing
from menu import Menu

# Affichage de l'assistance
def helpPDFtoFiles():
    print("\npython3 launch.py <Folder path> [Option]")
    print("\tFolder path:")
    print("\t\tExact or relative path")
    print("\tOption:")
    print("\t\tIf this parameter is leave blank, the option by default is -x")
    print("\t\t-x Parser from .pdf to .xml files")
    print("\t\t-t Parser from .pdf to .txt files")

# Verification de l'existence du dossier rentre en parametre
def checkFolderExist():
    return os.path.exists(FOLDER)

# Verification de l'option passee en parametre
def checkOption(option):
    if option is not None and option != 't' and option !='x':
        return False
    else:
        return True

def setupOptions():
    # cas de dossier invalide
    if checkFolderExist() == False:
        print("Program cannot find \"" + FOLDER + "\"")
        print("For more information : python3 launch.py -h")

    # cas d'option invalide
    elif checkOption(OPTION) == False:
        print("Invalid option \"" + OPTION + "\"")
        print("For more information : python3 launch.py -h")

    # cas valide
    else:
        # supprime des warning sous Windows
        if __name__ == '__main__':
            nbFiles = 30   # nombre de fichiers traités par processus
            proc = []   # contient tous les processus à lancer
            index = 0   # index des premiers processus


            # Traitement vers fichier .txt
            if OPTION == '-t':
                txt = ToTXT(FOLDER, FILES)
                numberTotalFiles = len(txt.files)
                progressBar = pbar(numberTotalFiles)

                while index+nbFiles < numberTotalFiles:
                    proc.append(multiprocessing.Process(target=txt.allPDF, args=(nbFiles, index, progressBar)))
                    index+=nbFiles
                # si le nombre de fichiers traités par le dernier processus est trop grand par rapport au nombre de fichier actuel / permet d'éviter de vérifer dans la boucle inutilement
                if index+nbFiles >= numberTotalFiles: 
                    nbLastFiles=numberTotalFiles-index # calcule le nombre des derniers fichiers à insérer
                    proc.append(multiprocessing.Process(target=txt.allPDF, args=(nbLastFiles, index, progressBar)))
                    
                # proc = [multiprocessing.Process(target=txt.allPDF, args=(nbFiles,i)) for i in range(0,numberTotalFiles, nbFiles)]
                # txt.allPDF(numberTotalFiles)

            # Traitement vers fichier .xml
            else:
                xml = ToXML(FOLDER, FILES)
                numberTotalFiles = len(xml.files)
                progressBar = pbar(numberTotalFiles)

                while index+nbFiles < numberTotalFiles:
                    proc.append(multiprocessing.Process(target=xml.allPDF, args=(nbFiles, index, progressBar)))
                    index+=nbFiles
                # si le nombre de fichiers traités par le dernier processus est trop grand par rapport au nombre de fichier actuel / permet d'éviter de vérifer dans la boucle inutilement
                if index+nbFiles >= numberTotalFiles: 
                    nbLastFiles=numberTotalFiles-index # calcule le nombre des derniers fichiers à insérer
                    proc.append(multiprocessing.Process(target=xml.allPDF, args=(nbLastFiles, index, progressBar)))
                    
                # proc = [multiprocessing.Process(target=xml.allPDF, args=(nbFiles,i)) for i in range(0,numberTotalFiles, nbFiles)]
                # xml.allPDF(numberTotalFiles)
            
            for t in proc:
                t.start()
            for t in proc:
                t.join()
            
            progressBar.progress(numberTotalFiles)

            finishMessage(numberTotalFiles)

def finishMessage(nbrTotalFiles):
    # Calcul de la duree du programme
    interval = time.time() - start_time
    interval = round(interval, 2)

    # Affichage de fin de programme
    print('\n' + "pdfParser execution completed")
    print('\t' + str(nbrTotalFiles) + " files processed")
    print('\t' + "Completed in " + str(interval) + " seconds" + '\n')

# --- Debut du programme ---
# Heure et index initial

# Verification du nombre de variables et initialisation des variables en parametre
if len(sys.argv) > 1:
    helpPDFtoFiles()
else:
    OPTION = input("Saisir le type de sortie (x : xml / t : txt / h : aide): ")
    while OPTION != "t" and OPTION != "x" and OPTION != "h":
        print("Veuillez saisir une option valide")
        OPTION = input("Saisir le type de sortie (x : xml / t : txt / h : aide): ")
    if OPTION == "h":
        helpPDFtoFiles()
    else:
        FOLDER = input("Saisir le nom du dossier à parser : ")
        while not checkFolderExist():
            print("Nom de dossier invalide")
            FOLDER = input("Saisir le nom du dossier à parser : ")
        menu = Menu(FOLDER)
        menu.lsPdf()
        numbers = input("Saisir les numéros de fichiers : ")
        FILES = menu.makeListChosen(numbers)  # TODO files est la liste des fichiers pdf choisis par l'utilisateur, à récupérer depuis menu

        start_time = time.time()
        
        setupOptions()


