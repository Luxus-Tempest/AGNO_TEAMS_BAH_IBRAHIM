### AGNO_TEAMS_BAH_IBRAHIM — Équipe d’agents IA pour Finance et RH

Ce repository regroupe des scripts Python orchestrant des équipes d’agents IA (basées sur la librairie `agno`) pour deux cas d’usage principaux :

- **Finance**: collecte d’actualités, analyse, synthèse et visualisation pour des actions technologiques majeures.
- 
- **Investissement**: collecte, analyse, synthèse et visualisation pour des actions technologiques majeures.

- **RH/Talent Matching**: parsing de CV (PDF), appariement avec une fiche de poste et génération d’un rapport recruteur.

Les prompts, rôles et paramètres des agents sont centralisés dans `constantes/` afin de faciliter la personnalisation.

---

### Fonctionnalités

- **Talent Matching** (`Talent_matching.py`)

  - Extraction de texte depuis des CV PDF via `PyMuPDF` (`fitz`).
  - Équipe RH composée de 3 agents : Parser, Matcher, Report Writer.
  - Compare le CV aux exigences de poste et produit un rapport clair (table, synthèse, recommandations).
  - Configuration des prompts/roles dans `constantes/Talent_matcher.py`.

- **Analyse Finance – Tech Stocks** (`finance_team_project.py`)

  - Agents : Analyse technique, Sentiment de marché (outils `YFinance`), Synthèse.
  - Orchestration d’équipe et rendu des réponses des membres.
  - Paramètres et prompts dans `constantes/finance.py`.

- **Générateur de rapport d’investissement** (`investment_report_generator.py`)
  - Agents : News, Analyse, Rédaction de rapport, Visualisation.
  - Pipeline de bout en bout: collecte → analyse → rapport → « visualisations » terminal.
  - Paramètres et prompts dans `constantes/investment_report_generator.py`.

---

### Prérequis

- **Python 3.10+** recommandé
- Clé API OpenAI valide
- Windows PowerShell (instructions ci-dessous), ou tout shell équivalent

Dépendances principales (installées via `pip`):

```bash
pip install agno python-dotenv PyMuPDF yfinance duckduckgo-search
```

Remarques:

- `agno` fournit les classes `Agent`, `Team`, modèles OpenAI et divers outils (`DuckDuckGoTools`, `YFinanceTools`, `ReasoningTools`).
- `PyMuPDF` (module `fitz`) est requis pour l’extraction de texte des PDF.

---

### Configuration

Créez un fichier `.env` à la racine du projet (par exemple `C:\AGNO_LEARNING\.env`) avec les variables suivantes :

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Notes:

- Les scripts lisent `OPENAI_API_KEY` via `python-dotenv`.

---

### Arborescence (extrait)

```text
AGNO_TEAMS_BAH_IBRAHIM/
  Talent_matching.py
  finance_team_project.py
  investment_report_generator.py
  constantes/
    Talent_matcher.py
    finance.py
    investment_report_generator.py
    cv_specimen.pdf (exemple; placez le CV test PDF ici)
```

---

### Utilisation rapide (Windows PowerShell)

Positionnez-vous à la racine du workspace, puis exécutez :

- **Talent Matching (RH)**
  - Déposez vos CV en PDF dans `AGNO_TEAMS_BAH_IBRAHIM/constantes/`.
  - Le script traite tous les `.pdf` trouvés dans ce dossier.

```powershell
python .\AGNO_TEAMS_BAH_IBRAHIM\Talent_matching.py
```

- **Tech Stocks – Équipe Finance**

```powershell
python .\AGNO_TEAMS_BAH_IBRAHIM\finance_team_project.py
```

- **Générateur de rapport d’investissement**

```powershell
python .\AGNO_TEAMS_BAH_IBRAHIM\investment_report_generator.py
```

Les sorties sont affichées dans la console (avec option `stream=True` dans plusieurs scripts pour un rendu progressif).

---

### Personnalisation

- **Prompts et rôles des agents**:

  - RH: `constantes/Talent_matcher.py` (`PARSER`, `MATCHER`, `WRITER`, `HR_TEAM`, `JOB_DESCRIPTION`).
  - Finance (Tech Stocks): `constantes/finance.py` (`TECH_AGENT`, `MARKET_AGENT`, `SYNTH_AGENT`, `TEAM`, `RESPONSE_PROMPT`).
  - Rapport d’investissement: `constantes/investment_report_generator.py` (`NEWS_AGENT`, `ANALYSIS_AGENT`, `REPORT_WRITER`, `DATA_VISUALIZER`, `TEAM`, `MAIN_PROMPT`).

- **Modèle OpenAI**: ajustez `MODEL_ID` dans `.env`.
- **Sources de données**: les outils `DuckDuckGoTools` et `YFinanceTools` sont activés dans les scripts concernés.

---

### Dépannage

- Erreur « Missing OPENAI_API_KEY/MODEL_ID »:

  - Vérifiez votre `.env` et relancez le terminal pour recharger l’environnement.

- `ModuleNotFoundError: fitz`:

  - Installez `PyMuPDF` (`pip install PyMuPDF`).

- Appels réseau lents/bloqués:

  - Vérifiez la connectivité Internet et les éventuels proxy/pare-feu.

- Sortie vide/incomplète:
  - Selon le modèle et les quotas API, la réponse peut varier. Réessayez ou changez `MODEL_ID`.
