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
$ pip install PyMuPDF
```

## Utilisation

- Le programme nécessite en paramètre le dossier dans lequel sont rangés les fichiers au format PDF à modifier. 
- Le dossier de résultat sera créer à l'emplacement donné en paramètre et rassemblera les fichiers textes générés à partir des fichier PDF.

```
$ Python ./launch.py <folder> [Option]
```

### Options

- -x : Le fichier résultat sera un .xml
- -t : Le fichier résultat sera un .txt

