from pydantic import BaseModel


class ExchangeCodeToTokensOutput(BaseModel):
    access_token: str
    id_token: str
    scope: str
    expires_in: int
    token_type: str
