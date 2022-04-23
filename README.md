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
python ./launch.py
```
### Menu

1- Choix de l'option:
    - x : fichiers résultats en format xml (.xml)
    - t : fichiers résultats en format texte (.txt)
    - h : affichage de l'aide

2- Choix du dossier contenant les fichiers pdf à extraire et dans lequel sera généré un dossier contenant les fichiers résultats:
    indiquez le chemin absolu ou le chemin relatif du dossier

3- Affichage des fichiers pdf numérotés

4- Saisie des fichiers à parser sur une ligne et séparés d'un espace par sélection:
    - pour sélectionner un seul fichier : 
        saisir un numéro correspondant à un fichier pdf
    - pour sélectionner plusieurs fichiers :
        saisir deux numéros qui seront séparés par un tiret ("-")
        le premier numéro doit être plus petit que le second
        les deux numéros de fichiers sont inclus dans la sélection
    - pour sélectionner tous les fichiers :
        saisir UNIQUEMENT le symbole d'étoile ("*")

Exemples de saisie valide de fichiers dans un dossier contenant 20 fichiers pdf:
    "2 5 3 10-15" : sélection des fichiers 2 5 3 10 11 12 13 14 15
    "*" : sélection des 20 fichiers


