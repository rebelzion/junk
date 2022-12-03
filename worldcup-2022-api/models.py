from __future__ import annotations
from sqlalchemy import Column, Integer, String, Date

from database import Base
from sqlalchemy.orm import Session


def delete_rows(db: Session, model: Base):
    db.query(model).delete()
    db.commit()


class FixtureResults(Base):
    __tablename__ = "fixture_results"

    date = Column(Date, nullable=False, primary_key=True)
    home_team = Column(String, nullable=False, primary_key=True)
    away_team = Column(String, nullable=False, primary_key=True)
    home_team_score = Column(Integer, nullable=True)
    away_team_score = Column(Integer, nullable=True)
    status = Column(String, nullable=False)
    yellow_cards = Column(Integer, nullable=True)
    red_cards = Column(Integer, nullable=True)
    stage = Column(String, nullable=False)

    @classmethod
    def add_fixture(cls, db: Session, fixture: FixtureResults):
        db.add(fixture)
        db.commit()

    @classmethod
    def update_fixture(cls, db: Session, fixture: FixtureResults):
        db.query(cls).filter_by(
            date=fixture.date,
            home_team=fixture.home_team,
            away_team=fixture.away_team,
        ).update(fixture)
        db.commit()


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

    @classmethod
    def add_standings(cls, db: Session, standings: Standings):
        db.add(standings)
        db.commit()

    @classmethod
    def update_standings(cls, db: Session, standings: Standings):
        db.query(Standings).filter(Standings.team ==
                                   standings.team).update(standings)
        db.commit()


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    team = Column(String, nullable=False)
    goals = Column(Integer, nullable=False, default=0)

    @classmethod
    def add_player(cls, db: Session, player: Player):
        db.add(player)
        db.commit()

    @classmethod
    def update_player_goals(cls, db: Session, player_name: str, new_goals: int):
        db.query(Player).filter(Player.name == player_name).update(
            {Player.goals: new_goals})
        db.commit()
