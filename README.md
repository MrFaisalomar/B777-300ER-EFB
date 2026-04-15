# B777-300ER Performance EFB 

A professional-grade Electronic Flight Bag (EFB) tool designed for flight simulation enthusiasts. This tool calculates critical takeoff performance data for the Boeing 777-300ER using real-world performance logic.

##  The Logic: Linear Interpolation
The core of this tool is a **Linear Interpolation Algorithm**. Since performance tables only provide data for specific weights, this program calculates the exact V-speeds (V1, VR, V2) for any custom weight entered by the pilot, ensuring high precision during the takeoff roll.

##  Features
- **Dynamic V-Speed Calculation:** Real-time calculation for Flaps 5 and Flaps 15.
- **Trip Fuel Estimator:** Calculates fuel requirements based on Distance, Fuel Flow, and Ground Speed (Wind correction included).
- **ISA Deviation Alerts:** Monitors ambient temperature to warn about performance changes.
- **Modern UI:** Built with `CustomTkinter` for a more modern design

##  Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/MrFaisalomar/B777-Performance-EFB.git](https://github.com/MrFaisalomar/B777-Performance-EFB.git)

