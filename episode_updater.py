from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from auth import auth, URL, S


sched = BlockingScheduler()

SPOILER = "Miraculous Ladybug Wiki:Spoiler Doctrine"


def protect(episode):
    PARAMS = {
        "title": episode,
        "protections": "edit=autoconfirmed|move=sysop",
        "expiry": "infinite",
        "token": auth(),
        "action": "protect",
        "format": "json",
        "reason": "BOT: The episode is scheduled to begin airing shortly."
    }
    R = S.post(URL, data=PARAMS)
    print(R.text)


def updSpoiler(episode: str, mode: int):
    # mode:
    # 0 - No longer spoiler
    # 1 - English premiere
    # other - World premiere
    page = S.post(URL, {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "titles": SPOILER,
        "formatversion": "2",
        "rvprop": "content",
        "rvslots": "main"
    })

    page_cont = page.json()["query"]["pages"][0]["revisions"][0]["slots"]["main"]["content"]

    if mode == 0:
        page_cont = page_cont.replace(f"<span style=\"font-weight: bold; color: #ffea00;\" name=\"{episode}\">✘</span>",
                                      f"<span style=\"font-weight: bold; color: #39fc03;\" name=\"{episode}\">✓</span>")
    elif mode == 1:
        page_cont = page_cont.replace(f"<span name=\"{episode}\">✘</span>",
                                      f"<span style=\"font-weight: bold; color: #ffea00;\" name=\"{episode}\">✘</span>")
        page_cont = page_cont.replace(f"<span style=\"font-weight: bold; color: #ff0000;\" name=\"{episode}\">✘</span>",
                                      f"<span style=\"font-weight: bold; color: #ffea00;\" name=\"{episode}\">✘</span>")
    else:
        page_cont = page_cont.replace(f"<span name=\"{episode}\">✘</span>",
                                      f"<span style=\"font-weight: bold; color: #ff0000;\" name=\"{episode}\">✘</span>")

    PARAMS = {
        "action": "edit",
        "title": SPOILER,
        "token": auth(),
        "format": "json",
        "summary": f"BOT: Updated status of episode \"{episode}\"",
        "text": page_cont
    }
    R = S.post(URL, data=PARAMS)
    print(R.text)


sched.add_job(protect, 'date', run_date=datetime(2022, 6, 14, 0, 30, 00), args=['Evolution'])
sched.add_job(updSpoiler, 'date', run_date=datetime(2022, 6, 14, 0, 30, 00), args=['Evolution', 0])

sched.start()
