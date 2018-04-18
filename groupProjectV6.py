#INSERT NAMES

import arcpy
import arcpy.mapping
import os
from arcpy import env
import random
import numpy  
env.overwriteoutput = True
arcpy.AddMessage("Hi")






# The following line is for code testing ONLY and will be overwritten automatically upon running the sript.
shapefileInput = "C:/Data/states/stateLayer.shp"
shapefileOutput = "C:/Data/states/THIS_IS_THE_OUTPUT.shp"
workspaceString = "C:/Data/outputs"
numberOfColors = 7;

#THE ABOVE FOUR LINES ARE THE ONLY LINES THAT NEED TO BE CHANGED BEFORE TESTING ON ANOTHER COMPUTER################################################












arcpy.env.workspace = workspaceString
#create a folder WITHIN the workspace folder that the user selected



# The following line MUST be uncommented before use in ArcToolbox.
#shapefileInput = arcpy.GetParameterAsText(0)
#shapefileOutput = arcpy.GetParameterAsText(1)

# Below, a temporary shapefile, containing the contents of the inputted shapefile, is created in the scratch geodatabase.


#arcpy.Delete_management(shapefile)
shapefile = "temp1A.shp" 
selectedShapefile = "temp1B.shp"

arcpy.CopyFeatures_management(shapefileInput, shapefile)

# Below, a text field is added to the temporary shapefile, which will hold the unqiue identifying code for each color group.
#field1 = arcpy.ValidateFieldName("ColorGrp", shapefile)
arcpy.AddField_management (shapefile, "ColorGrp", "TEXT")



# Below, a text field is added to the temporary shapefile, which will hold a list of the color codes of the polygons that each polygon borders.

newField2 = arcpy.ValidateFieldName("neighbors", shapefile)
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

currentColor = 1
countOfFeatures = arcpy.GetCount_management(shapefile)
with arcpy.da.UpdateCursor(shapefile, ["ColorGrp"]) as cursor:
    #initializing the color for each feature; will be overriden later
    for row in cursor:
        row[0] = str(currentColor)
        currentColor += 1
        if currentColor>numberOfColors:
            currentColor = 1 
        cursor.updateRow(row) 

enum1 = 0

listOfLists = []

print "MADE IT PAST UPDATE CURSOR"
changes = 1

lyr = 'layer1'
arcpy.MakeFeatureLayer_management (shapefile, lyr)

print "test1"
incrementing1 = 0
while (changes > 0):
    incrementing1 = incrementing1 + 1
    changes = 0
    print "test2"
    incrementing2 = 0
    with arcpy.da.UpdateCursor(lyr, ["xyIdent", "ColorGrp"]) as cursor:
        for row in cursor:
            xyIdentOfFeature = str(row[0])
            print(xyIdentOfFeature)
            #arcpy.Delete_management("feature1.shp")
            incrementing2 = incrementing2 + 1

            layerName = "temporaryLayer" + str(incrementing1) + "t" +str(incrementing2)
            output1 = layerName + ".shp" ###############################
            try:
                arcpy.Delete_management(output1)
            except:
                print("Attempted to delete file that does not exist")
                
            expression1 = "\"xyIdent\" = \'" + xyIdentOfFeature +"\'"
            #query = "\"FIELD\" = \'121\'" SOURCE BELOW
            #https://gis.stackexchange.com/questions/80204/what-causes-executeerror-error-000358-invalid-expression-failed-to-execute-se
            
            arcpy.SelectLayerByAttribute_management(lyr, "NEW_SELECTION", expression1)


            ###Copies features from the input feature class or layer to a new feature class. If the input is a layer which has a
            ###selection, only the selected features will be copied. If the input is a geodatabase feature class or shapefile,
            ###all features will be copied
            arcpy.CopyFeatures_management (lyr, output1)

            
            #arcpy.FeatureClassToFeatureClass_conversion (lyr, workspaceString, output1, expression1)

            #########The input to select by location must be a feature layer; it cannot be a feature class
            output2 = layerName + "layer"
            arcpy.MakeFeatureLayer_management (output1, output2)
            
            
            arcpy.SelectLayerByLocation_management(lyr, "BOUNDARY_TOUCHES", output2, '', 'NEW_SELECTION', '') #select all features that touch the selection
            arcpy.SelectLayerByAttribute_management(lyr, "REMOVE_FROM_SELECTION", expression1) #MUST REMOVE THE ORIGINAL FEATURE FROM THE SELECTION OF OTHER POLYGONS

            selectedShapefile = layerName + "juxtaposedPolygons.shp"
            
            arcpy.CopyFeatures_management(lyr, selectedShapefile)
            
            with arcpy.da.SearchCursor(selectedShapefile, ["xyIdent", "ColorGrp"]) as cursor2:
                options = [str(x) for x in range(1, (numberOfColors+1) )]
                
                #options = ["1", "2", "3", "4", "5", "6", "7"]
                
                for row2 in cursor2:
                    print options
                    print row2
                    if row2[1] in options:
                        print row2[1]
                        newString = str(row2[1])
                        options.remove(newString)
                print options
                print row[1]
                if len(options) > 0 and (row[1] not in options):
                    row[1] = random.choice(options)
                    changes += 1
                cursor.updateRow(row)
                
            #DELETE FILES NO LONGER NEEDED
            arcpy.Delete_management (output2)
            arcpy.Delete_management (output1)
            
                
print "MADE IT PAST COUNTER"
        

#Below, the output file is created and is given the contents of the temporary shapefile, which is then deleted.
arcpy.SelectLayerByAttribute_management(lyr, "CLEAR_SELECTION")
arcpy.CopyFeatures_management(lyr, "THIS_IS_THE_OUTPUT")

arcpy.Delete_management(lyr)

#DELETE FILES NO LONGER NEEDED
arcpy.Delete_management (selectedShapefile)
arcpy.Delete_management (shapefile)
