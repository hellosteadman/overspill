Trace Ansible Playbooks
=======================

Use the Vagrantfile to set up a local development environment.

* Install Python and Ansible (`pip install paramiko PyYAML jinja2 httplib2 ansible`).
* Add local_settings.py file
* Run `vagrant box add hashicorp/precise64`
* Run `ansible-galaxy install ShadowKoBolt.postgresql`
* Run `ansible-galaxy install nickjj.nodejs`
* Run `vagrant up` from the root directory.
* Visit 192.168.60.100:8000 in your browser.
* Develop!
