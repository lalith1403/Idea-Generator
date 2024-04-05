 # Any sort of meta data
import os
import json

class MetaData:
    def __init__(self, channel_id):
        self.channel_id = channel_id
        self.json_path = f"{channel_id}.json"
        self.default_values = {
            "channel_vision": {"motive": ""},
            "target_audience": {
                "age_range": "18-45",
                "gender_distribution": "",
                "culture_specifics": "",
                "viewer_ambition": ""
            },
            "content_type": {
                "video": False,
                "podcast": False,
                "blog": False,
                "social_media_posts": False,
                "youtube_long_form": False
            },
            "content_format": {
                "shorts": False,
                "reels": False,
                "linkedin_video": False,
                "twitter_video": False,
                "vlogs": False,
                "tutorials": False,
                "explainer_videos": False,
                "reviews": False,
                "unboxing": False,
                "podcasts": False,
                "interviews": False,
                "webinars": False,
                "live_sessions": False,
                "qna": False
            }
        }
        if os.path.exists(self.json_path):
            with open(self.json_path, 'r') as file:
                metaconfig = json.load(file)
                self.default_values.update(metaconfig)

    def dump_metaconfig(self):
        metaconfig = {
            "channel_vision": self.default_values["channel_vision"],
            "target_audience": self.default_values["target_audience"],
            "content_type": self.default_values["content_type"],
            "content_format": self.default_values["content_format"]
        }
        with open(self.json_path, 'w') as file:
            json.dump(metaconfig, file, indent=4)

    def read_metaconfig(self):
        with open(self.json_path, 'r') as file:
            metaconfig = json.load(file)
            self.channel_vision = metaconfig.get("channel_vision", {})
            self.target_audience = metaconfig.get("target_audience", {})
            self.content_type = metaconfig.get("content_type", {})
            self.content_format = metaconfig.get("content_format", {})

    def print_metaconfig(self, analyze=False):
        if not analyze:
            print("Channel Vision: ", self.default_values["channel_vision"])
            print("Target Audience: ", self.default_values["target_audience"])
            print("Content Type: ", self.default_values["content_type"])
            print("Content Format: ", self.default_values["content_format"])
        
        else:
            from langchain_community.llms import Ollama
            from langchain_core.prompts import ChatPromptTemplate

            llm = Ollama(model="llama2")

            # Constructing the prompt with explicit references to required variables
            prompt = ChatPromptTemplate.from_messages([
                ("system", f"Given the channel vision of {self.default_values['channel_vision']['motive']}, and targeting an audience primarily interested in {self.default_values['target_audience']['age_range']},"),
                ("system", f"considering the content type to be video: {self.default_values['content_type']['video']}, podcast: {self.default_values['content_type']['podcast']}, and the format to be shorts: {self.default_values['content_format']['shorts']}, reels: {self.default_values['content_format']['reels']},"),
                ("system", "how would you approach creating content that resonates with this audience?"),
                ("user", "{input}")
            ])

            # Ensure that 'input' is a variable expected to be filled by the user's input
            # For demonstration, let's assume 'input' is a placeholder for user input
            user_input = "What is the channel vision?"

            # Invoke the chain with all necessary information
            chain = prompt | llm
            # wrap this in tqdm
            output = chain.invoke({"input": user_input, "default_values": self.default_values})
            print(output)

