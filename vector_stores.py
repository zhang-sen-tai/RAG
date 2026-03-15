from langchain_chroma import Chroma
import config_data as config
from config_data import persist_directory
from langchain_community.embeddings import DashScopeEmbeddings


class VectorStoreService:
    # embedding 是外部传入的向量化模型对象，例如 DashScopeEmbeddings
    def __init__(self,embedding):
        self.embedding = embedding
        # 创建 Chroma 向量数据库对象
        self.vector_store = Chroma(
            collection_name = config.collection_name,
            # embedding_function 表示使用哪个 embedding 模型
            # 当进行向量搜索时，查询语句也需要转换成向量
            embedding_function = self.embedding,
            # persist_directory 表示向量数据库的本地存储路径
            # Chroma 会把数据保存到这个文件夹里（通常是 sqlite + index 文件）
            persist_directory = config.persist_directory
        )

    # 定义一个方法，用于获取 retriever（检索器）
    # 用于从向量数据库中检索与问题最相似的文本
    def get_retriever(self):
        """返回向量检索方便加入chain"""
        # as_retriever() 是 LangChain 提供的方法
        # 用于把向量数据库包装成一个 Retriever 对象
        # 这样就可以在 Chain / RAG / Agent 中直接使用
        return self.vector_store.as_retriever(

            # search_kwargs 是检索参数（字典类型）
            search_kwargs={
                # k 表示返回最相似的 k 条结果
                "k": config.similarity_top_k
            }
        )

if __name__ == '__main__':
    retriever = VectorStoreService(DashScopeEmbeddings(model=config.collection_model)).get_retriever()
    res = retriever.invoke("我身高180，体重130斤，穿多大码？")
    print(res)