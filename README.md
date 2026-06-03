# INVENIO — Générateur de fiches de sélection France Air

INVENIO est une application web interne pour les commerciaux **France Air**
(gamme Solution Habitat). Un commercial dépose une fiche technique GALLETTI
(DOCX ou PDF), et INVENIO génère automatiquement une **fiche de sélection PDF**
au design France Air.

> **Deux contraintes absolues :**
> 1. **100% gratuit** (Vercel + Baserow, offres gratuites).
> 2. **Ultra simple à maintenir** : une personne non technique met à jour toutes
>    les données via la page **Maintenance**, sans jamais voir de code.

---

## Sommaire

- [Ce que fait INVENIO](#ce-que-fait-invenio)
- [Architecture](#architecture)
- [Installation & développement](#installation--développement)
- [Variables d'environnement](#variables-denvironnement)
- [Les tables Baserow](#les-tables-baserow)
- [La page Maintenance](#la-page-maintenance)
- [Déploiement Vercel](#déploiement-vercel)
- [Tests](#tests)
- [Guide pour la commerciale](GUIDE_MAINTENANCE.md)

---

## Ce que fait INVENIO

Workflow en 6 écrans :

1. **Import** — dépôt d'une fiche GALLETTI (glisser-déposer), analyse automatique.
2. **Machine** — confirmation modèle / taille / type / acoustique (auto-détectés).
3. **Projet & Client** — n° projet, nom, recherche client avec autocomplétion.
4. **Contacts** — TCI / TCS du département + contact Solution.
5. **Options** — catalogue en accordéon, options pré-cochées d'après la désignation.
6. **Génération** — aperçu page de garde + génération du PDF (7 parties).

Le **PDF** contient : page de garde, sommaire, performances, texte de
prescription, plans, options retenues, page contacts (carte de France).

---

## Architecture

```
Frontend (React + Vite + TS + Tailwind)
        │  appels API REST
Backend (Python FastAPI)
   • Parser DOCX/PDF (extraction GALLETTI)
   • Génération PDF (WeasyPrint + Jinja2)
   • API contacts / clients / options / maintenance
        │
Base de données (Baserow — no-code, gratuit)
```

- **Aucune donnée métier en dur dans le code.** Contacts, options, textes,
  libellés, mappings de désignation : tout vit dans Baserow et s'édite depuis
  la page Maintenance.

Structure des dossiers : voir `src/` (backend) et `ui/` (frontend).

---

## Installation & développement

### Prérequis
- Python 3.12 (3.11 fonctionne aussi)
- Node.js 18+
- Pour la génération PDF en local : les bibliothèques système de WeasyPrint
  (`libpango`, `libcairo`…). Voir le `Dockerfile` pour la liste exacte.

### Backend
```bash
pip install -e .[dev]
cp .env.example .env        # puis renseignez BASEROW_TOKEN, etc.
uvicorn src.api.main:app --reload --port 8000
```

### Frontend
```bash
cd ui
npm install
npm run dev                 # http://localhost:5173 (proxy /api -> :8000)
```

### Build de production
```bash
cd ui && npm run build      # génère ui/dist (servi par FastAPI)
```

---

## Variables d'environnement

Voir `.env.example`. Les principales :

| Variable | Rôle |
|----------|------|
| `BASEROW_TOKEN` | jeton d'accès à l'API Baserow |
| `BASEROW_TABLE_*` | identifiants des tables Baserow |
| `MAINTENANCE_PASSWORD` | mot de passe de la page Maintenance |
| `VITE_API_URL` | URL de l'API (vide = même origine, en production) |

---

## Les tables Baserow

**Existantes** (à utiliser tel quel) :

| Table | ID | Contenu |
|-------|----|---------|
| CLIENTS | 939119 | code tiers, nom, code postal, département |
| Contacts FORCE DE VENTE | 939355 | TCI / TCS par département |
| Contacts SOLUTION | 939361 | contacts Solution |
| OPTIONS et ACCESSOIRES | 941070 | catalogue d'options |
| PRIX MACHINES | 939101 | prix |

**À créer** (renseigner ensuite les IDs dans `.env`) :

- **`DECODAGE_DESIGNATION`** — colonnes : `position_start`, `position_end`,
  `code_attendu`, `option_label`, `categorie`, `modele`.
- **`TEXTES_PRESCRIPTION`** — colonnes : `modele`, `texte_prescription`.
- **`LIBELLES_UI`** — colonnes : `cle`, `valeur`, `page`.

> Le code lit les colonnes de façon **tolérante** : plusieurs variantes de noms
> sont acceptées (ex. `Département`, `departement`, `dept`). Vous n'avez pas
> besoin de renommer vos colonnes existantes.

### La chaîne de désignation

Chaque fiche GALLETTI contient une chaîne du type :

```
VLS254HS0B  A000C00020G010I 00000000000000000000
```

- `VLS` = modèle, `254` = taille, `H` = PAC (`C` = GEG), `S` = standard (`L` = silencieux).
- Le bloc suivant encode les options **position par position**.

INVENIO extrait toujours cette chaîne **depuis l'intérieur du document**, jamais
depuis le nom du fichier. Les positions du « segment d'options » se comptent sur
la concaténation (sans espaces) des blocs qui suivent le premier bloc. La
correspondance position → option est définie dans la table
`DECODAGE_DESIGNATION` : **si GALLETTI change le format, la commerciale modifie
la table — pas le code.**

---

## La page Maintenance

Accessible via `/maintenance`, protégée par `MAINTENANCE_PASSWORD`. Six onglets,
en français, sans jargon :

1. **Contacts commerciaux** — consultation TCI/TCS par département + Solution.
2. **Options & accessoires** — ajouter / modifier / supprimer (filtre par modèle).
3. **Textes de prescription** — un éditeur par modèle, avec aperçu.
4. **Décodage désignation** — tableau « à la position X, le code Y = l'option Z ».
5. **Clients** — recherche, ajout, modification.
6. **Textes de l'interface** — modifier les mots affichés dans l'application
   (table `LIBELLES_UI`), sans toucher au code.

Détails pas-à-pas : voir **[GUIDE_MAINTENANCE.md](GUIDE_MAINTENANCE.md)**.

---

## Déploiement Vercel

1. `cd ui && npm run build`
2. Committer le build : `git add -f ui/dist/`
3. Pousser : Vercel build `src/api/main.py` (voir `vercel.json`) qui sert l'API
   **et** le frontend (`ui/dist`).
4. Renseigner les variables d'environnement dans les *Settings* Vercel.
5. **Désactiver la Deployment Protection** pour que les appels API fonctionnent.

Migration future vers Oracle Cloud Always Free : utiliser le `Dockerfile` fourni.

---

## Tests

```bash
python3 -m pytest tests/ -q      # tests backend
cd ui && npm run build           # vérifie la compilation TypeScript
```

Les tests couvrent le décodage de la désignation, la normalisation des tailles,
le décodage d'options et les routes API (sans Baserow réel).
