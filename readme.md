# Güdlft

Güdlft est une société qui a créé une plateforme numérique pour coordonner les compétitions de force (deadlifting, strongman) en Amérique du Nord et en Australie.

L'objectif de l'application est de rationaliser la gestion des compétitions entre les clubs (hébergement, inscriptions, frais et administration).


## Installation et exécution de l'application :

1 - Cloner le dépôt du projet à l'aide de la commande $ git clone https://github.com/isw120/P11 (vous pouvez également télécharger le code en temps qu'archive zip)

2 - Rendez-vous depuis un terminal à la racine du répertoire P11-master avec la commande ```$ cd P11-master```

3 - Créer un environnement virtuel pour le projet avec ```$ python -m venv env``` sous windows ou ```$ python3 -m venv env``` sous macos ou linux.

4 - Activez l'environnement virtuel avec ```$ env\Scripts\activate``` sous windows ou ```$ source env/bin/activate``` sous macos ou linux.

5 - Installez les dépendances du projet avec la commande ```$ pip install -r requirements.txt```

6 - Lancez le serveur flask avec la commande : ```$env:FLASK_APP = "server.py"``` ensuite ```python -m flask run```


### Rapport de test : 

Pour lancer le test utilisez la commande : ```pytest```

Pour générer une couverture de code utilisez la commande : ```pytest --cov-report html:cov_html --cov=.```

### Rapport de performances :

Pour lancer le rapport de performances utilisez la commande : ```locust```
