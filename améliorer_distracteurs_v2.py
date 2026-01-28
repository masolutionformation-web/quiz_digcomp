import json
import random

# Charger le fichier JSON original
with open('questions_digcomp_complet.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

def est_mauvais_distracteur(text):
    """Identifie les distracteurs absurdes à remplacer"""
    phrases_absurdes = [
        "éteindre",
        "redémarrer l'appareil plusieurs fois",
        "redémarrer l'unité centrale",
        "attendre que le problème se résolve",
        "débrancher tous les câbles",
        "appuyer sur toutes les touches",
        "fermer toutes les fenêtres",
        "demander de l'aide à quelqu'un",
        "utiliser un autre appareil",
        "revenir à l'étape précédente",
        "changer les paramètres au hasard",
        "vider la corbeille",
        "attendre quelques minutes",
        "faire une recherche sur internet",
        "consulter le manuel",
        "appeler le support",
        "photocopieuse laser",
        "câble d'alimentation secteur",
        "l'ajustement des paramètres",
        "ajuster les paramètres de synchronisation",
        "vider le cache dns du terminal",
        "changer les paramètres",
        "attendre l'exécution",
    ]
    text_lower = text.lower()
    return any(phrase in text_lower for phrase in phrases_absurdes)

def generer_distracteurs_par_question(question_obj):
    """Génère des distracteurs adaptés à chaque question spécifique"""
    
    question_text = question_obj["question"].lower()
    competence = question_obj["competence"].lower()
    niveau = question_obj["niveau"]
    
    # Banque de distracteurs ciblés par type de question
    
    # Questions sur la recherche en ligne
    if "mot" in question_text and "clé" in question_text or "recette" in question_text:
        return [
            "Dans la barre d'adresse du navigateur",
            "Dans l'explorateur de fichiers",
            "Dans une application de messagerie",
            "Dans le menu Démarrer"
        ]
    
    # Questions sur les actions après saisie
    if "tape" in question_text and ("entrée" in competence or "recherche" in competence):
        return [
            "Cliquer sur le bouton 'Accueil' du navigateur",
            "Ouvrir un nouvel onglet",
            "Attendre l'affichage automatique des résultats",
            "Sélectionner tout le texte saisi"
        ]
    
    # Questions sur la navigation
    if "retour" in question_text or "précédent" in question_text:
        return [
            "Actualiser la page avec F5",
            "Ouvrir un nouvel onglet",
            "Fermer l'onglet actuel",
            "Cliquer sur la flèche 'Suivant'"
        ]
    
    # Questions sur l'enregistrement de fichiers
    if "conserver" in question_text or "enregistrer" in question_text:
        return [
            "Copier le contenu dans le presse-papiers",
            "Créer un raccourci sur le Bureau",
            "Imprimer le document en PDF",
            "Envoyer le document par email"
        ]
    
    # Questions sur l'organisation des fichiers
    if "rangés" in question_text or "retrouver" in question_text:
        return [
            "Dans la barre des tâches",
            "Dans le navigateur web",
            "Dans les applications récentes",
            "Dans la corbeille"
        ]
    
    # Questions sur la recherche de fichiers    
    if "trouvez plus" in question_text or "quel outil" in question_text:
        return [
            "L'explorateur de fichiers uniquement",
            "La liste des fichiers récents",
            "Le gestionnaire de tâches",
            "Les propriétés du système"
        ]
    
    # Questions sur le partage de fichiers
    if "photo" in question_text and "ami" in question_text:
        return [
            "Le Bluetooth",
            "Un email",
            "Un câble réseau Ethernet",
            "Le partage de connexion Wi-Fi"
        ]
    
    # Questions sur les pièces jointes
    if "accroche" in question_text or "email" in question_text:
        return [
            "Un fichier en brouillon",
            "Un lien hypertexte",
            "Une signature électronique",
            "Un objet du message"
        ]
    
    # Questions sur le partage de fichiers par email
    if "partagez" in question_text and "email" in question_text:
        return [
            "Le fichier est compressé automatiquement",
            "Le fichier est converti en PDF",
            "Le fichier est stocké sur un cloud",
            "Le fichier est transféré puis supprimé"
        ]
    
    # Questions sur le clavier - barre d'espace
    if "espace" in question_text and "mots" in question_text:
        return [
            "La touche Tabulation (Tab)",
            "La touche Alt Gr",
            "La touche Windows",
            "La touche de verrouillage (Caps Lock)"
        ]
    
    # Questions sur les majuscules
    if "majuscule" in question_text:
        return [
            "La touche Alt",
            "La touche Ctrl",
            "La touche de verrouillage (Caps Lock)",
            "La touche Windows"
        ]
    
    # Questions sur la suppression de caractères
    if "effacer" in question_text or "backspace" in competence.lower():
        return [
            "La touche Suppr (Delete)",
            "La touche Entrée",
            "La touche de verrouillage (Caps Lock)",
            "La touche Alt Gr"
        ]
    
    # Questions sur les icônes d'email
    if "logo" in question_text and "email" in question_text:
        return [
            "Une icône de bulle de discussion",
            "Une icône de cloche (notifications)",
            "Une icône de calendrier",
            "Une icône de liste de tâches"
        ]
    
    # Questions sur WhatsApp/Messenger
    if "whatsapp" in question_text or "messenger" in question_text:
        return [
            "À partager des photos uniquement",
            "À gérer son emploi du temps",
            "À écrire des documents professionnels",
            "À sauvegarder ses contacts"
        ]
    
    # Questions sur les réseaux sociaux
    if "réseau social" in question_text:
        return [
            "Un outil de sauvegarde automatique",
            "Un système de gestion de fichiers en ligne",
            "Un logiciel de messagerie électronique",
            "Un service de stockage cloud"
        ]
    
    # Questions sur l'authentification
    if "compte personnel" in question_text or "mot de passe" in question_text:
        return [
            "Votre nom complet",
            "Votre adresse email uniquement",
            "Un code de vérification par SMS uniquement",
            "Votre empreinte digitale uniquement"
        ]
    
    # Questions sur la déconnexion
    if "déconnecter" in question_text:
        return [
            "Fermer la fenêtre du navigateur",
            "Activer le mode navigation privée",
            "Vider le cache du navigateur",
            "Désactiver les cookies"
        ]
    
    # Questions sur l'icône Maison
    if "maison" in question_text:
        return [
            "L'accès aux paramètres du compte",
            "La page de profil utilisateur",
            "L'historique de navigation",
            "Les favoris enregistrés"
        ]
    
    # Questions sur la mise en gras
    if "gras" in question_text:
        return [
            "Un 'S' barré (pour barré)",
            "Un 'I' incliné (pour italique)",
            "Un 'U' souligné (pour souligné)",
            "Un 'A' avec une flèche (pour taille)"
        ]
    
    # Questions sur le passage à la ligne
    if "ligne suivante" in question_text:
        return [
            "Appuyer plusieurs fois sur la barre d'espace",
            "Utiliser la touche Tab",
            "Cliquer en bas de la page",
            "Utiliser le raccourci Ctrl+L"
        ]
    
    # Questions sur l'édition de texte
    if "bojour" in question_text or "ajouter" in question_text:
        return [
            "J'utilise la fonction 'Rechercher et remplacer'",
            "Je surligne le mot et tape 'Bonjour'",
            "J'utilise la correction automatique",
            "Je double-clique sur le mot pour le corriger"
        ]
    
    # Questions sur les droits d'auteur - images
    if "image" in question_text and "google" in question_text:
        return [
            "Oui, si vous citez la source",
            "Oui, pour un usage personnel uniquement",
            "Oui, si vous modifiez légèrement l'image",
            "Oui, si l'image est en basse résolution"
        ]
    
    # Questions sur la citation
    if "texte écrit par quelqu'un" in question_text:
        return [
            "Le paraphraser sans mentionner l'auteur",
            "Le mettre entre guillemets sans source",
            "L'utiliser tel quel si c'est court",
            "Le traduire dans une autre langue"
        ]
    
    # Questions sur le symbole ©
    if "©" in question_text:
        return [
            "C indique la version du document (Copy)",
            "C'est un label de qualité certifiée",
            "Indication que le contenu peut être copié librement",
            "Marque de compatibilité avec les navigateurs"
        ]
    
    # Questions sur le volume
    if "son" in question_text and "fort" in question_text:
        return [
            "Le contraste de l'écran",
            "Les paramètres d'égalisation audio",
            "La vitesse de lecture de la vidéo",
            "La résolution de la vidéo"
        ]
    
    # Questions sur la luminosité
    if "écran" in question_text and "sombre" in question_text:
        return [
            "Le mode économie d'énergie",
            "Le contraste de l'écran",
            "Le délai de mise en veille",
            "La rotation automatique"
        ]
    
    # Distracteurs génériques selon le niveau
    if niveau == "Intermédiaire":
        return [
            "Paramétrer le pare-feu",
            "Vider le cache de l'application",
            "Mettre à jour le système d'exploitation",
            "Réinitialiser les paramètres réseau"
        ]
    elif niveau == "Avancé":
        return [
            "Configurer un reverse proxy",
            "Auditer les journaux système",
            "Déployer un système IDS",
            "Paramétrer une DMZ"
        ]
    else:  # Initial
        return [
            "Accéder aux paramètres",
            "Consulter l'aide en ligne",
            "Vérifier les mises à jour",
            "Redémarrer l'application"
        ]

# Traiter chaque question
questions_modifiées = 0
distracteurs_modifiés = 0

for question in questions:
    options = question.get("options", [])
    distracteurs_remplacement = generer_distracteurs_par_question(question)
    
    # Collecter les bons distracteurs existants et identifier les mauvais
    bons_distracteurs = []
    indices_a_remplacer = []
    
    for i, option in enumerate(options):
        if not option.get("isCorrect", False):
            if est_mauvais_distracteur(option["text"]):
                indices_a_remplacer.append(i)
            else:
                bons_distracteurs.append(option["text"])
    
    # Remplacer les mauvais distracteurs
    if indices_a_remplacer:
        # Mélanger les distracteurs de remplacement
        random.shuffle(distracteurs_remplacement)
        
        for idx, i in enumerate(indices_a_remplacer):
            if idx < len(distracteurs_remplacement):
                nouveau = distracteurs_remplacement[idx]
                # Vérifier qu'il n'est pas déjà utilisé
                if nouveau not in bons_distracteurs:
                    options[i]["text"] = nouveau
                    bons_distracteurs.append(nouveau)
                    distracteurs_modifiés += 1
        
        questions_modifiées += 1

# Sauvegarder le fichier modifié
with open('questions_digcomp_final.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"✅ Traitement terminé !")
print(f"📊 {questions_modifiées} questions ont été améliorées")
print(f"🔄 {distracteurs_modifiés} distracteurs ont été remplacés")
print(f"📁 Fichier sauvegardé : questions_digcomp_final.json")
