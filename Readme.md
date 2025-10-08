```
------------------------------------------------
 _______                                         
/       \                                        
$$$$$$$  | ______    ______    _______  __    __ 
$$ |__$$ |/      \  /      \  /       |/  |  /  |
$$    $$//$$$$$$  |/$$$$$$  |/$$$$$$$/ $$ |  $$ |
$$$$$$$/ $$    $$ |$$ |  $$/ $$ |      $$ |  $$ |
$$ |     $$$$$$$$/ $$ |      $$ \_____ $$ \__$$ |
$$ |     $$       |$$ |      $$       |$$    $$ |
$$/       $$$$$$$/ $$/        $$$$$$$/  $$$$$$$ |
                                       /  \__$$ |
                                       $$    $$/ 
                                        $$$$$$/  
------------------------------------------------- 
Perpetual Error Recursion Correction sYstem
------------------------------------------------- 
```

# the_pasta
This repository is for setting up Percy nodes.  For "It worked on my machine," see [local_llm.mp4](local_llm.mp4).
* In this setup, we have three personalities:
    * Percy for long-running tasks
    * Gretchen for groceries, especially milk expiration
    * Winslow for scheduling
* To invoke, "Hey, [NAME]"

## Description
Since I had some beer and made this public, the OS setup below to install Ansible to run `playbook.yml` on the Pi to be used as a Percy node.  The Anker PowerConf S330 does a good job.  Beyond that,
* Input is welcome but won't necessarily be incorporated
* A key exception is prompt engineering
>Note: There are probably some credentials in here, but if you're on my local network, we have bigger problems.

## OS Setup
### Install Ansible on the Pi(s)
```
sudo apt-get update -y
sudo apt install -y software-properties-common
sudo apt-add-repository -y --update ppa:ansible/ansible
sudo apt-get install -y \
    ansible \
    flac \
    portaudio19-dev
```
### Playbook
We assume you have Ansible installed on your host machine to invoke the playbook on the Pi(s).  From there, manage with `systemd`.
