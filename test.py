from requests import get, post
from lxml import html
from time import sleep
from concurrent.futures import ThreadPoolExecutor

collection = list()
webhook_url = "https://discord.com/api/webhooks/966881365209518081/JXb30LtxXdbmVe6s3t18UOkNaEt07ecci4pf3iLxtujeSm4bAa6e74FDw24l3iqxa4_I"
source = html.fromstring(get("https://kingofhup.com/หมวดหมู่/คลิปไทย").content)
max = int(source.xpath("//a[@class='page-link']/text()")[-2])


def fetch(page: int):
    doc = html.fromstring(
        get(f"https://kingofhup.com/หมวดหมู่/คลิปไทย?page={page}").content
    )
    print(f"[Success] :: fetched video from page {page}")
    image = doc.xpath("//div[@class='card p-1']/v-lazy-image/@src")
    title = doc.xpath("//div[@class='card p-1']/v-lazy-image/@title")
    url = [
        "https://kingofhup.com" + path
        for path in doc.xpath("//div[@class='position-relative']/a/@href")
    ]
    print(f"[Success] :: fetched {len(url)} videos from page {page}")
    for title, image, url in zip(title, image, url):
        path = html.fromstring(get(url, timeout=25).content)
        video = path.xpath("//div[@class='col-12']/iframe/@src")
        if video != []:
            video = str(video[0])
            print(f"[Success] :: fetched video {video} from page {page}")
            collection.append([video, title, image])


with ThreadPoolExecutor(max_workers=max) as executor:
    for number in range(max):
        executor.submit(fetch, number + 1)
executor.shutdown(wait=True)
for item in collection:
    status = post(
        webhook_url,
        json={
            "content": None,
            "username": "kingofhup.com",
            "avatar_url": "https://kingofhup.com/static/favicon.png",
            "embeds": [
                {
                    "author": {
                        "name": item[1],
                        "url": "https://kingofhup.com",
                        "icon_url": "https://kingofhup.com/static/favicon.png",
                    },
                    "description": "[ [ดูคลิปเต็ม](" + item[0] + ") ]",
                    "color": "16699392",
                    "image": {"url": item[2]},
                    "footer": {
                        "text": "ทำโดย luxz#8403",
       
                    },
                }
            ],
        },
    ).status_code
    print(f"[{status}] :: " + item[0])
    sleep(300)
