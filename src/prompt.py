# Prompts from the user combined with meta data

import json

class UserPrompt:
    def __init__(self):
        self.prompt_details = {
            "channel_analytics": "",
            "channel_theme": "",
        }

    def capture_user_input(self):
        print("Let's gather some additional information about your content needs.")
        # self.prompt_details["channel_analytics"] = input("Can you share some insights from your channel's analytics? ")
        # self.prompt_details["channel_theme"] = input("What is the current theme of your channel and any new experiments you are considering? ")

        self.prompt_details["channel_analytics"] = "Analytics tell me that we need to get more trendy content"
        self.prompt_details["channel_theme"] = "Kids coding to learn to build stuff to life and see their awe"

    def confirm_details(self):
        print("\nPlease confirm the additional details you've entered:")
        for key, value in self.prompt_details.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        confirmation = input("Is this information correct? (yes/no) ")
        if confirmation.lower() == 'yes':
            return True
        else:
            print("Let's try entering the details again.")
            self.capture_user_input()

    def engage_conversation(self):
        self.capture_user_input()
        # if self.confirm_details():
        #     print("Great! We have captured your additional requirements.")
        # else:
        #     self.engage_conversation()

    def get_prompt_details(self):
        return self.prompt_details

    def dump_prompt_details(self, file_path):
        with open(file_path, 'w') as file:
            json.dump(self.prompt_details, file, indent=4)

    def read_prompt_details(self, file_path):
        with open(file_path, 'r') as file:
            self.prompt_details = json.load(file)

