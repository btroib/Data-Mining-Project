from googleapiclient.discovery import build
import conf as CFG


def get_youtube_trailer(titles):
    """This function uses an Youtube API to parse the game trailers based on game titles scraped by the Web scraper"""
    youtube_trailer_list = []
    api_key = CFG.API_KEY
    youtube = build(CFG.SERVICE_NAME, CFG.VERSION, developerKey=api_key)
    for title in titles:
        request = youtube.search().list(key=api_key, part='snippet', q=f'{title} Trailer')
        response = request.execute()
        video_id = response['items'][0]['id']['videoId']
        trailer_url = 'https://www.youtube.com/watch?v=' + video_id
        youtube_trailer_list.append(trailer_url)
    return youtube_trailer_list
