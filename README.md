<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://img.freepik.com/free-vector/robot-arm-concept-illustration_114360-8436.jpg?t=st=1656519056~exp=1656519656~hmac=72a1bfa23b9fb27258f7614a4a378c813cf75a67f002c39cb10ed8537110442c&w=740" alt="Project logo"></a>
</p>

<h3 align="center">IWB ROS Python Package</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/kylelobo/The-Documentation-Compendium.svg)](https://github.com/kylelobo/The-Documentation-Compendium/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://github.com/kylelobo/The-Documentation-Compendium/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> IWB python package for robot simulation
    <br> 
</p>

## 📝 Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Running the Tests](#tests)
- [Usage](#usage)
- [Development](#development)
- [Built Using](#built_using)
- [TODO](../TODO.md)
- [Contributing](../CONTRIBUTING.md)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>

There are **the python package for iwb milling robot simulation**, relying on **ROS Noetic** distribution. With module "robot" and other relevant modules, the package performs **robot modeling, visualization, path planning, controlling, kinematics and dynamics calculation, robot simulation and computation**. The robot simulation and computation functionalities are realized by **IWB simulation package "iwbRBDL"**.

You can  **run script "demo.py" independently**, which already applied some functionalies of robot simulation. Of course, with IWB_ROBOT class in module "robot", you can also apply those functionalies with your own program. You can check the tutorial [**Here**](#usage) and the API document [**Here**](TODO)

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

These instructions will **get you a copy of the repository up** and enable it to **run with your system environment**. See [development](#development) for informations for developers.

The contents you need to walk through are:<br>
(*: the same as IWB ROS package.)
- System Environment (*)
- Prerequisites
  - ROS Noetic(*)
  - Moveit!(*)
  - Python3
  - Pykdl
  - hrl-kdl
  - iwbRBDL
  - Others
- Installation

### System Environment
***This instruction is the same as that in IWB ROS Package, you can skip it if you have already fulfilled all the requirements here.***

The packages work with ROS Noetic, which is primarily targeted at:

- **Ubuntu 20.04.4 LTS**

>Other systems are supported to varying degrees. (--- [**ROS Noetics**](http://wiki.ros.org/noetic))

Besides, if you are running everything with a virtual machine, the following configurations are recommended:

- **30 GB storage.**
- TODO...

You can follow the [**Tutorial Here**](https://ubuntu.tutorials24x7.com/blog/how-to-install-ubuntu-20-04-lts-on-windows-using-vmware-workstation-player) to setup a virtual machine.

### Prerequisites
###### Install ROS Noetic

The packages are based on ROS Noetic distribution. You may install the **desktop version** of ROS Noetic [**Here**](http://wiki.ros.org/noetic/Installation/Ubuntu). Please choose **Desktop-Full** install, which is also recommanded on that page.

~~Every time you want to run the packages with terminal, use the following command to **setup the ROS environment**.~~


```shell
source /opt/ros/noetic/setup.bash
```

~~if you want to source a different version of ROS, this line would be:~~

```shell
source /opt/ros/ROS-DISTRO/setup.bash
# for example ROS 2 foxy:
source /opt/ros/foxy/setup.bash
```

~~You may have noticed that it's possible to avoid doing this every time opening a terminal by **adding this line into your system "~/.bashrc"**. If you do so, please check if you append the line for **the ROS version that of your use**. (Remember this when transplant the project to a new ROS version, for example ROS 2 foxy)~~

~~Don't forget to try the turtle example provided in ROS tutorial to validate your installation.~~

Instead of running ROS from terminal, you can use ros python API to run ROS. The modules like "rospy" "roscore" or "rosnode" are quite helpful, which are installed during the installation of ROS. Our package will append the ROS python package directory to python module searching path for you (**But now it's for Noetic.** TODO: use system ROS-DISTRO to softcode this.).

###### Install Moveit

***You can skip this if you have followed the same one in IWB ROS packages' readme file.***

The path & motion planning parts of the packages are realized by **Moveit**, which is the most widely used for **robot manipulation**. And it cooperates well with ROS.

You can **install moveit ROS (binary) packages** by execute the following line in your terminal:

```shell
# here for ros noetic
sudo apt install ros-noetic-moveit 
```

_**tips:** You could always install missing ros packages using command line like:_


```shell
sudo apt update
sudo apt install ros-ROS_DISTRO-ros_package_name
# for example
sudo apt install ros-noetic-ros-control
```
The [**Moveit Tutorial**](https://ros-planning.github.io/moveit_tutorials/) can help you to understand its planning functionalities. The **Python interfaces** of Moveit are explained [Here](https://ros-planning.github.io/moveit_tutorials/doc/move_group_python_interface/move_group_python_interface_tutorial.html), which is quite helpful. And the process to **set up a robot configuration for Moveit** is shown [Here](https://ros-planning.github.io/moveit_tutorials/doc/setup_assistant/setup_assistant_tutorial.html).

Besides, for transplanting project to ROS 2, you may need Moveit2 instead of Moveit.

###### Python3

Ubuntu 20.04 and other versions of Debian Linux ship with Python 3 pre-installed.

~~You can also install it manually. But if so, there will be issues with library path. The python you install manually should be in directory like "/usr/local/bin...", but the one that is original with OS is in "/usr/bin...".~~

optional: install pip for further package installing.

```shell
sudo apt update
sudo apt -y upgrade
sudo apt install -y python3-pip
```

###### Install Pykdl

Note that Pykdl should be installed with the installation of ROS. You can also install it using:

```shell
sudo apt update
sudo apt install python3-pykdl
```

###### Install hrl-kdl
Hrl-kdl provides us with lots of utils for KDL, which can help us to **parse the robot URDF model** directly and **extract the kinematic chain** with only several steps. Its Tutorial is [**Here**](http://wiki.ros.org/pykdl_utils), which is somewhat out of date. Our tutorial also provide you with a light introduction of it, check it [**Here**](TODO).

For some reasons, it would be better to setup it from its repository clone. The following steps come from [**Here**](https://amir-yazdani.github.io/post/pykdl/), note that the version should be **"Python3 for Ubuntu 20.04 with ROS Noetic"**.

open a terminal and run:

```shell
cd
mkdir -p catkin_ws/src
cd ~/catkin_ws/src/
# clone the project repositroy (requires git tool)
git clone https://github.com/amir-yazdani/hrl-kdl.git
```
Checkout to the noetic-devel branch
```sh
cd hrl-kdl
git checkout noetic-devel
```

**Install pykd_utils**
```sh
cd pykdl_utils
# python3 setup.py build (maybe need sudo)
sudo python3 setup.py install
```

Install hrl_geom
```bash
cd ~/catkin_ws/src/hrl-kdl/hrl_geom/
python3 setup.py build
sudo python3 setup.py install
```

install urdf_parser and urdfdom-py

```bash
sudo apt-get install ros-noetic-urdf-parser-plugin
sudo apt-get install ros-noetic-urdfdom-py
```

Build the catkin workspace
```bash
cd ~/catkin_ws
# install catkin build tool package
sudo apt-get install python3-catkin-tools
# then build catkin
catkin build
```

Now the hrl-kdl has been succeessfully installed. 

###### iwbRBDL
TODO
###### Others
TODO

### Installing

After fulfilling the prerequisites, you can now install the package to your device.

Open a terminal (ctrl+alt+T) and run the lines below to **make new directory** for the project.

```shell
cd
mkdir -p my_pkg
cd my_pkg
```
Then run git command to **clone the packages into your new directory** (You may need permission for that, e.g. ask the owner to add you as a maintainer.):

```sh
# Do not ignore the point "." at last!
git clone https://gitlab.lrz.de/00000000014A6C01/sa_py_pkg.git .
```
Now check the packages you cloned. You can **install the package** using:

```sh
# You need sudo for that
sudo python3 setup.py install
```

It is recommended to **check the installation path of your python package (library directory)**. You can check it with python terminal interaction. Open a **new** terminal and run (must ensure the work directory is not the one you placed our repository, otherwise the package in the repository may be imported instead of the one you installed):

```sh
python3
```

to start Python3 terminal interaction, then run the following in that:

```sh
# Now you should be able to import our package
import iwb_ros.setting
iwb_ros.setting.bash_strout("package_path")
```

The output should be similar like:

```console
>>> iwb_ros.setting.bash_strout("package_path")
/usr/local/lib/python3.8/dist-packages/iwb_ros
```
which means your installation succeeds so far. You can **use ctrl+d** to quit the interaction programming of python3.

Since our package needs to **run bash script to use the launch file of ROS package**, you need to **change those scripts as executable**. In terminal the command for that should be "chmod +x FILENAME", but here you can run a script to achieve it. Open a new terminal and run:

```sh
cd my_pkg
# you need password for sudo
bash system_permission.sh 
```

Run it without error, then the package is ready for using.

## 🔧 Running the tests <a name = "tests"></a>

You can run demo.py for checking. Note that you need to **move it into a new directory** (differet from our project repository) to avoid importing the package in our repository.

You can either use python terminal command to run it, like:

```sh
cd path/to/it
python3 demo.py
```

Or you can also run it with IDE like vscode for bebug.

## 🎈 Usage <a name="usage"></a>

TODO

## 🚀 Development <a name = "development"></a>

The tree sturcture of the package is shown as follow:

TODO: tree structure


TODO API 

## ⛏️ Built Using <a name = "built_using"></a>

- [ROS Noeitcs](https://www.mongodb.com/) - Robot operation system API
- [Moveit](https://moveit.ros.org/) - Motion planning tool
- [Pykdl](http://docs.ros.org/en/diamondback/api/kdl/html/python/) - Robot kinematics
- [hrl-kdl](https://github.com/gt-ros-pkg/hrl-kdl/tree/125e8746814804b69ae1cd919276304da10e5d3c/pykdl_utils/src/pykdl_utils) - User interfaces of Pykdl 
- [iwbRBDL](https://gitlab.lrz.de/RoboticMilling/iwbrbdl) - IWB robot computation package

## ✍️ Authors <a name = "authors"></a>

- [@BBlab](https://github.com/kylelobo) - Student in mechanical engineering
- And ... more contributers in the future.
<!-- See also the list of [contributors](https://github.com/kylelobo/The-Documentation-Compendium/contributors) who participated in this project. -->

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- TODO: citing and inspiration mabe
- Thanks for your contribution to the project!
- ...
