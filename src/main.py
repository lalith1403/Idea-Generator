# Main entry point for the application

import os
import sys
from content_processor import ContentProcessor

# Importing local modules
from meta import MetaData
from prompt import UserPrompt
from timeline import ContentTimelineGenerator
from content_fetcher import ContentFetcher
from constants import TAVILY_API_KEY, SERP_API_KEY

def initialize_api_clients():
    """
    Initialize any API clients here. This is a placeholder function.
    Replace with actual initialization code for APIs used in the project.
    """
    # Initialize tavily API
    os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY
    os.environ["SERP_API_KEY"] = SERP_API_KEY

def main():
    # Initialize API clients
    initialize_api_clients()
    
    # Check if a new channel is being onboarded
    # default values added for now! Later on to be removed and uncommented lines to be used!
    # new_channel = input("Is a new channel being onboarded? (yes/no): ")
    new_channel = "yes"
    
    if new_channel.lower() == 'yes':
        # Create channel specific config metadata
        # channel_id = input("Enter the channel ID: ")
        channel_id = "abc123"
        meta_data = MetaData(channel_id)
        meta_data.dump_metaconfig()    

        # Create timeline
        timeline = ContentTimelineGenerator(meta_data)
        schedule = timeline.generate_timeline()


    else:
        # Load meta data
        # channel_id = input("Enter the channel ID: ")
        channel_id = "abc123"
        meta_data = MetaData(channel_id)
    
    # Print meta config
    # meta_data.print_metaconfig()
    # Get user prompt

    user_prompt = UserPrompt()
    user_prompt.engage_conversation()
    
    # TODO: Implement logic to process user prompt and meta data to generate content ideas
    # This might involve calling other modules or APIs to fetch and process data
    # For example, fetching content from various sources on the net as mentioned in the readme
    
    # content generation takes in: meta data, schedule and user prompt
    # Structure the three inputs and consolidate it into a single prompt
    print("Content generation logic begins here!")
    content_fetcher = ContentFetcher(meta_data, schedule, user_prompt)
    content = content_fetcher.fetch_content()

    # call ContentProcessor
    content_processor = ContentProcessor(meta_data, schedule, user_prompt, content)
    generated_content = content_processor.process_content()

    print(generated_content)

if __name__ == "__main__":
    
    main()

# Note: To implement the logic for fetching and processing data from various sources,
# you might need to create additional modules such as `content_fetcher.py` and `content_processor.py`.
# These modules can handle the specifics of fetching data from the internet and processing it
# according to the user prompts and meta data.



