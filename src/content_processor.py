# In this file, we get the search results from the content fetcher and process them to extract the content from the URLs.
# The output of this file is a dictionary of script, where each script has information about the following
# 1. title
# 2. type of content: 
# 3. platform: to get resolution details
# 4. content: actual content, with text, image prompts, design prompts, etc
# 5. B-roll: list of ideas/objects to be generated that can be inserted with step 4.
from langchain_community.llms import Ollama 
from langchain.prompts import PromptTemplate

from langchain.output_parsers import StructuredOutputParser
import json

class ContentProcessor:
    def __init__(self, meta_data, schedule, user_prompt, content):
        self.meta_data = meta_data
        self.schedule = schedule
        self.user_prompt = user_prompt
        self.content = content

    def generate_content(self, meta_content, llm):
        # returns content based on the meta_content
        response_schemas = [{
            "name": "ContentSchema",  # Add a name for the schema
            "description": "Schema for the content to be generated.",  # Add a description for the schema
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The content to be generated."
                },
                "platform": {
                    "type": "string",
                    "description": "The platform where the content will be published."
                },
                "content_type": {
                    "type": "string",
                    "description": "The type of content to be generated (e.g., post, short, reel)."
                }
            },
            "required": ["content", "platform", "content_type"]
        }]

        class ContentOutputParser(StructuredOutputParser):
            def get_format_instructions(self):
                return "Please format the output as a JSON object with fields content, platform and content_type."
            
            def parse(self, output):
                return output
        
        parser = ContentOutputParser(response_schemas=response_schemas)

        prompt = PromptTemplate(
            input_variables=["user_prompt", "content"],
            template="Given {platform} and {content_type}, generate the content for the following content: {content}. Return a JSON object with fields 'content', 'platform' and 'content_type'. Nothing additional should be output/printed!",
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )

        runnable = prompt | llm | parser
        content = runnable.invoke({"platform": meta_content["platform"], "content_type": meta_content["content_type"], "content": self.content})
        return content
    
    def process_content(self):
        class ContentOutputParser(StructuredOutputParser):
            def get_format_instructions(self):
                return "Please format the output as a JSON object with fields 'platform' and 'content_type'."

            def parse(self, output):
                # Assuming output is a JSON string that needs to be parsed according to the provided format instructions
                return output
        
        my_response_schemas = [{
            "name": "MetaContentSchema",  # Add a name for the schema
            "description": "Schema for the metadata of content including platform and content type.",  # Add a description for the schema
            "properties": {
                "platform": {
                    "type": "string",
                    "description": "The platform where the content will be published."
                },
                "content_type": {
                    "type": "string",
                    "description": "The type of content to be generated (e.g., post, short, reel)."
                }
            },
            "required": ["platform", "content_type"]
        }]
        

        parser = ContentOutputParser(response_schemas=my_response_schemas)
        prompt = PromptTemplate(
            input_variables=["user_prompt", "content"],
            template="Given {user_prompt}, return the multiple types of content and platform to be generated for the following content: {content}. Return a JSON object with fields 'platform' and 'content_type'. Nothing additional should be output/printed!",
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )

        llm = Ollama(model="llama2")
        runnable = prompt | llm | parser

        metacontent = runnable.invoke({"user_prompt": self.user_prompt, "content": self.content})

        print(repr(metacontent))
        metacontent = json.loads(metacontent)
        content = self.generate_content(metacontent, llm)
        return content
