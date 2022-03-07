# **Parseur_LLBG**
## Parseur d'articles scientifiques du format pdf au format texte ou xml.
<br>

## **1.Installations**

Afin de pouvoir profiter de ce programme vous devrez installer PyMuPDF :

>`$ pip install PyMuPDF`

Si votre version de pip n'est pas à jour :

>`$ pip install --upgrade pip`

<br>
<hr>
<br>

## **2.Exécution**

Le programme nécessite en paramètre le dossier dans lequel sont rangés les fichiers au format PDF à modifier. 
<br>Le dossier de résultat sera créer à l'emplacement donné en paramètre et rassemblera les fichiers textes générés à partir des fichier PDF.

>`$ Python <script_path>\launch.py <Folder path> [Option]`

<br>
<hr>
<br>

## **3. Explication générale**

A partir du chemin du dossier source nous regardons un par un les fichiers contenus dans ce dossier. Le sous-dossier "result" est créé afin de recevoir les fichiers textes générés par le programme à partir des fichiers au format PDF.
<br>Sur chacun des fichiers, nous vérifions s'il est au format PDF. Si c'est le cas le programme commence le traitement.
<br>Nous commençons par récupérer le nom du fichier avec une commande système, ensuite viens au tour du titre.
<br>Nous vérifions s'il est présent dans les méta-données du documents. S'il l'est nous vérifions s'il possède une valeur correcte. Sinon nous récupérons la première phrase/ligne du document.
<br>Ensuite les auteurs. Nous regardons à nouveau les méta-données pour savoir si une valeur est rentrée. Sinon nous recherchons les adresses email au sein de la première page. Et après un rapide traitement des données nous extrayons le nom, prénom et/ou surnom des auteurs.
<br>Enfin vient la partie Abstract résumant le contenu de l'article. Il se trouve toujours juste avant l'introduction et souvant précédé par un titre Abstract. en se basant sur ces quelques règles nous récupérons le texte en question.
<br>Toutes ces informations sont stockées dans différentes variables pouvant être manipulées à notre guise. Nous les écrivons dans un fichier texte possédant le même nom que le fichier pdf source dans le dossier result.
<br>Enfin un message s'affiche pour indiquer à l'utilisateur la fin du processus, le nombre de fichier traité et le temps d'exécution.

<br>
<hr>
<br>

## **Auteurs :**
 - Guilhem Mazoyer - Maitre Scrum
 - Baptiste Lelievre - Développeur
 - Lucia Lebrun - Développeur
 - Lea Schlaflang - Développeur
