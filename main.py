from fastapi import FastAPI, Form
from fastapi.responses import StreamingResponse
from pypix.pix import Pix
import io
from PIL import Image  # pip install pillow qrcode[pil]

app = FastAPI()

@app.post("/gerar-pix")
async def gerar_pix(chave: str = Form(...), valor: float = Form(0.0), nome: str = Form(""), desc: str = Form("")):
    pix = Pix()
    pix.set_key(chave)
    pix.set_name_receiver(nome)
    pix.set_description(desc)
    pix.set_amount(valor)
    pix.set_city_receiver("Sao Paulo")  # Seu padrão
    brcode = pix.get_br_code()
    img = pix.save_qrcode(quiet=True)  # Bytes do QR
    return {"payload": brcode, "qr": img}
