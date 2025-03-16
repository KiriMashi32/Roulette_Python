import random
import json
import os
from datetime import datetime

SCORES_FILE = "scores.json"

def init_barillet(nb_balles=1):
    barillet = [0] * (6 - nb_balles) + [1] * nb_balles
    random.shuffle(barillet)
    return barillet

def tirer(barillet, joueur):
    print(f"Le joueur {joueur} presse la détente...")
    if barillet.pop(0) == 1:
        print(f"BOUM ! Le joueur {joueur} est éliminé.")
        return True  # Partie terminée
    else:
        print("Clic... Rien ne se passe.")
        return False  # La partie continue

def jouer(nb_balles):
    barillet = init_barillet(nb_balles)
    joueur = 1
    while barillet:
        input(f"Joueur {joueur}, appuyez sur Entrée pour tirer.")
        if tirer(barillet, joueur):
            return joueur  # Retourner le joueur éliminé
        joueur = 2 if joueur == 1 else 1  # Changer de joueur
    return None  # Aucun joueur éliminé

def charger_scores():
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, "r") as file:
            return json.load(file)
    return {"parties": [], "scores": {}}

def sauvegarder_scores(data):
    with open(SCORES_FILE, "w") as file:
        json.dump(data, file, indent=4)

def afficher_classement(scores):
    classement = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    print("\nClassement général :")
    for joueur, score in classement:
        print(f"Joueur {joueur}: {score} points")

def main():
    print("Bienvenue au jeu de la Roulette Russe !")
    data = charger_scores()
    scores = data["scores"]
    scores_partie = {1: 0, 2: 0}
    while True:
        nb_balles = int(input("Entrez le nombre de balles dans le barillet (1-5): "))
        joueur_elimine = jouer(nb_balles)
        if joueur_elimine:
            scores_partie[joueur_elimine] += 1
            print(f"Le joueur {joueur_elimine} a été éliminé. Scores: Joueur 1 - {scores_partie[1]}, Joueur 2 - {scores_partie[2]}")
        else:
            print("Aucun joueur n'a été éliminé.")
        
        rejouer = input("Voulez-vous rejouer ? (o/n): ").lower()
        if rejouer != 'o':
            print("Merci d'avoir joué !")
            print(f"Scores finaux de la partie: Joueur 1 - {scores_partie[1]}, Joueur 2 - {scores_partie[2]}")
            for joueur, score in scores_partie.items():
                if str(joueur) in scores:
                    scores[str(joueur)] += score
                else:
                    scores[str(joueur)] = score
            data["parties"].append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "scores": scores_partie.copy()
            })
            data["scores"] = scores
            sauvegarder_scores(data)
            afficher_classement(scores)
            break

if __name__ == "__main__":
    main()