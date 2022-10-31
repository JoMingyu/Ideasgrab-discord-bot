import os
from typing import List

import requests
from bs4 import BeautifulSoup
from discord import SyncWebhook
from sqlalchemy.orm import Session

from src.database import SessionLocal
from src.models.idea import IdeaModel


def parse_response(response) -> List[str]:
    result = list()
    soup = BeautifulSoup(response.text, "html.parser")
    elements = soup.find("ol").find_all("li")

    for element in elements:
        result.append(element.text)

    return result


def get_ideas() -> List[str]:
    response = requests.get(url="https://www.ideasgrab.com/")

    result = parse_response(response)

    return result


def get_latest_idea(db: Session):
    idea = db.query(IdeaModel).order_by(IdeaModel.id.desc()).first()
    return idea.text


def set_latest_idea(db: Session, idea: str):
    idea = IdeaModel(text=idea)
    db.add(idea)
    db.commit()


def send_webhook(message: str):
    webhook = SyncWebhook.from_url(os.getenv("DISCORD_WEBHOOK_URL"))
    webhook.send(content=message)


def main(event=None, lambda_context=None):
    db = SessionLocal()

    ideas = get_ideas()
    latest_idea_now = ideas[0]
    latest_idea = get_latest_idea(db=db)

    while latest_idea != ideas[0]:
        send_webhook(ideas[0])
        ideas = ideas[1:]

    if latest_idea != latest_idea_now:
        set_latest_idea(db=db, idea=latest_idea_now)


if __name__ == "__main__":
    main()
