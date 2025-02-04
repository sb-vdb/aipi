# Setup the Raspberry Pi 5

This document guides through the basic setup of the system and how to use it remotely.

## Hardware
For most Demos, the bare Raspberry Pi 5 ("Raspi") is fine to use. For using the camera-based Demo, however, you need extra hardware. There are cameras and also [AI-accelerator kits](https://www.raspberrypi.com/products/ai-hat/) that are optimized for the Raspi.

## Operating System
Since the Raspis storage is a removable SD-card, you can just use another device that can write SD-cards, to install an operating system on it. I recommend using the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) for the complete setup of the OS.

![Screenshot of the Raspberry Pi Imager](https://assets.raspberrypi.com/static/4d26bd8bf3fa72e6c0c424f9aa7c32ea/d1b7c/imager.webp)

You can use any Linux-based OS. However, I recommend using the ``RaspbianOS 64-bit`` (based on Debian bookworm) operating system, as it is optimized for the Raspi and comes with Python and basic tooling pre-installed. 

In the next step of the installation process, you are asked to use a configuration and also asked to edit it. Use it to:
- setup a **device name** ("aipi" in my case)
- setup a **user**
- setup the **wireless network**, so it can connect straight away
- setup an **ssh-server**, so you can use the Raspi from any device in the local network

## Software
If you use RaspbianOS, you have everything setup to continue with the further guides. If you use another Linux-based operating system, you need to make sure to have installed:
- Python 3.10+
- and Python-tooling such as ``pip`` and ``venv``
- `dphys-swapfile` for large models, that don't fit inside the Raspi RAM

## Configure
Most things are configured through the applications used in the process. If you want to use large models with more than 7GB of weight sizes, we need to setup a swapfile. First we need to configure our swapfile:
```
sudo cp -f dphys-swapfile /etc/dphys-swapfile
```
This command takes the `dphys-swapfile` configuration file from this repo and copies it into `/etc/`, which is a root folder. So writing to it requires us to put `sudo` in front of the `cp` command to tell the system to run this command as root.
We then need to make `dphys-swapfile` work:
```
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
swapon
```

## Using the Raspi over the Network
If you setup user, network and ssh-server, you can basically just plug in the Raspi and never have it connected to a display or a keyboard ever. The SSH-server allows you to emulate a local console on any device that has network access to the Raspi, as if you would be using it on device.

Open a console (works for both Windows and Linux), and run:
```
ssh <user>@<device_name>
```
with `user` and `device_name` according to what you used during the installation of the Operating System. After successful connection, you are asked for your password. After logging in, you can use a shell just like locally.

There is one limitation to operating the Raspi via SSH. When you start a server application (like Ollama), it is started from within your shell (inside SSH client) and lives for as long the client lives. Without handling, after a time of idle, unfortunately, the connection will be terminated automatically, with the server application being shutdown with it.

This is why SSH server launch commands are appended a `&; disown` argument to. This detaches the process from the SSH client.

## Quick Shell Usage Intro

The Demo guides are aimed to explicitely list all commands needed, so you don't need to find out how to properly configure all tools to reproduce the Demos of this repo. Since targets of commands are all relative to the Repos top-folder: if you start there and follow the guides, everything should work without having to navigating any further than:
```
mkdir clones
cd clones
git clone https://github.com/sb-vdb/aipi.git
cd aipi
```
These four commands do:
1. create a directory `clones` (to keep things tidy)
2. navigate to the new directory
3. telling the ``git`` application to run its `clone` routine with the given URL as argument, which indeed clones the repo from the URL into a new directory with the repo's name
4. navigate to the cloned repo's folder, which is called `aipi`

That should be it for navigating and using CLI-stuff apart from just copying commands from these guides. If you want to learn more about CLI basics, keep reading:

---------------------
(Optional)

When talking about "navigate to ...", this comes down to the fact, that commands are always dispatched from a specific location. The current location is displayed on your current prompt line. Opening the terminal will usually start the session from your user folder.
The common short symbol for that location is `~`. This is a shortcut to the location ``/home/<username>/``. The first `/` is actually a location, too: the very root-directory where everything resides. It's good style to use your user space, whenever possible. Besides, there are also relative symbols for referencing the current folder ( `.` ) and its parent folder ( `..` ). A path like `/home/my_user/my_directory` is navigated by the system step-by-step. After every `/`, the system is at that other location. So, putting relative symbols can create dynamic but also transparent paths. `/home/my_user/../my_user/../my_user/../my_user` is a valid path.

Terminal commands are structured lines of text. The structure given by the Shell is actually not that much. It's just that the first term of your command must be the (path/)name of an executable. Anything after that may be formatted by the Shell, but then be passed as strings to the executable to be processed. Every structure past that first term is up to the command's program.

The probably most used command out there is `cd` for changing the directory. `cd` is an executable file, that lives somewhere on the system. Actually, it's placed inside ``/bin/``. And because that's where the Shell looks for executable files by default, we can just name the file to use it - but we could also explicitely name a whole path to any location. Typically, OS-level package managers put their managed applications into `/bin/` so their apps can be called just by their name. We can also configure the shell to lookup bare names in custom locations. But we will either use an explicit path, or properly installed applications.

`cd` is mainly used to navigate to paths that you name: 

```
cd some_subfolder       // relative without prepending "/"

cd /home/my_user        // absolute with prepending "/"
cd ~                    // shortcut symbol for user space
cd                      // leave blank to also go to user space
cd -                    // go to previously visited location
```

Creating a directory can be done with `mkdir <name-of-directory>`.

Using `ls` to list files:
```
// display contents of current folder
ls

// display contents of an explicit path
ls /home/my_user

// include hidden files
ls -a /home/my_user

// list-style
ls -l /home/my_user

// both features
ls -la /home/my_user
```

As mentioned, everything that comes after the program's name, is passed on to the program. How these arguments are used, is completely up to the program. It's conventional that dashes `-` and double-dashes `--` are used to configure sort of optional things.
Further, `-` indicates options with a single char name. Like `a` in `ls -a` is the short name of the option to list all files (also hidden dot-files). Since a single dash indicates single-char options, we can combine multiple such options into `-abcdefg` and all chars are interpreted individually. `--` indicate more verbose option names. Each option with a verbose name needs their own `--` prepended. For example, server launch commands are often given an IP address in the style `--ip=127.0.0.1`, or flagged for certain modes without an explicit value like `--debug`.

Most commands support the `--help` command with nothing else to it. For example `cd --help` shows an overview about the syntax for using and configuring `cd`.