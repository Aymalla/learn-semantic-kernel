import asyncio
import gradio as gr

from dotenv import load_dotenv

from ReleaseProcessChatbot import ChatBot

def main():

    # Create an instance of the ChatBot
    bot = ChatBot()

    # Create Gradio interface
    demo = gr.ChatInterface(
        type="messages",
        fn=bot.chat,
        chatbot=gr.Chatbot(type="messages"),
        title="Phil, your Release Chatbot",
        description="I can help you create and manage releases.",
        theme="default",
        examples=[
            "New color for the R22 mirror cap",
            "Update the infotainment system in the X33",
            "Door hinge in D21 rattling"
        ]
    )

    demo.launch()

# Run the main function
if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
