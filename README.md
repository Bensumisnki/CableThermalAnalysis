# CableThermalAnalysis
### Summary:
This python program was developed based on the paper titled "Fundamentals of the Thermal Analysis of Complex Arrangements of Underground Heat Sources" by Brakelmann Et al. and IEC 60287. Within the program, the WorkeSpace.py file allows the user to create installation scenarios in which DC cables of selectable properties and loading can be modeled. The simulation calculates the steady state temperature in degrees Celsius assuming uniform soil conditions and constant loading. The calculator considers small segments of the conductor as heat point sources, and iteratively calculates the temperature at each point of the cables.

### Cables Crossing Example:
Two circuits consisting of parallel Aluminum conductors loaded to 300 Amps are modeled crossing each other. The installation is modeled in the WorkSpace, then run. Results are shown plotted via color scale merged with the installation as well as the temperature along the length of each individual cable in the installation.  
<img width="694" alt="image" src="https://github.com/user-attachments/assets/1da19b8a-ab39-4bc8-86ca-3792f81aa53c" />
<img width="929" alt="image" src="https://github.com/user-attachments/assets/8397a4ff-bc07-45ea-b9a9-645f6ce8b15c" />

### Parallel Cables Example:
Two circuits consisting of parallel Aluminum conductors loaded to 300 Amps are modeled parallel to each other. The installation is modeled in the WorkSpace, then run. Results are shown plotted via color scale merged with the installation as well as the temperature along the length of each individual cable in the installation.  
<img width="679" alt="image" src="https://github.com/user-attachments/assets/ae507482-2843-4b43-918b-ae826ae52640" />
<img width="940" alt="image" src="https://github.com/user-attachments/assets/3345feec-6f59-4567-af67-4a584a15dad4" />

### How to Create a New Scenario:
1. Open WorkSpace.py
2. Create a new method that will hold scenario data (installation data such as soil thermal resistivity, ambient temperature, and cables).
```
def new_scenario():
```
3. Create an installation object. Input the ambient temperature and soil thermal resistivity.
```
installation = Installation(ambTemp=30)
installation.soil.thermalResistivity = 3.5
```
4. Create cables. When creating cables add the following:
   - current in amps
   - deltaL = the cable will be chopped up into small line segments of this length and considered as heat sources. 0.01 is a good length to start with. (unit of meter)
   - startX = starting x coordinate of the cable (units of the coordinate system are in meters)
   - starty = starting y coordinate of the cable (y value is the depth)
   - startz = starting z coordinate of the cable
   - cableID = name of the cable
   - insulationTR = Insulation Thermal Resistivity of cable insulation. (unit of k.m/W)
   - armorBeddingTR = not yet incorporated in program
   - jacketTR = not yet incorporated in program
   - sheathLossFactor = not yet incorporated in program
   - armorLossFactor = not yet incorporated in program
   - conductorMaterial = "Al" or "Cu"
   - insulationSystem = "RoundSolid" or "RoundStranded"
   - ConductorDiameter = diameter of conductor in meters
   - conductorDCResistance20 = Conductor DC resistance at 20degC (units of ohm/meter)
   - frequency
```
cable1 = Cable(current=300, deltaL=0.01, startx=0, starty=-0.77, startz=0, cableID='cable1', insulationTR=3.5, armorBeddingTR=0,jacketTR=0,sheathLossFactor=0,armorLossFactor=0, conductorMaterial="Al", insulationSystem="RoundStranded", conductorDiameter=0.02159, conductorDCResistance20=0.0000951443569553806, frequency=0)
```
5. Add cable segments. Include the next X, Y, and Z coordinate for the cable. The cable segment will linearly extend the cable from the start point to the end coordinate specified. Subsequent cable segment adds will be added to the end of the cable. The user will only need to specify the new end point of the of the segment they are adding. units of the coordinate system are in meters. There is currently no limit to the number of segments each cable can have. This step should be repeated until the layout of the user's cable is complete.
```
cable1.addSegment(0, -0.77, 50)
```
6. Add the cable to the installation
```
installation.addCable(cable1)
```
7. Steps 4-6 can be repeated for each cable the user would like to add to the installation.
8. Plot the installation before calculating temperature.
```
installation.plot()
```
9. Calculate the steady state temperature of the cables in the installation.
```
calc = CableThermalCalculation(installation,xOffset=0,yOffset=0,zOffset=0)
```
10. Plot the temperature results
```
calc.plotResults()
```

