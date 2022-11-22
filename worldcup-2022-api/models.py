from sqlalchemy import Column, Integer, String, Date

from database import Base


class FixtureResults(Base):
    __tablename__ = "fixture_results"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, primary_key=True, index=True)
    home_team = Column(String, nullable=False, primary_key=True, index=True)
    away_team = Column(String, nullable=False, primary_key=True, index=True)
    home_team_score = Column(Integer, nullable=True)
    away_team_score = Column(Integer, nullable=True)
    status = Column(String, nullable=False)
    yellow_cards = Column(Integer, nullable=True)
    red_cards = Column(Integer, nullable=True)
    stage = Column(String, nullable=False)


class Standings(Base):
    __tablename__ = "standings"

    id = Column(Integer, primary_key=True, index=True)
    group = Column(String, nullable=False)
    team = Column(String, nullable=False, unique=True, index=True)
    played = Column(Integer, nullable=False, default=0)
    won = Column(Integer, nullable=False, default=0)
    drawn = Column(Integer, nullable=False, default=0)
    lost = Column(Integer, nullable=False, default=0)
    goals_for = Column(Integer, nullable=False, default=0)
    goals_against = Column(Integer, nullable=False, default=0)
    goal_difference = Column(Integer, nullable=False, default=0)
    points = Column(Integer, nullable=False, default=0)


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    team = Column(String, nullable=False)
    goals = Column(Integer, nullable=False, default=0)