"""
    知识库
"""
import os
import hashlib
import config_data as config
from datetime import datetime
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sqlalchemy.util import md5_hex
from config_data import persist_directory

def check_md5(md5_str: str):
    """
        检查传入的md5字符串是否已经被处理过了
        :return False(md5未处理过) True(已经处理过)
    """
    if not os.path.exists(config.md5_path):
        # if 进来表示文件不存在，说明肯定没有处理过这个md5
        open(config.md5_path, 'w', encoding="utf-8").close()
        return False
    else:
        for line in open(config.md5_path, 'r', encoding="utf-8").readlines():
            line = line.strip()
            if line == md5_str:
                return True  # 处理过
        return False # 未处理


def save_md5(md5_str: str):
    """将传入的md5字符串，记录到文件内保存"""
    with open(config.md5_path, 'a', encoding="utf-8") as f:
        f.write(md5_str + "\n")


def get_string_md5(input_str: str, encoding="utf-8"):
    """将传入的字符串转换为md5字符串"""
    str_bytes = input_str.encode(encoding=encoding)

    md5_object = hashlib.md5()
    md5_object.update(str_bytes)
    md5_hex = md5_object.hexdigest()
    return md5_hex

class KnowledgeBaseService(object):

    def __init__(self):
        self.chroma = Chroma(
            collection_name = config.collection_name,
            embedding_function= DashScopeEmbeddings(
                model=config.collection_model,
                dashscope_api_key=config.DASHSCOPE_API_KEY
            ),
            persist_directory=config.persist_directory
        )  # 向量存储的实例
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            separators=config.separators,
            length_function=len
        )  # 文本分割器的对象

    def upload_by_str(self, data, filename):
        """将传入的字符串，进行向量化，存入向量数据库中"""
        md5_hex = get_string_md5(data)

        if check_md5(md5_hex):
            return "[跳过]知识库已加载该条数据"
        if len(data) > config.max_split_char_number:
            knowledge_chunks: list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunks: list[str] = [data]
        metadata= {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator":"森泰"
        }
        self.chroma.add_texts(
            knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks]
        )
        save_md5(md5_hex)
        return "[成功]内容已加载到知识库"
if __name__ == '__main__':
    """
    str1 = get_string_md5("AI大模型应用开发")
    str2 = get_string_md5("AI大模型应用开发")
    str3 = get_string_md5("AI大模型开发")
    print(str1)
    print(str2)
    print(str3)
    str4 = "Langchain学习"
    bo = check_md5(str4)
    if not bo:
        save_md5(str4)
    """
    know_rag = KnowledgeBaseService()
    ret = know_rag.upload_by_str("langchain是AI框架","AI程序员进阶宝典")
    print(ret)
