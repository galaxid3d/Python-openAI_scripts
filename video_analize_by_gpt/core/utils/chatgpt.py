from openai import OpenAI, APITimeoutError
import httpx
from config.settings import OPENAI_API_KEY, PROXY

RESPONSE_STRIP_CHARS = '«»„““”"❝❞„⹂〝〞〟＂‹›❮❯‚‘‘‛’❛❜❟`\'., '
CHAT_GPT_MODELS = {
    'GPT-3.5': 'gpt-3.5-turbo-0125',
    'GPT-4.0': 'gpt-4-turbo-preview',
}


class ChatGPT:
    """GPT chat assistant"""

    def __init__(
            self,
            api_key: str = '',  # OpenAI Api-key
            proxy: str = '',  # Proxy
            chars_strip: str = '',  # Chars to be removed from the edges of GPT responses
            system_prompt: str = '',  # Role
            system_prompt_adv: str = '',  # Additional options (example, JSON-format)
            model: str = '',  # model
            timeout: float = 60,  # timeout
            max_retries: int = 0,  # default is 2
            temperature: float = 1.0,  # default is 1.0
            top_p: float = 1.0,  # default is 1.0
            is_json: bool = False,
            is_stream: bool = False,
    ) -> None:
        self._chars_strip = chars_strip
        self._client = OpenAI(
            api_key=api_key,
            http_client=httpx.Client(proxies={"http://": proxy, "https://": proxy} if proxy else None),
            max_retries=max_retries,
            timeout=timeout
        )
        self._messages = [
            {
                'role': "system",
                'content': system_prompt + '\n' + system_prompt_adv
            },
        ]
        self._model = model
        self._temperature = temperature
        self._top_p = top_p
        self._response_format = {'type': "json_object"} if (
                is_json and model in model in ['gpt-4-turbo-preview', 'gpt-3.5-turbo-1106', 'gpt-3.5-turbo-0125']
        ) else {'type': "text"}
        self._is_stream = is_stream

    def get_answer(self, message: str, **replace_texts) -> str:
        """Get text response from GPT by prompt"""

        # Replacing all special keywords to text in message
        for replace_keyword, replace_text in replace_texts.items():
            message = message.replace(replace_keyword, replace_text)

        # Add user message
        self._messages.append({"role": "user", "content": message})

        # Get response from GPT
        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=self._messages,
                stream=self._is_stream,
                temperature=self._temperature,
                top_p=self._top_p,
                response_format=self._response_format,
            )
        except APITimeoutError:
            yield f"[Error!!! GPT didn't give response with {self._client.timeout:.2f} seconds!]"
            return
        except Exception as e:
            yield f"[Error!!! GPT something wrong: {str(e)}]"
            return

        if self._is_stream:
            text = ''
            for token in response:
                if not token.choices[0].finish_reason:
                    yield str(token.choices[0].delta.content)
                    text += str(token.choices[0].delta.content)
        else:
            text = response.choices[0].message.content.strip(self._chars_strip)
            yield text

        # Remember GPT response
        self._messages.append({"role": "assistant", "content": text})


def get_answer_by_chatgpt(api_key: str,
                          prompt_text: str,
                          system_prompt_text: str = '',  # Роль
                          system_prompt_adv_text: str = '',  # Доп. пожелания (напр. формат вывода ответа),
                          **replace_texts,
                          ):
    """Get text response from ChatGPT by prompt"""

    chat_gpt = ChatGPT(
        api_key=api_key,
        proxy=PROXY,
        model=CHAT_GPT_MODELS['GPT-4.0'],
        chars_strip=RESPONSE_STRIP_CHARS,
        is_stream=True,
        system_prompt=system_prompt_text,
        system_prompt_adv=system_prompt_adv_text,
    )

    try:
        response = chat_gpt.get_answer(prompt_text, **replace_texts)
    except Exception as e:
        print(e, flush=True)
        return "[Error!!! ChatGPT something wrong]"
    text = ''
    for chunk in response:
        text += chunk
    text = text.replace('###', '')

    return text


if __name__ == "__main__":
    from config.prompts import (video_meaning, video_meaning_system,
                                task_by_video_meaning, task_by_video_meaning_system,
                                task_checking, task_checking_system)
    from core.utils.youtube import get_youtube_subtitles

    subtitles = get_youtube_subtitles('https://www.youtube.com/watch?v=XtVEil-PqZc', timing=(0, 120))
    print(subtitles)
    print('#'*100)

    answer = get_answer_by_chatgpt(OPENAI_API_KEY,
                                   video_meaning,
                                   video_meaning_system,
                                   '',
                                   __subtitles__=subtitles)
    print(answer)
    print('_'*100)

    tasks = get_answer_by_chatgpt(OPENAI_API_KEY,
                                  task_by_video_meaning,
                                  task_by_video_meaning_system,
                                  '',
                                  __video_meaning__=answer)
    print(tasks)
    print('^'*100)

    children_answer = """Я придумал план как спасти деревню. Я построю высокий замок из песка и сделаю укрепления из бумаги и кортона"""#input("children= ")
    check_answer = get_answer_by_chatgpt(OPENAI_API_KEY,
                                         task_checking,
                                         task_checking_system,
                                         '',
                                         __task__=tasks,
                                         __children_answer__=children_answer)
    print(check_answer)
