import logging
import os

from releaseProcessPlugin import ReleaseProcessPlugin
from semantic_kernel import Kernel
from semantic_kernel.utils.logging import setup_logging
from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.functions.kernel_arguments import KernelArguments

from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)


class ChatBot:

    history: ChatHistory
    kernel: Kernel
    chat_completion: ChatCompletionClientBase
    execution_settings: AzureChatPromptExecutionSettings

    def __init__(self):
        # Initialize the kernel
        self.kernel = Kernel()

        # Create a history of the conversation
        self.history = ChatHistory()

        # Add Azure OpenAI chat completion
        self.chat_completion = AzureChatCompletion(
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
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
        self.__load_workflow_desciption()

    async def chat(self, message, history):

        # Add user input to the history
        self.history.add_user_message(message)

        # Get the response from the AI
        result = await self.chat_completion.get_chat_message_content(
            chat_history=self.history,
            settings=self.execution_settings,
            kernel=self.kernel,
        )

        # Add the message from the agent to the chat history
        self.history.add_message(result)

        return str(result)

    def __load_workflow_desciption(self):
        # Load the workflow from a file
        with open('workflows/release-workflow.txt', 'r') as file:
            release_process_definition = file.read()
            instructions = f"""
                You are a Release Process assistant. You must only answer requests related to Release Process.

                Below is the exact policy that you must follow to create a release for the user.

                POLICY:
                {release_process_definition}
                """
            # Add the system message to the history
            self.history.add_system_message(instructions)
