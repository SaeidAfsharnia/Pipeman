from timeit import repeat
from xProjectData import core as xpdCore
import os
import sys
from xConfig import baseConfig , assetConfig
import logging



# setup
logger = logging.getLogger(__name__)


#######################
# TYPE CLASS
#######################


class Type(object):
    
    
    def __init__(self, typ):

        self._project, self._block = xpdCore.getProjectBlock()
        self._basepath = os.path.join(baseConfig.PROJECTS_PATH, self._project, self._block)
        self.typePath = os.path.join(self._basepath,'assets', typ)
        #self.createType(typ)
        

    def createTypeDir(self):
        if os.path.isdir(self.typePath):
            return self.typePath
        else:
            os.makedirs(self.typePath)
            print(f'this is the path for scroll list: {self.typePath}')
            return self.typePath

   
    def getAssetType(self):
        # returns the asset
        print ('I am the getAsset func')


    def createAsset(self, name):
        assetObj = Asset(self, name)
        return assetObj



#######################
# ASSET CLASS
#######################

class Asset(object):
    
    
    def __init__(self, typeParent,name):
         self._typeParent = typeParent
         self._basepath = self._typeParent.typePath
         print(f'the asset base Path will be {self._basepath}')
         self._name = name
         self._assetPath = os.path.join(self._basepath ,str(self._name))
         print (f' this will be the asset path itself {self._assetPath}')
        
    

    def _makeAssetDir(self):

        assetPath = self._assetPath
        if os.path.isdir(assetPath):
            return assetPath
        else:
            os.mkdir(assetPath)
            return assetPath


    def getVersions(self):

        listVersions = os.listdir(self._basepath)
        existVersions = listVersions.sort()
        print(f'this is the list of existing versions {existVersions}')
        return existVersions

    
    def createVersion(self):
        versionObj = Version(self)
        return versionObj

    def getHighestVersion(self):
        self.verList = os.listdir(self._assetPath)
        print(f'I am checking this path: {self._assetPath} ')
        self.verNum = len(self.verList)
        print(f'there is : {self.verNum} versions available')
        return self.verNum



#######################
# VERSION CLASS
#######################

class Version(object):
    

    def __init__(self, assetParent):
         print (f'I recieved {assetParent} as assetParent')
         self._assetParent = assetParent
         print(f'this is the assetParent : {self._assetParent}')
         self._basepath = assetParent._assetPath
         print(f'this is asset path : {self._basepath}')
         self._version = self._assetParent.getHighestVersion() + 1
         self._verPath = os.path.join(self._basepath ,str(self._version))
         print(f'this will be the version Path: {self._verPath}')
         

    def makeVerDir(self):
        os.makedirs(self._verPath)

    def _createLod(self, lod):

        # check if it is a correct LOD
        if lod in assetConfig.GEO_LODS:
           
            # Make new instance of LOD Class
            lodObj = Lod( self, lod)
            return lodObj
        
        else:
           
            # show error
            logger.error(f"This {lod} is not a valid LOD")
            return
               

#######################
# LOD CLASS
#######################

class Lod(object):
    
    
    def __init__(self, versionParent, lod=None):

           
         print (f'I recieved {versionParent} as versionParent')
         print (f'I recieved {self} as self for LOD')
         print (f'I recieved {lod} as lod=None')
         self._versionParent = versionParent
         print(f'this is the versionParent : {self._versionParent}')
         self._basepath = versionParent._verPath
         print(f'this is the versionParent.path : {self._basepath}')
         self._lod = lod
         self._baseLodPath = self._basepath
         self._lodPath = os.path.join(self._baseLodPath ,str(self._lod))
         print(f'this is the lodPath: {self._lodPath}')
    
    def _isValidLod(self):

        return os.path.isdir(self._lodPath)


    def makeLodDir(self):
		
        # test for existing
        if self._isValidLod():
            return self._lodPath

        else:
            os.mkdir(self._lodPath)
     
    
    def _createRep(self, rep):

        # check if rep is a valid Rep
        if rep in assetConfig.GEO_REPS:
            repObj = Rep( self, rep)
            return repObj
        else:
            logger.error('this Representation is not valid')
            return


        
#######################
# REPRESENTATION CLASS
#######################

class Rep(object):
    
    
    def __init__(self, lodParent, rep=None):
         print (f'I recieved {lodParent} as lodParent')
         self._lodParent = lodParent
         print(f'this is the lodParent : {self._lodParent}')
         self._baseRepPath = lodParent._lodPath
         print(f'this is the lodParent.path : {self._baseRepPath}')
         self._rep = rep
         self._repPath = os.path.join(self._baseRepPath ,str(self._rep))
         print(f'this is the repPath: {self._repPath}')


    def _isExistRep(self):
        return os.path.isdir(self._repPath)


    def makeRepDir(self):

        if self._isExistRep():
            return self._repPath
        else:
            os.mkdir(self._repPath)

    def _makeSourcePath(self):
        self.sourceBasePath = os.path.join(self._repPath,"source.abc")
        print(f'this is the source path :{self.sourceBasePath}')
        return self.sourceBasePath
