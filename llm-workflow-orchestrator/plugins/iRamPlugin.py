import uuid
from typing import Annotated
from semantic_kernel.functions import kernel_function


class IRamPlugin:
    """iRam integration functions"""

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

    @kernel_function(
        name="create_change_context", description="Creates a change context"
    )
    def create_change_context(
        self,
        title: Annotated[
            str, "Change context title with high-level description of the change."
        ],
        module_org: Annotated[
            str,
            "The Modul Org (department) responsible for the car component affected by the change.",
        ],
        derivative: Annotated[
            str, "The derivative (car component) affected by the change."
        ],
    ):
        return {
            "id": str(uuid.uuid4()),
            "title": title,
            "module_org": module_org,
            "derivative": derivative,
        }

    @kernel_function(
        name="create_kitz",
        description="Creates a Change Object (KITZ) associated to a previously created Change Context",
    )
    def create_kitz(
        self,
        problem: Annotated[
            str, "Description of the problem that this KITZ object is trying to solve."
        ],
        benefit: Annotated[str, "Description of the benefits of solving."],
        solution: Annotated[str, "Description of the change itself."],
        delivery_date: Annotated[
            str, "Target delivery date for the change in DD/MM/YY format."
        ],
    ):
        return {
            "id": str(uuid.uuid4()),
            "problem": problem,
            "benefit": benefit,
            "solution": solution,
            "delivery_date": delivery_date,
        }
