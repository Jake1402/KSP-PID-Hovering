# KSP Rocket Hover using PID
This is a project inspired by a drive to understand both PID tuning loops and how someone might hover, guide and land rockets. Its a super simple script, which involves three classes that work together to generate guidance signals for the rocket. I plan to develop this more as time goes on but for now it is safe to consider this small side project "complete". Some cool features of this program includes 3DOF of control allowing the space craft to move in axis. As this is a PID system it will always try its best to hold itself at a desired altitude regardless of craft pitch (up to a critic point) this allows you to essentially perfectly hover around the KSC as demonstrated in the gif below.

![Hovering around KSC](https://github.com/Jake1402/KSP-PID-Hovering/blob/main/images/hover-around-ksc.gif)

### Install:
To install run this script you only need one dependency and that the KRPC mod for KSP and the appropriate python package.
1. Follow the instructions [Here](https://krpc.github.io/krpc/) for the KRPC mod for KSP.
2. Download this repository and extract contents.
3. Open up your command line and run `pip install -r requirements.txt`
4. Finally launch KSP load a rocket craft and run  `python pythonPIDHover.py`

### Future plans:
Future plans for this project include a few things. For one I plan to incorporate GUI in to this program to show the following:
- Live PID error graphed
- Current PID values
- Engage and disable selected PID options (vertical, horizontal, attitude)
- Displaying current vehicle states (fuel, coordinates, etc)

<br>Using a GUI i'd also like to allow user to have the ability to change PID values and target values in flight through this GUI.
