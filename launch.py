# -*- coding : utf-8 -*-

from toTXT import ToTXT
from toXML import ToXML
import sys, time, os
from progressbar import ProgressBar as pbar
import multiprocessing
from menu import Menu

# Affichage de l'assistance
def helpPDFtoFiles():
    print("\npython3 launch.py")
    print("\tChoice of option:")
    print("\t\tx Parser from .pdf to .xml files")
    print("\t\tt Parser from .pdf to .txt files")
    print("\t\th for help")
    print("\tFolder path:")
    print("\t\tExact or relative path")
    print("\tInput file numbers:")
    print("\t\tOne file:")
    print("\t\t\tEnter a number matching with a pdf file")
    print("\t\tSeveral files:")
    print("\t\t\tEnter two numbers separate by a dash ('-')")    
    print("\t\t\tThe two numbers are include in the selection")
    print("\t\tAll files:")
    print("\t\t\tEnter ONLY '*'")



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

# Verification du nombre de variables et initialisation des variables en parametre
OPTION = ""
FOLDER = ""
FILES = []
if len(sys.argv) != 1:
    helpPDFtoFiles()
else:
    OPTION = input("Output type / Option (x : xml / t : txt / h : help): ")
    while OPTION != "t" and OPTION != "x" and OPTION != "h":
        print("Wrong option")
        OPTION = input("Output type / Option (x : xml / t : txt / h : help): ")
    if OPTION == "h":
        helpPDFtoFiles()
    else:
        FOLDER = input("Path that contains the folder to parse: ")
        while not checkFolderExist() or sorted([_ for _ in os.listdir(FOLDER) if _.endswith(r".pdf")]) == []:
            print("Pathname not valid")
            FOLDER = input("Path that contains the folder to parse: ")
        menu = Menu(FOLDER)
        menu.lsPdf()
        numbers = input("Enter the file numbers: ")
        while not menu.checkInputList(numbers):
            print("File numbers not valid")
            numbers = input("Enter the file numbers: ")
        FILES = menu.makeListChosen(numbers)
        print(FILES)
        # Heure et index initial
        start_time = time.time()
        
        setupOptions()


