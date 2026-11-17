"""SQLAlchemy-modeller."""

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Skjemaversjon(Base):
    """Én rad med skjemaversjonen databasefila ble laget med (AD-13)."""

    __tablename__ = "skjemaversjon"

    versjon: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
