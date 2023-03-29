# COMMunication InformaTion System (COMMITS)

### Attention, ceci est un projet réalisé dans le cadre de l'UE LU1IN021 à Sorbonne Université, aucune garantie concernant le fonctionnement du code et la documentation n'est donnée !

PROJET : 

Nom de projet : COMMunication InformaTion System (COMMITS)

By : Jules P. & Alejandra M.

Monitoring de statistiques utiles dans la gestion d'un local et lever d'alertes lors du dépassement de valeurs définies
avec avertissement auprès des utilisateurs.

Ce projet à été conçu avec un Raspberry Pi 4 et des capteurs Grove. 

# PREREQUIS : 

--> Installer la bibliothèque python supplémentaire suivante :
- influxdb

Les autres bibliothèques sont normalement inclues avec l'image fournie avec le Raspberry Pi.

--> Installer Grafana et InfluxDB sur le RPI


#### InfluxDB

sudo apt update
sudo apt upgrade -y

wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -
source /etc/os-release
echo "deb https://repos.influxdata.com/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/influxdb.list

sudo apt update && sudo apt install -y influxdb

sudo systemctl unmask influxdb.service
sudo systemctl start influxdb
sudo systemctl enable influxdb.service

--> Enter in InfluxDB with "influx"

create database local
use local

create user grafana with password 'unmdppourAlias' with all privileges
grant all privileges on local to grafana

show users


--> Retour attendu :

user admin

\---- -----

grafana true

#### Grafana

wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list

sudo apt update && sudo apt install -y grafana

sudo systemctl unmask grafana-server.service
sudo systemctl start grafana-server
sudo systemctl enable grafana-server.service


-----> More information on this useful blog : https://simonhearne.com/2020/pi-influx-grafana/

Configurer comme souhaité l'affchage graphique des données et remplacer l'URL pour l'embed dans le fichier HTML

Changer les paramètres aux valeurs suivantes dnas le fichier /etc/grafana/grafana.ini
/!\ Enlevez les ; pour activer les lignes et grafana doit être redémarrez pour prendre en compte les nouveaux paramètres.

\----------------------------

allow_embedding = true

\[auth.anonymous]

\# enable anonymous access

enabled = true

\----------------------------


# DESCRIPTION DU CONTENU ET DE LA REPARTITION DU CODE :

-> static/css : feuilles du styles de la page web
-> templates : code source de la page web

-> main.py : code principale de l'affichage des données et appels des autres fonctions utiles
-> sensors.py : fonctions permettant la collecte des données et l'interaction avec les capteurs
-> discord_alert.py : fonction pour l'émission d'une requête pour afficher une alerte sur Discord
-> collect.py : fonctions pour l'interaction avec la base de donnée (enregistrement ou lecture)
-> web.py : code avec Flask pour rendre la page web, collecter et afficher les données dessus
