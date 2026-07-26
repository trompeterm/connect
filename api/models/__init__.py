from models.mlp import Connect4MLP
from models.cnn import Connect4CNN

def get_model(name):
    models = {
        "mlp": Connect4MLP,
        "cnn": Connect4CNN,
    }

    if name not in models:
        raise ValueError(f"Model '{name}' not found. Available models: {list(models.keys())}")

    return models[name]()