# Fonctionnement

1. A partir du chemin du dossier source nous regardons un par un les fichiers contenus dans ce dossier. Le sous-dossier "result" est créé afin de recevoir les fichiers textes générés par le programme à partir des fichiers au format PDF.
2. Sur chacun des fichiers, nous vérifions s'il est au format PDF. Si c'est le cas le programme commence le traitement.
3. Nous commençons par récupérer le nom du fichier avec une commande système, ensuite viens au tour du titre.
4. Nous vérifions s'il est présent dans les méta-données du documents. S'il l'est nous vérifions s'il possède une valeur correcte. Sinon nous récupérons la première phrase/ligne du document.
5. Ensuite les auteurs. Nous regardons à nouveau les méta-données pour savoir si une valeur est rentrée. Sinon nous recherchons les adresses email au sein de la première page. Et après un rapide traitement des données nous extrayons le nom, prénom et/ou surnom des auteurs.
6. Enfin vient la partie Abstract résumant le contenu de l'article. Il se trouve toujours juste avant l'introduction et souvant précédé par un titre Abstract. en se basant sur ces quelques règles nous récupérons le texte en question.
7. Toutes ces informations sont stockées dans différentes variables pouvant être manipulées à notre guise. Nous les écrivons dans un fichier texte possédant le même nom que le fichier pdf source dans le dossier result.
8. Enfin un message s'affiche pour indiquer à l'utilisateur la fin du processus, le nombre de fichier traité et le temps d'exécution.