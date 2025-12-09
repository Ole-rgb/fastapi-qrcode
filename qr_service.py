import qrcode
import io
import hashlib
from cachetools import TTLCache
from models import QRParams


# In-memory cache for QR codes with TTL of 5 minutes
qr_store = TTLCache(maxsize=32, ttl=300)


def make_qr_hash(data: QRParams) -> str:
    """Generate a unique hash for the QR code based on its encoded url and parameters."""
    key_string = f"{'|'.join(map(str, data.model_dump().values()))}"
    print("*** Key String: ", key_string, " ***")
    return hashlib.sha256(key_string.encode("utf-8")).hexdigest()


def generate_qr(data: QRParams) -> tuple[str, bytes]:
    """
    Generate a QR code based on the provided parameters.
    
    :param data: QRParams object containing unique parameters for the QR code.
    :return: Tuple of (qr_id, image_bytes)
    """
    qr = qrcode.QRCode(
        border=data.borders,
        error_correction=qrcode.constants.ERROR_CORRECT_L
    )
    qr.add_data(data.link)
    qr.make(fit=True)
    img = qr.make_image(fill_color=data.qr_color, back_color=data.bg_color)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    
    qr_id = make_qr_hash(data)
    qr_store[qr_id] = buffer.getvalue()
    
    print("*** Cache: ", [k for k, v in qr_store.items()], " ***")
    
    return qr_id, buffer.getvalue()


def retrieve_qr(qr_id: str) -> bytes | None:
    """
    Retrieve the QR code image by its ID.
    
    :param qr_id: The unique identifier for the QR code.
    :return: QR code image bytes or None if not found.
    """
    return qr_store.get(qr_id)
