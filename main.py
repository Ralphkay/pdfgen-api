import uuid
from typing import Optional

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

import httpx
import pdfgen
from fastapi import FastAPI
from pydantic import BaseModel

# pdfkit.from_url('http://google.com', 'out.pdf')

app = FastAPI()


class TextData(BaseModel):
    body: str
    filename: Optional[str] = f"{uuid.uuid4()}"


@app.post("/api/v1/from-url")
async def generate_pdf_from_url(url: str, name: Optional[str] = uuid.uuid4()):
    async with httpx.AsyncClient() as client:
        res = await client.get(url)
        await pdfgen.from_url(url, f"{name}.pdf")
        # pdfkit.from_url(res.text, 'pdf.pdf')
    return res.text


@app.post('/api/v1/from-text')
async def generate_pdf_from_text(doc: TextData):
    await pdfgen.from_string(doc.body, f"{doc.filename}.pdf")
    return 'done'

#
# @app.get('/private')
# async def private(token: str = Depends(oauth2_scheme)):
#     return {"token":token}