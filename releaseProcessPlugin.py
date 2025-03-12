import string
import uuid
from typing import Annotated
from semantic_kernel.functions import kernel_function
from semantic_kernel.contents.chat_history import ChatHistory


class ReleaseProcessPlugin:

    @kernel_function(
        name="start_over",
        description="Starts a new process to create a release for the user"
    )
    def start_over(self, chatHistory: ChatHistory) -> str:
        return "Let's start over"
    
    @kernel_function(
        name="ask_clarification",
        description="Prompts the customer for clarification on their request."
    )
    def ask_clarification(self,
                                 prompt: Annotated[str, "The prompt to ask the customer."]):
        return {
            "prompt": prompt
        }

    @kernel_function(
        name="create_change_context",
        description="Creates a change context"
    )
    def create_change_context(
        self,
        title: Annotated[str, "Change context title with high-level description of the change."],
        module_org: Annotated[str, "The Modul Org (department) responsible for the car component affected by the change."],
        derivative: Annotated[str, "The derivative (car component) affected by the change."],
    ):
        return {
            "id": str(uuid.uuid4()),
            "title": title,
            "module_org": module_org,
            "derivative": derivative
        }

    @kernel_function(
        name="create_kitz",
        description="Creates a Change Object (KITZ) associated to a previously created Change Context"
    )
    def create_kitz(self,
                           problem: Annotated[str, "Description of the problem that this KITZ object is trying to solve."],
                           benefit: Annotated[str, "Description of the benefits of solving."],
                           solution: Annotated[str, "Description of the change itself."],
                           delivery_date: Annotated[str, "Target delivery date for the change in DD/MM/YY format."],
                           ):
        return {
            "id": str(uuid.uuid4()),
            "problem": problem,
            "benefit": benefit,
            "solution": solution,
            "delivery_date": delivery_date
        }

    @kernel_function(
        name="search_previous_kmnrs",
        description="Searches for previously completed Changes (KMNRs) to use as reference for new Change Contexts / Change Objects (KITZ)"
    )
    def search_previous_kmnrs(self,
                                     search_query: Annotated[str, "Search query to find previous KMNRs."]):
        return [
            {
                "id": str(uuid.uuid4()),
                "module_org": "KE02",
                "derivative": "X12",
                "title": "New mirror cap variant for the X12"
            },
            {
                "id": str(uuid.uuid4()),
                "module_org": "FE04",
                "derivative": "R44",
                "title": "Door hinge issues on R44"
            },
            {
                "id": str(uuid.uuid4()),
                "module_org": "KU12",
                "derivative": "F44",
                "title": "Steering wheel position"
            }
        ]
