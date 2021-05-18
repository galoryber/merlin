
from mythic_payloadtype_container.MythicCommandBase import *
from mythic_payloadtype_container.MythicRPC import *
import json

# Set to enable debug output to Mythic
debug = False


class ShellArguments(TaskArguments):
    def __init__(self, command_line):
        super().__init__(command_line)
        self.args = {
            "arguments": CommandParameter(
                name="arguments",
                type=ParameterType.String,
                description="Commandline string or arguments to run in the shell",
                required=True,
            ),
        }

    async def parse_arguments(self):
        if len(self.command_line) > 0:
            if self.command_line[0] == '{':
                self.load_args_from_json_string(self.command_line)
            else:
                self.add_arg("arguments", self.command_line)


class ShellCommand(CommandBase):
    cmd = "shell"
    needs_admin = False
    help_cmd = "shell"
    description = "Execute the commandline string or arguments in the operating system's default shell"
    version = 1
    author = "@Ne0nd0g"
    argument_class = ShellArguments
    attackmapping = ["T1059"]

    async def create_tasking(self, task: MythicTask) -> MythicTask:

        # Executable Arguments
        args = []
        # TODO Handle argument parsing when quotes and escapes are used
        arguments = task.args.get_arg("arguments").split()
        if len(arguments) == 1:
            args.append(arguments[0])
        elif len(arguments) > 1:
            for arg in arguments:
                args.append(arg)

        # Merlin jobs.Command message type
        command = {
            "command": "shell",
            "args": args,
        }

        task.args.add_arg("type", 10, ParameterType.Number)  # jobs.CMD = 10
        task.args.add_arg("payload", json.dumps(command), ParameterType.String)

        task.display_params = f'{task.args.get_arg("arguments")}'

        # Remove everything except the Merlin data
        task.args.remove_arg("arguments")

        if debug:
            await MythicRPC().execute("create_output", task_id=task.id, output=f'[DEBUG]Returned task:\r\n{task}\r\n')

        return task

    async def process_response(self, response: AgentResponse):
        pass
