The controller is the orchestrator of the idea engine. 
It is responsible for managing the flow of ideas and executing the actions needed to generate new ideas.

Steps:
1. Onboard Channel. Get Channel specific information. If Channel is already onboarded, get channel specific JSON and load into Metadata
2. Given the metadata, create a timeline for the channel for a given time period, defaulting to 1 week. If timeline exists, display the timeline
3. combining the timeline and metadata, construct a concise Langchain Prompt, and pass it to the LLM
    1. At this point, we need info about target platforms, target content, and feel of content(audio-visual)
4. Generate ideas from LLM for each of the types of content and platforms.



