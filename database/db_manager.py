from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from .models import Base, User, Stake, Reward, Claim, DailySummary
from typing import List, Dict
from datetime import datetime, UTC

class DatabaseManager:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)


    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)


    def get_session(self):
        return self.SessionLocal()


    def store_stakes(self, stakes: Dict[str, Dict[str, int]], date: datetime):
        session = self.get_session()
        try:
            for user_address, validators in stakes.items():
                user = session.query(User).filter_by(address=user_address).first()
                if not user:
                    user = User(address=user_address)
                    session.add(user)

                    for validator_address, amount in validators.items():
                        stake = Stake(user=user, validator_address=validator_address, amount=amount, date=date)
                        session.add(stake)

            session.commit()
        finally:
            session.close()


    def store_rewards(self, rewards: Dict[str, int], date: datetime):
        session = self.get_session()
        try:
            for user_address, amount in rewards.items():
                user = session.query(User).filter_by(address=user_address).first()
                if not user:
                    user = User(address=user_address)
                    session.add(user)

                reward = Reward(user=user, amount=amount, date=date)
                session.add(reward)

            session.commit()
        finally:
            session.close()

    def store_daily_summary(self, summary: Dict[str, int], date: datetime):
        session = self.get_session()
        try:
            daily_summary = DailySummary(
                date=date,
                total_staked=summary['total_staked_balance'],
                average_staked=summary['average_staked'],
                largest_stake=summary['largest_staked_balance'],
                total_users=summary['total_users_with_balance'],
                eligible_users=summary['total_eligible_users'],
                total_rewards=summary['total_rewards']
            )
            session.add(daily_summary)
            session.commit()
        finally:
            session.close()


    def get_user_stakes(self, address: str, date: datetime = None) -> List[Stake]:
        session = self.get_session()
        try:
            query = session.query(Stake).filter(Stake.user_address == address)
            if date:
                query = query.filter(Stake.date == date)
            return query.all()
        finally:
            session.close()


    def get_user_rewards(self, address: str, date: datetime = None) -> List[Reward]:
        session = self.get_session()
        try:
            query = session.query(Reward).filter(Reward.user_address == address)
            if date:
                query = query.filter(Reward.date == date)
            return query.all()
        finally:
            session.close()

    def claim_rewards(self, address: str) -> int:
        session = self.get_session()
        try:
            rewards = session.query(Reward).filter(Reward.user_address == address, Reward.claimed == False).all()
            total_claimed = sum(reward.amount for reward in rewards)

            for reward in rewards:
                reward.claimed = True

            claim = Claim(user_address=address, amount=total_claimed)
            session.add(claim)

            session.commit()
            return total_claimed
        finally:
            session.close()


    def get_daily_summary(self, date: datetime) -> DailySummary:
        session = self.get_session()
        try:
            return session.query(DailySummary).filter(DailySummary.date == date).first()
        finally:
            session.close()


    def get_average_summary(self) -> Dict[str, float]:
        session = self.get_session()

        try:
            result = session.query(
                func.avg(DailySummary.average_staked).label('average_staked'),
                func.avg(DailySummary.eligible_users).label('average_eligible_users'),
                func.max(DailySummary.largest_stake).label('max_stake')
            ).first()

            return {
                'average_staked': float(result.average_staked) if result.average_staked else 0.0,
                'average_eligible_users': float(result.average_eligible_users) if result.average_eligible_users else 0.0,
                'max_stake': float(result.max_stake) if result.max_stake else 0.0
            }
        finally:
            session.close()