from pydantic import BaseModel
from enum import Enum, unique
from typing import Optional

class NoValue(Enum):

    def __repr__(self):
        return '<%s.%s>' % (self.__class__.__name__, self.name)

@unique
class Templates(NoValue):
    VERIFICATION_CODE = 'verification_token.html'
    FINISHED_TEST = 'finished_test.html'

class EmailActorMessage(BaseModel):
    recipient: str
    template: Templates
    context: dict = {}


# -----
# -----


class QrCodeData(BaseModel):
    login: str
    exp: int


# -----
@unique
class SocketMessageType(NoValue):
    TOKEN = 'TOKEN'
    AWAIT_RESULT = 'AWAIT_RESULT'


class SocketMessage(BaseModel):
    kind: SocketMessageType
    token: Optional[str]


# ----


class ExaminationResult(BaseModel):
    fk_user: str
    analyzer: str
    id: int
    examination_date: str
    leukocytes: Optional[str] = None
    nitrite: Optional[str] = None
    urobilinogen: Optional[str] = None
    protein: Optional[str] = None
    ph: Optional[str] = None
    blood: Optional[str] = None
    specific_gravity: Optional[str] = None
    ascorbate: Optional[str] = None
    ketone: Optional[str] = None
    bilirubin: Optional[str] = None
    glucose: Optional[str] = None
    micro_albumin: Optional[str] = None


class VerifiedUser(BaseModel):
    login: str
    analyzer_code: str
    examination_id: int

class FinishedTest(BaseModel):
    email: str
    #result: ExaminationResult

# ----
@unique
class TestsEventType(NoValue):
    VERIFIED_USER = 'VERIFIED_USER'
    FINISHED_ANALYZE = 'FINISHED_ANALYZE'
    FINISHED_TEST = 'FINISHED_TEST'


class TestsEvent(BaseModel):
    kind: TestsEventType
    data: ExaminationResult | VerifiedUser | FinishedTest


# -----


@unique
class UsersEventType(NoValue):
    DELETED = 'DELETED'
    CHANGED_WALLET_STATE = 'CHANGED_WALLET_STATE'
    NEW_USER = 'NEW_USER'
    UPDATED_INFO = 'UPDATED_INFO'
    NEW_VERIFICATION = 'NEW_VERIFICATION'


class WalletChangeData(BaseModel):
    login: str
    change_amount: float


class UserData(BaseModel):
    email: str
    login: str
    wallet: float = 0.0

class UserVerification(BaseModel):
    email: str
    code: str

class UsersEvent(BaseModel):
    kind: UsersEventType
    data: UserData | WalletChangeData | UserVerification
