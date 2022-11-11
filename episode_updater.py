
from datetime import datetime
from enum import Enum
from auth import auth, URL, S
from page_tools import get_page, set_page
import json
import action_fox as action_fox
from apscheduler.schedulers.blocking import BlockingScheduler


SPOILER = "Miraculous Ladybug Wiki:Spoiler Doctrine"

class Mode(Enum):
    FULL = 0
    ENG = 1
    WW = 2



def protect(episode: str):
    PARAMS = {
        "title": episode,
        "protections": "edit=autoconfirmed|move=sysop",
        "expiry": "infinite",
        "token": auth(),
        "action": "protect",
        "format": "json",
        "reason": "The episode is scheduled to begin airing shortly."
    }
    R = S.post(URL, data=PARAMS)
    action_fox.send(f"Protection update attempted for \"{episode}\"",
                    f"```json\n{json.dumps(json.loads(R.text), indent=2)}\n```",
                    16711680)


def updSpoiler(episode: str, m: Mode):
    page_cont = get_page(SPOILER)

    if m == Mode.FULL:
        page_cont = page_cont.replace(f"<span style=\"font-weight: bold; color: #ffea00;\" name=\"{episode}\">✘</span>",
                                      f"<span style=\"font-weight: bold; color: #39fc03;\" name=\"{episode}\">✓</span>")
        to = "FULL"
    elif m == Mode.ENG:
        page_cont = page_cont.replace(f"<span name=\"{episode}\">✘</span>",
                                      f"<span style=\"font-weight: bold; color: #ffea00;\" name=\"{episode}\">✘</span>")
        page_cont = page_cont.replace(f"<span style=\"font-weight: bold; color: #ff0000;\" name=\"{episode}\">✘</span>",
                                      f"<span style=\"font-weight: bold; color: #ffea00;\" name=\"{episode}\">✘</span>")
        to = "ENG"
    else:
        page_cont = page_cont.replace(f"<span name=\"{episode}\">✘</span>",
                                      f"<span style=\"font-weight: bold; color: #ff0000;\" name=\"{episode}\">✘</span>")
        to = "WW"

    set_page(SPOILER, page_cont, f"Spoiler doctrine update attempted for \"{episode}\" mode:{to}",
             f"BOT: Updated status of episode \"{episode}\"")


def updTmp(episode: str, m: Mode):
    page_cont = get_page(episode)

    page_cont = page_cont.replace("{{WW Spoiler}}", "{{Spoiler}}")
    if m == Mode.ENG:
        page_cont = page_cont.replace("{{Spoiler}}", "{{Spoiler|recent=yes}}")
    elif m == Mode.FULL:
        page_cont = page_cont.replace("{{Spoiler}}", "")
        page_cont = page_cont.replace("{{Spoiler|recent=yes}}", "")

    set_page(episode, page_cont, f"Spoiler template update attempted on page {episode}", "BOT: Updated spoiler template")


def episode_update(long: str, short: str, m: Mode):
    if m == Mode.WW:
        protect(long)
    updTmp(long, m)
    updSpoiler(short, m)


sched = BlockingScheduler()


sched.add_job(episode_update, 'date', run_date=datetime(2022, 11, 12, 14, 0, 0), args=['Determination',
                                                                                       'Determination',
                                                                                       Mode.ENG])
sched.add_job(episode_update, 'date', run_date=datetime(2022, 11, 12, 14, 0, 10), args=['Jubilation',
                                                                                       'Jubilation',
                                                                                       Mode.FULL])

sched.add_job(episode_update, 'date', run_date=datetime(2022, 11, 19, 14, 0, 0), args=['Passion',
                                                                                       'Passion',
                                                                                       Mode.ENG])
sched.add_job(episode_update, 'date', run_date=datetime(2022, 11, 19, 14, 0, 10), args=['Illusion',
                                                                                       'Illusion',
                                                                                       Mode.FULL])
sched.start()
