from CableInstallation import Installation, Cable
from CableTherm import CableThermalCalculation

def parallel_cables():
    #Create installation object
    installation = Installation(ambTemp=30)
    installation.soil.thermalResistivity = 3.5

    # Cable 2 is modeled after the reference cable - PV-Solar 2kV 600 KCMIL cable
    cable2 = Cable(current=300, deltaL=0.01, startx=0, starty=-0.77, startz=0, cableID='cable2', insulationTR=3.5,
                   armorBeddingTR=0, jacketTR=0, sheathLossFactor=0, armorLossFactor=0, conductorMaterial="Al",
                   insulationSystem="RoundStranded", conductorDiameter=0.02159,
                   conductorDCResistance20=0.0000951443569553806,
                   frequency=0)
    cable2.addSegment(0, -0.77, 50)

    # Cable 3 is modeled after the reference cable - PV-Solar 2kV 500 KCMIL cable
    cable3 = Cable(current=300, deltaL=0.01, startx=0.02160, starty=-0.77, startz=0, cableID='cable3', insulationTR=3.5,
                   armorBeddingTR=0, jacketTR=0, sheathLossFactor=0, armorLossFactor=0, conductorMaterial="Al",
                   insulationSystem="RoundStranded", conductorDiameter=0.02159,
                   conductorDCResistance20=0.0000951443569553806,
                   frequency=0)
    cable3.addSegment(0.02160, -0.77, 50)

    # Cable 2 is modeled after the reference cable - PV-Solar 2kV 600 KCMIL cable
    cable4 = Cable(current=300, deltaL=0.01, startx=0, starty=-1.07, startz=0, cableID='cable4', insulationTR=3.5,
                   armorBeddingTR=0, jacketTR=0, sheathLossFactor=0, armorLossFactor=0, conductorMaterial="Al",
                   insulationSystem="RoundStranded", conductorDiameter=0.02159,
                   conductorDCResistance20=0.0000951443569553806,
                   frequency=0)
    cable4.addSegment(0, -1.07, 50)

    # Cable 3 is modeled after the reference cable - PV-Solar 2kV 500 KCMIL cable
    cable5 = Cable(current=300, deltaL=0.01, startx=0.02160, starty=-1.07, startz=0, cableID='cable5', insulationTR=3.5,
                   armorBeddingTR=0, jacketTR=0, sheathLossFactor=0, armorLossFactor=0, conductorMaterial="Al",
                   insulationSystem="RoundStranded", conductorDiameter=0.02159,
                   conductorDCResistance20=0.0000951443569553806,
                   frequency=0)
    cable5.addSegment(0.02160, -1.07, 50)

    #add cables to the installation
    installation.addCable(cable2)
    installation.addCable(cable3)
    installation.addCable(cable4)
    installation.addCable(cable5)

    # Create 3D plot of the installation
    installation.plot()

    # Create a new calculation object
    calc = CableThermalCalculation(installation,xOffset=0,yOffset=-0.05,zOffset=0)



    #Plot temperature results of the thermal calculation
    calc.plotResults()

def cable_crossing():
    #Create installation object
    installation = Installation(ambTemp=30)
    installation.soil.thermalResistivity = 3.5

    #Cable 2 is modeled after the reference cable - PV-Solar 2kV 600 KCMIL cable
    cable2 = Cable(current=300, deltaL=0.01, startx=0, starty=-0.77, startz=0, cableID='cable2', insulationTR=3.5,
                   armorBeddingTR=0,jacketTR=0,sheathLossFactor=0,armorLossFactor=0, conductorMaterial="Al",
                   insulationSystem="RoundStranded", conductorDiameter=0.02159, conductorDCResistance20=0.0000951443569553806,
                   frequency=0)
    cable2.addSegment(0, -0.77, 50)
    #cable2.addSegment(30, -0.762, 50)
    #cable2.addSegment(30, -0.762, 80)
    #cable2.addSegment(60, -0.762, 80)


    # Cable 3 is modeled after the reference cable - PV-Solar 2kV 500 KCMIL cable
    cable3 = Cable(current=300, deltaL=0.01, startx=0.02160, starty=-0.77, startz=0, cableID='cable3', insulationTR=3.5,
                   armorBeddingTR=0, jacketTR=0, sheathLossFactor=0, armorLossFactor=0, conductorMaterial="Al",
                   insulationSystem="RoundStranded", conductorDiameter=0.02159, conductorDCResistance20=0.0000951443569553806,
                   frequency=0)
    cable3.addSegment(0.02160, -0.77, 50)

    #create cable object with a 90 degree bend
    #Cable 2 is modeled after the reference cable - PV-Solar 2kV 600 KCMIL cable
    cable4 = Cable(current=300, deltaL=0.01, startx=-25, starty=-1.07, startz=25, cableID='cable4', insulationTR=3.5,
                   armorBeddingTR=0,jacketTR=0,sheathLossFactor=0,armorLossFactor=0, conductorMaterial="Al",
                   insulationSystem="RoundStranded", conductorDiameter=0.02159, conductorDCResistance20=0.0000951443569553806,
                   frequency=0)
    #cable4.addSegment(-5, -0.77, 25)
    #cable4.addSegment(-2, -1.07, 25)
    #cable4.addSegment(2, -1.07, 25)
    #cable4.addSegment(5, -0.77, 25)
    cable4.addSegment(25, -1.07, 25)

    #create cable object with a 90 degree bend
    #Cable 2 is modeled after the reference cable - PV-Solar 2kV 600 KCMIL cable
    cable5 = Cable(current=300, deltaL=0.01, startx=-25, starty=-1.07, startz=25.02160, cableID='cable5', insulationTR=3.5,
                   armorBeddingTR=0,jacketTR=0,sheathLossFactor=0,armorLossFactor=0, conductorMaterial="Al",
                   insulationSystem="RoundStranded", conductorDiameter=0.02159, conductorDCResistance20=0.0000951443569553806,
                   frequency=0)
    #cable5.addSegment(-5, -0.77, 25.02160)
    #cable5.addSegment(-2, -1.07, 25.02160)
    #cable5.addSegment(2, -1.07, 25.02160)
    #cable5.addSegment(5, -0.77, 25.02160)
    cable5.addSegment(25, -1.07, 25.02160)



    #add cables to the installation
    installation.addCable(cable2)
    installation.addCable(cable3)
    installation.addCable(cable4)
    installation.addCable(cable5)

    # Create 3D plot of the installation
    installation.plot()

    # Create a new calculation object
    calc = CableThermalCalculation(installation,xOffset=0,yOffset=-0.05,zOffset=0)

    #Plot temperature results of the thermal calculation
    return calc.plotResults()

#parallel_cables()
cable_crossing()