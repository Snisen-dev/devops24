# Some Tips and Tricks for Working With YAML and Ansible

## yamllint

    $ sudo apt install yamllint

## ansible-lint

    $ sudo apt install ansible-lint

## Visual Studio Code

- Extension "Ansible" (från Red Hat). Ansible language support

## Install Ansible in a Virtual Environment

    $ python -m venv my_environment
    $ source my_environment/bin/activate
    $ python -m pip install ansible ansible-lint
    $ [do your stuff]
    $ deactivate
