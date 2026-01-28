#!/usr/bin/env python3
"""
Script to submit DigComp quiz results to Google Forms
Provides multiple submission methods: direct POST, pre-filled URL, and browser automation
"""

import requests
import json
import webbrowser
from typing import Dict, List, Optional
from collections import defaultdict
from urllib.parse import urlencode

# Google Form configuration
FORM_BASE_URL = "https://docs.google.com/forms/d/e/1FAIpQLSf2Sa6kudUT3hVMuhxFY0oNaedKbPuZu85yQnxqypY0Eohikg"
FORM_SUBMIT_URL = f"{FORM_BASE_URL}/formResponse"
FORM_VIEW_URL = f"{FORM_BASE_URL}/viewform"

# Form field entry IDs
FORM_FIELDS = {
    "nom": "entry.752468721",
    "prenom": "entry.650519905",
    "domain1": "entry.1390360142",  # DOMAINE 1 : INFORMATIONS ET DONNÉES
    "domain2": "entry.494398783",   # DOMAINE 2 : COMMUNICATION ET COLLABORATION
    "domain3": "entry.818563881",   # DOMAINE 3 : CRÉATION DE CONTENU DIGITAL
    "domain4": "entry.1140857471",  # DOMAINE 4 : RÉSOLUTION DES PROBLÈMES
    "domain5": "entry.911865149",   # DOMAINE 5 : SÉCURITÉ NUMÉRIQUE
    "global": "entry.294442511"     # RESULTAT GLOBAL
}

# Domain name mapping from questions JSON to form fields
DOMAIN_MAPPING = {
    "DOMAINE 1 : INFORMATIONS ET DONNÉES": "domain1",
    "DOMAINE 2 : COMMUNICATION ET COLLABORATION": "domain2",
    "DOMAINE 3 : CRÉATION DE CONTENU": "domain3",
    "DOMAINE 4 : RÉSOLUTION DE PROBLÈMES": "domain4",
    "DOMAINE 5 : SÉCURITÉ": "domain5"
}


def calculate_domain_results(user_answers: List[Dict], all_questions: List[Dict]) -> Dict[str, float]:
    """
    Calculate percentage results for each domain
    
    Args:
        user_answers: List of user answers with question indices and selected options
        all_questions: Full questions dataset from JSON
        
    Returns:
        Dictionary with domain percentages
    """
    domain_scores = defaultdict(lambda: {"correct": 0, "total": 0})
    
    for answer in user_answers:
        question_index = answer.get("questionIndex", 0)
        selected_option_index = answer.get("selectedOption", -1)
        
        if question_index < len(all_questions) and selected_option_index >= 0:
            question = all_questions[question_index]
            domain = question.get("domaine", "")
            options = question.get("options", [])
            
            # Count as attempt for this domain
            domain_scores[domain]["total"] += 1
            
            # Check if answer is correct
            if selected_option_index < len(options):
                if options[selected_option_index].get("isCorrect", False):
                    domain_scores[domain]["correct"] += 1
    
    # Calculate percentages
    domain_percentages = {}
    for domain, scores in domain_scores.items():
        if scores["total"] > 0:
            percentage = round((scores["correct"] / scores["total"]) * 100, 1)
            domain_percentages[domain] = percentage
        else:
            domain_percentages[domain] = 0.0
    
    return domain_percentages


def calculate_global_result(domain_percentages: Dict[str, float]) -> float:
    """
    Calculate overall global percentage from domain percentages
    
    Args:
        domain_percentages: Dictionary of domain percentages
        
    Returns:
        Global percentage (average of all domains)
    """
    if not domain_percentages:
        return 0.0
    
    total = sum(domain_percentages.values())
    average = total / len(domain_percentages)
    return round(average, 1)


def get_form_prefill_url(
    nom: str,
    prenom: str,
    domain_results: Dict[str, float],
    global_result: Optional[float] = None
) -> str:
    """
    Generate a pre-filled form URL that can be opened in a browser
    This is the recommended method when direct submission requires authentication
    
    Args:
        nom: Last name
        prenom: First name
        domain_results: Dictionary with domain names as keys and percentages as values
        global_result: Optional global percentage (calculated if not provided)
        
    Returns:
        Pre-filled URL string
    """
    if global_result is None:
        global_result = calculate_global_result(domain_results)
    
    params = {
        FORM_FIELDS['nom']: nom,
        FORM_FIELDS['prenom']: prenom,
        FORM_FIELDS['global']: str(global_result)
    }
    
    for domain_name, domain_key in DOMAIN_MAPPING.items():
        percentage = domain_results.get(domain_name, 0.0)
        params[FORM_FIELDS[domain_key]] = str(percentage)
    
    return f"{FORM_VIEW_URL}?{urlencode(params)}"


def open_prefilled_form(
    nom: str,
    prenom: str,
    domain_results: Dict[str, float],
    global_result: Optional[float] = None
) -> str:
    """
    Open a pre-filled form in the default browser
    User just needs to click "Submit" in the browser
    
    Args:
        nom: Last name
        prenom: First name
        domain_results: Dictionary with domain names as keys and percentages as values
        global_result: Optional global percentage (calculated if not provided)
        
    Returns:
        The URL that was opened
    """
    url = get_form_prefill_url(nom, prenom, domain_results, global_result)
    
    if global_result is None:
        global_result = calculate_global_result(domain_results)
    
    print(f"📱 Opening pre-filled form for {prenom} {nom}")
    print(f"   Global result: {global_result}%")
    for domain_name, percentage in domain_results.items():
        print(f"   {domain_name}: {percentage}%")
    print(f"\n🌐 URL: {url}")
    print("\n✅ Please click 'Envoyer' (Submit) in the browser to complete submission")
    
    webbrowser.open(url)
    return url


def submit_to_google_form(
    nom: str,
    prenom: str,
    domain_results: Dict[str, float],
    global_result: Optional[float] = None,
    use_browser: bool = False
) -> bool:
    """
    Submit quiz results to Google Form
    
    Args:
        nom: Last name
        prenom: First name
        domain_results: Dictionary with domain names as keys and percentages as values
        global_result: Optional global percentage (calculated if not provided)
        use_browser: If True, opens pre-filled form in browser instead of direct POST
        
    Returns:
        True if submission successful, False otherwise
    """
    # Validate required fields
    if not nom or not prenom:
        print("❌ Error: Name and first name are required")
        return False
    
    # Calculate global result if not provided
    if global_result is None:
        global_result = calculate_global_result(domain_results)
    
    # If browser mode, open pre-filled form
    if use_browser:
        open_prefilled_form(nom, prenom, domain_results, global_result)
        return True  # Assume user will submit
    
    # Try direct POST submission
    form_data = {
        FORM_FIELDS["nom"]: nom,
        FORM_FIELDS["prenom"]: prenom,
        FORM_FIELDS["global"]: str(global_result)
    }
    
    # Add domain results
    for domain_name, domain_key in DOMAIN_MAPPING.items():
        percentage = domain_results.get(domain_name, 0.0)
        form_data[FORM_FIELDS[domain_key]] = str(percentage)
    
    # Submit to Google Form
    try:
        response = requests.post(
            FORM_SUBMIT_URL,
            data=form_data,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            timeout=10
        )
        
        # Google Forms redirects on success (status 200 or 302/303)
        if response.status_code in [200, 302, 303]:
            print(f"✅ Results successfully submitted for {prenom} {nom}")
            print(f"   Global result: {global_result}%")
            for domain_name, percentage in domain_results.items():
                print(f"   {domain_name}: {percentage}%")
            return True
        elif response.status_code == 401:
            print("⚠️  Direct submission requires authentication")
            print("💡 Opening pre-filled form in browser instead...")
            open_prefilled_form(nom, prenom, domain_results, global_result)
            return True
        else:
            print(f"⚠️  Direct submission failed (status {response.status_code})")
            print("💡 Opening pre-filled form in browser instead...")
            open_prefilled_form(nom, prenom, domain_results, global_result)
            return True
            
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Network error: {e}")
        print("💡 Opening pre-filled form in browser instead...")
        open_prefilled_form(nom, prenom, domain_results, global_result)
        return True


def submit_from_json_results(
    nom: str,
    prenom: str,
    user_answers: List[Dict],
    questions_file: str = "questions_digcomp_final.json",
    use_browser: bool = False
) -> bool:
    """
    Submit results from quiz JSON data structure
    
    Args:
        nom: Last name
        prenom: First name
        user_answers: List of user answers from quiz
        questions_file: Path to questions JSON file
        use_browser: If True, opens pre-filled form in browser
        
    Returns:
        True if submission successful, False otherwise
    """
    try:
        # Load all questions
        with open(questions_file, 'r', encoding='utf-8') as f:
            all_questions = json.load(f)
        
        # Calculate domain results
        domain_results = calculate_domain_results(user_answers, all_questions)
        
        # Submit to form
        return submit_to_google_form(nom, prenom, domain_results, use_browser=use_browser)
        
    except FileNotFoundError:
        print(f"❌ Error: Questions file '{questions_file}' not found")
        return False
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON in '{questions_file}'")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


if __name__ == "__main__":
    # Example usage with sample data
    print("DigComp Quiz Results Submission Tool")
    print("=" * 50)
    
    # Example: Submission with browser fallback
    print("\n📝 Testing submission (with browser fallback if needed)")
    sample_domain_results = {
        "DOMAINE 1 : INFORMATIONS ET DONNÉES": 75.0,
        "DOMAINE 2 : COMMUNICATION ET COLLABORATION": 85.5,
        "DOMAINE 3 : CRÉATION DE CONTENU": 65.0,
        "DOMAINE 4 : RÉSOLUTION DE PROBLÈMES": 70.0,
        "DOMAINE 5 : SÉCURITÉ": 80.0
    }
    
    success = submit_to_google_form(
        nom="Test",
        prenom="User",
        domain_results=sample_domain_results,
        use_browser=True  # Force browser mode for demo
    )
    
    if success:
        print("\n✅ Submission initiated successfully!")
    else:
        print("\n❌ Submission failed")
