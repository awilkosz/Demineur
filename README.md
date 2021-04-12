# Démineur

Un démineur réalisé en python avec la bibliothèque graphique Tkinter. Le projet a été créé avec l'IDE Spyder.

# Règles du démineur

Le but du démineur consiste à ouvrir toutes les cases ne contenant pas de bombe dans une matrice générée aléatoirement. Une case est ouverte lors du clic de l'utilisateur sur un bouton de la matrice. Si la case ne contient pas de bombe, un chiffre apparait, ce chiffre signifie qu'une bombe se situe dans l'une des huit cases autour de la case ouverte.

Le joueur, peut poser un drapeau sur une case avec le clic droit de la souris, ce drapeau sert de repère au joueur afin de marquer les emplacement ou une bombe pourrait se trouver. Lorsqu'une case est marquée, il est impossible de l'ouvrir avec le clic gauche. Si l'utilisateur souhaite retirer le marqueur, il doit refaire un clic droit sur la case marquée, un point d'interrogation apparait. Le point d'interrogation peut signifier que le joueur hésite entre entre plusieurs cases à propos de la présence d'une bombe. Il est important de noter qu'il est possible de cliquer sur un bouton avec un point d'interrogation).

Un autre clic droit retire le point d'interrogation. Si le joueur clique sur une case vide, (qui n'est pas entourée par une bombe), les cases aux alentours ne contenant pas de bombes sont révélées, ce processus se répète pour chaque cases vide révélées.

La partie se termine lorsque le joueur a cliqué sur une bombe, (dans ce cas toutes les bombes de la matrice sont révélées) ou lorsque le joueur a cliqué sur toutes les cases ne contenant pas de bombes, dans ce cas, le joueur remporte la partie.

# Contenu 

Le projet contient un fichier DEMINEUR.py contenant le code du démineur, un dossier d'images contenant l'image utilisée pour afficher les bombes en cas de défaite, et un fichier drawio contenant la maquette du démineur, les règles du jeu, et son pseudo code.

# Contexte

J'ai réalisé ce projet au cours de mon Titre Professionnel Concepteur Développeur d'Applications. Je n'ai eu que quelques jours pour réaliser la totalité du projet, avec sa maquette, et son pseudo code. Un défaut subsiste au rendu final du projet, si un utilisateur ouvre toutes les cases d'une même ligne, ou d'une même colonne, la fenêtre du jeu se réduit pour chaque ligne / colonne; je n'ai jamais réussi à corriger ce problème.
