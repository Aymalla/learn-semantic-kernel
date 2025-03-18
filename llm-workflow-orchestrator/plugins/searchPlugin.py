import uuid
from typing import Annotated
from semantic_kernel.functions import kernel_function


class SearchPlugin:
    """Search integrtion functions"""

    @kernel_function(
        name="search_previous_kmnrs",
        description="Searches for previously completed Changes (KMNRs) to use as reference for new Change Contexts / Change Objects (KITZ)",
    )
    def search_previous_kmnrs(
        self, search_query: Annotated[str, "Search query to find previous KMNRs."]
    ):
        return [
            {
                "id": str(uuid.uuid4()),
                "module_org": "KE02",
                "derivative": "X12",
                "title": "New mirror cap variant for the X12",
            },
            {
                "id": str(uuid.uuid4()),
                "module_org": "FE04",
                "derivative": "R44",
                "title": "Door hinge issues on R44",
            },
            {
                "id": str(uuid.uuid4()),
                "module_org": "KU12",
                "derivative": "F44",
                "title": "Steering wheel position",
            },
        ]
