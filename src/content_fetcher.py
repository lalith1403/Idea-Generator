# Let's make use of SERP API to fetch content from Google!

# Idea is to first idenitfy topics to search about. Then for each topic, we fetch content using API.
# then, we create a hook, that is the post/image/video will be scripted/approached from this POV

# For example, if we have a topic "How to make money online", we will come up with a variety of perspectives
# - How to make money online writing? selling services? the future of money online? etc...

# Then picking one, we fetch content as usual on the topic.
# Align the content to match the hook. 

# Steps
# 1. Parse prompt through LLM to get 5 perspectives/POVs from which the topic can be covered
# 2. Select a POV, create search prompts engineered for maximum entropy
# 3. Use SERP API to fetch content from Google
# 4. Align the content to match the hook


# We will then use this hook to generate content for each topic.

import json
from prompt import UserPrompt
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate


class ContentFetcher:
    def __init__(self, meta_data, schedule, user_prompt):
        self.meta_data = meta_data
        self.schedule = schedule
        self.user_prompt = user_prompt
        self.llm = Ollama(model="llama2")

    def generate_search_prompts(self):
        # Load user prompt details
        prompt_details = self.user_prompt.get_prompt_details()

        # Generate POVs based on user prompt
        pov_prompt = f"Generate 5 different perspectives on {prompt_details['channel_theme']}, separated by commas."
        pov_prompt += f"For example, when it comes to coding, 5 perspectives are: 1. building a project from scratch, 2. exploring the applications, 3.seeing what a celebrity said about a topic, 4. understanding philsophy behing building. 5. seeing the pros and cons of a project"
        pov_prompt += f"The perspectives can be anything! Please do come up unique perspectives rather than just using the ones given as example! Think and then generate your own!"
        pov_prompt += f"The perspectives should be relevant to the channel theme and should be able to be used to generate content for the channel"
        pov_prompt += f"Use || as delimiter to separate the POVs and mark the end of each POV with a ||"
        povs = self.llm(pov_prompt)
        povs = povs.split('||')

        search_prompts = []
        for pov in povs:
            # For each POV, create a search prompt
            search_prompt = f"Find trending content about {prompt_details['channel_theme']} from the perspective of {pov.strip()}"
            search_prompts.append([search_prompt])

        return search_prompts

    def summarize_search_prompts(self, search_prompts):
        # Summarize the search prompts
        summarized_search_prompts = []
        for search_prompt in search_prompts:
            summarized_search_prompt = self.llm(f"Given {search_prompt}, summarize it in 10 words or less ideal for a google search. Only want summarized prompts, no need for any explanations or context or agreement to my command")
            summarized_search_prompts.append(summarized_search_prompt)
        
        return summarized_search_prompts


    def fetch_content(self):
        search_prompts = self.generate_search_prompts()
        search_prompts = self.summarize_search_prompts(search_prompts)

        from pprint import pprint
        # pprint(search_prompts)

        import os
        from serpapi import GoogleSearch
        import requests

        # TODO: Make the search more resilient
        
        search_results = {}
        for search_prompt in search_prompts:
            params = {
                "q": search_prompt,
                "hl": "en",
                "gl": "us",
                "api_key": os.getenv("SERPAPI_KEY")  # API key is set as an environment variable
            }
            search = GoogleSearch(params)
            results = search.get_dict()
            
            top_hits = []
            for i in range(5):
                if i < len(results.get("organic_results", [])):
                    result = results["organic_results"][i]
                    
                    # Fetch the content from the URL
                    url = result["link"]
                    response = requests.get(url)
                    content = response.text
                    
                    # Extract the content from the HTML
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(content, "html.parser")
                    text = soup.get_text()
                    
                    top_hits.append({
                        "title": result["title"],
                        "link": url,
                        "snippet": result["snippet"],
                        "content": text
                    })
            
            if "search_metadata" in results:
                serpapi_url = results["search_metadata"]["json_endpoint"]
            else:
                serpapi_url = "URL not found"
            
            search_results[search_prompt] = {
                "top_hits": top_hits,
                "serpapi_url": serpapi_url
            }
        
        return search_results
