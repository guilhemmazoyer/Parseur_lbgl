from lib2to3.pgen2.token import OP
from fileManager import fileManager as fM
# from pdfToTxt import pdfToTxt
# from pdfToXML import pdfToXML
import sys, platform, time, os

# Affichage de l'assistance
def helpPDFtoFiles():
    # TODO
    print("")

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

# Recuperation du systeme d'exploitation, True si "Windows", False sinon
OS_NAME = (platform.system() == "Windows")

# Verification de l'existence du dossier rentre en parametre
FOLDER_EXIST = os.path.exists(FOLDER)

# assistance
if FOLDER == '-h' or FOLDER == "help":
    helpPDFtoFiles()

# cas de dossier invalide
elif FOLDER_EXIST == False:
    print("Dossier inexistant")
    print("Pour plus d'informations : Python launch.py -h")

# cas d'option invalide
elif OPTION is not None and OPTION != '-t' and OPTION !='-x':
    print("Option invalide")
    print("Pour plus d'informations : Python launch.py -h")

# cas valide
else:
    # Initialise la class fileManager
    fM.__init__(FOLDER, OPTION)
    if OS_NAME:
        fM.pdfFilesProcessingWindows()
    else:
        fM.pdfFilesProcessing()

    # Calcul de la duree du programme
    interval = time.time() - start_time

    # Affichage de fin de programme
    print('\n' + "Execution de pdfParser termine")
    print('\t' + str(fM.getIndex()) + " fichiers traites")
    print('\t' + "Realise en " + str(interval) + " secondes" + '\n')