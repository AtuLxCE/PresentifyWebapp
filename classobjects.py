from pydantic import BaseModel
from typing import Optional, ClassVar

class PDF(BaseModel):
    textdata: Optional[str]
    title: Optional[str]
    author: Optional[str]


class Presentation(BaseModel):
    title :Optional[str] = None
    author: Optional[str] = None
    # abstract = Optional[str]
    introduction:Optional[str] = None
    literature_review: Optional[str] = None
    methodology:Optional[str]= None
    results :Optional[str]= None
    conclusions: Optional[str]= None

class TextSummaryRequest(BaseModel):
    text: str

class TextSummaryResponse(BaseModel):
    summary: str
