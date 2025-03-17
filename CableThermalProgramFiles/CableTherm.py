import math
import numpy as np
import matplotlib.pyplot as plt
from CableInstallation import Installation, Cable
import pandas as pd
import plotly.express as px

#Eventually may want to pass in an array of the cables and the soil into the calculation object
class CableThermalCalculation:
    """
    Collection of functions to calculate thermal rise in cable installations
    """

    def __init__(self, installation, xOffset=0, yOffset=-0.05, zOffset=0):
        """
        Init statement to calculate the deltaT
        """
        self.results = self.deltaTEqn(installation, xOffset, yOffset, zOffset)
        self.installation = installation


    def deltaTEqn(self, installation, xOffset=0, yOffset=-0.05, zOffset=0, convReq=0.1):
        """
        Calculates the temperatures along the cable object at a slight offset from the cable coordinates specified by
        the user. For example, if the user sepecifies an xOffset of 0, yOffset of -1, and zOffset of 0, then the
        temperature will be calculated 1 meter below the length of the cable.
        :param cable: cable object. Contains info on cable temperature, losses, and other properties
        :param soil: soil object
        :param xOffset: x direction offset from point sources to calculate temperature increase. default 0
        :param yOffset: y direction offset from point sources to calculate temperature increase. default -0.05
        :param zOffset: z direction offset from point sources to calculate temperature increase. default 0
        :param convReq: Float value. Thermal calculation will iterate until the delta temperature is less than the specified value. defaults to 0.1
        :return:
        """

        def deltaTIsEqn(cable: Cable, soil: Installation.Soil):
            """
            Might be able to use an entire array instead of indexing one by one.
            Calculates the first term of the the equation to determine the cable temperature
            𝑊𝑐,𝑖,𝑖𝑠 * (𝑇𝑐𝑎𝑏,𝑖 + 𝑇4,𝑖)
            :param cable: cable object
            :param soil: soil object
            :return: result of first term. Float
            """
            Tcabi = (cable.insulationTR + (1 + cable.sheathLossFactor) * cable.armorBeddingTR + (1 + cable.sheathLossFactor + cable.armorLossFactor) * cable.jacketTR)
            return (cable.sectionWattLosses * cable.cablecoords[3]) * (Tcabi + soil.thermalResistivity)

        #Array to hold the coordinate data and delta temperature data
        deltaTempArr = []
        converged = False
        counter = 1

        while not converged:
            print("iteration: ", counter)
            counter += 1

            # Set converged flag to true. Will be set to false if the temperature delta in the iteration are too high.
            converged = True

            #Update the watt losses of cables in the installation. Updates based on the temperature of the cable section
            for cable in installation.cable_list:
                cable.updateConductorWattLoss()

            #Loop through each cable in the installation and calculate the temperature increase for each cable
            for cableI in installation.cable_list:
                # Placeholder deltaTemp array for intermediary calcs
                deltaTemp = np.zeros(cableI.cablecoords.shape[1], dtype=np.float64)

                #Record the cableI cable section temperatures to determine if the calculation has converged. This records the temperature
                #before the iteration has modified the CableI temperature.
                sectionCableTempBuffer = cableI.sectionCableTemp.copy()

                #reset cableI section temperatures to zero
                cableI.sectionCableTemp = deltaTemp

                # Create a zeros array for r+ and r- variables
                r_plus = np.zeros(cableI.cablecoords.shape[1], dtype=np.float64)
                r_minus = np.zeros(cableI.cablecoords.shape[1], dtype=np.float64)

                # Step through each cable in the installation and calculate the temp increase at the cable+specified offset
                for cableJ in installation.cable_list:
                    #Check if cableI and cableJ are the same
                    #If they are not the same proceed with the following code
                    #Thermal impact of CableJ on Cable I
                    if cableJ.cableID != cableI.cableID:

                        # Step through each coordinate in the cable+specified offset
                        for i in range(deltaTemp.shape[0]):
                            r_plus = np.sqrt((cableI.cablecoords[0][i] - cableJ.cablecoords[0]) ** 2 + (cableI.cablecoords[1][i] - cableJ.cablecoords[1]) ** 2 + (cableI.cablecoords[2][i] - cableJ.cablecoords[2]) ** 2)
                            r_minus = np.sqrt((cableI.cablecoords[0][i] - cableJ.cablecoords[0]) ** 2 + (cableI.cablecoords[1][i] + cableJ.cablecoords[1]) ** 2 + (cableI.cablecoords[2][i] - cableJ.cablecoords[2]) ** 2)
                            r_plus_inv = np.divide(1,r_plus) #,out=np.zeros_like(r_plus), where=r_plus!=0)
                            r_minus_inv = np.divide(1,r_minus) #, out=np.zeros_like(r_minus), where=r_minus!=0)
                            dt = r_plus_inv - r_minus_inv

                            #Multiply dt by segment length deltaL
                            dt = dt * cableJ.cablecoords[3] * cableJ.sectionWattLosses

                            #Update the delta temperature of the ith segment of CableI, by adding dt to array
                            deltaTemp[i] += np.sum(dt)

                    #If cableI is the same as cableJ
                    #CableI thermal impact on itself
                    elif cableI.cableID == cableJ.cableID:
                        # Step through each coordinate in the cable+specified offset
                        for i in range(cableI.cablecoords.shape[1]):
                            r_plus = np.sqrt((cableI.cablecoords[0][i] - cableJ.cablecoords[0]) ** 2 + (
                                        cableI.cablecoords[1][i] - cableJ.cablecoords[1]) ** 2 +
                                        (cableI.cablecoords[2][i] - cableJ.cablecoords[2]) ** 2)
                            r_minus = np.sqrt((cableI.cablecoords[0][i] - cableJ.cablecoords[0]) ** 2 + (
                                        cableI.cablecoords[1][i] + cableJ.cablecoords[1]) ** 2 +
                                        (cableI.cablecoords[2][i] - cableJ.cablecoords[2]) ** 2)

                            # at the index of the calc where the impact of the segment on itself is being calculated, set to 1 to avoid division error
                            r_plus[i] = 1
                            r_minus[i] = 1

                            #calculate the inverses of r_plus and r_minues
                            r_plus_inv = np.divide(1, r_plus)  # ,out=np.zeros_like(r_plus), where=r_plus!=0)
                            r_minus_inv = np.divide(1, r_minus)  # , out=np.zeros_like(r_minus), where=r_minus!=0)

                            # Calculate the difference of r_plus_inv - r_minus_inv per eqn(3) of white paper
                            # For transient calculation, the additional factors should be multiplied to r_plu_inv and r_minus_inv before subtracting
                            dt = r_plus_inv - r_minus_inv

                            # Multiply dt by cableK segment length deltaL and watt losses
                            dt = dt * cableJ.cablecoords[3] * cableJ.sectionWattLosses

                            # Update the delta temperature of the ith segment of CableI, by adding dt to array
                            deltaTemp[i] += np.sum(dt)


                        #Smoothing function to make temperature of small segments the average of the two adjacent points
                        #May not work properly if two small segments are adjacent
                        for i in range(cableI.cablecoords.shape[1]-1):
                            #Replace the temperature of the small segment with the average of the two adjacent point temps
                            if cableI.cablecoords[3][i] < cableI.deltaL:
                                deltaTemp[i] = (deltaTemp[i-1]+deltaTemp[i+1])/2

                    #Calculate the delta temperature based on the soil thermal conductivity
                deltaTIs = deltaTIsEqn(cableI, installation.soil)


                # Calculate the new temperature of each segment of cableI
                cableI.sectionCableTemp = deltaTIs + (
                            deltaTemp / (4 * math.pi * (1 / installation.soil.thermalResistivity))
                            + installation.ambTemp)

                # Calculatate the temperature delta from the calculation iteration
                cableSectionTempDelta = np.absolute(sectionCableTempBuffer - cableI.sectionCableTemp)

                # Check if the maximum temperature delta is within the specified convergence limit. If not, set the converged flag to false
                if np.max(cableSectionTempDelta) > convReq:
                    converged = False


        return None

    def plotResults(self):
        """
        Creates 3D plot of the thermal results calculation. Prints the max cable temperature of each cable.
        :return: plotly plot
        """
        frames = []
        for cable in self.installation.cable_list:
            print(cable.cableID)
            cable_df = pd.DataFrame({
                'cableX': cable.cablecoords[0],
                'cableY': cable.cablecoords[1],
                'cableZ': cable.cablecoords[2],
                'cableTemp': cable.sectionCableTemp,
                'cableDiameter': cable.conductorDiameter
            })
            frames.append(cable_df)

        installation_df = pd.concat(frames)

        fig1 = px.scatter_3d(installation_df, x='cableX',
                            y='cableZ',
                            z='cableY',
                            color='cableTemp')
        fig1.update_layout(scene=dict(zaxis=dict(range=[None, 0], ), ),)

        #fig1.show()

        frames=[]
        for cable in self.installation.cable_list:
            cable_length = np.zeros_like(cable.cablecoords[3])
            cable_length[0] += cable.cablecoords[3][0]
            for i in range(1, cable.cablecoords[3].shape[0]):
                cable_length[i] = cable_length[i - 1] + cable.cablecoords[3][i]
            cable_df2 = pd.DataFrame({
                'cableLength': cable_length,
                'cableTemp': cable.sectionCableTemp,
                'cableID':cable.cableID
            })
            frames.append(cable_df2)

        result = pd.concat(frames)
        fig2 = px.scatter(result,x='cableLength',y='cableTemp',color='cableID')
        #fig2.show()
        fig1.write_html("C:/Users/bensu/PycharmProjects/CableThermAnalysis - Steady State/.venv/3DLayout.html")
        fig2.write_html("C:/Users/bensu/PycharmProjects/CableThermAnalysis - Steady State/.venv/2DTemp.html")
        return fig1, fig2

        '''
        for cable in self.installation.cable_list:
            cable_length = np.zeros_like(cable.cablecoords[3])
            cable_length[0] += cable.cablecoords[3][0]
            for i in range(1, cable.cablecoords[3].shape[0]):
                cable_length[i] = cable_length[i - 1] + cable.cablecoords[3][i]
            plt.scatter(cable_length, cable.sectionCableTemp, label=cable.cableID)
            print(cable.cableID, "Max Temp:", np.max(cable.sectionCableTemp))

        # To show the plot
        plt.legend()
        plt.show()
        '''

