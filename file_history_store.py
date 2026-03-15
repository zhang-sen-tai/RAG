import json
import os
from abc import ABC
from typing import Sequence
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage,message_to_dict,messages_from_dict

def get_history(session_id):
    return FileChatMessageHistory(session_id, "./chat_history")

class FileChatMessageHistory(BaseChatMessageHistory, ABC):
    def __init__(self, session_id , store_path):
        self.session_id = session_id
        self.store_path = store_path
        self.file_path = os.path.join(self.store_path, self.session_id)

        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def add_messages(self,messages:Sequence[BaseMessage]) -> None:
        all_messages = list(self.messages)
        all_messages.extend(messages)

        new_messages = [message_to_dict(message) for message in all_messages]

        # 将数据写入文件
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f)

    @property  # @property装饰器将messages方法变成成员属性用
    def messages(self) -> list[BaseMessage]:
        # 当前文件内： list[字典]
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_data = json.load(f)  # 返回值就是：list[字典]
                return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []

    def clear(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)

