# Alyra Final Project - Machine Learning & Deep Learning

Projet final de la formation Alyra : deux projets ML/DL complets.

## Projets

### 1. Pokemon Classifier (Deep Learning)
Classification d'images de Pokemon (151 classes, 1ère génération) avec CNN et Transfer Learning.

**Contenu :**
- `PokemonClassifier.ipynb` - CNN from scratch
- `PokemonClassifier_TransferLearning.ipynb` - Transfer Learning avec EfficientNet
- `api/` - API FastAPI pour l'inférence
- `frontend/` - Interface Vue.js

**Modèles entraînés :**
- `pokemon_classifier.keras` - CNN custom (~77% accuracy)
- `pokemon_classifier_efficientnet.keras` - EfficientNet (~87% accuracy)

### 2. Developer Productivity (Machine Learning)
Analyse et prédiction de la productivité des développeurs.

**Contenu :**
- `Developer_Productivity.ipynb` - Analyse exploratoire et modèles ML
- `Developer_Productivity_Synthetic_Syncora.csv` - Dataset

---

## Installation

### Dataset Pokemon

Le dataset (~4 Go, 32 000+ images) n'est pas inclus dans le repo.

**Option 1 : Via kagglehub (recommandé)**
```python
import kagglehub

path = kagglehub.dataset_download("brkurzawa/original-150-pokemon-image-search-results")
print("Path to dataset files:", path)
```

**Option 2 : Téléchargement manuel**
1. Aller sur [Kaggle - Original 151 Pokemon Image Search Results](https://www.kaggle.com/datasets/brkurzawa/original-150-pokemon-image-search-results)
2. Télécharger et extraire dans `DL-PokemonClassification/PokemonData/`

### Dépendances

```bash
# Pokemon Classifier
cd DL-PokemonClassification
pip install -r requirements.txt

# API
cd api
pip install -r requirements.txt
```

---

## Utilisation

### Entraînement
Exécuter les notebooks Jupyter dans l'ordre.

### API Pokemon Classifier
```bash
cd DL-PokemonClassification/api
uvicorn main:app --reload
```

### Frontend
```bash
cd DL-PokemonClassification/frontend
npm install
npm run dev
```

---

## Stack technique

- **Deep Learning** : TensorFlow/Keras, EfficientNet
- **Machine Learning** : Scikit-learn, Pandas, NumPy
- **API** : FastAPI
- **Frontend** : Vue.js, Vite
- **Visualisation** : Matplotlib, Seaborn
