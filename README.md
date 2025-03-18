# Semantic kernel learning

This repository used for learning purposes and to experiment with the [Semantic Kernel](https://learn.microsoft.com/en-us/semantic-kernel/overview/).

## Chat Completion Workflow

This small sample demonstrate how LLM can be used for orchestrating a workflow for data collection and passing it to a downstream system.

Two main inputs are provided to the LLM to enable intelligent navigation through the workflow:

* Workflow Definition (see [release workflow](workflows/release-workflow.txt))
* LLM Function Definitions (see [functionDefinitions.py](./chat-completion-workflow/plugins/))

I this sample, calls to external systems performed by functions are mocked in the plugin definitions.

## Initial Setup

To run this sample you need to have an instance of Azure AI Foundry with an OpenAI chat model deployed (chatgpt-4o preferrably) - see [documentation](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource?pivots=web-portal).

Once your model is ready, create an `.env` file by copying `.env.template` and replacing values with your configuration.

this repository using [Gradio](https://www.gradio.app/docs) UI builder to create chatbot ui. 

## Setup

This sample is using [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers) to provide a consistent development environment. To use it, you need to have [Docker](https://www.docker.com/) and [Visual Studio Code](https://code.visualstudio.com/) installed.

Install Python dependencies if not previously done (this is not required if you open the project in a devcontainer):

```bash
make setup
```

## Running the sample

Run the sample that is using the Chat completion service of Semantic Kernel by running the following command:

```bash
make chatbot
```

To run the sample using the Chat completion Agent feature of the Semantic Kernel, run the following command:

```bash
make chatbot-agent
```
