# Guide de la page Maintenance

Ce guide s'adresse à la personne qui met à jour INVENIO. **Aucune compétence
technique n'est nécessaire.** Vous n'aurez jamais à toucher au code ni à GitHub.

---

## 1. Se connecter

1. Ouvrez l'application INVENIO.
2. En haut à droite, cliquez sur **⚙︎ Maintenance**.
3. Saisissez le **mot de passe** (fourni par France Air) et cliquez sur
   **Déverrouiller**.

Vous arrivez sur une page avec **6 onglets** en haut. Cliquez sur un onglet pour
changer de section.

---

## 2. Les 6 onglets

### 👥 Contacts commerciaux
Tapez un **numéro de département** (ex. `69`) puis cliquez sur **Afficher**.
Vous voyez les TCI / TCS de ce département et les contacts Solution.

### 🧩 Options & accessoires
Le catalogue d'options proposées aux commerciaux.
- **+ Ajouter** : crée une nouvelle option (code, libellé, catégorie, prix…).
- **✎** : modifie une ligne.
- **🗑** : supprime une ligne (une confirmation est demandée).
- Le menu **Tous les modèles** filtre l'affichage.

### 📝 Textes de prescription
Le texte qui apparaît dans le PDF, **un par modèle**.
1. Choisissez le **modèle** dans le menu.
2. Écrivez ou modifiez le texte dans la grande zone.
3. Cliquez sur **Aperçu** pour voir le rendu.
4. Cliquez sur **✓ Enregistrer**.

### 🔠 Décodage désignation
C'est le tableau qui explique à INVENIO **quelles options sont incluses** selon
la désignation GALLETTI.

> Chaque ligne dit : « à telle **position** de la désignation, si le **code** est
> tel, alors c'est telle **option** ».

Si GALLETTI change un jour sa façon d'écrire les désignations, il suffit de
corriger ce tableau ici — **rien d'autre à faire**.

- **Position début / Position fin** : l'emplacement dans la désignation.
- **Code attendu** : la suite de caractères à reconnaître.
- **Option** : le nom de l'option correspondante.

### 🏢 Clients
Recherchez un client, ajoutez-en un nouveau ou modifiez ses informations
(code tiers, nom, code postal, département).

### 🏷️ Textes de l'interface
Permet de **changer les mots affichés dans l'application** (titres, boutons…).
- La colonne **Identifiant** relie le texte à un endroit précis : **ne la
  changez pas**.
- Modifiez uniquement la colonne **Texte affiché**.
- Exemple : pour changer le grand titre de l'accueil, trouvez la ligne
  `home.titre` et modifiez son texte.

---

## 3. Règles d'or

- ✅ Après chaque modification, un message **« ✓ Enregistré »** confirme.
- ✅ Le bouton **Annuler** abandonne une saisie en cours.
- ✅ Tout est sauvegardé dans votre base **Baserow** : vous pouvez aussi y aller
  directement si vous préférez.
- ⚠️ Ne changez pas les **identifiants** (colonne de gauche dans « Textes de
  l'interface » et codes des options) sauf si vous savez ce que vous faites.

---

## 4. En cas de souci

- **« Mot de passe incorrect »** : vérifiez le mot de passe auprès de France Air.
- **Une donnée ne s'affiche pas** : vérifiez qu'elle existe bien dans Baserow et
  que le département/modèle est correctement orthographié.
- Pour toute question technique, contactez l'administrateur de l'application.
