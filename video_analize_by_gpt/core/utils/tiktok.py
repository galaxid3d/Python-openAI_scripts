# import os


def get_tiktok_subtitles(video_url: str) -> str:
    """Getting subtitles from TikTok video"""
    subtitles = []

    link = video_url[video_url.index('=') + 1:]
    try:
        pass
        # subtitles = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(link, languages)
    except Exception as e:
        print("Unknown error when getting Tik-Tok subtitles", str(e))

    subtitles_filtered = [text['text'] for text in subtitles]

    return ' '.join(subtitles_filtered)
