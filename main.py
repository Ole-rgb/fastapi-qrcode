from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import io

from models import QRParams
from qr_service import generate_qr, retrieve_qr


app = FastAPI(
    title="QR Code API",
    description="FastAPI application, deployed via Vercel, that generates QR codes.",
    version="1.0.0",
)


# Allow frontend origin (change to your frontend URL)
origins = [
    "http://localhost:3000", # local frontend dev
    "http://192.168.0.62:3000",                   # LAN dev frontend
    "https://qrcode-frontend-iota.vercel.app",   # deployed frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   # important: allow OPTIONS and all methods
    allow_headers=["*"],
)


@app.post("/qr", response_class=JSONResponse)
def create_qr(data: QRParams):
    """
    Create a QR code based on the provided parameters.
    
    **Parameters:**
    - **link**: The URL to be encoded in the QR code
    - **qr_color**: Color of the QR code (default: "black")
    - **bg_color**: Background color of the QR code (default: "white")
    - **borders**: Border size of the QR code (default: 0)
    
    **Returns:**
    - **message**: Success message
    - **image_url**: URL to retrieve the generated QR code
    - **metadata**: Input parameters used to generate the QR code
    """
    qr_id, _ = generate_qr(data)
    
    return {
        "message": "QR created",
        "image_url": f"/qr/{qr_id}",
        "metadata": {
            "data": data,
        }
    }


@app.get("/qr/{qr_id}", response_class=StreamingResponse)
def get_qr(qr_id: str):
    """
    Retrieve the QR code image by its ID.
    
    **Parameters:**
    - **qr_id**: The unique identifier for the QR code (returned from POST /qr)
    
    **Returns:**
    - PNG image stream of the QR code
    - 404 error if QR code not found or expired
    """
    qr_data = retrieve_qr(qr_id)
    if qr_data is None:
        return JSONResponse(status_code=404, content={"error": "QR not found"})

    buffer = io.BytesIO(qr_data)
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="image/png")
