import youtube_transcript_api


def get_youtube_subtitles(video_url: str,
                          languages: list[str] = ['ru', 'en', 'de'],
                          timing: tuple[float, float] = (0, 10 ** 100,)) -> str:
    """Getting subtitles from YouTube video"""
    subtitles = []

    link = video_url[video_url.index('=') + 1:]
    try:
        # Variant 1 - get all languages then translate to russian
        # subtitles_all = youtube_transcript_api.YouTubeTranscriptApi.list_transcripts(link)
        # subtitles = subtitles_all.find_transcript(languages).translate('ru').fetch()

        # Variant 2 - trying get only ru, en, de languages
        subtitles = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(link, languages)
    except youtube_transcript_api._errors.TranscriptsDisabled:
        print("Subtitles are disabled for this video")
    except youtube_transcript_api._errors.CouldNotRetrieveTranscript:
        print(f"No transcripts were found for language codes: {languages}")
    except Exception as e:
        print("Unknown error when getting YouTube subtitles", str(e))

    subtitles_filtered = [text['text'] for text in subtitles
                          if timing[0] <= text['start'] <= timing[1]
                          and not text['text'].startswith('[') and not text['text'].endswith(']')]

    return ' '.join(subtitles_filtered)
