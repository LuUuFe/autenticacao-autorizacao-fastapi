from getpass import getpass

from passlib.hash import pbkdf2_sha256
from sqlalchemy import select

from app.database import SessionLocal
from app.models import Usuario


def main():
    email = input("E-mail: ").strip().lower()
    if not email or "@" not in email or len(email) > 254:
        raise SystemExit("Informe um e-mail válido.")

    with SessionLocal() as db:
        if db.scalar(select(Usuario).where(Usuario.email == email)):
            raise SystemExit("Este e-mail já está cadastrado.")

        senha = getpass("Senha: ")
        if not 8 <= len(senha) <= 1024:
            raise SystemExit("A senha deve ter entre 8 e 1024 caracteres.")

        senha_hash = pbkdf2_sha256.using(rounds=600_000).hash(senha)
        db.add(Usuario(email=email, senha_hash=senha_hash))
        db.commit()

    print("Usuário criado.")


if __name__ == "__main__":
    main()
