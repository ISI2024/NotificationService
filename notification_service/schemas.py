from pydantic import BaseModel
from enum import unique
from typing import Optional
from common import enums

@unique
class Templates(enums.NoValue):
    VERIFICATION_CODE = 'verification_token.html'
    FINISHED_TEST = 'finished_test.html'

class EmailActorMessage(BaseModel):
    recipient: str
    template: Templates
    context: dict = {}