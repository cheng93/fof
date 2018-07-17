class Command:
    async def execute():
        raise NotImplementedError

class CommandRunnerMixin:
    async def execute(self, command):
        return await command.execute()