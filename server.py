import http.server
import socketserver
import os
import webbrowser

# Configuration du serveur
PORT = 8000
web_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")
os.makedirs(web_dir, exist_ok=True)

# Copie le fichier HTML dans le dossier web
html_content = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scores de la Roulette Russe</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #2c3e50;
            color: #ecf0f1;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        h1 {
            color: #e74c3c;
            text-align: center;
            margin-bottom: 30px;
        }
        
        .container {
            display: flex;
            justify-content: space-between;
            width: 90%;
            max-width: 1000px;
        }
        
        .section {
            background-color: #34495e;
            border-radius: 10px;
            padding: 20px;
            margin: 10px;
            width: 45%;
        }
        
        h2 {
            color: #f39c12;
            border-bottom: 1px solid #f39c12;
            padding-bottom: 10px;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #576574;
        }
        
        th {
            background-color: #2980b9;
        }
        
        .highlight {
            background-color: rgba(46, 204, 113, 0.2);
        }
        
        .refresh-btn {
            background-color: #2ecc71;
            border: none;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 20px 0;
            cursor: pointer;
            border-radius: 5px;
            transition: background-color 0.3s;
        }
        
        .refresh-btn:hover {
            background-color: #27ae60;
        }
        
        .last-update {
            font-size: 12px;
            color: #bdc3c7;
            text-align: center;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <h1>🔫 SCORES DE LA ROULETTE RUSSE 🔫</h1>
    
    <button class="refresh-btn" onclick="loadScores()">Rafraîchir les scores</button>
    
    <div class="container">
        <div class="section">
            <h2>Classement Général</h2>
            <table id="general-scores">
                <tr>
                    <th>Position</th>
                    <th>Joueur</th>
                    <th>Score</th>
                </tr>
                <!-- Les scores seront ajoutés ici dynamiquement -->
            </table>
        </div>
        
        <div class="section">
            <h2>Parties Récentes</h2>
            <table id="recent-games">
                <tr>
                    <th>Date</th>
                    <th>Joueur 1</th>
                    <th>Joueur 2</th>
                </tr>
                <!-- Les parties seront ajoutées ici dynamiquement -->
            </table>
        </div>
    </div>
    
    <p class="last-update" id="update-time"></p>
    
    <script>
        function loadScores() {
            fetch('scores.json?nocache=' + new Date().getTime())
                .then(response => response.json())
                .then(data => {
                    updateGeneralScores(data.scores);
                    updateRecentGames(data.parties);
                    document.getElementById('update-time').textContent = 'Dernière mise à jour: ' + new Date().toLocaleString();
                })
                .catch(error => {
                    console.error('Erreur lors du chargement des scores:', error);
                    document.getElementById('update-time').textContent = 'Erreur de chargement des scores';
                });
        }
        
        function updateGeneralScores(scores) {
            const table = document.getElementById('general-scores');
            // Conserver uniquement l'en-tête de la table
            table.innerHTML = '<tr><th>Position</th><th>Joueur</th><th>Score</th></tr>';
            
            // Convertir les scores en tableau et trier par score décroissant
            const sortedScores = Object.entries(scores)
                .map(([joueur, score]) => ({ joueur, score }))
                .sort((a, b) => b.score - a.score);
            
            // Ajouter chaque ligne au tableau
            sortedScores.forEach((item, index) => {
                const row = table.insertRow(-1);
                row.insertCell(0).textContent = index + 1;
                // Afficher le vrai nom du joueur ou "Joueur X" pour les anciens scores
                const displayName = isNaN(item.joueur) ? item.joueur : 'Joueur ' + item.joueur;
                row.insertCell(1).textContent = displayName;
                row.insertCell(2).textContent = item.score;
            });
        }
        
        function updateRecentGames(parties) {
            const table = document.getElementById('recent-games');
            // Conserver uniquement l'en-tête de la table
            table.innerHTML = '<tr><th>Date</th><th>Joueur 1</th><th>Joueur 2</th></tr>';
            
            // Prendre les 10 dernières parties
            const recentGames = parties.slice(-10).reverse();
            
            // Ajouter chaque partie au tableau
            recentGames.forEach(game => {
                const row = table.insertRow(-1);
                row.insertCell(0).textContent = game.date;
                
                // Trouver les noms des joueurs et leur score
                const playerKeys = Object.keys(game.scores);
                
                // Première cellule joueur
                const player1Key = playerKeys[0] || '1';
                const player1Name = isNaN(player1Key) ? player1Key : 'Joueur ' + player1Key;
                const player1Score = game.scores[player1Key] || 0;
                row.insertCell(1).textContent = `${player1Name}: ${player1Score}`;
                
                // Deuxième cellule joueur
                const player2Key = playerKeys[1] || '2';
                const player2Name = isNaN(player2Key) ? player2Key : 'Joueur ' + player2Key;
                const player2Score = game.scores[player2Key] || 0;
                row.insertCell(2).textContent = `${player2Name}: ${player2Score}`;
                
                // Surligner le gagnant (celui qui a un point)
                if (player1Score > 0) {
                    row.cells[1].classList.add('highlight');
                }
                if (player2Score > 0) {
                    row.cells[2].classList.add('highlight');
                }
            });
        }
        
        // Charger les scores au chargement de la page
        document.addEventListener('DOMContentLoaded', loadScores);
        
        // Rafraîchir automatiquement les scores toutes les 10 secondes
        setInterval(loadScores, 10000);
    </script>
</body>
</html>
'''

with open(os.path.join(web_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Serveur web démarré sur http://localhost:{PORT}")
print("Ouvrez votre navigateur à cette adresse pour voir les scores")

# Changer le répertoire de travail pour le dossier web
os.chdir(web_dir)

# Ouvrir automatiquement le navigateur
webbrowser.open(f'http://localhost:{PORT}')

# Démarrer le serveur HTTP
with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Serveur arrêté.")