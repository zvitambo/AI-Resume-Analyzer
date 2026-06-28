
import json


def extract_json_from_response(response_text: str) -> dict:
    json_acceptable_string = response_text.replace("'", "\"")
    return json.loads(json_acceptable_string) 