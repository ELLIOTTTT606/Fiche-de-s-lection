# Pages de garde (PNG)

Déposez ici les images de page de garde, **une par modèle + taille**, nommées
exactement :

```
{MODELE}_{TAILLE}.png
```

Exemples : `PLP_52.png`, `VLS_254.png`, `MPED_76.png`.

- Le PNG sert de fond à la page de garde du PDF.
- INVENIO superpose par-dessus le **nom du projet** (bleu France Air) et le
  **type de machine**.
- Si une image contient déjà un texte d'exemple (ex. `PLP_45`, `PLP_52`), le
  générateur pose un rectangle de la couleur du fond (`#eef0f1`) pour le masquer
  avant d'écrire le vrai texte.

Si l'image d'un modèle/taille est absente, INVENIO génère tout de même la fiche
avec une page de garde sobre affichant le modèle et la taille.
