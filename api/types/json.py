from sqlalchemy.types import TypeDecorator, TEXT
import json


class JsonType(TypeDecorator):
    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is None:
            return "{}"
        return json.dumps(value, ensure_ascii=False)

    def process_result_value(self, value, dialect):
        if not value:
            return {}
        return json.loads(value)
