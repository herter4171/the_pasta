# the_pasta
This repository is for setting up Percy nodes.  In this setup, we have three personalities:
* Percy for long-running tasks
* Gretchen for groceries, especially milk expiration
* Winslow for scheduling

## Description
Since I had some beer and made this public, the OS setup below to install Ansible implies running `playbook.yml` on the Pi to be used as a Percy node.  The Anker PowerConf S330 does a good job.  Beyond that,
* Input is welcome but won't necessarily be incorporated
* A key exception is prompt engineering
>Note: There are probably some credentials in here, but if you're on my local network, we have bigger problems.

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
