from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, DateTime, ForeignKey, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
jogador_pacote = Table(
    "jogador_pacote",
    Base.metadata,
    Column("jogador_id", ForeignKey("jogadores.id"), primary_key=True),
    Column("pacote_id", ForeignKey("pacotes_itens.id"), primary_key=True),
    Column("data_aquisicao", DateTime, default=datetime.now),
)
jogador_jogo = Table(
    "jogador_jogo",
    Base.metadata,
    Column("jogador_id", ForeignKey("jogadores.id"), primary_key=True),
    Column("jogo_id", ForeignKey("jogos.id"), primary_key=True),
    Column("adicionado_em", DateTime, default=datetime.now),
)
class Categoria(Base):
    __tablename__ = "categorias"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), unique=True)
    descricao: Mapped[Optional[str]] = mapped_column(Text)
    jogos: Mapped[List["Jogo"]] = relationship(back_populates="categoria")
class Jogo(Base):
    __tablename__ = "jogos"
    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(150))
    descricao: Mapped[Optional[str]] = mapped_column(Text)
    preco: Mapped[float] = mapped_column(default=0.0)
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"))
    categoria: Mapped["Categoria"] = relationship(back_populates="jogos")
    pacotes_itens: Mapped[List["PacoteItem"]] = relationship(back_populates="jogo")
    jogadores_favoritos: Mapped[List["Jogador"]] = relationship(
        secondary=jogador_jogo, back_populates="jogos_favoritos"
    )
class PacoteItem(Base):
    __tablename__ = "pacotes_itens"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(150))
    descricao: Mapped[Optional[str]] = mapped_column(Text)
    preco: Mapped[float] = mapped_column(default=0.0)
    jogo_id: Mapped[int] = mapped_column(ForeignKey("jogos.id"))
    jogo: Mapped["Jogo"] = relationship(back_populates="pacotes_itens")
    jogadores: Mapped[List["Jogador"]] = relationship(
        secondary=jogador_pacote, back_populates="pacotes_adquiridos"
    )
class Jogador(Base):
    __tablename__ = "jogadores"
    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(80), unique=True)
    email: Mapped[str] = mapped_column(String(120), unique=True)
    senha_hash: Mapped[str] = mapped_column(String(255))
    data_cadastro: Mapped[datetime] = mapped_column(default=datetime.now)
    pacotes_adquiridos: Mapped[List["PacoteItem"]] = relationship(
        secondary=jogador_pacote, back_populates="jogadores"
    )
    jogos_favoritos: Mapped[List["Jogo"]] = relationship(
        secondary=jogador_jogo, back_populates="jogadores_favoritos"
    )