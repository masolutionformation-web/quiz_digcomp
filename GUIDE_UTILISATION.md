# Guide d'utilisation - Envoi des résultats au formulaire Google

## 🎯 Fonctionnalité implémentée

Le bouton **"Enregistrer les résultats"** sur la page de résultats du quiz permet maintenant d'envoyer automatiquement vos résultats à un formulaire Google Forms pré-rempli.

## ✨ Comment ça fonctionne

### 1. Compléter le quiz

- Configurez votre quiz (nombre de questions, niveaux de difficulté)
- Répondez à toutes les questions
- Consultez vos résultats à la fin

### 2. Enregistrer les résultats

Sur l'écran de résultats, cliquez sur le bouton **"📤 Enregistrer les résultats"**

### 3. Validation dans le formulaire Google

- Un nouvel onglet s'ouvre automatiquement
- Le formulaire Google Forms est **déjà pré-rempli** avec vos résultats :
  - **Résultat global** (en %)
  - **Domaine 1** : Informations et données (en %)
  - **Domaine 2** : Communication et collaboration (en %)
  - **Domaine 3** : Création de contenu digital (en %)
  - **Domaine 4** : Résolution des problèmes (en %)
  - **Domaine 5** : Sécurité numérique (en %)
- **Il vous suffit de cliquer sur "Envoyer"** pour soumettre le formulaire

## 🔧 Détails techniques

### Champs du formulaire Google Forms

Le script JavaScript utilise les IDs de champs suivants :

```javascript
const formFields = {
    domaine1: 'entry.1390360142',  // DOMAINE 1 : INFORMATIONS ET DONNÉES
    domaine2: 'entry.494398783',   // DOMAINE 2 : COMMUNICATION ET COLLABORATION
    domaine3: 'entry.818563881',   // DOMAINE 3 : CRÉATION DE CONTENU DIGITAL
    domaine4: 'entry.1140857471',  // DOMAINE 4 : RÉSOLUTION DES PROBLÈMES
    domaine5: 'entry.911865149',   // DOMAINE 5 : SÉCURITÉ NUMÉRIQUE
    global: 'entry.294442511'      // RESULTAT GLOBAL
};
```

### Calcul des résultats

Les résultats sont calculés automatiquement dans le script `app.js` :

1. **Par domaine** : Pourcentage de bonnes réponses pour chaque domaine DigComp
2. **Global** : Pourcentage de bonnes réponses sur l'ensemble du quiz

### Structure du code

#### Fichiers modifiés

- **`app.js`** (lignes 340-402) :
  - `generateGoogleFormsUrl()` : Génère l'URL du formulaire pré-rempli
  - `submitToGoogleForms()` : Ouvre le formulaire dans un nouvel onglet

#### Fichiers de référence

- **`submit_results_to_form.py`** : Script Python équivalent avec soumission automatique
- **`FORM_SUBMISSION_GUIDE.md`** : Documentation pour l'intégration backend

## ⚠️ Points d'attention

### Bloqueur de pop-ups

Si le navigateur bloque l'ouverture du formulaire :

1. Un message d'alerte vous indiquera le problème
2. Autorisez les fenêtres pop-up pour ce site
3. L'URL du formulaire sera disponible dans la console (F12)

### Vérification des résultats

Avant de cliquer sur "Envoyer" dans le formulaire Google :

- ✅ Vérifiez que tous les champs sont bien remplis
- ✅ Vérifiez que les pourcentages correspondent à vos résultats affichés sur la page

## 🚀 Exemple d'utilisation

```
1. Vous terminez le quiz avec ces résultats :
   - Score global : 75%
   - Domaine 1 : 80%
   - Domaine 2 : 85%
   - Domaine 3 : 60%
   - Domaine 4 : 70%
   - Domaine 5 : 80%

2. Vous cliquez sur "Enregistrer les résultats"

3. Une alerte s'affiche :
   "✅ Le formulaire Google Forms a été ouvert dans un nouvel onglet.
   
   📋 Les résultats sont déjà pré-remplis.
   Vous devez juste cliquer sur 'Envoyer' pour soumettre vos résultats."

4. Dans le nouvel onglet, le formulaire Google affiche :
   - RESULTAT GLOBAL : 75
   - RESULTAT DOMAINE 1 : 80
   - RESULTAT DOMAINE 2 : 85
   - RESULTAT DOMAINE 3 : 60
   - RESULTAT DOMAINE 4 : 70
   - RESULTAT DOMAINE 5 : 80

5. Vous cliquez sur "Envoyer" et vos résultats sont enregistrés !
```

## 🛠️ Dépannage

### Le formulaire ne s'ouvre pas

**Problème** : Le bouton ne fait rien ou affiche un message d'erreur de pop-up

**Solution** :
1. Vérifiez que les pop-ups sont autorisées pour ce site
2. Consultez la console JavaScript (F12) pour voir l'URL du formulaire
3. Copiez-collez l'URL dans un nouvel onglet manuellement

### Les résultats ne sont pas pré-remplis

**Problème** : Le formulaire s'ouvre mais les champs sont vides

**Solution** :
1. Vérifiez que vous avez bien terminé le quiz
2. Consultez la console JavaScript pour voir les données envoyées
3. Vérifiez que les IDs de champs correspondent toujours au formulaire Google

### Erreur dans les calculs

**Problème** : Les pourcentages affichés ne semblent pas corrects

**Solution** :
1. Vérifiez le nombre de questions par domaine
2. Consultez `domainResults` dans la console (F12)
3. Vérifiez que toutes les questions ont bien été répondues

## 📝 Notes

- Cette fonctionnalité fonctionne entièrement côté client (JavaScript)
- Aucun serveur backend n'est nécessaire
- Les données ne sont envoyées qu'au formulaire Google (pas de stockage intermédiaire)
- Le formulaire Google doit rester accessible et les IDs de champs ne doivent pas changer
