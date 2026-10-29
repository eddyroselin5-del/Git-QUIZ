import json
import random
import socket
import threading

# Configuration du serveur
# Pour sécuriser par VPN, remplacez par l'IP de votre interface VPN (ex: WireGuard/Tailscale 10.x.x.x ou 100.x.x.x)
# Mettre "0.0.0.0" écoute sur toutes les interfaces (utilisez l'IP VPN de votre machine pour restreindre).
HOST = "0.0.0.0"
PORT = 5555

# Banque de questions multi-thèmes (au moins 15 questions par thème pour supporter le Niveau 3)
QUESTION_BANK = {
    "Programmation & Réseaux": [
        {
            "q": "Quel protocole de transport garantit la livraison ordonnée des paquets ?",
            "choices": ["UDP", "TCP", "ICMP", "IP"],
            "answer": 1,
        },
        {
            "q": "En Python, quel mot-clé sert à définir une fonction anonyme ?",
            "choices": ["def", "lambda", "func", "anonymous"],
            "answer": 1,
        },
        {
            "q": "Quel port standard est utilisé par défaut pour HTTPS ?",
            "choices": ["80", "21", "443", "8080"],
            "answer": 2,
        },
        {
            "q": "Que signifie l'acronyme SQL ?",
            "choices": [
                "Structured Query Language",
                "Simple Quick Loop",
                "System Query Linux",
                "Secure Question Link",
            ],
            "answer": 0,
        },
        {
            "q": "Quel composant assure la conversion des noms de domaine en IP ?",
            "choices": ["DHCP", "DNS", "FTP", "SSH"],
            "answer": 1,
        },
        {
            "q": "Quel langage est principalement utilisé pour styliser les pages web ?",
            "choices": ["HTML", "PHP", "CSS", "Python"],
            "answer": 2,
        },
        {
            "q": "Dans quel mode de transmission les données circulent dans les deux sens simultanément ?",
            "choices": ["Simplex", "Half-Duplex", "Full-Duplex", "Multiplex"],
            "answer": 2,
        },
        {
            "q": "Quel module Python est utilisé pour créer des interfaces graphiques de base ?",
            "choices": ["pygame", "tkinter", "requests", "sqlite3"],
            "answer": 1,
        },
        {
            "q": "Quelle structure de données LIFO (Last In, First Out) utilise-t-on en programmation ?",
            "choices": ["File (Queue)", "Pile (Stack)", "Table de hachage", "Arbre"],
            "answer": 1,
        },
        {
            "q": "Quel protocole réseau est non orienté connexion sur la couche transport ?",
            "choices": ["TCP", "UDP", "HTTP", "FTP"],
            "answer": 1,
        },
        {
            "q": "Quel type de base de données est SQLite ?",
            "choices": ["Relationnelle", "NoSQL", "Orientée objet", "Distribuée"],
            "answer": 0,
        },
        {
            "q": "Comment appelle-t-on une variable déclarée à l'intérieur d'une classe en Python ?",
            "choices": [
                "Variable globale",
                "Attribut / Variable d'instance",
                "Constante",
                "Pointeur",
            ],
            "answer": 1,
        },
        {
            "q": "Quel outil permet de versionner son code source ?",
            "choices": ["Docker", "Git", "XAMPP", "Apache"],
            "answer": 1,
        },
        {
            "q": "Quelle commande Linux permet de lister les fichiers d'un dossier ?",
            "choices": ["dir", "ls", "cd", "cat"],
            "answer": 1,
        },
        {
            "q": "Quel protocole sécurisé est utilisé pour l'administration distante des serveurs ?",
            "choices": ["Telnet", "SSH", "HTTP", "FTP"],
            "answer": 1,
        },
    ],
    "Jeux Vidéo": [
        {
            "q": "Quel studio a développé le jeu à succès 'Cyberpunk 2077' ?",
            "choices": [
                "Ubisoft",
                "CD Projekt Red",
                "Bethesda",
                "Rockstar Games",
            ],
            "answer": 1,
        },
        {
            "q": "Dans quel jeu trouve-t-on le personnage de Master Chief ?",
            "choices": ["Doom", "Halo", "Mass Effect", "Destiny"],
            "answer": 1,
        },
        {
            "q": "Quel est le moteur de jeu créé par Epic Games ?",
            "choices": ["Unity", "Godot", "Unreal Engine", "CryEngine"],
            "answer": 2,
        },
        {
            "q": "En quelle année est sorti le premier jeu de la franchise Grand Theft Auto ?",
            "choices": ["1995", "1997", "2001", "1991"],
            "answer": 1,
        },
        {
            "q": "Quel jeu de type Battle Royale a popularisé le genre développé par Epic Games ?",
            "choices": ["Apex Legends", "PUBG", "Fortnite", "Call of Duty"],
            "answer": 2,
        },
        {
            "q": "Quel est le nom de la princesse à sauver dans la plupart des jeux Super Mario ?",
            "choices": ["Daisy", "Peach", "Zelda", "Rosalina"],
            "answer": 1,
        },
        {
            "q": "Quel RPG de science-fiction a été développé par Bethesda en 2023 ?",
            "choices": ["Starfield", "Skyrim", "Fallout 4", "Cyberpunk"],
            "answer": 0,
        },
        {
            "q": "Quel constructeur a créé la console portable historique Game Boy ?",
            "choices": ["Sega", "Sony", "Nintendo", "Atari"],
            "answer": 2,
        },
        {
            "q": "Dans Minecraft, quel matériau est nécessaire pour fabriquer une pioche en diamant ?",
            "choices": ["Fer", "Obsidienne", "Diamant", "Or"],
            "answer": 2,
        },
        {
            "q": "Quel est le jeu le plus vendu de tous les temps ?",
            "choices": ["GTA V", "Minecraft", "Tetris", "Wii Sports"],
            "answer": 1,
        },
        {
            "q": "Quel personnage emblématique de Sega court à une vitesse fulgurante ?",
            "choices": ["Mario", "Crash Bandicoot", "Sonic", "Spyro"],
            "answer": 2,
        },
        {
            "q": "Quel jeu de stratégie en temps réel se déroulant dans l'espace a été créé par Blizzard ?",
            "choices": ["Warcraft", "StarCraft", "Command & Conquer", "Age of Empires"],
            "answer": 1,
        },
        {
            "q": "Quel est le nom du plombier vert, frère de Mario ?",
            "choices": ["Wario", "Luigi", "Toad", "Yoshi"],
            "answer": 1,
        },
        {
            "q": "Dans quel jeu incarne-t-on Geralt de Riv ?",
            "choices": ["The Witcher", "Dark Souls", "Skyrim", "God of War"],
            "answer": 0,
        },
        {
            "q": "Quel jeu indépendant de construction et d'automatisation a été créé par Wube Software ?",
            "choices": ["Factorio", "Satisfactory", "RimWorld", "Terraria"],
            "answer": 0,
        },
    ],
    "Sciences & Tech": [
        {
            "q": "Quelle est la planète la plus proche du Soleil ?",
            "choices": ["Vénus", "Mercure", "Mars", "Jupiter"],
            "answer": 1,
        },
        {
            "q": "Quel physicien a formulé la théorie de la relativité restreinte ?",
            "choices": [
                "Isaac Newton",
                "Albert Einstein",
                "Nikola Tesla",
                "Galilée",
            ],
            "answer": 1,
        },
        {
            "q": "Quel composant est considéré comme le 'cerveau' d'un ordinateur ?",
            "choices": ["RAM", "Processeur (CPU)", "Carte mère", "Disque SSD"],
            "answer": 1,
        },
        {
            "q": "Quel gaz compose la majeure partie de l'atmosphère terrestre ?",
            "choices": ["Oxygène", "Azote (N2)", "Dioxyde de carbone", "Hydrogène"],
            "answer": 1,
        },
        {
            "q": "Quel est l'élément chimique représenté par le symbole 'Au' ?",
            "choices": ["Argent", "Or", "Aluminum", "Argon"],
            "answer": 1,
        },
        {
            "q": "En quelle année l'homme a-t-il marché sur la Lune pour la première fois ?",
            "choices": ["1965", "1969", "1971", "1973"],
            "answer": 1,
        },
        {
            "q": "Quelle est l'unité de mesure de la résistance électrique ?",
            "choices": ["Volt", "Ampère", "Ohm", "Watt"],
            "answer": 2,
        },
        {
            "q": "Quel télescope spatial lancé en 2021 a succédé à Hubble ?",
            "choices": [
                "Kepler",
                "James Webb",
                "Spitzer",
                "Chandra",
            ],
            "answer": 1,
        },
        {
            "q": "Quel est le symbole chimique du fer ?",
            "choices": ["Fe", "Ir", "F", "Fr"],
            "answer": 0,
        },
        {
            "q": "Quelle est la vitesse approximative de la lumière dans le vide (en km/s) ?",
            "choices": ["30 000", "300 000", "3 000 000", "150 000"],
            "answer": 1,
        },
        {
            "q": "Comment appelle-t-on l'étude des fossiles ?",
            "choices": ["Géologie", "Paléontologie", "Archéologie", "Zoologie"],
            "answer": 1,
        },
        {
            "q": "Quel inventeur est associé à l'ampoule électrique à incandescence industrialisée ?",
            "choices": [
                "Nikola Tesla",
                "Thomas Edison",
                "Alexander Graham Bell",
                "Guglielmo Marconi",
            ],
            "answer": 1,
        },
        {
            "q": "Quelle est la formule chimique de l'eau ?",
            "choices": ["CO2", "H2O", "NaCl", "CH4"],
            "answer": 1,
        },
        {
            "q": "Quel est le plus grand organe du corps humain ?",
            "choices": ["Le foie", "Le cœur", "La peau", "Le cerveau"],
            "answer": 2,
        },
        {
            "q": "Quel métal liquide est couramment utilisé dans les anciens thermomètres ?",
            "choices": ["Plomb", "Mercure", "Zinc", "Étain"],
            "answer": 1,
        },
    ],
    "Culture Générale": [
        {
            "q": "Quelle est la capitale de l'Australie ?",
            "choices": ["Sydney", "Melbourne", "Canberra", "Brisbane"],
            "answer": 2,
        },
        {
            "q": "Combien de pays composent l'île de Madagascar ?",
            "choices": ["1", "2", "3", "4"],
            "answer": 0,
        },
        {
            "q": "Quel peintre a peint la toile 'La Nuit étoilée' ?",
            "choices": [
                "Claude Monet",
                "Vincent van Gogh",
                "Pablo Picasso",
                "Leonardo da Vinci",
            ],
            "answer": 1,
        },
        {
            "q": "Dans quel pays se trouvent les pyramides de Gizeh ?",
            "choices": ["Mexique", "Soudan", "Égypte", "Grèce"],
            "answer": 2,
        },
        {
            "q": "Quelle est la monnaie officielle du Japon ?",
            "choices": ["Yuan", "Won", "Yen", "Ringgit"],
            "answer": 2,
        },
        {
            "q": "Quel océan est le plus grand du monde ?",
            "choices": [
                "Océan Atlantique",
                "Océan Indien",
                "Océan Pacifique",
                "Océan Arctique",
            ],
            "answer": 2,
        },
        {
            "q": "Qui a écrit le roman 'Les Misérables' ?",
            "choices": [
                "Alexandre Dumas",
                "Victor Hugo",
                "Émile Zola",
                "Albert Camus",
            ],
            "answer": 1,
        },
        {
            "q": "En quelle année a eu lieu la chute du mur de Berlin ?",
            "choices": ["1987", "1989", "1991", "1993"],
            "answer": 1,
        },
        {
            "q": "Quel est le plus long fleuve du monde (généralement admis) ?",
            "choices": ["Le Nil", "L'Amazone", "Le Mississippi", "Le Yangtsé"],
            "answer": 0,
        },
        {
            "q": "Combien de continents compte-t-on sur Terre (modèle standard à 7) ?",
            "choices": ["5", "6", "7", "8"],
            "answer": 2,
        },
        {
            "q": "Quelle est la langue officielle la plus parlée au Brésil ?",
            "choices": ["Espagnol", "Portugais", "Anglais", "Français"],
            "answer": 1,
        },
        {
            "q": "Quel pays a la forme d'une botte sur la carte ?",
            "choices": ["Espagne", "Grèce", "Italie", "Inde"],
            "answer": 2,
        },
        {
            "q": "Qui a sculpté la statue du 'Penseur' ?",
            "choices": ["Michel-Ange", "Auguste Rodin", "Donatello", "Claude Monet"],
            "answer": 1,
        },
        {
            "q": "Quel est le sommet le plus haut du monde ?",
            "choices": ["K2", "Kilimandjaro", "Mont Everest", "Mont Blanc"],
            "answer": 2,
        },
        {
            "q": "Quelle est la capitale du Canada ?",
            "choices": ["Toronto", "Vancouver", "Ottawa", "Montréal"],
            "answer": 2,
        },
    ],
    "Cinéma & Pop Culture": [
        {
            "q": "Quel réalisateur a dirigé la trilogie originale 'Le Seigneur des Anneaux' ?",
            "choices": [
                "Steven Spielberg",
                "Peter Jackson",
                "Christopher Nolan",
                "James Cameron",
            ],
            "answer": 1,
        },
        {
            "q": "Quel est le nom du vaisseau spatial de Han Solo dans Star Wars ?",
            "choices": [
                "Star Destroyer",
                "Faucon Millennium",
                "X-Wing",
                "Enterprise",
            ],
            "answer": 1,
        },
        {
            "q": "Quel film de Christopher Nolan explore les rêves imbriqués ?",
            "choices": ["Interstellar", "Tenet", "Inception", "Memento"],
            "answer": 2,
        },
        {
            "q": "Quel acteur incarne Iron Man dans l'univers cinématographique Marvel (MCU) ?",
            "choices": [
                "Chris Evans",
                "Robert Downey Jr.",
                "Mark Ruffalo",
                "Chris Hemsworth",
            ],
            "answer": 1,
        },
        {
            "q": "Dans Harry Potter, quel est le nom du directeur de Poudlard au début de l'histoire ?",
            "choices": [
                "Severus Rogue",
                "Albus Dumbledore",
                "Minerva McGonagall",
                "Sirius Black",
            ],
            "answer": 1,
        },
        {
            "q": "Quel studio d'animation a créé le film 'Le Voyage de Chihiro' ?",
            "choices": [
                "Pixar",
                "Studio Ghibli",
                "DreamWorks",
                "Walt Disney Animation",
            ],
            "answer": 1,
        },
        {
            "q": "Quel film relate l'histoire tragique du paquebot insubmersible en 1997 ?",
            "choices": ["Avatar", "Titanic", "Gladiator", "Inception"],
            "answer": 1,
        },
        {
            "q": "Quel super-héros DC protège la ville de Gotham City ?",
            "choices": ["Superman", "The Flash", "Batman", "Aquaman"],
            "answer": 2,
        },
        {
            "q": "Quelle série Netflix met en scène des adolescents luttant contre le 'Monde à l'Envers' ?",
            "choices": ["Dark", "Stranger Things", "The Witcher", "Wednesday"],
            "answer": 1,
        },
        {
            "q": "Quel est le nom du requin géant dans le film culte de Steven Spielberg de 1975 ?",
            "choices": ["Megalodon", "Bruce (Les Dents de la mer)", "Jaws", "Nemo"],
            "answer": 2,
        },
        {
            "q": "Dans la matrice (Matrix), quelle pilule Neo choisit-il de prendre ?",
            "choices": ["La pilule bleue", "La pilule rouge", "Les deux", "Aucune"],
            "answer": 1,
        },
        {
            "q": "Quel réalisateur est célèbre pour ses films pulp et non-linéaires comme Pulp Fiction ?",
            "choices": [
                "Martin Scorsese",
                "Quentin Tarantino",
                "David Fincher",
                "Ridley Scott",
            ],
            "answer": 1,
        },
        {
            "q": "Quel est le nom du royaume sous-marin fictif de l'univers Marvel où règne Namor ou T'Challa ?",
            "choices": ["Asgard", "Wakanda", "Atlantis", "Talokan"],
            "answer": 3,
        },
        {
            "q": "Quelle saga cinématographique met en scène des dinosaures clonés dans un parc d'attractions ?",
            "choices": [
                "Jurassic Park",
                "Terminator",
                "Alien",
                "Predator",
            ],
            "answer": 0,
        },
        {
            "q": "Quel détective privé fictif est créé par Arthur Conan Doyle ?",
            "choices": [
                "Hercule Poirot",
                "Sherlock Holmes",
                "Columbo",
                "Arsène Lupin",
            ],
            "answer": 1,
        },
    ],
}


def handle_client(client_socket, address):
    print(f"[+] Client connecté depuis : {address}")
    try:
        # 1. Envoyer les thèmes disponibles
        themes_data = list(QUESTION_BANK.keys())
        client_socket.sendall(json.dumps(themes_data).encode("utf-8"))

        # 2. Recevoir le choix du thème et du niveau du client
        request_raw = client_socket.recv(4096).decode("utf-8")
        if not request_raw:
            return
        request_data = json.loads(request_raw)

        chosen_theme = request_data.get("theme")
        chosen_level = request_data.get("level")  # 1 (5q), 2 (10q), 3 (15q)

        if chosen_theme not in QUESTION_BANK:
            client_socket.sendall(
                json.dumps({"error": "Thème invalide"}).encode("utf-8")
            )
            client_socket.close()
            return

        # Déterminer le nombre de questions selon le niveau
        if chosen_level == 1:
            num_questions = 5
        elif chosen_level == 2:
            num_questions = 10
        elif chosen_level == 3:
            num_questions = 15
        else:
            num_questions = 5

        # Sélectionner et mélanger les questions
        pool = QUESTION_BANK[chosen_theme].copy()
        random.shuffle(pool)
        selected_questions = pool[:num_questions]

        # Envoyer le nombre total de questions
        client_socket.sendall(
            json.dumps({"total": len(selected_questions)}).encode("utf-8")
        )

        score = 0

        # Boucle du quiz
        for idx, q_item in enumerate(selected_questions):
            # Envoyer la question courante
            q_payload = {
                "index": idx + 1,
                "total": len(selected_questions),
                "question": q_item["q"],
                "choices": q_item["choices"],
            }
            client_socket.sendall(json.dumps(q_payload).encode("utf-8"))

            # Recevoir la réponse du client
            ans_raw = client_socket.recv(1024).decode("utf-8")
            if not ans_raw:
                break
            ans_data = json.loads(ans_raw)
            client_answer = ans_data.get("answer")

            # Valider
            is_correct = client_answer == q_item["answer"]
            if is_correct:
                score += 10  # 10 points par bonne réponse

            # Renvoyer le résultat immédiat de la question
            feedback = {
                "correct": is_correct,
                "correct_answer": q_item["answer"],
                "current_score": score,
            }
            client_socket.sendall(json.dumps(feedback).encode("utf-8"))

        # Fin du quiz - envoyer le score final
        final_msg = {"final_score": score, "max_score": len(selected_questions) * 10}
        client_socket.sendall(json.dumps(final_msg).encode("utf-8"))

    except Exception as e:
        print(f"[-] Erreur avec le client {address}: {e}")
    finally:
        client_socket.close()
        print(f"[-] Connexion fermée pour {address}")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] Serveur QCM Gamer démarré sur {HOST}:{PORT}")
    print(
        "[*] Note VPN : Pour restreindre l'accès au réseau VPN, modifiez HOST avec l'IP VPN du serveur."
    )

    while True:
        client_socket, addr = server.accept()
        thread = threading.Thread(
            target=handle_client, args=(client_socket, addr)
        )
        thread.daemon = True
        thread.start()


if __name__ == "__main__":
    start_server()