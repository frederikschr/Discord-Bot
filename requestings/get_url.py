import urllib.request
import re

def get_words(keyword: str):
    word_list = []

    words = keyword.split()

    for word in words:
        word_list.append(word)

    return "+".join(word_list)

def get_url(keyword: str):
    keyword = get_words(keyword)
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + keyword)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    url = ("https://www.youtube.com/watch?v=" + video_ids[0])
    return url



