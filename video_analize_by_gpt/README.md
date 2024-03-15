# Python-video_analize_by_gpt
Scripts for:
* getting subtitles from YouTube;
* analysis of the meaning of a video by subtitles via ChatGPT;
* analysis of the meaning of a video via Gemini Pro;
* generating tasks for children and then checking their answers via ChatGPT.

Created by 02.2024

## API Description:

The `logs` field in all requests has been added for future logging by execution stages. If you don't need it, just remove it.

# POST http://127.0.0.1:8080/api/v1/subtitles/youtube
* **Input value**:
* * `video_url` (required) - link to YouTube video [string]
* * `languages` (optional) - an array of languages in which to search for subtitles [array [string]] (default Russian, English, German).
* * * Input values like this: `languages: ['ru']` or `languages: ['en', 'fr']`, language codes as a string
* * `timing` (optional) - time interval in a video for which subtitles are needed [array [float]] (by default the entire video duration).
* * * Input values like this: [22.5, 775.6] (input the beginning and end of the time interval in seconds (floating point number))
* **Output value**:
* `subtitles` - subtitles [string]
* `logs` - logs [object]
* 
# POST http://127.0.0.1:8080/api/v1/subtitles/tiktok
* **Input value**:
* * `video_url` (required) - link to Tik-Tok video [string]
* **Output value**:
* `subtitles` - subtitles [string]
* `logs` - logs [object]

# POST http://127.0.0.1:8080/api/v1/video/meaning
* **Input value**:
* * `subtitles` (required) - subtitles [string]
* **Output value**:
* `meaning` - description of the meaning of the video from GPT [string]
* `logs` - logs [object]

# POST http://127.0.0.1:8080/api/v1/task/generate
* **Input value**:
* * `meaning` (required) - description of the meaning of the video [string]
* **Output value**:
* `task` - one task from GPT on video description [string]
* `logs` - logs [object]

# POST http://127.0.0.1:8080/api/v1/task/check
* **Input value**:
* * `task` (required) - one task [string]
* **Output value**:
* `task_check` - the result of checking from GPT the correspondence of the task and the child’s answer [string]
* `logs` - logs [object]
