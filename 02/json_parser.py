from typing import Callable
import json


def default_function(key, token):
    return f"{key=}, {token=}"


def process_json(
    json_str: str,
    required_keys: list[str] | None = None,
    tokens: list[str] | None = None,
    callback: Callable[[str, str], None] | None = None,
) -> None:

    if required_keys is None:
        required_keys = []
    if tokens is None:
        tokens = []
    if callback is None:
        callback = default_function

    try:
        dict_from_json = {key: value.lower() for key, value in json.loads(json_str).items()}
    except Exception as exc:
        raise ValueError('Invalid JSON string') from exc

    set_req_keys = set(required_keys)
    lower_token = {token.lower(): token for token in tokens}

    for key, value in dict_from_json.items():
        if key not in set_req_keys:
            continue

        set_value = set(value.split())

        for token in lower_token:
            if token not in set_value:
                continue

            print(callback(key, lower_token[token]))


# например:
# if __name__ == '__main__':
#     json_str_ex = '{"key1": "Word1 word2", "key2": "word2 word3"}'
#     required_keys_ex = ["key1", "KEY2"]
#     tokens_ex = ["WORD1", "word2"]

#     process_json(json_str_ex, required_keys_ex, tokens_ex, lambda key, token: f"{key=}, {token=}")

    # выведет:
    # key="key1", token="WORD1"
    # key="key1", token="word2"
