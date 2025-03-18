from typing import Annotated
from semantic_kernel.functions import kernel_function


class CommonPlugin:
    """Common tasks"""

    @kernel_function(
        name="start_over",
        description="Starts a new process to create a release for the user",
    )
    def start_over(self) -> str:
        return "Let's start over"

    @kernel_function(
        name="ask_clarification",
        description="Prompts the customer for clarification on their request.",
    )
    def ask_clarification(
        self, prompt: Annotated[str, "The prompt to ask the customer."]
    ):
        return {"prompt": prompt}
