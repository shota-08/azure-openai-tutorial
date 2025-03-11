import os
from dotenv import load_dotenv
from openai import AzureOpenAI

class AzureOpenAIClient:
    def __init__(self):
        # 環境変数をロード
        load_dotenv()

        # Azure OpenAI のクライアント設定
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.api_version = os.getenv("OPENAI_API_VERSION")
        self.chat_deployment = os.getenv("OPENAI_CHAT_DEPLOYMENT")
        self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

        self.client = AzureOpenAI(api_key=self.api_key, api_version=self.api_version, azure_endpoint=self.azure_endpoint)
        self.USER_NAME = "user"
        self.ASSISTANT_NAME = "assistant"