# Given the channel meta data, we will generate content timeline for a duration, default being a week
# This is like the schedule for the channel
# The timeline will be a list of content items, each with a date, title, and description
# The date will be a datetime object
# The title will be a string
# The description will be a string
# The timeline will be a list of content items
# The content items will be dictionaries with the following keys:
# - date: a datetime object
# - title: a string
# - description: a string

'''
Aspiration is to make it so that we can generate a content timeline for a given channel, and then use that timeline to generate a list of content items for the channel.

Train a model on the basis of variety of channels, how they progressed and what analytics to track!

'''

from datetime import datetime, timedelta
from meta import MetaData

from langchain_community.llms import Ollama 
from langchain_core.prompts import ChatPromptTemplate

class ContentTimelineGenerator:
    def __init__(self, meta_data: MetaData):
        self.meta_data = meta_data
        self.model = Ollama(model="llama2")

    def generate_content_ideas(self, num_ideas=7):
        prompt_text = self._create_prompt()
        from langchain.output_parsers import StructuredOutputParser

        class TimelineStructuredOutputParser(StructuredOutputParser):
            def get_format_instructions(self):
                return "Please format the output as a list of strings, each formatted as 'date: title, description'."

            def parse(self, output):
                # print("Output", output)
                timeline = []
                for item in output.split('\n'):
                    if item and ': ' in item:  # Ensure the item is not empty and contains the delimiter
                        date, rest = item.split(': ', 1)
                        if ', ' in rest:  # Additional check for the second split
                            title, description = rest.split(', ', 1)
                            timeline.append({'date': date, 'title': title, 'description': description})
                        else:
                            continue  # Handle the case where ', ' is not in rest appropriately
                    else:
                        continue  # Skip items that do not contain the ': ' delimiter
                return timeline

        my_response_schemas = [{
            "name": "ContentItem",  # Add a name for the schema
            "description": "Schema for a content item in the timeline.",  # Add a description for the schema
            "properties": {
                "date": {
                    "type": "string",
                    "format": "date",
                    "description": "The date when the content is scheduled, formatted as YYYY-MM-DD."
                },
                "title": {
                    "type": "string",
                    "description": "The title of the content item."
                },
                "description": {
                    "type": "string",
                    "description": "A brief description of the content item."
                }
            },
            "required": ["date", "title", "description"]
        }]
        
        parser = TimelineStructuredOutputParser(response_schemas=my_response_schemas)

        def validate_timeline_data(timeline_data):
            """
            Validates the timeline data to ensure it's in the expected format.
            Each item should have 'date', 'title', and 'description' keys.
            """
            for item in timeline_data:
                if not all(key in item for key in ['date', 'title', 'description']):
                    raise ValueError(f"Missing keys in item: {item}")
                if not isinstance(item['date'], str) or not isinstance(item['title'], str) or not isinstance(item['description'], str):
                    raise TypeError("One of 'date', 'title', or 'description' is not a string.")
            print("All timeline data items are correctly formatted.")

        # Validate the parsed timeline data
        # timeline_data = parser.parse(chain.invoke({"input": f"Create timeline for {num_ideas} days"}))
        chain = prompt_text | self.model | parser
        # chain = prompt_text | self.model
        timeline_data = chain.invoke({"input": f"Create timeline for {num_ideas} days"})
        validate_timeline_data(timeline_data)
        return timeline_data

    def _create_prompt(self):
        prompt = "Given the details below, you are the best there is to generate a content timeline for a channel with the following characteristics: "
        prompt += f"Vision: {self.meta_data.default_values['channel_vision']['motive']}, "
        prompt += f"Target Audience: {self.meta_data.default_values['target_audience']['age_range']}, "
        prompt += f"Content Type: {self.meta_data.default_values['content_type']['video']}, "
        prompt += f"Content Format: {self.meta_data.default_values['content_format']['shorts']}. "

        prompt += f"Sample prompt a dictionary: '2024-03-01: Title: 'Sample Title', Description: 'Sample Description'"
    
        prompt = ChatPromptTemplate.from_messages([("system",prompt), ("user",prompt)])
        # prompt += "Format the output as a dictionary of 'date', 'title', and 'description', and each entry as an independent key. "
        return prompt

    def generate_timeline(self):
        content_ideas = self.generate_content_ideas()
        # content_ideas is of type str
        start_date = datetime.now()
        schedule = []
        
        for i, idea in enumerate(content_ideas):
            content_item = {
                'date': (start_date + timedelta(days=i)).strftime('%Y-%m-%d'),
                'title': f"Content Idea {i+1}",
                'description': idea
            }
            schedule.append(content_item)
        return schedule


