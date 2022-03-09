# Parseur_LLBG
Parseur d'articles scientifiques du format pdf au format texte ou xml.

## Auteurs
 - Guilhem Mazoyer - Maitre Scrum
 - Baptiste Lelievre - Développeur
 - Lucia Lebrun - Développeur
 - Lea Schlaflang - Développeur

## Installation

### Python3

Ce programme est écrit en [python3](https://www.python.org/downloads/).

### Librairies

Il vous faudra au minimum pip3 pour pouvoir installer les librairies suivantes :

```
sudo apt install python3-pip
```

PyMuPDF
```
pip install PyMuPDF
```

## Utilisation

```
python ./launch.py <folder> [Option]
```
### Folder

- Le programme nécessite en paramètre le dossier dans lequel sont rangés les fichiers au format PDF à extraire. 
- Le dossier de résultat sera créé à cette emplacement donné en paramètre et rassemblera les fichiers résultats générés à partir des fichiers au format PDF.

### Options

- -x : Le fichier résultat sera un .xml
- -t : Le fichier résultat sera un .txt

