
from telegraph import Telegraph

tele_ = Telegraph()

def telegrapher(a_title: str, content: str) -> str:
    auth_name = tele_.create_account(short_name="Kakashi")
    resp = tele_.create_page(
        title=a_title,
        author_name=auth_name,
        author_url="https://t.me/xplugin",
        html_content=content,
    )
    link_ = resp["url"]
    return link_