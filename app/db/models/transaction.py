from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from ..database import Base


class Transaction(Base):
    id = Column(Integer, primary_key=True, index=True)
    reference_number = Column(String, nullable=False, index=True)
    payment_system = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    is_verified = Column(Boolean, nullable=False, default=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    project_id = Column(Integer, ForeignKey("project.id"))

    user = relationship("User", back_populates="transactions")
    project = relationship("Project", back_populates="transactions")