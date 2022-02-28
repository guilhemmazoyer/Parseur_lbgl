<h1>Parseur_LLBG</h1>
<h2>Parseur d'articles scientifiques du format pdf au format texte.</h2>

<h3 style="text-decoration:underline">1.Installations</h3>

<p>Afin de pouvoir profiter de ce programme vous devrez installer PyMuPDF :</p>
<div style="color: #eeeeee; font-family: consolas; overflow:auto; width:auto; background: #111827; padding:1%; border-radius: 0.5em;">
    <span>pip install PyMuPDF</span>
</div>
<hr>
<p>Si votre version de pip n'est pas à jour :</p>
<div style="color: #eeeeee; font-family: consolas; overflow:auto; width:auto; background: #111827; padding:1%; border-radius: 0.5em;">
    <span>pip install --upgrade pip</span>
</div>

<h3 style="text-decoration:underline">2.Exécution</h3>
<p>
    Le programme nécessite en paramètre le dossier dans lequel sont rangés les fichiers au format PDF à modifier.
    <br>Le dossier de résultat sera créer à l'emplacement donné en paramètre et rassemblera les fichiers textes générés à partir des fichier PDF.
</p>
<div style="color: #eeeeee; font-family: consolas; overflow:auto; width:auto; background: #111827; padding:1%; border-radius: 0.5em;">
    <span>Python [script_path]\pdfToTextLLBG.py [source_path]</span>
</div>

<h3 style="text-decoration:underline">3.Explication générale</h3>
<p>
    A partir du chemin du dossier source nous regardons un par un les fichiers contenus dans ce dossier. Le sous-dossier "result" est créé afin de recevoir les fichiers textes générés par le programme à partir des fichiers au format PDF.
    <br>Sur chacun des fichiers, nous vérifions s'il est au format PDF. Si c'est le cas le programme commence le traitement.
    <br>Nous commençons par récupérer le nom du fichier avec une commande système, ensuite viens au tour du titre.
    <br>Nous vérifions s'il est présent dans les méta-données du documents. S'il l'est nous vérifions s'il possède une valeur correcte. Sinon nous récupérons la première phrase/ligne du document.
    <br>Ensuite les auteurs. Nous regardons à nouveau les méta-données pour savoir si une valeur est rentrée. Sinon nous recherchons les adresses email au sein de la première page. Et après un rapide traitement des données nous extrayons le nom, prénom et/ou surnom des auteurs.
    <br>Enfin vient la partie Abstract résumant le contenu de l'article. Il se trouve toujours juste avant l'introduction et souvant précédé par un titre Abstract. en se basant sur ces quelques règles nous récupérons le texte en question.
    <br>Toutes ces informations sont stockées dans différentes variables pouvant être manipulées à notre guise. Nous les écrivons dans un fichier texte possédant le même nom que le fichier pdf source dans le dossier result.
    <br>Enfin un message s'affiche pour indiquer à l'utilisateur la fin du processus, le nombre de fichier traité et le temps d'exécution.
</p>

<h3 style="font-size:150%">Auteurs :</h3>
<ul style="color: #efefef; font-size:125%">
    <li>Guilhem Mazoyer - Maitre Scrum</li>
    <li>Baptiste Lelievre - Développeur</li>
    <li>Lucia Lebrun - Développeur</li>
    <li>Lea Schlaflang - Développeur</li>
</ul>