"""
This module contains the command line interface for the sh_copilot package.
"""

from argparse import ArgumentParser

from sh_copilot.ai.models import AIModelFactory

parser = ArgumentParser(
    prog="Shell Copilot",
    description="Shell Copilot is a command line tool that uses AI to help you in your daily tasks.",
)

parser.add_argument(
    "-m",
    "--model",
    type=str,
    default="fake",
    help="AI model to use",
    choices=AIModelFactory.catalog.keys(),
)
