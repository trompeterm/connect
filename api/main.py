from pathlib import Path

import uvicorn
import torch
from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import get_model

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/predict")
async def predict(board: list[list[int]] = Body(...)):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_name = "cnn"
    model = get_model(model_name).to(device)
    model.load_state_dict(torch.load(Path(__file__).resolve().parent / "models" / "best.pt", map_location=device))
    model.eval()

    board_tensor = torch.tensor(board, dtype=torch.float32).unsqueeze(0).to(device)
    with torch.no_grad():
        output = model(board_tensor)
        prediction = output.argmax(dim=1).item()

    return {"predicted_move": prediction}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)