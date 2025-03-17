import math

import numpy
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from IECTables import iec60287_Table2, iec60287_Table1


#Contains all cables and soil associated with the installation
class Installation:
    def __init__(self, ambTemp, thermalResistivity=1):
        """
        Stores all cable data and soil data within the installation
        :param ambTemp: Ambient Soil Temperature
        """
        self.cable_list = []
        self.num_cables = 0
        self.soil = self.Soil(thermalResistivity)
        self.ambTemp = ambTemp

    class Soil:
        def __init__(self, thermalResistivity):
            """
            Soil Object
            :param rho: Soil Rho Value
            """
            self.thermalResistivity = thermalResistivity
            #self.thermalConductivity = 1/thermalResistivity


    def addCable(self, cable):
        """
        Adds a cable object to the installation
        :param cable: cable object
        :return:
        """
        self.cable_list.append(cable)
        self.num_cables += 1

    def plot(self):
        """
        Function to create a 3D plot of the cables in the installatin
        :return:
        """
        # plot cable coordinates in 3D
        fig = plt.figure()

        # syntax for 3-D projection
        ax = plt.axes(projection='3d')

        #Loop through each cable and plot the coordinates to the scatter plot
        for cable in self.cable_list:
            cableCoords = cable.cablecoords
            ax.scatter(cableCoords[0], cableCoords[2], cableCoords[1], label=cable.cableID)

        # syntax for plotting
        ax.set_title('Cable Plot')
        plt.legend()
        plt.show()


#Contains all point sources associated with cable and cable properties
class Cable:
    def __init__(self, current: float, deltaL: float, startx: float, starty: float, startz: float, cableID: str,
                 insulationTR: float, armorBeddingTR: float, jacketTR: float, sheathLossFactor: float,
                 armorLossFactor: float, conductorMaterial: str, insulationSystem: str, conductorDiameter: float,
                 conductorDCResistance20: float, frequency: int):
        '''
        Cable object. Stores cable segments (straight lines of point sources), cable coordinates, cable watt loss/meter,
        length per point source(deltL).
        :param w_prime: watt loss / meter
        :param deltaL:  line source length (unit of meter)
        :param startx:  starting x coordinate of the cable (Axis unit of meter)
        :param starty:  starting y coordinate of the cable (depth) (Axis unit of meter)
        :param startz:  starting z coordinate of the cable (Axis unit of meter)
        :param cableID: ID of cable. Should not be the same cable ID in the same installation
        :param insulationTR: insulation thermal resistivity. (unit of k.m/W)
        :param conductorMaterial: "Al" for Aluminum, "Cu" for copper
        :param insulationSystem: example = "RoundStranded". Refer to IECTable2 for more options
        :param conductorDiameter: Conductor diameter (unit of meter)
        :param conductorDCResistance20: Conductor DC resistance at 20degC (units of ohm/meter)
        '''
        #cable identifier
        self.cableID = cableID

        self.current = current

        # Calculation of watt losses of the cable. Watts/meter
        #self.w_prime = current * current * self.resistance

        # Default maximum distance between point sources that make up a cable segment.
        self.deltaL = deltaL

        # Array of segment objects that make up a cable
        self.segm_array = []

        # Array of all point sources that make up a cable
        #[x],[y],[z],[deltaL]
        self.cablecoords = np.array([[],[],[],[]])

        # Array of the losses for each section of the cable
        # Losses are dependent on the cable section temperature
        self.sectionWattLosses = np.array([])

        # Array to track the temperature of each cable section
        self.sectionCableTemp = np.array([])

        # Track the number of cable segments that make up the cable (used for indexing)
        self.num_segm = 0

        # Track the head coordinate of the cable (ie. end of cable).
        # When adding cable segments, the new segment is added to the head of the cable
        self.cableHeadX = startx
        self.cableHeadY = starty
        self.cableHeadZ = startz

        #Cable Property Variables
        self.conductorMaterial = conductorMaterial
        self.insulationSystem = insulationSystem
        self.frequency = frequency #Hz
        self.conductorDiameter = conductorDiameter #For now we will pass in the DC resistance instead of calculating
        self.conductorDCResistance20 = conductorDCResistance20 #For now we will pass in the DC resistance instead of calculating it based on diameter. Ohm/meter
        self.insulationTR = insulationTR
        self.armorBeddingTR = armorBeddingTR
        self.jacketTR = jacketTR
        self.sheathLossFactor=sheathLossFactor
        self.armorLossFactor=armorLossFactor


    class Segment:
        def __init__(self, startX: float, endX: float, startY: float, endY: float, startZ: float, endZ: float, deltaL: float):
            """
            Straight line segment of a cable. Subcomponent of cable
            :param startX: segment's starting x coordinates
            :param endX: segment's ending x coordinate
            :param startY: segment's starting y coordinate. Y = depth
            :param endY: segment's ending y coordinate. Y = depth
            :param startZ: segment's starting z coordinate
            :param endZ: segment's ending z coordinate
            :param deltaL: maximum distance between point sources
            """
            self.startX = startX
            self.startY = startY
            self.startZ = startZ
            self.endX = endX
            self.endY = endY
            self.endZ = endZ
            self.deltaL = deltaL

            # Array to store the coordinates of the point sources that make up the cable
            # [[x1,x2,...],[y1,y2,...],[z1,z2,...],[deltaL1,deltaL2,...]]
            self.coordinates = np.array([[], [], [], []])

        def updateSegmentCoords(self) -> None:
            """
            Calculates the coordinates of the line segment based on the objects deltaL, Start, and End point.
            Adds the point source coordinates and DeltaLs to the segment coordinates array
            :return: none
            """
            deltaX = float(0)
            deltaY = float(0)
            deltaZ = float(0)

            # Determine the spacing between each point source in the X,Y,and Z directions
            # Calculate the total delta from start to end in the X,Y,and Z directions
            deltaX = self.endX-self.startX
            deltaY = self.endY-self.startY
            deltaZ = self.endZ-self.startZ

            #calculate absolute values for segment distance calculation
            absdeltaX = abs(deltaX)
            absdeltaY = abs(deltaY)
            absdeltaZ = abs(deltaZ)

            #calculate the total length of the segment
            segmDist = math.sqrt(absdeltaX**2+absdeltaY**2+absdeltaZ**2)

            # Normalize the delta x,y, and z based on the delta L value
            deltaX = self.deltaL * deltaX/segmDist
            deltaY = self.deltaL * deltaY/segmDist
            deltaZ = self.deltaL * deltaZ/segmDist

            # Set the starting coordinates of the segment
            coordX = self.startX
            coordY = self.startY
            coordZ = self.startZ

            # Calculate the distance from the current position in the segment to the end of the segment
            dist = math.sqrt((coordX-self.endX)**2 + (coordY-self.endY)**2 + (coordZ-self.endZ)**2)

            # Loop until the distance to the end of the segment is less than deltaL
            while (dist > self.deltaL):
                #print(dist, coordX,coordY, deltaX, deltaY)
                # Create placeholder numpy array of coordinates to append to segment coordinate array
                placeholder_array = np.array([[coordX],[coordY],[coordZ],[self.deltaL]])

                # Append new point source coordinate and segment length to the segment coordinate array
                self.coordinates = np.append(self.coordinates, placeholder_array,axis=1)

                # Calculate x,y,and z coordinate of next point source in segment
                coordX += deltaX
                coordY += deltaY
                coordZ += deltaZ

                # Calculate the new distance from the current coordinate to the end of the array
                dist = math.sqrt((coordX - self.endX)**2 + (coordY-self.endY)**2 + (coordZ-self.endZ)**2)

            # Add final length at the end of the segment. deltaL is overridden by the actual distance of the final segment
            if (dist <= self.deltaL):
                # Create numpy array of coordinates to append to segment coordinate array
                placeholder_array = np.array([[coordX], [coordY], [coordZ], [dist]])

                # Append new point source coordinate and segment length to the segment coordinate array
                self.coordinates = np.append(self.coordinates, placeholder_array, axis=1)

            return

    def addSegment(self, endX, endY, endZ) -> None:
        """
        Adds a new segment to the cable. Segment is added to the cable head and ends at the user entered end coordinates
        Adds segment object to the cable's segm_array and increases the num_segm counter
        :param endX: ending x coordinate of the segment
        :param endY: ending y coordinate of the segment (depth)
        :param endZ: ending z coordinate of the segment
        :return: none
        """
        # Create cable segment with dimensions that places it at the head of the cable
        cable_segment = self.Segment(self.cableHeadX, endX, self.cableHeadY, endY, self.cableHeadZ, endZ, self.deltaL)

        # Calculate the coordinates of the new segment
        cable_segment.updateSegmentCoords()

        # Append the segment object to the segment array
        self.segm_array.append(cable_segment)

        # Update the header coordinates of the cable
        self.cableHeadX = cable_segment.endX
        self.cableHeadY = cable_segment.endY
        self.cableHeadZ = cable_segment.endZ

        #increment the number of segments in the segment array
        self.num_segm += 1

        #Update cable coordinate array after adding a segment to the cable
        self.updateCableCoords()

        # Update cable section array sizes to match number of cable point sources
        #self.sectionWattLosses = np.full(self.cablecoords.shape[1],self.w_prime)
        self.sectionWattLosses = np.zeros(self.cablecoords.shape[1])
        self.sectionCableTemp = np.full(self.cablecoords.shape[1],90, dtype=np.float64)

        return

    def getCableHead(self):
        """
        Function to return the head of the cable. Returns X, Y, Z value as 3 variables
        :return: cableHeadX, cableHeadY, cableHeadZ
        """
        return self.cableHeadX, self.cableHeadY, self.cableHeadZ

    def updateCableCoords(self):
        """
        Updates the cable coord array [[x1,x2,...],[y1,y2,...],[z1,z2,...],[deltaL1,deltaL2,...]]
        :return: None
        """
        # Reset the cable coordinate array to an empty array.
        self.cablecoords = np.array([[],[],[],[]])

        # Move all segment coordinates to the cable coordinate array
        for i in range(self.num_segm):
            self.cablecoords = np.append(self.cablecoords,self.segm_array[i].coordinates,axis=1)

        return

    def updateSkinEffectFactor(self, dcResistanceOperatingTemp):
        #Calculations from section 2.1.2 Skin Effect Factor Ys from IEC 60287
        p1 = 8*math.pi*self.frequency*0.0000001*iec60287_Table2["SkinFactor"][self.conductorMaterial][self.insulationSystem]
        xs = numpy.sqrt(p1/dcResistanceOperatingTemp)
        if xs.all()>=0 and xs.all()<=2.8:
            return (xs**4/(192+0.8*xs**4))
        elif xs.all()>2.8 and xs.all()<=3.8:
            return (-0.136-0.0177*xs+0.056*3*xs**2)
        elif xs.all()>3.8:
            return (0.354*xs-0.733)
        else:
            return -1

    def updateProximityEffectFactor(self, dcResistanceOperatingTemp):
        #for simplification distance between conductor axis is taken to be diameter of conductor ie. touching
        p1 = 8 * math.pi * self.frequency * 0.0000001 * iec60287_Table2["ProximityFactor"][self.conductorMaterial][
            self.insulationSystem]
        xp = numpy.sqrt(p1 / dcResistanceOperatingTemp)
        p2 = xp**4/(192+0.8*xp**4)
        p3 = 0.312+(1.18)/((p2)+0.27)
        return p2*p3

    def updateResistance(self):
        """
        dcResistanceOperatingTemp = DC resistance of the conductor at operating temp (ohms/m).
        dcResistance20 = DC resistance of the conductor at 20degC (ohms/m). Derived from IEC 60228
        constMassTemp = Constant mass temp coefficient at 20degC. AL is 4.03X10^-3, CU is 3.93x10^-3
        maxOpTemp = cable's maximum operating temperature
        skinfactor = skin effect factor. Table 2 of IEC 60287. AL Round Stranded and AL Round Solid is 1.
        proximityfactor = proximity effect factor. Table 2. AL Round Stranded is 0.8. AL Round Solid is 1.
        :return:
        """
        #Updates the AC resistance of a cable
        #The following two should be cable variables calculated or passed in by the user
        #For now the DC resistance will be passed in from the datasheet instead of the conductor diameter
        #dcResistance20 = (iec60287_Table1["Resistivity"]["Conductor"][self.conductorMaterial])/(math.pi*(self.conductorDiameter/2)**2)
        dcResistance20 = self.conductorDCResistance20
        constMassTemp = iec60287_Table1["TempCoeff"]["Conductor"][self.conductorMaterial]

        #update DC resistance based on the section operating temperatures
        dcResistanceOperatingTemp = np.zeros_like(self.sectionWattLosses)
        dcResistanceOperatingTemp = dcResistance20 * (1 + constMassTemp * (self.sectionCableTemp - 20))
        #print(self.cableID, ": DC Resistance @ 20degC (ohm/m) :", dcResistance20)
        #print(self.cableID, ": DC Resistance @", self.sectionCableTemp[0],"degC (ohm/m) :", dcResistanceOperatingTemp[0])

        #update the skin and proximity effect factors based on the new dc resistance operating temp
        skinfactor = self.updateSkinEffectFactor(dcResistanceOperatingTemp)
        #print(self.cableID,": Skin Factor :",skinfactor[0])
        proximityfactor = self.updateProximityEffectFactor(dcResistanceOperatingTemp)
        #print(self.cableID, ": Proximity Factor :", proximityfactor[0])

        #return the section resistances of the cable updated for the section temperatures
        return dcResistanceOperatingTemp*(1+skinfactor+proximityfactor)

    def updateConductorWattLoss(self):
        #Calculate the resistance of each section of cable. Used for calculating section Watt losses
        sectionResistance = self.updateResistance()
        #print(self.cableID, ": Section Resistance (ohm) :", sectionResistance[0])
        #Update watt losses of each segment (units of W/m)
        self.sectionWattLosses = self.current * self.current * sectionResistance
        #print(self.cableID,": Section Watt Loss (W/m) :",self.sectionWattLosses[0])
