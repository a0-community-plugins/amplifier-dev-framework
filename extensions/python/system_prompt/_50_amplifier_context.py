from python.helpers.extension import Extension


class AmplifierContext(Extension):

    async def execute(self, system_prompt: list[str] = [], **kwargs):
        prompt = self.agent.read_prompt("fw.amplifier.reference.md")
        if prompt:
            system_prompt.append(prompt)
