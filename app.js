// État global de l'application
let allQuestions = [];
let quizQuestions = [];
let currentQuestionIndex = 0;
let score = 0;
let userAnswers = [];
let selectedOption = null;

// Configuration du quiz
let quizConfig = {
    numQuestions: 20,
    niveaux: ['Initial', 'Intermédiaire', 'Avancé']
};

// Charger les questions depuis le fichier JSON
async function loadQuestions() {
    try {
        const response = await fetch('questions_digcomp_final.json');
        allQuestions = await response.json();
        console.log(`✅ ${allQuestions.length} questions chargées`);
    } catch (error) {
        console.error('❌ Erreur lors du chargement des questions:', error);
        alert('Impossible de charger les questions. Veuillez vérifier que le fichier questions_digcomp_final.json est présent.');
    }
}

// Sélectionner des questions aléatoires selon les critères
function selectQuizQuestions() {
    // Filtrer les questions selon les niveaux sélectionnés
    const filteredQuestions = allQuestions.filter(q =>
        quizConfig.niveaux.includes(q.niveau)
    );

    if (filteredQuestions.length === 0) {
        alert('Aucune question ne correspond aux critères sélectionnés.');
        return [];
    }

    // Grouper les questions par domaine, compétence et niveau
    const groupedQuestions = {};

    filteredQuestions.forEach(question => {
        const key = `${question.domaine}|${question.competence}|${question.niveau}`;
        if (!groupedQuestions[key]) {
            groupedQuestions[key] = [];
        }
        groupedQuestions[key].push(question);
    });

    // Sélectionner une question aléatoire de chaque groupe
    const selectedQuestions = [];
    const groups = Object.values(groupedQuestions);

    // Mélanger les groupes
    shuffleArray(groups);

    // Prendre une question aléatoire de chaque groupe jusqu'à atteindre le nombre souhaité
    let groupIndex = 0;
    while (selectedQuestions.length < quizConfig.numQuestions && selectedQuestions.length < filteredQuestions.length) {
        const group = groups[groupIndex % groups.length];
        const availableQuestions = group.filter(q => !selectedQuestions.includes(q));

        if (availableQuestions.length > 0) {
            const randomQuestion = availableQuestions[Math.floor(Math.random() * availableQuestions.length)];
            selectedQuestions.push(randomQuestion);
        }

        groupIndex++;

        // Éviter une boucle infinie
        if (groupIndex > groups.length * 100) break;
    }

    // Mélanger les questions sélectionnées
    shuffleArray(selectedQuestions);

    // Mélanger les options de chaque question
    selectedQuestions.forEach(question => {
        shuffleArray(question.options);
    });

    return selectedQuestions;
}

// Fonction utilitaire pour mélanger un tableau
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

// Gestion des écrans
function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    document.getElementById(screenId).classList.add('active');
}

// Démarrer le quiz
function startQuiz() {
    // Récupérer la configuration
    quizConfig.numQuestions = parseInt(document.getElementById('num-questions').value);
    quizConfig.niveaux = [];

    if (document.getElementById('niveau-initial').checked) quizConfig.niveaux.push('Initial');
    if (document.getElementById('niveau-intermediaire').checked) quizConfig.niveaux.push('Intermédiaire');
    if (document.getElementById('niveau-avance').checked) quizConfig.niveaux.push('Avancé');

    if (quizConfig.niveaux.length === 0) {
        alert('Veuillez sélectionner au moins un niveau de difficulté.');
        return;
    }

    // Sélectionner les questions
    quizQuestions = selectQuizQuestions();

    if (quizQuestions.length === 0) {
        return;
    }

    // Ajuster le nombre de questions si nécessaire
    quizConfig.numQuestions = Math.min(quizConfig.numQuestions, quizQuestions.length);
    quizQuestions = quizQuestions.slice(0, quizConfig.numQuestions);

    // Réinitialiser l'état
    currentQuestionIndex = 0;
    score = 0;
    userAnswers = [];
    selectedOption = null;

    // Mettre à jour l'affichage
    document.getElementById('total-questions').textContent = quizConfig.numQuestions;
    document.getElementById('current-score').textContent = 0;

    // Afficher l'écran de quiz
    showScreen('quiz-screen');
    displayQuestion();
}

// Afficher la question actuelle
function displayQuestion() {
    const question = quizQuestions[currentQuestionIndex];

    // Masquer la carte de feedback
    document.getElementById('feedback-card').style.display = 'none';

    // Mettre à jour la barre de progression
    const progress = ((currentQuestionIndex + 1) / quizConfig.numQuestions) * 100;
    document.getElementById('progress-fill').style.width = `${progress}%`;
    document.getElementById('current-question').textContent = currentQuestionIndex + 1;

    // Afficher les détails de la question
    document.getElementById('question-domain').textContent = question.domaine.replace('DOMAINE ', 'D');
    document.getElementById('question-level').textContent = question.niveau;
    document.getElementById('question-text').textContent = question.question;

    // Afficher les options
    const optionsContainer = document.getElementById('options-container');
    optionsContainer.innerHTML = '';

    question.options.forEach((option, index) => {
        const optionElement = document.createElement('div');
        optionElement.className = 'option';
        optionElement.textContent = option.text;
        optionElement.dataset.index = index;

        optionElement.addEventListener('click', () => selectOption(index));

        optionsContainer.appendChild(optionElement);
    });

    // Réinitialiser la sélection
    selectedOption = null;
    document.getElementById('validate-btn').disabled = true;
}

// Sélectionner une option
function selectOption(index) {
    selectedOption = index;

    // Mettre à jour l'affichage
    document.querySelectorAll('.option').forEach((opt, i) => {
        if (i === index) {
            opt.classList.add('selected');
        } else {
            opt.classList.remove('selected');
        }
    });

    // Activer le bouton de validation
    document.getElementById('validate-btn').disabled = false;
}

// Valider la réponse
function validateAnswer() {
    if (selectedOption === null) return;

    const question = quizQuestions[currentQuestionIndex];
    const selectedOptionData = question.options[selectedOption];
    const isCorrect = selectedOptionData.isCorrect;

    // Enregistrer la réponse
    userAnswers.push({
        question: question,
        selectedOption: selectedOption,
        isCorrect: isCorrect
    });

    // Mettre à jour le score
    if (isCorrect) {
        score += question.points;
        document.getElementById('current-score').textContent = score;
    }

    // Afficher le feedback visuel sur les options
    document.querySelectorAll('.option').forEach((opt, i) => {
        opt.classList.add('disabled');

        if (question.options[i].isCorrect) {
            opt.classList.add('correct');
        } else if (i === selectedOption && !isCorrect) {
            opt.classList.add('incorrect');
        }
    });

    // Afficher la carte de feedback
    const feedbackCard = document.getElementById('feedback-card');
    const feedbackIcon = document.getElementById('feedback-icon');
    const feedbackTitle = document.getElementById('feedback-title');
    const feedbackMessage = document.getElementById('feedback-message');

    if (isCorrect) {
        feedbackIcon.textContent = '✅';
        feedbackTitle.textContent = 'Excellente réponse !';
        feedbackTitle.style.color = '#11998e';
    } else {
        feedbackIcon.textContent = '❌';
        feedbackTitle.textContent = 'Réponse incorrecte';
        feedbackTitle.style.color = '#eb3349';
    }

    feedbackMessage.textContent = question.commentaire;
    feedbackCard.style.display = 'block';

    // Désactiver le bouton de validation
    document.getElementById('validate-btn').disabled = true;
}

// Passer à la question suivante
function nextQuestion() {
    currentQuestionIndex++;

    if (currentQuestionIndex < quizQuestions.length) {
        displayQuestion();
    } else {
        showResults();
    }
}

// Afficher les résultats
function showResults() {
    const totalQuestions = quizQuestions.length;
    const correctAnswers = userAnswers.filter(a => a.isCorrect).length;
    const wrongAnswers = totalQuestions - correctAnswers;
    const percentage = Math.round((correctAnswers / totalQuestions) * 100);

    // Calculer le total des points possibles
    const maxPoints = quizQuestions.reduce((sum, q) => sum + q.points, 0);

    // Afficher les statistiques globales
    document.getElementById('final-score').textContent = `${percentage}%`;
    document.getElementById('correct-answers').textContent = correctAnswers;
    document.getElementById('wrong-answers').textContent = wrongAnswers;
    document.getElementById('total-points').textContent = `${score} / ${maxPoints}`;

    // Animer le cercle de score
    const circumference = 2 * Math.PI * 90;
    const offset = circumference - (percentage / 100) * circumference;
    document.getElementById('score-circle-fill').style.strokeDashoffset = offset;

    // Calculer les résultats par domaine
    const resultsByDomain = {};

    userAnswers.forEach(answer => {
        const domain = answer.question.domaine;
        if (!resultsByDomain[domain]) {
            resultsByDomain[domain] = {
                correct: 0,
                total: 0
            };
        }
        resultsByDomain[domain].total++;
        if (answer.isCorrect) {
            resultsByDomain[domain].correct++;
        }
    });

    // Afficher les résultats par domaine
    const domainResultsContainer = document.getElementById('results-by-domain');
    domainResultsContainer.innerHTML = '<h3 style="margin-bottom: 16px; font-size: 1.25rem;">Résultats par domaine</h3>';

    Object.entries(resultsByDomain).forEach(([domain, stats]) => {
        const domainPercentage = Math.round((stats.correct / stats.total) * 100);

        const domainElement = document.createElement('div');
        domainElement.className = 'domain-result';
        domainElement.innerHTML = `
            <div class="domain-name">${domain}</div>
            <div class="domain-stats">
                <span style="font-size: 0.875rem; color: var(--text-secondary);">${stats.correct} / ${stats.total} correctes</span>
                <span class="domain-score">${domainPercentage}%</span>
            </div>
        `;

        domainResultsContainer.appendChild(domainElement);
    });

    // Afficher l'écran de résultats
    showScreen('results-screen');
}

// Recommencer le quiz
function restartQuiz() {
    showScreen('welcome-screen');
}

// Initialisation
document.addEventListener('DOMContentLoaded', async () => {
    // Charger les questions
    await loadQuestions();

    // Événements
    document.getElementById('start-btn').addEventListener('click', startQuiz);
    document.getElementById('validate-btn').addEventListener('click', validateAnswer);
    document.getElementById('next-btn').addEventListener('click', nextQuestion);
    document.getElementById('restart-btn').addEventListener('click', restartQuiz);
});
