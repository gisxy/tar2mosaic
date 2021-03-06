# -*- coding: utf-8 -*-
# Author:Guzhongren

# Date: 2017-08-02
# Update: 2017-08-03
if __name__ == "__main__":

    import os
    import tarfile
    import zipfile
    import shutil
    import xml.dom.minidom as xmlDom
    from xml.etree import ElementTree
    import arcpy
    # ******************************************************************************
    # basicPath= r"F:\Temp"														#**
    #imageFolder = "extract_gf_metadata.in"										#**
    rootFolder = arcpy.GetParameterAsText(0)
    targetRoot = arcpy.GetParameterAsText(1)
    resultMosiac = arcpy.GetParameterAsText(2)
    def printDialog(message):
        arcpy.AddMessage(message)

    #printDialog("开始查找文件夹中的tar.gz文件")

    def getRasterWorldFileInfo(imagePaht):
        arcpy.ExportRasterWorldFile_management(imagePaht)

    #获取xml中用到的值
    def getTagText(xmlFile, tag):
        domTree = xmlDom.parse(xmlFile)
        root = domTree.documentElement
        node = root.getElementsByTagName(tag)[0]
        rc = ""
        for node in node.childNodes:
            if node.nodeType in (node.TEXT_NODE, node.CDATA_SECTION_NODE):
                rc = rc + node.data
        printDialog(rc)
        return rc
    def getImageInfo(imageFullPath):
        # row col bands format pixelType size x-scale y-scale
        raster =arcpy.Raster(imageFullPath)
        rasterInfo=range(0,8)
        rasterInfo[0]=raster.height
        rasterInfo[1]=raster.width
        rasterInfo[2]=raster.bandCount
        rasterInfo[3]=raster.format
        rasterInfo[4]=raster.pixelType
        rasterInfo[5]=raster.uncompressedSize
        rasterInfo[6]=raster.meanCellWidth
        rasterInfo[7]=raster.meanCellHeight
        return rasterInfo
    def getSPOT6PointInfo(xmlFile):
        xmlStruct= ElementTree.parse(xmlFile)
        pointInfo= range(0,8)
        root= xmlStruct.getroot()
        pointsStruct=root.find("Dataset_Content").find("Dataset_Extent")
        points= pointsStruct.findall('Vertex')
        pointInfo[0]=float(points[0].find("LON").text)
        pointInfo[1]=float(points[0].find("LAT").text)
        pointInfo[2]=float(points[1].find("LON").text)
        pointInfo[3]=float(points[1].find("LAT").text)
        pointInfo[4]=float(points[2].find("LON").text)
        pointInfo[5]=float(points[2].find("LAT").text)
        pointInfo[6]=float(points[3].find("LON").text)
        pointInfo[7]=float(points[3].find("LAT").text)
        return pointInfo
    def getSPOT6MSMetaInfo(xmlFile, tarFilePath):
        '''ProductName','Sensor Name','Sensor ID','Acquisition Date','Orbit ID','Sun Elevation'
            ,'Sun Azimuth','Satellite Elevation','Satellite Azimuth','Cloud Cover','OffNadir','Archive Type','Archive Path',
             'Scene Path','Scene Row','GroupName',row, col, bands, format, pixelType, size, sacle '''
        xx = ElementTree.parse(xmlFile)
        metaInfo=range(0,23)
        metaInfo[0]=''
        metaInfo[1]=xx.find("Dataset_Sources").find("Source_Identification").find("SOURCE_DESCRIPTION").text
        metaInfo[2]=xx.find("Dataset_Sources").find("Source_Identification").find("Strip_Source").find("BAND_MODE").text
        metaInfo[3]=(xx.find("Dataset_Sources").find("Source_Identification").find("Strip_Source").find("IMAGING_DATE").text+\
                    " "+xx.find("Dataset_Sources").find("Source_Identification").find("Strip_Source").find("IMAGING_TIME").text).replace("-","/")[0:19]

        metaInfo[4]=""
        metaInfo[5]=float(xx.find("Geometric_Data").find("Use_Area").find("Located_Geometric_Values").find("Solar_Incidences").find("SUN_ELEVATION").text)
        metaInfo[6]=float(xx.find("Geometric_Data").find("Use_Area").find("Located_Geometric_Values").find("Solar_Incidences").find("SUN_AZIMUTH").text)
        metaInfo[7]=None
        metaInfo[8]=None
        metaInfo[9]=None
        metaInfo[10]=xx.find("Geometric_Data").find("Use_Area").find("Located_Geometric_Values").find("Acquisition_Angles").find("VIEWING_ANGLE").text
        metaInfo[11]="Compressed"
        metaInfo[12]=tarFilePath
        metaInfo[13]=None
        metaInfo[14]=None
        metaInfo[15]=""
        metaInfo[16]=float(xx.find("Raster_Data").find("Raster_Dimensions").find("NROWS").text)
        metaInfo[17]=float(xx.find("Raster_Data").find("Raster_Dimensions").find("NCOLS").text)
        metaInfo[18]=float(xx.find("Raster_Data").find("Raster_Dimensions").find("NBANDS").text)
        metaInfo[19]=xx.find("Dataset_Identification").find("DATASET_QL_FORMAT").text
        metaInfo[20]=float(xx.find("Raster_Data").find("Raster_Encoding").find("NBITS").text)
        metaInfo[21]=os.path.getsize(tarFilePath)
        metaInfo[22]= 6
        return metaInfo
    def getSPOT6PMetaInfo(xmlFile, tarFilePath):
        '''ProductName','Sensor Name','Sensor ID','Acquisition Date','Orbit ID','Sun Elevation'
            ,'Sun Azimuth','Satellite Elevation','Satellite Azimuth','Cloud Cover','OffNadir','Archive Type','Archive Path',
             'Scene Path','Scene Row','GroupName',row, col, bands, format, pixelType, size, sacle '''
        xx = ElementTree.parse(xmlFile)
        metaInfo=range(0,23)
        metaInfo[0]=''
        metaInfo[1]=xx.find("Dataset_Sources").find("Source_Identification").find("SOURCE_DESCRIPTION").text
        metaInfo[2]=xx.find("Dataset_Sources").find("Source_Identification").find("Strip_Source").find("BAND_MODE").text
        metaInfo[3]=(xx.find("Dataset_Sources").find("Source_Identification").find("Strip_Source").find("IMAGING_DATE").text+ \
                     " "+xx.find("Dataset_Sources").find("Source_Identification").find("Strip_Source").find("IMAGING_TIME").text).replace("-","/")[0:19]

        metaInfo[4]=""
        metaInfo[5]=float(xx.find("Geometric_Data").find("Use_Area").find("Located_Geometric_Values").find("Solar_Incidences").find("SUN_ELEVATION").text)
        metaInfo[6]=float(xx.find("Geometric_Data").find("Use_Area").find("Located_Geometric_Values").find("Solar_Incidences").find("SUN_AZIMUTH").text)
        metaInfo[7]=None
        metaInfo[8]=None
        metaInfo[9]=None
        metaInfo[10]=xx.find("Geometric_Data").find("Use_Area").find("Located_Geometric_Values").find("Acquisition_Angles").find("VIEWING_ANGLE").text
        metaInfo[11]="Compressed"
        metaInfo[12]=tarFilePath
        metaInfo[13]=None
        metaInfo[14]=None
        metaInfo[15]=""
        metaInfo[16]=float(xx.find("Raster_Data").find("Raster_Dimensions").find("NROWS").text)
        metaInfo[17]=float(xx.find("Raster_Data").find("Raster_Dimensions").find("NCOLS").text)
        metaInfo[18]=float(xx.find("Raster_Data").find("Raster_Dimensions").find("NBANDS").text)
        metaInfo[19]=xx.find("Dataset_Identification").find("DATASET_QL_FORMAT").text
        metaInfo[20]=float(xx.find("Raster_Data").find("Raster_Encoding").find("NBITS").text)
        metaInfo[21]=os.path.getsize(tarFilePath)
        metaInfo[22]= 6
        return metaInfo
    def getGF1PointInfo(xmlFile):
        root= ElementTree.parse(xmlFile)
        pointInfo= range(0,8)
        pointInfo[0]=float(root.find("TopLeftLongitude").text)
        pointInfo[1]=float(root.find("TopLeftLatitude").text)
        pointInfo[2]=float(root.find("TopRightLongitude").text)
        pointInfo[3]=float(root.find("TopRightLatitude").text)
        pointInfo[4]=float(root.find("BottomLeftLongitude").text)
        pointInfo[5]=float(root.find("BottomLeftLatitude").text)
        pointInfo[6]=float(root.find("BottomRightLongitude").text)
        pointInfo[7]=float(root.find("BottomRightLatitude").text)
        return pointInfo
    def getGF1MetaInfo(xmlFile, tarFilePath):
        '''ProductName','Sensor Name','Sensor ID','Acquisition Date','Orbit ID','Sun Elevation'
            ,'Sun Azimuth','Satellite Elevation','Satellite Azimuth','Cloud Cover','OffNadir','Archive Type','Archive Path',
             'Scene Path','Scene Row','GroupName',row col bands format pixelType size sacle '''
        xx = ElementTree.parse(xmlFile)
        metaInfo=range(0,23)
        metaInfo[0]=xx.find("ProductLevel").text
        metaInfo[1]=xx.find("SatelliteID").text
        metaInfo[2]=xx.find("SensorID").text
        metaInfo[3]=xx.find("ReceiveTime").text
        metaInfo[4]=xx.find("OrbitID").text
        metaInfo[5]=xx.find("SolarZenith").text
        metaInfo[6]=xx.find("SolarAzimuth").text
        metaInfo[7]=xx.find("SatelliteAzimuth").text
        metaInfo[8]=xx.find("SatelliteZenith").text
        metaInfo[9]=xx.find("CloudPercent").text
        metaInfo[10]=None
        metaInfo[11]="Compressed"
        metaInfo[12]=tarFilePath
        metaInfo[13]=xx.find("ScenePath").text
        metaInfo[14]=xx.find("SceneRow").text
        metaInfo[15]=""
        metaInfo[16]=xx.find("HeightInPixels").text
        metaInfo[17]=xx.find("WidthInPixels").text
        metaInfo[18]=xx.find("Bands").text
        metaInfo[19]='GEOTIFF'
        metaInfo[20]= xx.find("PixelBits").text
        metaInfo[21]=os.path.getsize(tarFilePath)
        metaInfo[22]= float(xx.find("ImageGSD"))
        return metaInfo
    def getGF2PointInfo(xmlFile):
        root= ElementTree.parse(xmlFile)
        pointInfo= range(0,8)
        pointInfo[0]=float(root.find("TopLeftLongitude").text)
        pointInfo[1]=float(root.find("TopLeftLatitude").text)
        pointInfo[2]=float(root.find("TopRightLongitude").text)
        pointInfo[3]=float(root.find("TopRightLatitude").text)
        pointInfo[4]=float(root.find("BottomLeftLongitude").text)
        pointInfo[5]=float(root.find("BottomLeftLatitude").text)
        pointInfo[6]=float(root.find("BottomRightLongitude").text)
        pointInfo[7]=float(root.find("BottomRightLatitude").text)
        return pointInfo
    def getGF2MetaInfo(xmlFile, tarFilePath):
        '''ProductName','Sensor Name','Sensor ID','Acquisition Date','Orbit ID','Sun Elevation'
            ,'Sun Azimuth','Satellite Elevation','Satellite Azimuth','Cloud Cover','OffNadir','Archive Type','Archive Path',
             'Scene Path','Scene Row','GroupName',row col bands format pixelType size sacle '''
        xx = ElementTree.parse(xmlFile)
        metaInfo=range(0,23)
        metaInfo[0]=xx.find("ProductLevel").text
        metaInfo[1]=xx.find("SatelliteID").text
        metaInfo[2]=xx.find("SensorID").text
        metaInfo[3]=xx.find("ReceiveTime").text
        metaInfo[4]=xx.find("OrbitID").text
        metaInfo[5]=xx.find("SolarZenith").text
        metaInfo[6]=xx.find("SolarAzimuth").text
        metaInfo[7]=xx.find("SatelliteAzimuth").text
        metaInfo[8]=xx.find("SatelliteZenith").text
        metaInfo[9]=xx.find("CloudPercent").text
        metaInfo[10]=None
        metaInfo[11]="Compressed"
        metaInfo[12]=tarFilePath
        metaInfo[13]=xx.find("ScenePath").text
        metaInfo[14]=xx.find("SceneRow").text
        metaInfo[15]=""
        metaInfo[16]=xx.find("HeightInPixels").text
        metaInfo[17]=xx.find("WidthInPixels").text
        metaInfo[18]=xx.find("Bands").text
        metaInfo[19]='GEOTIFF'
        metaInfo[20]= xx.find("PixelBits").text
        metaInfo[21]=os.path.getsize(tarFilePath)
        metaInfo[22]= float(xx.find("ImageGSD").text)
        return metaInfo
    def getZY3PointInfo(xmlFile):
        root = ElementTree.parse(xmlFile)
        xx=root.find("productInfo").find("ProductGeographicRange")
        LeftTopPoint=xx.find("LeftTopPoint")
        RightTopPoint=xx.find("RightTopPoint")
        LeftBottomPoint=xx.find("LeftBottomPoint")
        RightBottomPoint=xx.find("RightBottomPoint")
        ponitInfo=range(0,8)
        ponitInfo[0]=float(LeftTopPoint.find("Longtitude").text)
        ponitInfo[1]=float(LeftTopPoint.find("Latitude").text)
        ponitInfo[2]=float(RightTopPoint.find("Longtitude").text)
        ponitInfo[3]=float(RightTopPoint.find("Latitude").text)
        ponitInfo[4]=float(LeftBottomPoint.find("Longtitude").text)
        ponitInfo[5]=float(LeftBottomPoint.find("Latitude").text)
        ponitInfo[6]=float(RightBottomPoint.find("Longtitude").text)
        ponitInfo[7]=float(RightBottomPoint.find("Latitude").text)
        return ponitInfo
    def getZY3MetaInfo(xmlFile,tarFilePath):
        root = ElementTree.parse(xmlFile)
        xx=root.find("productInfo")
        '''ProductName','Sensor Name','Sensor ID','Acquisition Date','Orbit ID','Sun Elevation'
            ,'Sun Azimuth','Satellite Elevation','Satellite Azimuth','Cloud Cover','OffNadir','Archive Type','Archive Path',
             'Scene Path','Scene Row','GroupName',row col bands format pixelType size sacle '''
        metaInfo=range(0,23)
        metaInfo[0]=xx.find("ProductLevel").text
        metaInfo[1]=xx.find("SatelliteID").text
        metaInfo[2]=xx.find("SensorID").text
        metaInfo[3]=xx.find("AcquisitionTime").text
        metaInfo[4]=xx.find("OrbitID").text
        metaInfo[5]=xx.find("SunAltitude").text
        metaInfo[6]=xx.find("SunAzimuth").text
        metaInfo[7]=xx.find("SatAltitude").text
        metaInfo[8]=xx.find("SatAzimuth").text
        metaInfo[9]=xx.find("CloudPercent").text
        metaInfo[10]= None
        metaInfo[11]="Compressed"
        metaInfo[12]=tarFilePath
        metaInfo[13]=xx.find("ScenePath").text
        metaInfo[14]=xx.find("SceneRow").text
        metaInfo[15]=""
        metaInfo[16]=xx.find("HeightInPixels").text
        metaInfo[17]=xx.find("WidthInPixels").text
        metaInfo[18]=xx.find("Bands").text
        metaInfo[19]='GEOTIFF'
        metaInfo[20]=xx.find("PixelByte").text
        metaInfo[21]=os.path.getsize(tarFilePath)
        metaInfo[22]=(float(xx.find("ImageGSD").find("Line").text)+float(xx.find("ImageGSD").find("Sample").text))/2.0
        return metaInfo
    def getZY02CPointInfo(xmlFile):
        root = ElementTree.parse(xmlFile)
        ponitInfo=range(0,8)
        ponitInfo[0]=float(root.find("TopLeftLongitude").text)
        ponitInfo[1]=float(root.find("TopLeftLatitude").text)
        ponitInfo[2]=float(root.find("TopRightLongitude").text)
        ponitInfo[3]=float(root.find("TopRightLatitude").text)
        ponitInfo[4]=float(root.find("BottomLeftLongitude").text)
        ponitInfo[5]=float(root.find("BottomLeftLatitude").text)
        ponitInfo[6]=float(root.find("BottomRightLongitude").text)
        ponitInfo[7]=float(root.find("BottomRightLatitude").text)
        return ponitInfo
    def getZY02CMetaInfo(xmlFile,tarFilePath):
        xx = ElementTree.parse(xmlFile)
        '''ProductName','Sensor Name','Sensor ID','Acquisition Date','Orbit ID','Sun Elevation'
            ,'Sun Azimuth','Satellite Elevation','Satellite Azimuth','Cloud Cover','OffNadir','Archive Type','Archive Path',
             'Scene Path','Scene Row','GroupName'''
        metaInfo=range(0,23)
        metaInfo[0]=xx.find("ProductLevel").text
        metaInfo[1]=xx.find("SatelliteID").text
        metaInfo[2]=xx.find("SensorID").text
        metaInfo[3]=xx.find("ReceiveTime").text
        metaInfo[4]=xx.find("OrbitID").text
        metaInfo[5]=xx.find("SolarZenith").text
        metaInfo[6]=xx.find("SolarAzimuth").text
        metaInfo[7]=xx.find("SatelliteZenith").text
        metaInfo[8]=xx.find("SatelliteAzimuth").text
        metaInfo[9]=xx.find("CloudPercent").text
        metaInfo[10]=None
        metaInfo[11]="Compressed"
        metaInfo[12]=tarFilePath
        metaInfo[13]=xx.find("ScenePath").text
        metaInfo[14]=xx.find("SceneRow").text
        metaInfo[15]=""
        metaInfo[16]=xx.find("HeightInPixels").text
        metaInfo[17]=xx.find("WidthInPixels").text
        metaInfo[18]=xx.find("Bands").text
        metaInfo[19]='GEOTIFF'
        metaInfo[20]=xx.find("PixelBits").text
        metaInfo[21]=os.path.getsize(tarFilePath)
        metaInfo[22]=xx.find("ImageGSD").text
        return metaInfo
    def calculateJPW(topLeftLon,topLeftLat,topRightLon,topRightLat,bottowLeftLon,bottowLeftLat,bottowRightLon,bottowRightLat,jpgWidth,jpgHight,jpwFullPath):
        A=(topRightLon-topLeftLon)/jpgWidth
        E=-(topLeftLat-bottowLeftLat)/jpgHight
        D=(topRightLat-topLeftLat)/jpgWidth
        B=(bottowLeftLon-topLeftLon)/jpgHight
        file_object=open(jpwFullPath, 'w')
        data=[str(A)+"\n",str(D)+"\n",str(B)+"\n",str(E)+"\n",str(topLeftLon)+"\n",str(topLeftLat)]
        file_object.writelines(data)
        file_object.flush()
        file_object.close()
        #移动文件并删除文件夹
    def addJPG2Mosaic(jpgPath,metaInfo):
        arcpy.AddRastersToMosaicDataset_management(resultMosiac, "Raster Dataset", jpgPath, "UPDATE_CELL_SIZES", "UPDATE_BOUNDARY", "NO_OVERVIEWS", "", "0", "1500", "", "", "SUBFOLDERS", "ALLOW_DUPLICATES", "NO_PYRAMIDS", "CALCULATE_STATISTICS", "NO_THUMBNAILS", "", "NO_FORCE_SPATIAL_REFERENCE")
        fieldStatistics = ('ProductName','SensorName','SensorID','AcquisitionDate','OrbitID','SunElevation','SunAzimuth','SatelliteElevation','SatelliteAzimuth','CloudCover','OffNadir','ArchiveType','ArchivePath','ScenePath','SceneRow','GroupName','Row','Col','BandCount','DataFormat','PixelType','ImageSize','PixelSize')
        #fieldStatistics = ('ProductName')
        queryStr = "Name='"+os.path.basename(jpgPath)[:-4]+"'"
        arcpy.AddMessage(queryStr)
        with arcpy.da.UpdateCursor(resultMosiac, fieldStatistics,queryStr) as cursor:
            row = cursor.next()
            for i in range(0,23):
                row[i]=metaInfo[i]
            cursor.updateRow(row)
    #path=folder+preName
    def doALL(path,tarFilePath,xmlName,jpgName,jpwName,pointFunc,metaFunc):
        pointInfo=pointFunc(path+xmlName)
        img = arcpy.Raster(path+jpgName)
        jpgWidth=img.width
        jpgHight=img.height
        calculateJPW(pointInfo[0],pointInfo[1],pointInfo[2],pointInfo[3],pointInfo[4],pointInfo[5],pointInfo[6],pointInfo[7],jpgWidth,jpgHight,path+jpwName)
        addJPG2Mosaic(path+jpgName,metaFunc(path+xmlName,tarFilePath))
    def moveFileDeleteFolders(currentPath, targetPath):  #currentPath===targetPath在此项目中相等
        #拷贝数据到根目录
        for p, dirn, fn in os.walk(currentPath):
            if fn:
                for f in fn:
                    filepath = os.path.join(p, f)
                    shutil.copy(filepath, targetPath)
        #删除根目录下的文件夹
        for parent, dirnames, filename in os.walk(targetPath):
            for dirname in dirnames:
                if os.path.isdir(os.path.join(parent, dirname)):
                    shutil.rmtree(os.path.join(parent, dirname))

    #根据后缀名删除文件删除rootFolder文件夹下的.rpb、.tiff、.tiff.xml文件
    #@param: args, array   ex:[".rpb"、".tiff"、".tiff.xml"]
    #@param root string  ex: r"D:\your\path"
    def deleteFilesByExtention(args, root):
        for parent, dirnames, filenames in os.walk(root):
            for filename in filenames:
                for arg in args:
                    if arg in filename:
                        deleteFilePath = os.path.join(root, filename)
                        os.remove(deleteFilePath)
    for parent, dirnames, filenames in os.walk(rootFolder):
        for filename in filenames:
            #tarPath = os.path.join(rootFolder, filename+ os.sep+ filename)
            packagePath = os.path.join(parent, filename)
            jpgFilePath = ""
            jpgFileName = ""

            #根据高分系列处理一号和二号类型
            if "GF2" in filename:
                unTarFolderName = filename[0:-7]
                unTarFolderPath = targetRoot + os.sep + "GF2" + os.sep + unTarFolderName
                isMatch= False
                try:
                    with tarfile.TarFile.open(packagePath, 'r') as tars:
                        for tarInfo in tars:
                            isMatch= True
                            if "MSS1.xml" in tarInfo.name:
                                data = tarInfo.name
                                tars.extract(tarInfo, unTarFolderPath)
                            if "MSS1.jpg" in tarInfo.name:
                                tars.extract(tarInfo, unTarFolderPath)
                                jpgFileName = tarInfo.name
                            if "PAN1.xml" in tarInfo.name:
                                data = tarInfo.name
                                tars.extract(tarInfo, unTarFolderPath)
                            if "PAN1.jpg" in tarInfo.name:
                                tars.extract(tarInfo, unTarFolderPath)
                                jpgFileName = tarInfo.name
                except Exception, e:
                    printDialog(e)
                deleteFilesByExtention([".rpb", ".tiff", ".aux.xml"], unTarFolderPath)
                if isMatch:
                    #MSS1
                    doALL(unTarFolderPath+os.sep+unTarFolderName,packagePath,"-MSS1.xml","-MSS1.jpg","-MSS1.jpw",getGF2PointInfo,getGF2MetaInfo)
                    #PAN1
                    doALL(unTarFolderPath+os.sep+unTarFolderName,packagePath,"-PAN1.xml","-PAN1.jpg","-PAN1.jpw",getGF2PointInfo,getGF2MetaInfo)
            if "GF1" in filename:
                unTarFolderName = filename[0:-7]
                unTarFolderPath = targetRoot + os.sep + "GF1" + os.sep + unTarFolderName
                isMatch= False
                try:
                    with tarfile.TarFile.open(packagePath, 'r') as tars:
                        for tarInfo in tars:
                            isMatch= True
                            if "MSS2.xml" in tarInfo.name:
                                data = tarInfo.name
                                tars.extract(tarInfo, unTarFolderPath)
                                xmlFilePath = os.path.join(unTarFolderPath, tarInfo.name)
                            if "MSS2.jpg" in tarInfo.name:
                                tars.extract(tarInfo, unTarFolderPath)
                                jpgFileName = tarInfo.name
                            if "PAN2.xml" in tarInfo.name:
                                data = tarInfo.name
                                tars.extract(tarInfo, unTarFolderPath)
                                xmlFilePath = os.path.join(unTarFolderPath, tarInfo.name)
                            if "PAN2.jpg" in tarInfo.name:
                                tars.extract(tarInfo, unTarFolderPath)
                                jpgFileName = tarInfo.name
                except Exception, e:
                    printDialog(e)
                deleteFilesByExtention([".rpb", ".tiff"], unTarFolderPath)
                if isMatch:
                    #MSS2
                    doALL(unTarFolderPath+os.sep+unTarFolderName,packagePath,"-MSS2.xml","-MSS2.jpg","-MSS2.jpw",getGF2PointInfo,getGF2MetaInfo)
                    #PAN2
                    doALL(unTarFolderPath+os.sep+unTarFolderName,packagePath,"-PAN2.xml","-PAN2.jpg","-PAN2.jpw",getGF2PointInfo,getGF2MetaInfo)
            if "SPOT6" in filename:
                printDialog(u"正在处理" + filename + u"数据")
                unTarFolderName = filename[0:-4]
                unTarFolderPath = targetRoot + os.sep + "SPOT6" + os.sep + unTarFolderName
                zipFileName = ""
                isMatch= False
                try:
                    with zipfile.ZipFile(packagePath, "r") as zips:
                        for zipfile in zips.filelist:
                            isMatch=True
                            zipFileName = zipfile.filename
                            if "SPOT6_MS" in zipFileName:
                                printDialog(u"处理全色影像" + zipFileName)
                                #DIM_SPOT6_MS_201501250304475_SEN_1311812101
                                if "DIM_SPOT6_MS" in zipFileName:
                                    printDialog(u"正在解压" + zipFileName + u"文件")
                                    zips.extract(zipFileName, unTarFolderPath)

                                #PREVIEW_SPOT6_MS_201501250304475_SEN_1311812101.JPG
                                if "PREVIEW_SPOT6_MS" in zipFileName and ".JPG" in zipFileName:
                                    printDialog(u"正在解压" + zipFileName + u"文件")
                                    zips.extract(zipFileName, unTarFolderPath)
                                #IMG_SPOT6_MS_201501250304475_SEN_1311812101_R1C1.J2W
                                # if "SPOT6_MS" in zipFileName and ".J2W" in zipFileName:
                                #     printDialog(u"正在解压" + zipFileName + u"文件")
                                #     zips.extract(zipFileName, unTarFolderPath)
                                # msFolderPath= os.path.join(parent+ os.sep+ dirnames, zipfile.filename)
                                # moveFileDeleteFolders(msFolderPath, unTarFolderPath)
                            #处理全色影像
                            if "SPOT6_P" in zipFileName:
                                printDialog(u"处理全色影像" + zipFileName)
                                pJPG = ""
                                if "DIM_SPOT6_P" in zipFileName:
                                    printDialog(u"正在解压" + zipFileName + u"文件")
                                    zips.extract(zipFileName, unTarFolderPath)
                                if "PREVIEW_SPOT6_P" in zipFileName and ".JPG" in zipFileName:
                                    printDialog(u"正在解压" + zipFileName + u"文件")
                                    zips.extract(zipFileName, unTarFolderPath)
                                    pJPG = zipFileName
                                # if "SPOT6_P" in zipFileName and ".J2W" in zipFileName:
                                #     printDialog(u"正在解压" + zipFileName + u"文件")
                                #     zips.extract(zipFileName, unTarFolderPath)
                                #改名坐标文件
                                # J2WOriginaName= os.path.join(unTarFolderPath, zipFileName.name[0:-3]+"J2W")
                                # J2WTargetName= J2WOriginaName[0:-9]+"MSS2.jgw"
                                # MSSJpgwFile= os.rename(panTfwxOriginaName, MSSJpgwFileName)

                except Exception, e:
                    printDialog(e)
                #zipExtractPath = zipFileName[0:-3]
                moveFileDeleteFolders(unTarFolderPath, unTarFolderPath)
                if isMatch:
                    spot6UntarFolderPath= os.path.join(targetRoot, "SPOT6"+os.sep+ unTarFolderName)
                    for pa, dirs, fns in os.walk(spot6UntarFolderPath):
                        for fn in fns:
                            if "PREVIEW_SPOT6_MS" in fn and "JPG" in fn:
                                xmlFilePath=os.path.join(targetRoot,"SPOT6"+os.sep+ unTarFolderName+os.sep+ "DIM"+fn[7:-3]+"XML")
                                printDialog(xmlFilePath)
                                pointInfo= getSPOT6PointInfo(xmlFilePath)
                                img =arcpy.Raster(unTarFolderPath+ os.sep+fn)
                                jpgWidth=img.width
                                jpgHight=img.height
                                calculateJPW(pointInfo[0],pointInfo[1],pointInfo[2],pointInfo[3],pointInfo[4],pointInfo[5],pointInfo[6],pointInfo[7],jpgWidth,jpgHight,unTarFolderPath+os.sep+"PREVIEW"+fn[7:-3]+"jpw")
                                addJPG2Mosaic(unTarFolderPath+ os.sep+fn,getSPOT6MSMetaInfo(xmlFilePath,packagePath))
                            elif "PREVIEW_SPOT6_P" in fn and "JPG" in fn:
                                xxmlFilePath=os.path.join(targetRoot,"SPOT6"+os.sep+ unTarFolderName+os.sep+ "DIM"+fn[7:-3]+"XML")
                                printDialog(xmlFilePath)
                                pointInfo= getSPOT6PointInfo(xmlFilePath)
                                img = arcpy.Raster(unTarFolderPath+ os.sep+fn)
                                jpgWidth=img.width
                                jpgHight=img.height
                                calculateJPW(pointInfo[0],pointInfo[1],pointInfo[2],pointInfo[3],pointInfo[4],pointInfo[5],pointInfo[6],pointInfo[7],jpgWidth,jpgHight,unTarFolderPath+os.sep+"PREVIEW"+fn[7:-3]+"jpw")
                                addJPG2Mosaic(unTarFolderPath+ os.sep+fn,getSPOT6PMetaInfo(xmlFilePath,packagePath))
                            else:
                                printDialog(u"xml文件处理！！")
            if "ZY02C" in filename:
                unTarFolderName = filename[0:-7]
                unTarFolderPath = targetRoot + os.sep + "ZY02C" + os.sep + unTarFolderName
                isMatch=False
                try:
                    with tarfile.TarFile.open(packagePath, 'r') as tars:
                        for tarInfo in tars:
                            isMatch=True
                            if "HRC" in tarInfo.name:
                                if unTarFolderName+".xml" == tarInfo.name:
                                    data = tarInfo.name
                                    tars.extract(tarInfo, unTarFolderPath)
                                if unTarFolderName+".jpg" == tarInfo.name:
                                    tars.extract(tarInfo, unTarFolderPath)
                                    jpgFileName = tarInfo.name
                            if "PMS" in tarInfo.name:
                                if "MUX" in tarInfo.name:
                                    if unTarFolderName+"-MUX.xml" == tarInfo.name:
                                        data = tarInfo.name
                                        tars.extract(tarInfo, unTarFolderPath)
                                    if unTarFolderName+"-MUX.jpg" == tarInfo.name:
                                        tars.extract(tarInfo, unTarFolderPath)
                                        jpgFileName = tarInfo.name
                                if "PAN" in tarInfo.name:
                                    if unTarFolderName+"-PAN.xml" == tarInfo.name:
                                        data = tarInfo.name
                                        tars.extract(tarInfo, unTarFolderPath)
                                    if unTarFolderName+"-PAN.jpg" == tarInfo.name:
                                        tars.extract(tarInfo, unTarFolderPath)
                                        jpgFileName = tarInfo.name
                except Exception, e:
                    printDialog(e)
                if isMatch:
                    if "HRC" in unTarFolderName:
                        doALL(unTarFolderPath+os.sep+unTarFolderName,packagePath,".xml",".jpg",".jpw",getZY02CPointInfo,getZY02CMetaInfo)
                    elif "PMS" in unTarFolderName:
                        doALL(unTarFolderPath+os.sep+unTarFolderName,packagePath,"-MUX.xml",".-MUXjpg","-MUX.jpw",getZY02CPointInfo,getZY02CMetaInfo)
                    else:
                        printDialog(u"资源系列未知类型！！")
            if "zy3" in filename:
                unTarFolderName = filename[0:-4]
                unTarFolderPath = targetRoot + os.sep + "ZY3" + os.sep + unTarFolderName
                isMatch=False
                try:
                    with tarfile.TarFile.open(packagePath, 'r') as tars:
                        for tarInfo in tars:
                            isMatch=True
                            ##############################zy3###################################
                            if unTarFolderName+".xml" == tarInfo.name:
                                tars.extract(tarInfo, unTarFolderPath)
                            if "pre.jpg" in tarInfo.name:
                                tars.extract(tarInfo, unTarFolderPath)

                except Exception, e:
                    printDialog(e)
                if isMatch:
                    doALL(unTarFolderPath+os.sep+unTarFolderName,packagePath,".xml","_pre.jpg","_pre.jpw",getZY3PointInfo,getZY3MetaInfo)
    print(u"finshed")