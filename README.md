# Shell Copilot

## Description

Shell Copilot is a set of tools to help you in your daily shell usage.

## Installation

To install Shell Copilot, simply run the following command:

```bash
pip install --user sh-copilot
```

or with an isolated environment:

```bash
python -m venv ~/bin/sh_copilot_venv
~/bin/sh_copilot_venv/bin/pip install sh-copilot

ln -s ~/bin/sh_copilot_venv/bin/sh_copilot ~/bin/sh_copilot
ln -s ~/bin/sh_copilot_venv/bin/sc ~/bin/sc
```

## Usage

To use Shell Copilot, simply run the following command :

```bash
sh_copilot --help
```

or with the alias :

```bash
sc --help
```

## Contributing

To contribute to Shell Copilot, simply fork the repository and create a pull request. Please make sure to include a detailed description of your changes. Here are the things I will check during the review :

- Is CHANGELOG.md have been updated (**required**)
- Is the lint score did not decrease (**required**)
- Is the test coverage did not decrease (**required**)
- Is the documentation have been updated (**if required**)
- If tests have been added (**optional**)

### Development

This repository uses [Taskfile](https://taskfile.dev) to manage the development tasks. To see the available tasks, run the following command:

```bash
task --list
```