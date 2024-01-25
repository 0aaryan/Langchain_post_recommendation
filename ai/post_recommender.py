from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.prompts import PromptTemplate

from dotenv import load_dotenv

load_dotenv()


class PostRecommender:
    def __init__(self, model_name="gpt-3.5-turbo", tags_txt_path="tags.txt"):
        self.model_name = model_name
        self.tags_txt_path = tags_txt_path
        self.all_tags = self.load_tags()

    def load_tags(self):
        tags = []
        with open(self.tags_txt_path, "r") as f:
            for line in f.readlines():
                tags.append(line.strip())
        return tags

    class Tags(BaseModel):
        username: str = Field(description="username of the user")
        tags: list = Field(
            description="python list of tags that the user might be intrested in"
        )

    def get_user_tags(self, username, posts):
        parser = JsonOutputParser(pydantic_object=self.Tags)

        tags_prompt = """you are a social media expert , you study social media data
        i have a user and the post he likes , i want to classify the users intrest based on the post he likes into tags
        give atleast 10 tags that the user might be intrested in
        tags should be strictly from this list dont use any other tags
        output should have atleast 10 tags
        tag list : {tags}
        user name : {user_name}
        posts he likes : {posts}
        output format should be in json format without any code blocks
        """

        prompt = PromptTemplate(
            template=tags_prompt,
            input_variables=["user_name", "posts", "tags"],
            output_parser=parser,
            partial_variables={
                "format_instruction": parser.get_format_instructions(),
            },
        )

        model = ChatOpenAI(model=self.model_name)
        chain = prompt | model | parser
        ouput = chain.invoke(
            {"user_name": username, "posts": posts, "tags": self.all_tags}
        )
        return ouput

    def get_topic_tags(self, topic):
        pass

    def recommend_users(self, topic, user_tags_json):
        pass
