from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    id_card = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    name = Column(String, nullable=False, index=True)
    password = Column(String, nullable=False)
    avatar = Column(String, nullable=True)
    is_superuser = Column(Boolean(), default=False)
    is_active = Column(Boolean(), default=True)

    projects = relationship("Project", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")