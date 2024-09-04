from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    address = Column(String, primary_key=True)
    stakes = relationship("Stake", back_populates="user")
    rewards = relationship("Reward", back_populates="user")
    claims = relationship("Claim", back_populates="user")


class Stake(Base):
    __tablename__ = 'stakes'

    id = Column(Integer, primary_key=True)
    user_address = Column(String, ForeignKey('users.address'))
    validator_address = Column(String)
    amount = Column(BigInteger)
    date = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="stakes")

class Reward(Base):
    __tablename__ = 'rewards'

    id = Column(Integer, primary_key=True)
    user_address = Column(String, ForeignKey('users.address'))
    amount = Column(BigInteger)
    claimed_at = Column(DateTime, default=datetime.utcnow)
    claimed = Column(Boolean, default=False)

    user = relationship("User", back_populates="rewards")


class Claim(Base):
    __tablename__ = 'claims'

    id = Column(Integer, primary_key=True)
    user_address = Column(String, ForeignKey('users.address'))
    amount = Column(BigInteger)
    date = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="claims")

class DailySummary(Base):
    __tablename__ = 'daily_summaries'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, unique=True)
    total_staked = Column(BigInteger)
    average_staked = Column(BigInteger)
    largest_stake = Column(BigInteger)
    total_users = Column(Integer)
    eligible_users = Column(Integer)
    total_rewards = Column(BigInteger)
