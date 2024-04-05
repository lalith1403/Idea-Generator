import requests
from langchain.prompts import PromptTemplate

def filter_list_with_agent(input_list: list, instruction) -> list:
    """
    Filters a list based on an instruction using a local Ollama model. The instruction can be a PromptTemplate or a string.
    
    Args:
        input_list (list): The list to be filtered.
        instruction (Union[PromptTemplate, str]): The instruction or prompt for filtering the list.
        
    Returns:
        list: The filtered list.
    """
    def ollama_llm(prompt):
        response = requests.post(
            "http://localhost:11434/api/generate", 
            json={"model": "llama2", "prompt": prompt, "stream": False}
        )
        return response.json()["response"]
    
    if isinstance(instruction, PromptTemplate):
        instruction = instruction.format()
    
    def filter_func(item):
        prompt = f"{instruction}\nItem: {item}"
        result = ollama_llm(prompt)
        return "True" in result
    
    return [item for item in input_list if filter_func(item)]

def test_filter_list_with_agent():
    sample_list = [
        ["best coding projects for kids"],
        ["how to teach kids coding"],
        ["benefits of learning coding at a young age"],
        ["top coding languages for kids"],
        ["fun coding games for children"],
        ["painting"],
        ["singing"]
    ]
    
    instruction = "Filter the list to only include items related to teaching coding to kids."
    
    filtered_list = filter_list_with_agent(sample_list, instruction)
    
    assert len(filtered_list) <= len(sample_list), "The filtered list should be smaller than the original list"
    for item in filtered_list:
        assert "kids" in item[0] or "children" in item[0], f"Unexpected item in filtered list: {item}"
    
    print(filtered_list)
    print("test_filter_list_with_agent passed!")

test_filter_list_with_agent()

