# -*- coding : utf-8 -*-

from lib2to3.pgen2.token import OP
from toTXT import ToTXT
from toXML import ToXML
import sys, time, os
import multiprocessing
from multiprocessing import Pool

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
    if option is not None and option != '-t' and option !='-x':
        return False
    else:
        return True

def setupOptions():
    # assistance
    if FOLDER == '-h' or FOLDER == "help":
        helpPDFtoFiles()

    # cas de dossier invalide
    elif checkFolderExist() == False:
        print("Program cannot find \"" + FOLDER + "\"")
        print("For more information : python3 launch.py -h")

    # cas d'option invalide
    elif checkOption(OPTION) == False:
        print("Invalid option \"" + OPTION + "\"")
        print("For more information : python3 launch.py -h")

    # cas valide
    else:
        # Initialise la class ToFormat
        if OPTION == '-t':
            ToTXT.__init__(ToTXT, FOLDER)
            numberTotalFiles = len(ToTXT.files)
            nbFiles=20   # nombre de fichiers traités par processus
            proc = []   # contient tous les processus à lancer
            index = 0   # index des premiers processus
            while index+nbFiles < numberTotalFiles:
                proc.append(multiprocessing.Process(target=ToTXT.allPDF, args=(ToTXT, nbFiles, index,)))
                index+=nbFiles
            # si le nombre de fichier de traité par le dernier processus est trop grand par rapport au nombre de fichier actuel / permet d'éviter de vérifer dans la boucle inutilement
            if index+nbFiles >= numberTotalFiles: 
                nbLastFiles=numberTotalFiles-index # calcule le nombre des derniers fichiers à insérer
                proc.append(multiprocessing.Process(target=ToTXT.allPDF, args=(ToTXT, nbLastFiles,index,)))
                
            #proc = [multiprocessing.Process(target=ToTXT.allPDF, args=(ToTXT, nbFiles,i,)) for i in range(0,numberTotalFiles, nbFiles)]
            for t in proc:
                t.start()
            for t in proc:
                t.join()
            
            #ToTXT.allPDF(ToTXT, numberTotalFiles)
        else:
            # TODO implémenter multiprocessing
            ToXML.__init__(ToXML, FOLDER)
            numberTotalFiles = len(ToXML.files)
            ToXML.allPDF(ToXML, numberTotalFiles)

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
start_time = time.time()

# Verification du nombre de variables et initialisation des variables en parametre
if len(sys.argv) < 2:
    helpPDFtoFiles()

elif len(sys.argv) == 2:
    FOLDER = sys.argv[1]
    OPTION = '-t'
    setupOptions()

elif len(sys.argv) == 3:
    FOLDER = sys.argv[1]
    OPTION = sys.argv[2]
    setupOptions()

else:
    helpPDFtoFiles()
