from lib2to3.pgen2.token import OP
from toTXT import ToTXT
from toXML import ToXML
import sys, time, os

# Affichage de l'assistance
def helpPDFtoFiles():
    print("\nPython launch.py <Folder path> [Option]")
    print("\tFolder path:")
    print("\t\tExact or relative path")
    print("\tOption:")
    print("\t\tIf this parameter is leave blank, the option by default is -x")
    print("\t\t-x Parser from .pdf to .xml files")
    print("\t\t-t Parser from .pdf to .txt files")

# Verification de l'existence du dossier rentre en parametre
def checkFolderExist():
    return os.path.exists(FOLDER)

# Verification de l'option passée en parametre
def checkOption(option):
    if OPTION is not None and OPTION != '-t' and OPTION !='-x':
        return False
    else:
        return True

# Heure et index initial
start_time = time.time()

# Verification du nombre de variables et initialisation des variables en parametre
if len(sys.argv) < 2:
    helpPDFtoFiles()

elif len(sys.argv) == 2:
    FOLDER = sys.argv[1]
    OPTION = '-x'

elif len(sys.argv) == 3:
    FOLDER = sys.argv[1]
    OPTION = sys.argv[2]

else:
    helpPDFtoFiles()

# assistance
if FOLDER == '-h' or FOLDER == "help":
    helpPDFtoFiles()

# cas de dossier invalide
elif checkFolderExist() == False:
    print("The \"" + FOLDER + "\" folder does not exist")
    print("For more information : Python launch.py -h")

# cas d'option invalide
elif checkOption == False:
    print("Invalid option")
    print("For more information : Python launch.py -h")

# cas valide
else:
    # Initialise la class ToFormat
    if OPTION == '-t':
        ToTXT.__init__(ToTXT, FOLDER)
        ToTXT.allPDF(ToTXT)
    else:
        ToXML.__init__(ToXML, FOLDER)
        ToXML.allPDF(ToXML)

    # Calcul de la duree du programme
    interval = time.time() - start_time

    # Affichage de fin de programme
    print('\n' + "pdfParser execution completed")
    print('\t' + str(len(ToXML.files)) + " files processed")
    print('\t' + "Completed in " + str(interval) + " seconds" + '\n')