from pydantic import BaseModel, Field

class Result(BaseModel):
    court_name: str | None = Field(default=None)
    date: str | None = Field(default=None)
    department_name: str | None = Field(default=None)
    recorder: str | None = Field(default=None)
    signature: str | None = Field(default=None)
    judges: list[str] | None = Field(default=None)
    legal_bases: list[str] | None = Field(default=None)

class InputJudgement(BaseModel):
    judgment: str = Field(min_length=1000, max_length=14000)

class InputAsk(BaseModel):
    text: str = Field(min_length=5, max_length=500)