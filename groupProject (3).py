#INSERT NAMES

import arcpy
import arcpy.mapping
import os
from arcpy import env
import random
import numpy  
env.overwriteoutput = True

# The following line is for code testing ONLY and will be overwritten automatically upon running the sript.
shapefileInput = "C:/Users/Elliot/Documents/Senior Year/Spring 2018/GEOG 5223 - GIS Design & Imple/Group Project/Data/tl_2017_us_state.shp"
shapefileOutput = "C:/Users/Elliot/Documents/Senior Year/Spring 2018/GEOG 5223 - GIS Design & Imple/Group Project/Output/Output1.shp"

# The following line MUST be uncommented before use in ArcToolbox.
#shapefileInput = arcpy.GetParameterAsText(0)
#shapefileOutput = arcpy.GetParameterAsText(1)

# Below, a temporary shapefile, containing the contents of the inputted shapefile, is created in the scratch geodatabase.
numberOfColors = 5;
shapefile = arcpy.env.scratchGDB + os.path.sep + "temporary1"
arcpy.CopyFeatures_management(shapefileInput, shapefile)

# Below, a text field is added to the temporary shapefile, which will hold the unqiue identifying code for each color group.
newField1 = arcpy.ValidateFieldName("ColorGroup", shapefile)
arcpy.AddField_management (shapefile, newField1, "INT")

# Below, a text field is added to the temporary shapefile, which will hold a list of the color codes of the polygons that each polygon borders.
newField12 = arcpy.ValidateFieldName("neighbors", shapefile)
arcpy.AddField_management (shapefile, newField2, "TEXT")

# Below, a text field (xyIdent) is added to the temporary shapefile, which will hold the unqiue identifying code for each individual polygon feature in the shapefile.
arcpy.AddGeometryAttributes_management (shapefile, "CENTROID_INSIDE", "", "", "")
newField3 = arcpy.ValidateFieldName("xyIdent", shapefile)
arcpy.AddField_management (shapefile, newField3, "TEXT")
arcpy.CalculateField_management (shapefile, "xyIdent", "str(!INSIDE_X!) + str( !INSIDE_Y!)", "PYTHON")
arcpy.DeleteField_management (shapefile, "INSIDE_X")
arcpy.DeleteField_management (shapefile, "INSIDE_Y")



# Geoprocessing is below.
#

numberOfColors = 7
currentColor = 1
countOfFeatures = arcpy.GetCount_management(shapefile)
with arcpy.da.UpdateCursor(shapefile, "ColorGroup") as cursor:
    #initializing the color for each feature; will likely be overriden later
    #throwiong spagheti at the wall
    for row in cursor:
        row[0] = currentColor
        currentColor ++
        if currentColor>numberOfColors:
            currentColor = 1 
        cursor.updateRow(row) 


list listOfLists = []
with arcpy.da.UpdateCursor(shapefile, ["xyIdent", "ColorGroup", "neighbors"], sql_clause=(None,"ORDER BY rand")) as cursor:
    for row in cursor:
        currentFeatureID = row[0]
        #select feature with currentFeatureID
        SelectLayerByLocation_management (shapefile, "BOUNDARY_TOUCHES", shapefile, "", "NEW_SELECTION", "NOT_INVERT") #select all features that touch the selection
        list newList = []
        newList.append(currentFeatureID)
        with arcpy.da.UpdateCursor(shapefile, ["xyIdent", "ColorGroup", "neighbors"], sql_clause=(None,"ORDER BY rand")) as cursor2:
            for row in cursor2:
                currentFeatureID2 = row[0]
                if not(currentFeatureID2==currentFeatureID):
                    newList.append(currentFeatureID2)
        listOfLists.append(newList)

                
counter = 0   
while counter<countOfFeatures:
    #check adjacency; our main algorithm
    #If touching and color codes are the same, change color codes and reset the counter
    #else increment counter
    

    
with arcpy.da.UpdateCursor(shapefile, ["xyIdent", "ColorGroup", "neighbors"], sql_clause=(None,"ORDER BY rand")) as cursor:
    for row in cursor:
        currentFeatureID = row[0]
        SelectLayerByLocation_management (shapefile, "BOUNDARY_TOUCHES", shapefile, "", "NEW_SELECTION", "NOT_INVERT")
        
        idValue=
        row[2] =
        cursor.updateRow(row)



#Below, the output file is created and is given the contents of the temporary shapefile, which is then deleted.
arcpy.CopyFeatures_management(shapefile, shapefileOutput)
arcpy.Delete_management(shapefile)
