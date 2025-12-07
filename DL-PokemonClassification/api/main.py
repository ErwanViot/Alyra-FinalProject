from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
import numpy as np
from pathlib import Path
from PIL import Image
import io

app = FastAPI(title="Pokemon Classifier API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Charger le modèle et les labels au démarrage
MODEL_PATH = Path(__file__).parent.parent / "pokemon_classifier_efficientnet.keras"
model = None
labels = None

@app.on_event("startup")
async def load_model():
    global model, labels
    model = tf.keras.models.load_model(MODEL_PATH)

    # Charger les labels depuis le dataset
    data_path = Path(__file__).parent.parent / "PokemonData"
    labels = sorted([d.name for d in data_path.iterdir() if d.is_dir()])
    print(f"Modèle chargé: {len(labels)} classes")


def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """Prétraite une image pour le modèle EfficientNet."""
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((256, 256))
    img_array = np.array(img, dtype=np.float32)
    img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)
    return img_array


@app.post("/predict")
async def predict(files: list[UploadFile] = File(...)):
    """Prédit le Pokémon pour une ou plusieurs images."""
    results = []

    for file in files:
        image_bytes = await file.read()
        img_array = preprocess_image(image_bytes)

        prediction = model.predict(np.expand_dims(img_array, 0), verbose=0)

        # Top 3 prédictions
        top3_idx = np.argsort(prediction[0])[-3:][::-1]
        top3 = [
            {"name": labels[i], "confidence": float(prediction[0][i])}
            for i in top3_idx
        ]

        results.append({
            "filename": file.filename,
            "predictions": top3
        })

    return {"results": results}


@app.get("/health")
async def health():
    return {"status": "ok", "model_loaded": model is not None}
