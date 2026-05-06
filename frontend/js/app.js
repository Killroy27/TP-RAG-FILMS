const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const chatDisplay = document.getElementById('chat-display');
const mainScroll = document.getElementById('main-scroll');

// État de l'application
let conversationHistory = [];

// Gestion des chips de filtrage (Sidebar)
const chips = document.querySelectorAll('.filter-chip');
chips.forEach(chip => {
    chip.addEventListener('click', () => {
        chips.forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
        const input = chip.querySelector('input');
        if (input) input.checked = true;
    });
});

// Charger le statut au démarrage
async function updateStatus() {
    try {
        const response = await fetch('/api/status');
        if (response.ok) {
            const data = await response.json();
            document.getElementById('status-movies').textContent = data.total_movies;
            document.getElementById('status-index').textContent = data.index_ready ? 'Prêt' : 'Erreur';
        }
    } catch (e) {
        console.error("Erreur statut:", e);
    }
}
updateStatus();

function addMessage(text, isBot = true, sources = []) {
    // Ajouter à l'historique local (limité aux 10 derniers)
    conversationHistory.push({ text: text, is_user: !isBot });
    if (conversationHistory.length > 10) conversationHistory.shift();

    const row = document.createElement('div');
    row.classList.add('message-row');
    row.classList.add(isBot ? 'bot' : 'user');

    const msg = document.createElement('div');
    msg.classList.add('message');
    msg.classList.add(isBot ? 'bot-message' : 'user-message');
    
    // Remplacer les retours à la ligne par <br>
    msg.innerHTML = text.replace(/\n/g, '<br>');

    // Affichage des sources en grille si disponibles
    if (isBot && sources && sources.length > 0) {
        const grid = document.createElement('div');
        grid.classList.add('movie-results');
        
        sources.forEach(movie => {
            const card = document.createElement('div');
            card.classList.add('movie-card');
            const year = movie.release_date ? movie.release_date.split('-')[0] : 'N/A';
            
            card.innerHTML = `
                <div class="movie-card-content">
                    <div class="title">${movie.title}</div>
                    <div class="info">
                        <span>${year}</span>
                        <span class="rating">${movie.vote_average}/10</span>
                    </div>
                </div>
            `;
            grid.appendChild(card);
        });
        msg.appendChild(grid);
    }

    row.appendChild(msg);
    chatDisplay.appendChild(row);
    mainScroll.scrollTop = mainScroll.scrollHeight;
    return msg;
}

function showLoading() {
    const row = document.createElement('div');
    row.classList.add('message-row', 'bot', 'loading-row');
    
    const dots = document.createElement('div');
    dots.classList.add('typing-dots');
    dots.innerHTML = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
    
    row.appendChild(dots);
    chatDisplay.appendChild(row);
    mainScroll.scrollTop = mainScroll.scrollHeight;
    return row;
}

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = userInput.value.trim();
    if (!message) return;

    // Récupérer le filtre actif
    const activeChip = document.querySelector('.filter-chip.active');
    const langInput = activeChip ? activeChip.querySelector('input') : null;
    const langValue = langInput ? langInput.value : 'all';
    const finalLang = langValue === 'all' ? null : langValue;

    // Ajouter message utilisateur
    addMessage(message, false);
    userInput.value = '';

    // Afficher indicateur de chargement
    const loadingRow = showLoading();

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                message: message, 
                lang_filter: finalLang,
                history: conversationHistory.slice(0, -1) // On envoie l'historique sans le dernier message utilisateur
            })
        });

        if (!response.ok) throw new Error(`Erreur serveur: ${response.status}`);

        const data = await response.json();
        loadingRow.remove();

        if (data.answer) {
            addMessage(data.answer, true, data.sources);
        } else {
            addMessage("Une erreur est survenue lors du traitement.", true);
        }

    } catch (error) {
        if (loadingRow) loadingRow.remove();
        addMessage(`Erreur : ${error.message}. Vérifiez que le serveur est actif.`, true);
        console.error(error);
    }
});
