import os

md5_path = "./md5.txt"

# Chroma
collection_name = "rag"
collection_model = "text-embedding-v4"
persist_directory = "./chroma_db"
chat_model_name = "qwen3-max"
# Spliter
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n","\n",".","。","!","！","?","？"," ",""]
max_split_char_number = 1000

similarity_top_k = 2

from dotenv import load_dotenv
load_dotenv()
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

session_config = {
        "configurable": {
            "session_id": "user_001",
        }
    }
