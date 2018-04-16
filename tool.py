#INSERT NAMES

import arcpy
import arcpy.mapping
import os
from arcpy import env
import random
import numpy  
env.overwriteoutput = True
arcpy.AddMessage("Hi")

arcpy.env.workspace = "C:/Users/G5223/Documents/ArcGIS/Test.gdb"

# The following line is for code testing ONLY and will be overwritten automatically upon running the sript.
shapefileInput = "C:/Users/G5223/Documents/ArcGIS/Test.gdb/states"
shapefileOutput = "C:/Users/G5223/Documents/ArcGIS/Output1.shp"

# The following line MUST be uncommented before use in ArcToolbox.
#shapefileInput = arcpy.GetParameterAsText(0)
#shapefileOutput = arcpy.GetParameterAsText(1)

# Below, a temporary shapefile, containing the contents of the inputted shapefile, is created in the scratch geodatabase.
numberOfColors = 5;
#shapefile = arcpy.env.scratchGDB + os.path.sep + "temporary2.shp"
shapefile = "C:/Users/G5223/Documents/ArcGIS/temp27.shp" #KEEP CHANGING THIS VALUE AS NECESSARY****************************************************
selectedShapefile = "C:/Users/G5223/Documents/ArcGIS/Test.gdb/select27"

arcpy.CopyFeatures_management(shapefileInput, shapefile)

# Below, a text field is added to the temporary shapefile, which will hold the unqiue identifying code for each color group.
newField1 = arcpy.ValidateFieldName("ColorGroup", shapefile)
arcpy.AddField_management (shapefile, newField1, "TEXT")

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

numberOfColors = 7
currentColor = 1
countOfFeatures = arcpy.GetCount_management(shapefile)
with arcpy.da.UpdateCursor(shapefile, ["ColorGroup"]) as cursor:
    #initializing the color for each feature; will likely be overriden later
    #throwiong spagheti at the wall
    for row in cursor:
        row[0] = str(currentColor)
        currentColor += 1
        if currentColor>numberOfColors:
            currentColor = 1 
        cursor.updateRow(row) 

arcpy.MakeFeatureLayer_management(shapefile, 'lyr')

enum1 = 0

listOfLists = []

print "MADE IT PAST UPDATE CURSOR"
changes = 1

print "test1"
while (changes > 0):
    changes = 0
    print "test2"
    with arcpy.da.UpdateCursor('lyr', ["xyIdent", "ColorGroup"]) as cursor:
        for row in cursor:
            xyIdentOfFeature = row[0]
            
            try:
                arcpy.Delete_management("feature1.shp")
            except:
                print "nothing exists"
            arcpy.FeatureClassToFeatureClass_conversion ('lyr', "C:/Users/G5223/Documents/ArcGIS/", 'feature1')#, xyIdent == xyIdentOfFeature, '', '') 
            
            print row
            selection = arcpy.SelectLayerByLocation_management('feature1', "BOUNDARY_TOUCHES", 'lyr', '', 'NEW_SELECTION', 'NOT_INVERT') #select all features that touch the selection
            
            try:
                arcpy.Delete_management(selectedShapefile)
            except:
                print "nothing exists"
            arcpy.CopyFeatures_management(selection, selectedShapefile)
            with arcpy.da.SearchCursor(selectedShapefile, ["xyIdent", "ColorGroup"]) as cursor2:
                options = ["1", "2", "3", "4", "5", "6", "7"]
                for row2 in cursor2:
                    print options
                    print row2
                    if row2[1] in options:
                        print row2[1]
                        newString = str(row2[1])
                        options.remove(newString)
                        print "test4"
                print options
                print row[1]
                if len(options) > 0 and (row[1] not in options):
                    row[1] = random.choice(options)
                    changes += 1
                    print "test5"
                cursor.updateRow(row)
                
counter = 0
countOfFeatures = (int)(str(countOfFeatures))

while counter<countOfFeatures:
    #print counter
    counter += 1
    if counter > countOfFeatures:
        break
    #check adjacency; our main algorithm
    #If touching and color codes are the same, change color codes and reset the counter
    #else increment counter
    
print "MADE IT PAST COUNTER"
    
with arcpy.da.UpdateCursor(shapefile, ["xyIdent", "ColorGroup", "neighbors"], sql_clause=(None,"ORDER BY rand")) as cursor:
    for row in cursor:
        currentFeatureID = row[0]
        #SelectLayerByLocation_management (shapefile, "BOUNDARY_TOUCHES", shapefile, "", "NEW_SELECTION", "NOT_INVERT")
        
##        idValue=
##        row[2] =
        #cursor.updateRow(row)



#Below, the output file is created and is given the contents of the temporary shapefile, which is then deleted.
arcpy.CopyFeatures_management(shapefile, shapefileOutput)
arcpy.Delete_management(shapefile)
