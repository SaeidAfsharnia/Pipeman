from xProjectData import core as xpdCore
from xConfig import baseConfig
from xConfig import assetConfig
import xAsset.core as xACore
import maya.cmds as cmds
import imp



# RELOAD
imp.reload(xACore)


 #we make a function to make wndows

winname="Pipeline"
if (cmds.window(winname,q=True,ex=True)):
    cmds.deleteUI(winname)
cmds.window(winname,t="PipeMan",s=False,w=160,h=700)
cmds.columnLayout()
cmds.text('')

#cmds.text(l=" Please enter Project name", al = "left")


cmds.rowColumnLayout()
# Project field
cmds.frameLayout(l="Project Level", lw = 50)
inpProject = cmds.textFieldGrp(l = "Project Name:", text = "mnof")
# Block field
inpShot = cmds.textFieldGrp(l = "Shot Name:", text = "shot0010")

cmds.button(l="Create Project and Block",c="createPR()", h = 30, bgc = (0.2, 0.3 , 0.3), al = "right")


# Create Asset
cmds.separator(w=400,bgc=(0.2,0.2,0.2), h = 10)
cmds.frameLayout(l="Asset Level", lw = 50)


inpType = cmds.radioButtonGrp( label='Asset Type', labelArray4=['geo', 'shader', 'camera','light'], numberOfRadioButtons=4 )
cmds.separator(h = 10)
inpLodRadio = cmds.radioButtonGrp( label='LOD', labelArray3=['lo', 'md', 'hi'], numberOfRadioButtons=3 )
cmds.separator(h = 10)

inpAssetName = cmds.textFieldGrp(l = "Asset Name:", text = "name")
cmds.separator(h = 10)

# Publish Button
cmds.button(l="PUBLISH",c="publish()", h = 60, bgc = (0.6, 0.6 , 0))

cmds.separator(h = 10)
cmds.text('List of existing assets')


# Exist Assets

assetDirList=cmds.textScrollList(sc = 'assetSelection()', h = 200,ams=True)

cmds.separator(h = 10)
cmds.text('Import selected asset')
cmds.button(l="IMPORT",c="importAsset()", h = 60, bgc = (0.1, 0.5, 0.4))


cmds.showWindow()
    

#start of the functions




def createPR():
    '''Project Level'''
    project = cmds.textFieldGrp(inpProject, q = True, text = True)
    projectObj =xpdCore.Project(project, create=True)
    '''Block Level'''
    block = cmds.textFieldGrp(inpShot, q = True, text = True)
    blockObj = projectObj.createBlock(block)
    xpdCore.setProjectBlock(project, block)
    xpdCore.getListOfProjectBlocks(project)

def publish():
    name = cmds.textFieldGrp(inpAssetName, q = True, text = True)
    inpRadio = cmds.radioButtonGrp(inpType, q = True, sl = True)
    if inpRadio == 1:
        typ = 'geo'
    if inpRadio == 2:
        typ = 'shader'
    if inpRadio == 3:
        typ = 'camera'
    else:
        type = 'light'
        
    # Make Type folder
    typeObj = xACore.Type(typ)
    typeObj.createTypeDir()
    
    # Make Asset folder
    assetObj = typeObj.createAsset(name)
    assetObj._makeAssetDir()
    
    # Create versions
    assetObj.getHighestVersion()
    versionObj = assetObj.createVersion()
    versionObj.makeVerDir()
        
    # Make LOD folder
    inpLod = cmds.radioButtonGrp(inpLodRadio, q = True, sl = True)
    if inpLod == 1:
        lod = 'lo'
    if inpLod == 2:
        lod = 'md'
    if inpLod == 3:
        lod = 'hi'
    lodObj = versionObj._createLod(lod)
    lodObj.makeLodDir()
    
    # Make Rep folder
    rep = 'abc'
    repObj = lodObj._createRep(rep)
    repObj.makeRepDir()
    
    # Publish the source inside the directory
    selection = cmds.ls(sl = True)[0]
    cmds.AbcExport(j = f'-root |{selection} -file {repObj._makeSourcePath()}')
    
    # Update Asset Scroll List
    filePath = repObj.sourceBasePath
    cmds.textScrollList(assetDirList, e=True, append=filePath)

    
def assetSelection():
    global selectedAsset
    selectedAsset=cmds.textScrollList(assetDirList,q=True,si=1)
    print ("selected asset is: "+selectedAsset[0])
    return selectedAsset[0]

     
def importAsset():
    cmds.AbcImport(selectedAsset, d=1) 


    
    
    
    
    
    
    
    