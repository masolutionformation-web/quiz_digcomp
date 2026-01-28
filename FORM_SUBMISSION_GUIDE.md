# Using the Google Forms Submission Script

## Quick Start

The `submit_results_to_form.py` script automatically submits DigComp quiz results to your Google Forms results collection form.

### Basic Usage

```python
from submit_results_to_form import submit_to_google_form

# Prepare your domain results
domain_results = {
    "DOMAINE 1 : INFORMATIONS ET DONNÉES": 75.0,
    "DOMAINE 2 : COMMUNICATION ET COLLABORATION": 85.5,
    "DOMAINE 3 : CRÉATION DE CONTENU": 65.0,
    "DOMAINE 4 : RÉSOLUTION DE PROBLÈMES": 70.0,
    "DOMAINE 5 : SÉCURITÉ": 80.0
}

# Submit to form (automatically handles browser fallback)
submit_to_google_form(
    nom="Dupont",
    prenom="Jean",
    domain_results=domain_results
)
```

## Integration with Your Quiz App

### Method 1: Add Export Button to Results Page

Add this button to your HTML results page:

```html
<button onclick="exportToForm()" class="export-btn">
    📤 Envoyer au formulaire Google
</button>
```

Add this JavaScript function:

```javascript
async function exportToForm() {
    // Get user name from input or results
    const nom = document.getElementById('user-nom').value;
    const prenom = document.getElementById('user-prenom').value;
    
    // Call Python backend endpoint
    const response = await fetch('/api/submit-results', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            nom: nom,
            prenom: prenom,
            domainResults: domainResults
        })
    });
    
    if (response.ok) {
        alert('✅ Résultats envoyés avec succès !');
    }
}
```

### Method 2: Generate Pre-filled URL

Get a shareable URL with pre-filled results:

```python
from submit_results_to_form import get_form_prefill_url

url = get_form_prefill_url(
    nom="Dupont",
    prenom="Jean",
    domain_results=domain_results
)

print(f"Share this URL: {url}")
```

### Method 3: Browser Auto-Open

Automatically open the form in the user's browser:

```python
from submit_results_to_form import open_prefilled_form

# Opens form in browser, user just clicks "Submit"
open_prefilled_form(
    nom="Dupont",
    prenom="Jean",
    domain_results=domain_results
)
```

## How It Works

1. **Direct POST** - First tries to submit directly to Google Forms
2. **Browser Fallback** - If authentication is required (status 401), automatically opens a pre-filled form in the user's default browser
3. **User Completes** - User just needs to click "Envoyer" (Submit) button

## Authentication Note

Google Forms may require authentication for submissions. The script automatically handles this by:
- Detecting authentication errors
- Opening a pre-filled form in the browser
- Letting the user submit while logged into their Google account

This provides a seamless user experience without requiring complex authentication setup.
