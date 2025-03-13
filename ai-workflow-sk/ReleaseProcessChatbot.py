import logging
import os

from releaseProcessPlugin import ReleaseProcessPlugin
from semantic_kernel import Kernel
from semantic_kernel.utils.logging import setup_logging
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents import ChatHistory
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)


class ChatBot:

    history: ChatHistory
    kernel: Kernel
    chat_completion: ChatCompletionClientBase
    execution_settings: AzureChatPromptExecutionSettings
    service_id: str = "chat-completion"

    def __init__(self):
        # Initialize the kernel
        self.kernel = Kernel()

        # Create a history of the conversation
        self.history = ChatHistory()

        # Add Azure OpenAI chat completion
        self.chat_completion = AzureChatCompletion(
            service_id=self.service_id,
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.kernel.add_service(self.chat_completion)

        # Set the logging level for  semantic_kernel.kernel to DEBUG.
        setup_logging()
        logging.getLogger("kernel").setLevel(logging.DEBUG)

        # Add a plugin (the LightsPlugin class is defined below)
        self.kernel.add_plugin(
            ReleaseProcessPlugin(),
            plugin_name="ReleaseProcess",
        )

        # Enable planning
        self.execution_settings = AzureChatPromptExecutionSettings()
        self.execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

        # Load the workflow description
        instructions = self.__load_instructions()

        # Add the system message to the history
        self.history.add_system_message(instructions)

    async def chat(self, message, history):

        # Add user input to the history
        self.history.add_user_message(message)

        # Get the response from the AI
        response = await self.chat_completion.get_chat_message_content(
            chat_history=self.history,
            settings=self.execution_settings,
            kernel=self.kernel,
        )
        
        # Handle function calls if any
        self.__handle_function_calls(response)
        
        # Add the message from the agent to the chat history
        self.history.add_message(response)
        
        self.__print_history()

        return str(response)

    def __load_instructions(self) -> str:
        # Load the workflow from a file
        with open('workflows/release-workflow.txt', 'r') as file:
            release_process_definition = file.read()
            instructions = f"""
                You are a Release Process assistant. You must only answer requests related to Release Process.

                Below is the exact policy that you must follow to create a release for the user.

                POLICY:
                {release_process_definition}
                """
            return instructions

    def __handle_function_calls(self, response):
        """ Handle function calls from the response.
        This method checks if the last message in the history contains a function call.
        extension to add more logic to handle special uses cases like clear history objects
        Args:
            response (_type_): _ChatMessageContent_: The response from the agent.
        """
        if len(self.history) >= 2:
            last_message = self.history.messages[-2].to_dict()
            tool_calls = last_message.get("tool_calls", [])
            for tool_call in tool_calls:
                function_call = tool_call.get("function")
                if function_call:
                    # Check if the tool call is a function call
                    function_name = function_call["name"]
                    arguments = function_call["arguments"]
                    if "start_over" in function_name:
                        self.__start_over()

    def __start_over(self):
        # Clear the history
        self.history.clear()
        # Add the system message to the history
        self.history.add_system_message(self.__load_instructions())
        
    def __print_history(self):
        print([msg.to_dict() for msg in self.history.messages])

