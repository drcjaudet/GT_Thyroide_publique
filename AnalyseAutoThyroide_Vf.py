
from math import *
#import numpy as np
import SimpleITK as sitk
import time
import pydicom
import os

def impression(img_metadata, f , Stat_vector,activite, volume_fantome,firsttime,Treshold_vector,image,nomdufichier ):
        ##############ecriture de la premiere ligne################
    if firsttime==0: #write for the first time all the description value
        ############écriture de la premiére ligne
        f.write(str("Nom_Fichier_DICOM;PatientName;PatientID;StudyDate (YYMMDD);AcquisitionDate (YYMMDD);AcquisitionTime (hhmmss);Modality;SeriesDescription;ManufacturerModelName;ProtocolName;PixelSpacing (mm);Table Height;Table Traverse;taille Matrice X;taille Matrice Y;ActualFrameDuration (s);Acquisition time (s);Counts Accumulated"))
        f.write(str(";Energie window name;Energie(KeV);Collimateur Type;Collimateur Name" )) #modification 12/11/2021
        f.write(str(";Volume Theorique (ml);activite theorique (MBq)")) 
        for Nseuil in range(len(Treshold_vector)):
            VS="_"+str(Treshold_vector[Nseuil])+"%"
            f.write(str("; Seuil(% max)"+VS))
            f.write(str(";region"+VS+";Min (kCps)_F"+VS+";Max(kCps)_F"+VS+";mean(kCps)_F"+VS+";median(kCps)_F"+VS+";Coups Totaux(kCps)_F"+VS+";Nombre de Pixel_F"+VS+";CV(%)_F"+VS+";Rcentre de gravite(mm)_F"+VS+";surface(mm^2)_F"+VS))  
            f.write(str(";sensibilite (Cps/(MBq.s))"+VS))
        f.write(str("; SAM (kCps)"))
        f.write(str(";sensibilite SAM (Cps/(MBq.s)))"))
        f.write("\n")
    ###ecriture des metada pour correspondant au patient###
    try:
        f.write(str(nomdufichier)+";")
    except:
        f.write("NA"+";")
    try:
        f.write(str(img_metadata.PatientName)+";")
    except:
        f.write("NA"+";")
    try:    
        f.write(str(img_metadata.PatientID)+";")
    except:
        f.write("NA"+";")   
    try:    
        f.write(str(img_metadata.StudyDate)+";")
    except:
        f.write("NA"+";") 
    try:    
        f.write(str(img_metadata.AcquisitionDate)+";")
    except:
        f.write("NA"+";") 
    try:    
        f.write(str(img_metadata.AcquisitionTime)+";")
    except:
        f.write("NA"+";")   
    try:
        f.write(str( img_metadata.Modality)+";")
    except:
        f.write("NA"+";")
    try:
        f.write(str(img_metadata.SeriesDescription)+";")
    except:
        f.write("NA"+";")
    try:
        f.write(str(img_metadata.ManufacturerModelName)+";")
    except:
        f.write("NA"+";")  
    try:
        f.write(str(img_metadata.ProtocolName)+";")
    except:
        f.write("NA"+";")
    try:
        f.write(str(img_metadata.PixelSpacing)+";")
    except:
        f.write("NA"+";")
    try:
        f.write(str(img_metadata.TableHeight)+";")
    except:
        f.write("NA"+";")
    try:
        f.write(str(img_metadata.TableTraverse)+";")
    except:
        f.write("NA"+";")
    try:
        f.write(str(img_metadata.Columns)+";")
    except:
        f.write("NA"+";")
    try:
        f.write(str(img_metadata.Rows)+";")
    except:
        f.write("NA"+";")
    try:
        DureeAcquisition=img_metadata.ActualFrameDuration/(1000)
        f.write(str(DureeAcquisition)+";")
    except:
        f.write("NA"+";")
    try:
        #DebutAcquisitionEnS=getSec(img_metadata.AcquisitionTime)
        DebutAcquisitionEnS=img_metadata.AcquisitionTime
        f.write(str(DebutAcquisitionEnS)+";")
    except:
        f.write("NA"+";")
    try:       
        f.write(str(img_metadata.CountsAccumulated)+";")
    except:
        f.write("NA"+";")
    try:       
        f.write(str(img_metadata.EnergyWindowInformationSequence[0].EnergyWindowName)+";") #Code Meaning?
    except:
        f.write("NA"+";")
    try:       
        f.write(str((img_metadata.EnergyWindowInformationSequence[0].EnergyWindowRangeSequence[0].EnergyWindowLowerLimit+img_metadata.EnergyWindowInformationSequence[0].EnergyWindowRangeSequence[0].EnergyWindowUpperLimit)/2)+";")
    except:
        f.write("NA"+";")
    try:       
        f.write(str((img_metadata.DetectorInformationSequence[0].CollimatorType))+";")   #Collimator/grid Name ,Collimator Type
    except:
        f.write("NA"+";")
    try:       
        f.write(str((img_metadata.DetectorInformationSequence[0].CollimatorGridName))+";")
    except:
        f.write("NA"+";")
    ###Analyse### 
    f.write(str(volume_fantome))
    f.write(';')
    f.write(str(activite))
    for iteration in range(len(Stat_vector)):        
        stat_filter=Stat_vector[iteration]
        f.write(';') 
        f.write(str(Treshold_vector[iteration]))
        f.write(';')     
        f.write("Fantome thyroide")
        f.write(';')
        f.write(str(stat_filter.GetMinimum(1)/1000)) #/1000 pour être en kCps
        f.write(';')
        f.write(str(stat_filter.GetMaximum(1)/1000))
        f.write(';')
        f.write(str(stat_filter.GetMean(1)/1000))
        f.write(';')
        f.write(str(stat_filter.GetMedian(1)/1000))
        f.write(';')
        f.write(str(stat_filter.GetSum(1)/1000))
        f.write(';')
        f.write(str(stat_filter.GetNumberOfPixels(1)))
        f.write(';')
        try: 
            f.write(str(stat_filter.GetStandardDeviation(1)/stat_filter.GetMean(1)))
        except:
            f.write("NA")
        f.write(';')
        Coorcentre=stat_filter.GetCenterOfGravity(1)
        R=sqrt( Coorcentre[0]**2+ Coorcentre[1]**2)
        f.write(str(R))
        f.write(';')
        f.write(str(stat_filter.GetPhysicalSize(1)))
        f.write(';')
        try:     
            f.write(str(  (stat_filter.GetSum(1))/((DoseAuMomentMesure*1000)*(DureeAcquisition/60))   ))
        except:
            f.write("NA")
    #rajoute SAM
    RS=[5,5] #résolution pour la dilatation en mm
    f.write(';')
    try:  
        f.write(str(SAM(image,RS)/1000))
    except:
        f.write("NA")
    f.write("\n")
    print("     Analyse:ok")                  

def SAM(image,RS):
    labelmap = sitk.OtsuThreshold(image,0,1)
    #verification que la dilatation ne sorte pas de l'image
    stats= sitk.LabelIntensityStatisticsImageFilter()
    stats.Execute(labelmap,image)
    MinNVoxel=min(stats.GetBoundingBox(1)[0],stats.GetBoundingBox(1)[1],stats.GetBoundingBox(1)[2],stats.GetBoundingBox(1)[3])
    PorteEVP=int(max(RS)*3/min(image.GetSpacing()))
    if (MinNVoxel-3)<PorteEVP:
        PorteEVP=MinNVoxel-3
    ########verif place pour la dilatation+mesure de fond
    for i in range(PorteEVP):
        labelmap=sitk.BinaryDilate(labelmap)
    #####################creation d'un label avec le fond  label=2) et le volume ideal (label=1)
    label_fond=labelmap
    for i in range(3): ####crérer un donut 3fois plus grand
         label_fond=sitk.BinaryDilate(label_fond)
    label_fond=(label_fond-labelmap)*2
    labelmap=labelmap+label_fond
    #su.PushVolumeToSlicer(labelmap,name="label",className='vtkMRMLLabelMapVolumeNode')
    #su.PushVolumeToSlicer(label_fond,name="fond_label",className='vtkMRMLLabelMapVolumeNode')
        ###########netoyage si SUV >2.5 fois mean region?        
    stats= sitk.LabelIntensityStatisticsImageFilter()
    stats.Execute(labelmap,image)
    SAM_value=stats.GetSum(1)-(stats.GetNumberOfPixels(1)*stats.GetMean(2))  ####attention pas sure du mean et number of pixels?
    return SAM_value


def main_image_Traitement(image,img_metadata,f,firsttime,Treshold_vector,nomdufichier):
    #Choix en function du nom de la serie  de l'activité utilisé et du volume du phantome correspondant:
    NomDeLaSerie=str(img_metadata.PatientName)
    activite="a rentrer"
    volume_fantome="a determiner"
    ########################recentrer l'image sur zero
    Size=image.GetSize()
    Spacing=image.GetSpacing() 
    if len(Size)>3.0: #########enléve la 4eme dimension
        EF=sitk.ExtractImageFilter()        
        EF.SetSize([Size[0],Size[1],Size[2],0])
        EF.SetIndex([0,0,0,0])
        image=EF.Execute(image) 
    labelOtsu = sitk.OtsuThreshold(image,0,1)
    stats= sitk.LabelIntensityStatisticsImageFilter()
    stats.Execute(labelOtsu,image)
    maxImage=stats.GetMaximum(1)
    coord_Max=stats.GetMaximumIndex(1)
    if Size[2]>1.0:  ########## si plusieur images 3d selectionne la plus intense
        EF=sitk.ExtractImageFilter()        
        EF.SetSize([Size[0],Size[1],1])
        EF.SetIndex([0,0,coord_Max[2]])
        image=EF.Execute(image)
        #su.PushToSlicer(image,"etape3",1)   
    #transformation image en 2D#######
    Size=image.GetSize()
    EF=sitk.ExtractImageFilter()
    if (Size[0]<Size[1]) and (Size[0]<Size[2]):
        EF.SetSize([0,Size[1],Size[2]])
    elif (Size[0]>Size[1]) and (Size[1]<Size[2]):
        EF.SetSize([Size[0],0,Size[2]])
    else:
        EF.SetSize([Size[0],Size[1],0])   
    EF.SetIndex([0,0,0])
    image2D=EF.Execute(image)
    image2D=sitk.Cast(image2D, sitk.sitkFloat64)
    image=image2D
    ##########################################
    ##################deconvolution et debruitage
    RS=[5,5] #résolution spatiale en mm
    Stat_vector=[]
    for iteration in range(len(Treshold_vector)):
        threshold=Treshold_vector[iteration]      
        ###########segmenter a partir d'un seuil fixe 
        labelmap=sitk.BinaryThreshold(image, threshold/100*maxImage , int(maxImage)+1 , int(1),int(0) ) #attention 
        #####################analyse des donnees
        stat_filter = sitk.LabelIntensityStatisticsImageFilter()
        stat_filter.Execute(labelmap,image)
        Stat_vector.append(stat_filter)
    #####################analyse et ecrituredans le fichier 
    impression(img_metadata, f , Stat_vector,activite, volume_fantome,firsttime,Treshold_vector,image,nomdufichier )


def main(data_directory, adresse_save_result, Treshold_vector):
    timeInit = time.time()
    Nimageouverte=0
    Nimagetraitees=0
    firsttime=0 #for printing the radiomics key on the first line
    f = open(adresse_save_result, 'w') #open the file for saving result
   ########################################iterate trough subfolder##############
    directory_list=[]
    i=0 #number of sub folder
    for root, dirs, files in os.walk(data_directory):
        for subdirname in dirs:
            directory_list.append(os.path.join(root,subdirname))
    #print(data_directory)
    #print(directory_list)
    ################################partie principale du code
    for i in range(len(directory_list)):
        data_directory=directory_list[i].replace('\\','/')
        series_IDs = sitk.ImageSeriesReader.GetGDCMSeriesIDs(data_directory)
        if not series_IDs:
            print("ERROR: given directory \""+data_directory+"\" does not contain a DICOM series.")
            #sys.exit(1)
        else:
            for i,series_ID in enumerate(series_IDs):   
                Nimageouverte=Nimageouverte+1
                series_file_names = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(data_directory, series_ID,useSeriesDetails=False) #useSeriesDetails ?
                try:
                    img_metadata=pydicom.dcmread(series_file_names[0])
                    #importation des metadata lié à l'image
                    #print(img.GetSpacing())
                    #print(img.GetSize())
                    if img_metadata.Modality=='NM': #and img_metadata.SeriesDescription=="[DetailWB_CTAC_2i-10s-PSF] Body": #"PET TAP AC HD (AC)": #"[DetailWB_CTAC_2i-10s-PSF] Body"
                    #if 1==1: #"PET TAP AC HD (AC)": #"[DetailWB_CTAC_2i-10s-PSF] Body"
                        print(series_file_names)
                        try:
                            timeRMR1 = time.time()
                            Nimagetraitees=Nimagetraitees+1
                            series_reader = sitk.ImageSeriesReader()
                            series_reader.SetFileNames(series_file_names)
                            nomdufichier=series_file_names[0].split('/')[-1] #selectionne le nom du fichier
                            nomdufichier=nomdufichier.split('.')[0] #enleve l'extension: dcm, nrrd...
                            img = series_reader.Execute()  #importation de l'image           
                            #img= sitk.Cast(img, sitk.sitkFloat64)
                            #su.PushToSlicer(img, "image_"+series_ID,1) #test de rapatriement
                            main_image_Traitement(img,img_metadata,f,firsttime, Treshold_vector,nomdufichier)
                            firsttime=1 #just write the first ligne one time
                            timeRMR2 = time.time()
                            TimeForrunFunctionRMR2 = timeRMR2 - timeRMR1
                            print(u"La fonction de traitement s'est executée en " + str(TimeForrunFunctionRMR2) +" secondes")
                            print("\n")
                        except RuntimeError:
                            print ("--> Probleme avec l'importation et/ou le triatement d'image")
                except RuntimeError:
                    print ("--> Probleme avec la lecture des metadata")
    if firsttime!=0:
        f.close()
    print("\n")
    print("Nombre d'image total lue:"+str(Nimageouverte)+"\n")
    print("Nombre d'image total traité:"+str(Nimagetraitees)+"\n" )
    timefinal = time.time()
    TimeTotal = timefinal - timeInit
    print(u"Le traitement de l'ensemble des données c'est executée en " + str(TimeTotal) +" secondes")

##################################Execution du code############################################
############################################################################################### 

Treshold_vector=[5,10,15,20,25,30,35,40] # Seuil en % du max a tester

data_directory="Adresse fichier à analyser"
adresse_save_result="adresse fichier d'analyse a sauver.csv"

main(data_directory, adresse_save_result,Treshold_vector)




