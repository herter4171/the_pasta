# the_pasta
This repository is for setting up Percy nodes.

## OS Setup

### Install Ansible
```
sudo apt-get update -y
sudo apt install -y software-properties-common
sudo apt-add-repository -y --update ppa:ansible/ansible
sudo apt-get install -y \
    ansible \
    flac \
    portaudio19-dev
```