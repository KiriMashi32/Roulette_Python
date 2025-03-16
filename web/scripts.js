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
        row.insertCell(1).textContent = item.joueur;
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
        
        // Utiliser les pseudos au lieu des identifiants numériques
        // Si les clés sont des objets avec nom et score
        const joueurs = Object.keys(game.scores);
        
        if (joueurs.length >= 2) {
            row.insertCell(1).textContent = joueurs[0];  // Nom du joueur 1
            row.insertCell(2).textContent = joueurs[1];  // Nom du joueur 2
            
            // Surligner le perdant (celui qui a un point)
            if (game.scores[joueurs[0]] > 0) {
                row.cells[1].classList.add('highlight');
            }
            if (game.scores[joueurs[1]] > 0) {
                row.cells[2].classList.add('highlight');
            }
        } else {
            // Fallback pour compatibilité avec l'ancien format
            row.insertCell(1).textContent = game.scores['1'] || 0;
            row.insertCell(2).textContent = game.scores['2'] || 0;
            
            if (game.scores['1'] > 0) {
                row.cells[1].classList.add('highlight');
            }
            if (game.scores['2'] > 0) {
                row.cells[2].classList.add('highlight');
            }
        }
    });
}

// Charger les scores au chargement de la page
document.addEventListener('DOMContentLoaded', loadScores);

// Rafraîchir automatiquement les scores toutes les 10 secondes
setInterval(loadScores, 10000);