# Позволяет вести диалог с Chat GPT

from openai import OpenAI, APITimeoutError
import httpx

OPENAI_API_KEY = 'INSERT_YOUR_API_KEY_FROM_OpenAI_ACCOUNT'
RESPONSE_STRIP_CHARS = '«»„““”"❝❞„⹂〝〞〟＂‹›❮❯‚‘‘‛’❛❜❟`\'., '
CHAT_GPT_MODELS = {
    'GPT-3.5': 'gpt-3.5-turbo-1106',
    'GPT-4.0': 'gpt-4-1106-preview',
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
                is_json and model in model in ['gpt-4-1106-preview', 'gpt-3.5-turbo-1106']) else {'type': "text"}
        self._is_stream = is_stream

    def get_answer(self, message: str, **replace_texts) -> str:
        """Get text response from GPT by prompt"""

        # Replacing all special keywords to text in message
        for replace_keyword, replace_text in replace_texts.items():
            message.replace(replace_keyword, replace_text)

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
            yield [f"[Error!!! GPT didn't give response with {self._client.timeout:.2f} seconds!]"]
            return
        except Exception as e:
            yield [f"[Error!!! GPT something wrong: {str(e)}]"]
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


if __name__ == "__main__":
    chat_gpt = ChatGPT(
        api_key=OPENAI_API_KEY,
        model=CHAT_GPT_MODELS['GPT-3.5'],
        chars_strip=RESPONSE_STRIP_CHARS,
        is_stream=True,
    )
    print("Starting dialog with GPT:\n")

    step = 1
    while True:
        print(f"{step:2}. You:", end="\n    ")
        question = input("What do you want to ask GPT: ")
        if not question:
            break

        answer = chat_gpt.get_answer(question)
        print(f"{step:2}. GPT:", end="\n    ")
        for chunk in answer:
            print(chunk, end="")
        print()

        print('_' * 100, end='\n\n')
        step += 1

