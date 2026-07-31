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


from data.transforms import CNNBoard

transform = CNNBoard()

device = torch.device(
    "cuda" if torch.cuda.is_available()
    else "cpu"
)

model = get_model("cnn").to(device)

model.load_state_dict(
    torch.load(
        Path(__file__).resolve().parent / "models" / "best.pt",
        map_location=device
    )
)

model.eval()


@app.post("/predict")
async def predict(board: list[list[int]] = Body(...)):

    # Convert input board to tensor
    board_tensor = torch.tensor(
        board,
        dtype=torch.float32
    )

    # Convert 6x7 board -> 2x6x7 for CNN
    board_tensor = transform(board_tensor)

    # Add batch dimension:
    # (2,6,7) -> (1,2,6,7)
    board_tensor = board_tensor.unsqueeze(0)

    board_tensor = board_tensor.to(device)

    with torch.no_grad():
        output = model(board_tensor)

        probabilities = torch.softmax(
            output,
            dim=1
        )

        prediction = torch.argmax(
            probabilities,
            dim=1
        ).item()

    return {
        "predicted_move": prediction,
        "confidence": probabilities[0][prediction].item(),
        "probabilities": probabilities[0].tolist()
    }


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)