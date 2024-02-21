from flask import Blueprint, request, jsonify
from core.utils.youtube import get_youtube_subtitles
from core.utils.tiktok import get_tiktok_subtitles
from core.utils.chatgpt import get_answer_by_chatgpt
from config.settings import OPENAI_API_KEY
from config.prompts import (video_meaning, video_meaning_system,
                            task_by_video_meaning, task_by_video_meaning_system,
                            task_checking, task_checking_system)
import json

endpoints_bp = Blueprint('endpoints_bp', __name__)


@endpoints_bp.route('/api/v1/subtitles/youtube', methods=['POST'])
def get_youtube_subtitles_by_video():
    # response structure
    response = {
        'subtitles': '',
        'logs': {},
    }

    # getting data from request
    data = request.json
    video_url = data.get('video_url', '')
    languages = data.get('languages', ['ru', 'en', 'de'])
    timing = data.get('timing', (0, 10 ** 100,))

    if not video_url or not languages or not timing:
        return jsonify({'error': 'Неверно переданы параметры'}), 400

    subtitles = get_youtube_subtitles(video_url, languages, timing)

    # forming response
    response['subtitles'] = subtitles

    return jsonify(response)


@endpoints_bp.route('/api/v1/subtitles/tiktok', methods=['POST'])
def get_tiktok_subtitles_by_video():
    # response structure
    response = {
        'subtitles': '',
        'logs': {},
    }

    # getting data from request
    data = request.json
    video_url = data.get('video_url', '')

    if not video_url:
        return jsonify({'error': 'Неверно переданы параметры'}), 400

    subtitles = get_tiktok_subtitles(video_url)

    # forming response
    response['subtitles'] = subtitles

    return jsonify(response)


@endpoints_bp.route('/api/v1/video/meaning', methods=['POST'])
def get_video_meaning_by_subtitles():
    # response structure
    response = {
        'meaning': '',
        'logs': {},
    }

    # getting data from request
    data = request.json
    subtitles = data.get('subtitles', '')

    if not subtitles:
        return jsonify({'error': 'Неверно переданы параметры'}), 400

    meaning = get_answer_by_chatgpt(OPENAI_API_KEY,
                                    video_meaning,
                                    video_meaning_system,
                                    '',
                                    __subtitles__=subtitles)

    # forming response
    response['meaning'] = meaning

    return jsonify(response)


@endpoints_bp.route('/api/v1/task/generate', methods=['POST'])
def get_task_by_video_meaning():
    # response structure
    response = {
        'task': '',
        'logs': {},
    }

    # getting data from request
    data = request.json
    meaning = data.get('meaning', '')

    if not meaning:
        return jsonify({'error': 'Неверно переданы параметры'}), 400

    task = get_answer_by_chatgpt(OPENAI_API_KEY,
                                 task_by_video_meaning,
                                 task_by_video_meaning_system,
                                 '',
                                 __video_meaning__=meaning)

    # forming response
    response['task'] = task

    return jsonify(response)


@endpoints_bp.route('/api/v1/task/check', methods=['POST'])
def get_checking_task():
    # response structure
    response = {
        'task_check': '',
        'logs': {},
    }

    # getting data from request
    data = request.json
    task = data.get('task', '')
    children_answer = data.get('children_answer', '')

    if not task or not children_answer:
        return jsonify({'error': 'Неверно переданы параметры'}), 400

    task_check = get_answer_by_chatgpt(OPENAI_API_KEY,
                                       task_checking,
                                       task_checking_system,
                                       '',
                                       __task__=task,
                                       __children_answer__=children_answer)

    # forming response
    response['task_check'] = task_check

    return jsonify(response)
