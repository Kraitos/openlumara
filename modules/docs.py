import core

class Docs(core.module.Module):
    """Allows your AI to grab documentation about anything you want. Has OpenLumara documentation included!"""

    settings = {
        "documentation_path": {
            "description": "The folder to grab docs from. It uses folders with markdown files. The default `docs` folder is the openlumara documentation!",
            "default": "docs"
        },
        "insert_system_prompt": {
            "description": "Will make your AI aware of all documentation subjects available to it. Stays small in system prompt because it only lists the top-level folders, which are the topics the documentation is about, not the individual pages.",
            "default": True
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = core.storage.StorageDict("docs", "markdown")

    async def on_system_prompt(self):
        if not self.config.get("insert_system_prompt"):
            return None

        topic_str = ", ".join(self.data.keys())

        return f"Topics available to fetch documentation on: {topic_str}"

    def _find_topic(self, topic: str):
        found = False
        for key in self.data.keys():
            if key.lower().strip() == topic.lower().strip():
                found = True
                break
        return found

    async def list_documentation(self, topic: str):
        """Grabs documentation about a specific topic. Use ONLY on topic listed within the `documentation` section of your system prompt"""

        if not self._find_topic(topic):
            return self.result("Documentation about that topic was not found. Please rely on your own knowledge or try a web search.", success=False)

        return self.result(list(self.data[topic.lower().strip()].keys()))

    async def read_documentation(self, topic: str, subject: str):
        """Reads documentation about a specific subject within a specific topic. Use list_documentation before calling this."""

        if not self._find_topic(topic):
            return self.result("Documentation about that topic was not found. Please rely on your own knowledge or try a web search.", success=False)


        if subject not in self.data[topic]:
            return self.result("That subject does not exist within that topic. Please use list_documentation first to see the available subjects within this documentation.", success=False)

        return self.data.get(topic).get(subject)
