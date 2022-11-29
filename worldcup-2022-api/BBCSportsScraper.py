from ipaddress import collapse_addresses
from bs4 import BeautifulSoup
import requests
import datetime
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
from typing import List, Optional
from enum import Enum
import tqdm


class LEAGUE(Enum):
    SPANISH_LA_LIGA = "spanish-la-liga"
    ENGLISH_PREMIER_LEAGUE = "premier-league"
    ENGLISH_CHAMPIONSHIP = "championship"
    ITALIAN_SERIE_A = "italian-serie-a"
    FRENCH_LIGUE_ONE = "french-ligue-one"
    GERMAN_BUNDESLIGA = "german-bundesliga"
    ARGENTINA_PRIMERA = "argentine-primera-division"
    BRAZIL_LIGA = "brazilian-league"
    PORTUGUES_LIGA = "portuguese-primeira-liga"
    CHAMPIONS_LEAGUE = "champions-league"
    EUROPA_LEAGUE = "europa-league"
    EUROPA_CONFERENCE_LEAGUE = "europa-conference-league"
    WORLD_CUP = "world-cup"

    def get_list():
        return list(map(lambda c: c.value, LEAGUE))


class BBCSoccerScraper:
    def __init__(self, use_prod: bool = False):
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--incognito")
        if use_prod:
            options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)

    def _get_url(self, date: str, league: str):
        """
        date: YYYY-MM
        league: eg. argentine-primera-division
        """
        return f"https://www.bbc.com/sport/football/{league}/scores-fixtures/{date}"

    def scrape_leagues(self, date: str, leagues: Optional[List[str]] = None):
        results = {}
        if not leagues:
            leagues = LEAGUE.get_list()
        for league in tqdm.tqdm(leagues, position=0, leave=True):
            results[league] = self.scrape(date, league)
        return results

    def _get_soup(self, date, league):
        sleeping_time = random.randint(1, 5)
        print(f"Sleeping for {sleeping_time} seconds to avoid being blocked.")
        time.sleep(sleeping_time)

        if league == "world-cup":
            url = self._get_url(
                date=f"{date.year}-{date.month:02d}-{date.day:02d}", league=league
            )
        else:
            url = self._get_url(date=f"{date.year}-{date.month:02d}", league=league)
        print(f"url: {url}")

        self.driver.get(url)

        # click on Show scorers button
        time.sleep(random.randint(1, 3))
        elem = self.driver.find_element(By.XPATH, "//*[text()='Show scorers']")
        elem.click()
        # wait until page is loaded
        time.sleep(random.randint(1, 3))

        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        return soup

    def scrape(self, date: datetime.datetime, league: str):

        soup = self._get_soup(date, league)
        results = self._get_matches_date_half_and_fulltime_score(soup)

        return results

    def _parse_score_events(self, score_events):

        events_and_player = re.findall(r"((\w+) \([^\)]+\))", score_events)
        events_by_player = {}
        for events, player in events_and_player:
            events = re.findall(r"\((.*)\)", events)
            if player not in events_by_player:
                events_by_player[player] = {
                    "red_cards": 0,
                    "h1_goals": 0,
                    "h2_goals": 0,
                    "penalties_scored": 0,
                }
            if events:
                events = events[0].split(", ")
                for ev in events:
                    if "dismissed" not in ev.lower():
                        score_ev = re.findall(r"(\d+)'(\+\d+)*\sminutes(\spen)*", ev)[0]
                        min = int(score_ev[0])
                        is_pen = score_ev[2] != ""

                        if min <= 45:
                            events_by_player[player]["h1_goals"] += 1
                        else:
                            events_by_player[player]["h2_goals"] += 1
                        if is_pen:
                            events_by_player[player]["penalties_scored"] += 1
                    else:
                        events_by_player[player]["red_cards"] += 1

        # for player, events in events_by_player.items():
        #     print(player, events)
        return events_by_player

    def _parse_score(self, score):
        score = score.split(", ")

        total_ev = ""
        for ev in score:
            if ev.count(")") > ev.count("("):
                total_ev += f", {ev}"
            else:
                total_ev += ev

        events_by_player = self._parse_score_events(total_ev)

        stats = {
            "total_goals": 0,
            "h1_goals": 0,
            "h2_goals": 0,
            "penalties_scored": 0,
            "red_cards": 0,
            "event_by_player": events_by_player,
        }

        stats["h1_goals"] = sum([ev["h1_goals"] for pl, ev in events_by_player.items()])
        stats["h2_goals"] = sum([ev["h2_goals"] for pl, ev in events_by_player.items()])
        stats["total_goals"] = stats["h1_goals"] + stats["h2_goals"]
        stats["penalties_scored"] = sum(
            [ev["penalties_scored"] for pl, ev in events_by_player.items()]
        )
        stats["red_cards"] = sum(
            [ev["red_cards"] for pl, ev in events_by_player.items()]
        )

        return stats

    def _get_matches_date_half_and_fulltime_score(
        self, soup, date: Optional[datetime.datetime] = None
    ):
        els = soup.find_all(
            ["ul", "span", "h3"],
            {
                "class": [
                    "gs-u-display-none gs-u-display-block@m qa-full-team-name sp-c-fixture__team-name-trunc",
                    "sp-c-fixture__status-wrapper qa-sp-fixture-status",
                    "sp-c-fixture__status sp-c-fixture__status--live-sport",
                    'sp-c-fixture__player-action sp-c-fixture__scorers sp-c-fixture__scorers-home gel-brevier gel-1/2"',
                    'sp-c-fixture__player-action sp-c-fixture__scorers sp-c-fixture__scorers-away gel-brevier gel-1/2"',
                    "gel-minion sp-c-match-list-heading",
                    "gel-minion gs-u-align-center gs-u-mt",
                ]
            },
        )

        home_team, away_team, home_score, away_score, status = (
            None,
            None,
            None,
            None,
            None,
        )
        prev_attrs = None
        results = []
        status = None

        # for ele in els:
        #     print(f"[{ele.text}]")
        # return []

        for el in els:
            attrs = el.attrs["class"]
            text = el.text
            text = text.strip().rstrip().lower()

            if "sp-c-match-list-heading" in attrs:
                if not date:
                    current_year = datetime.datetime.now().year
                    _, day_num, month = map(lambda x: x.lower(), text.split())
                    day_num = int(re.sub(r"\D", "", day_num))
                    date = datetime.datetime.strptime(
                        f"{current_year} {day_num} {month}", "%Y %d %B"
                    )

            if "qa-full-team-name" in attrs:
                if home_team:
                    away_team = text
                else:
                    home_team = text
            elif "qa-sp-fixture-status" in attrs:
                status = text
                if text != "ft" and "mins" not in text:
                    # we are done with this match, it was not played (postponed, cancelled, etc.)
                    home_score = 0 if home_score in [None, ""] else home_score
                    away_score = 0 if away_score in [None, ""] else away_score
                    results.append(
                        ((home_team, home_score, away_score, away_team), date, text)
                    )
                    home_team, away_team, home_score, away_score, status = (
                        None,
                        None,
                        None,
                        None,
                        None,
                    )
                elif not "sp-c-fixture__scorers-home" in prev_attrs:
                    # we are done with this match, it's 0-0
                    home_score = 0 if home_score in [None, ""] else home_score
                    away_score = 0 if away_score in [None, ""] else away_score
                    results.append(
                        ((home_team, home_score, away_score, away_team), date, status)
                    )
                    home_team, away_team, home_score, away_score, status = (
                        None,
                        None,
                        None,
                        None,
                        None,
                    )
            elif "sp-c-fixture__scorers-home" in attrs:
                home_score = text
            elif "sp-c-fixture__scorers-away" in attrs:
                away_score = text
                home_score = 0 if home_score in [None, ""] else home_score
                away_score = 0 if away_score in [None, ""] else away_score
                results.append(
                    ((home_team, home_score, away_score, away_team), date, status)
                )
                home_team, away_team, home_score, away_score, status = (
                    None,
                    None,
                    None,
                    None,
                    None,
                )
            prev_attrs = attrs

        # parse scores
        final_results = []
        for (home_team, home_score, away_score, away_team), date, status in results:
            home_stats = {}
            away_stats = {}
            if status == "ft" or "mins" in status:
                if isinstance(away_score, str):
                    away_stats = self._parse_score(away_score)
                    away_score = (
                        away_stats["total_goals"],
                        away_stats["h1_goals"],
                        away_stats["h2_goals"],
                    )
                else:
                    away_score = [0, 0, 0]
                if isinstance(home_score, str):
                    home_stats = self._parse_score(home_score)
                    home_score = (
                        home_stats["total_goals"],
                        home_stats["h1_goals"],
                        home_stats["h2_goals"],
                    )
                else:
                    home_score = [0, 0, 0]
            final_results.append(
                (
                    (home_team, home_score, away_score, away_team),
                    date,
                    status,
                    home_stats,
                    away_stats,
                )
            )
        return final_results
