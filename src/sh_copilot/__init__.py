"""
Main module for Shell Copilot
"""
import sys

from sh_copilot.cli import parser
from sh_copilot.copilot import ShCopilot
from sh_copilot.ai import AIContext, AIModelFactory
from sh_copilot.config import Config

__version__ = "0.1.0"


def main():
    """
    Main function for Shell Copilot
    """
    cli_args = parser.parse_args()

    config = Config().load()

    ai_model_class = AIModelFactory.get_model(name=cli_args.model)
    ai_model = ai_model_class(**config.model.get(ai_model_class.name, {}))
    ai_context = AIContext(**config.context)

    shell = ShCopilot(
        ai_context=ai_context,
        ai_model=ai_model,
        **config.copilot,
    )

    shell.cmdloop()


if __name__ == "__main__":
    main()
