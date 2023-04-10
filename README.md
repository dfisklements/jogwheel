# jogwheel
Code and plans for a desktop jogwheel based on the qtpy rp2040 and an as6500 magnetic encoder

![outside](jogwheel1.jpg)
![inside](jogwheel2.jpg)

## Hardware

QT-Py RP2040 ~ $10 <https://www.adafruit.com/product/4900>
- Small
- usb-C
- runs circuitpython (and others)
- can emulate an HID device

AS-5600 magnetic encoder ~ $3
- Cheap!
- no moving parts
    can be completely sealed
- uses i2c

6808ZZ ball Bearing ~ $10
- I had one lying around
- nice size for a jog wheel - wide center of gravity

Misc other parts
- 608 bearing
- 3d printed body
- some clear material for translucent base section (can be 3dp as well)
- heavy base
- stemma qt connector
- misc wires and soldering equipment

## software

see code folder

## 3d print files

Included are a base and a top, as well as a spinner handle

the top and base will need to be printed with aligned seems, and will need to be filed down until they are pretty flat.  I did this manually with both sandpaper and with a file, both worked fine.

see stl folder for models



