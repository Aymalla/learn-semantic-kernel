import asyncio
import argparse
import gradio as gr

from dotenv import load_dotenv
from releaseProcessAgent import ReleaseProcessAgent
from releaseProcessChatbot import ReleaseProcessChatbot


def main(type: str):
    # Create an instance of the ChatBot
    bot_title = "Release Process Chatbot"
    bot = ReleaseProcessChatbot()
    if type == "agent":
        bot = ReleaseProcessAgent()
        bot_title = "Release Process Chatbot-Agent"

    # Create Gradio interface
    demo = gr.ChatInterface(
        type="messages",
        fn=bot.chat,
        chatbot=gr.Chatbot(type="messages"),
        title=bot_title,
        description="I can help you create and manage releases.",
        theme="default",
        examples=[
            "New color for the R22 mirror cap",
            "Update the infotainment system in the X33",
            "Door hinge in D21 rattling",
            "Search for the latest changes of X12 derivative",
        ],
    )

    demo.launch()


# Run the main function
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-type",
        "--type",
    )
    args = parser.parse_args()

    load_dotenv()
    asyncio.run(main(args.type))
