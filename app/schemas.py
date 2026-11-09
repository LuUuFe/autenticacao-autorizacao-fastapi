from pydantic import BaseModel, ConfigDict, Field


class TarefaDados(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    titulo: str = Field(min_length=1, max_length=120)
    descricao: str | None = Field(default=None, max_length=2000)
    concluida: bool = False


class TarefaResposta(TarefaDados):
    model_config = ConfigDict(from_attributes=True)

    id: int


class Token(BaseModel):
    access_token: str
    token_type: str
