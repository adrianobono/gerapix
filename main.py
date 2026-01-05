from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import subprocess
import uuid  # Para txid único

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def form():
    return """
    <h2>Gerador Pix Estático</h2>
    <form action="/pix" method="post">
        <label>Chave Pix: <input type="text" name="chave" required></label><br>
        <label>Nome Recebedor: <input type="text" name="nome" required></label><br>
        <label>Cidade: <input type="text" name="cidade" value="Sao Paulo" required></label><br>
        <label>Valor (R$): <input type="number" name="valor" step="0.01"></label><br>
        <label>Descrição: <input type="text" name="desc" maxlength="140"></label><br>
        <label>TXID (auto): <input type="text" name="txid" placeholder="Gerado auto"></label><br>
        <input type="submit" value="Gerar Payload + QR">
    </form>
    """

@app.post("/pix")
async def pix(chave: str = Form(...), nome: str = Form(...), cidade: str = Form(...), 
              valor: str = Form(0), desc: str = Form(""), txid: str = Form("")):
    if not txid: txid = str(uuid.uuid4())[:25].upper().replace('-', '')
    cmd = (f"gerapix --chave={chave} --nome={nome} --cidade={cidade} "
           f"{'--valor=' + valor if valor else ''} "
           f"{'--txid=' + txid if txid else ''} "
           f"{'--desc=' + desc if desc else ''}")
    result = subprocess.run(cmd.split(), capture_output=True, text=True, cwd="/app")  # cwd se precisar
    return {"payload": result.stdout.strip(), "cmd_used": cmd, "txid": txid}
