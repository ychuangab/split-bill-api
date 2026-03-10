from typing import Optional
from pydantic import BaseModel, field_validator, model_validator


class Participant(BaseModel):
    name: str
    paid: float

    @field_validator("paid")
    @classmethod
    def paid_non_negative(cls, v: float) -> float:
        if v < 0:
            raise ValueError("paid must be >= 0")
        return v


class SplitRequest(BaseModel):
    currency: Optional[str] = None
    participants: list[Participant]

    @model_validator(mode="after")
    def participants_non_empty(self) -> "SplitRequest":
        if not self.participants:
            raise ValueError("participants must not be empty")
        return self


class Balance(BaseModel):
    name: str
    balance: float


class Settlement(BaseModel):
    from_: str
    to: str
    amount: float

    model_config = {"populate_by_name": True}

    def model_dump(self, **kwargs):
        d = super().model_dump(**kwargs)
        d["from"] = d.pop("from_")
        return d


class SplitResponse(BaseModel):
    total: float
    per_person_share: float
    balances: list[Balance]
    settlements: list[Settlement]
