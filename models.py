from pydantic import BaseModel, Field


class QRParams(BaseModel):
    """
    QRParams represent the parameters used for generating a QR code.
    """
    link: str = Field(..., description="The URL to be encoded in the QR code")
    qr_color: str = Field(default="black", description="Color of the QR code")
    bg_color: str = Field(default="transparent", description="Background color of the QR code")
    borders: int = Field(default=0, description="Border size of the QR code")
