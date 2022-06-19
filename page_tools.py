from auth import auth, URL, S
import action_fox
import json


def get_page(page: str):
    page_res = S.post(URL, {
            "action": "query",
            "format": "json",
            "prop": "revisions",
            "titles": page,
            "formatversion": "2",
            "rvprop": "content",
            "rvslots": "main"
        })
    action_fox.send(f"Downloaded page for \"{page}\"",
                    f"_{page}_",
                    5814783)

    return page_res.json()["query"]["pages"][0]["revisions"][0]["slots"]["main"]["content"]


def set_page(page: str, content: str, message="def", summary="BOT: updated page"):
    if message == "def":
        message = f"Page {page} has been updated."

    PARAMS = {
        "action": "edit",
        "title": page,
        "token": auth(),
        "format": "json",
        "summary": summary,
        "text": content
    }
    R = S.post(URL, data=PARAMS)
    action_fox.send(message,
                    f"```json\n{json.dumps(json.loads(R.text), indent=2)}\n```",
                    16711680)
