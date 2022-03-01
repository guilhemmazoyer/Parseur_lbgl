from lib2to3.pgen2.token import OP
from pdfToTxt import pdfToTxt
import sys

FOLDER = sys.argv[1]
OPTION = sys.argv[2]

if OPTION == '-t':
    pdfToTxt(FOLDER)
    print("Analyse terminé !")
elif OPTION == '-x':
    pass
else:
    print("options inconnu !")