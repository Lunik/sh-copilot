"""
Copilot shell
"""

import cmd
import sys

from sh_copilot.ai import AIAuthorType, AIMessage
from sh_copilot.config import Config


class ShCopilot(cmd.Cmd):
    """
    Copilot shell
    """

    intro = "Welcome to the Shell Copilot. Type help or ? to list commands.\n"
    prompt = "you> "

    def __init__(self, streamed, ai_context, ai_model) -> None:
        super().__init__()
        self.streamed = streamed
        self.ai_context = ai_context
        self.ai_model = ai_model

    def do_exit(self, arg: str) -> bool:  # pylint: disable=unused-argument
        """
        Exit the program
        """
        print("\nBye bye =)")
        return True

    def do_config(self, arg: str) -> bool:
        """
        Show the configuration
        """
        args = arg.split()

        if len(args) == 0:
            args.append("edit")

        match args[0]:
            case "edit":
                # Start the editor to edit the configuration
                config = Config().edit()

                for key, value in config.copilot.items():
                    setattr(self, key, value)

                self.ai_model = self.ai_model.__class__(**config.model)
                self.ai_context = self.ai_context.__class__(**config.context)

                print("Configuration updated")

            case "show":
                # Show the configuration
                config = Config().load()
                print(config.model_dump())

            case _:
                # Show the help
                print("Usage: config [edit|show|help]")

    def default(self, line) -> bool:
        """
        Default command
        """
        if line == "EOF":
            return self.do_exit(line)
        if line == "":
            return False

        human_message = AIMessage(content=line, author=AIAuthorType.HUMAN)
        self.ai_context.add(message=human_message)

        if self.streamed:
            ai_message_stream = self.ai_model.chat_completion_stream(
                context=self.ai_context
            )

            header_printed = False
            for ai_message in ai_message_stream:
                if not header_printed:
                    sys.stdout.write(str(ai_message))
                    header_printed = True
                else:
                    sys.stdout.write(ai_message.content)
                    sys.stdout.flush()

            sys.stdout.write("\n")
        else:
            ai_message = self.ai_model.chat_completion(context=self.ai_context)
            print(ai_message)

        self.ai_context.add(message=ai_message)

        return None
