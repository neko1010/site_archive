import xml.etree.ElementTree as ET
import os
import sys
import shutil
from datetime import datetime
import csv

def gw_data(filepath):
    """
    Gathering gage numbers and states for GW sites
    """
    gw_ID = []
    gw_state = []
    with open(filepath) as f:
        lines = f.readlines()
        for line in csv.reader(lines[1:], quotechar = '"', delimiter = ','):
            gw_ID.append(line[3])
            gw_state.append(line[6])
    return gw_ID, gw_state


def sw_data(filepath):
    """
    Gathering gage numbers and states for SW sites
    """
    sw_ID = []
    sw_state = []
    with open(filepath) as f:
        lines = f.readlines()
        for line in csv.reader(lines[1:], quotechar = '"', delimiter = ','):
            sw_ID.append(line[1])
            sw_state.append(line[3])
    return sw_ID, sw_state

def get_tree(filepath):
    """
    Open XML file using the ElementTree library
    
    """
    xml_tree = ET.parse(filepath)
    
    return xml_tree


def xml_data(xml_tree):
    """
    Parse the XML file and extract data of interest: 
        Measurement number (if present)
        Site number 
        Site name 
        Inspection type (if present)
        Date
    """
    meas = []
    ## if only one meas in xml- i think i remember multiples possible
    #meas = ""
    gage_no = ""
    insp_type= []
    dt = ""
    date = ""

    for child in xml_tree.iter():
        
        if "MeasurementNumber" in child.tag:
            meas.append(child.text)
            #meas = child.text
        
        if "SiteIdentifier" in child.tag:
            gage_no = child.text
             
        if "SpecialInspType" in child.tag:
            insp_type.append(child.text)

        if "StartDateTime" in child.tag:
            dt = child.text
    
    ## Something strange here: all datetime strings are YYYY-MM-DD, BUT
    ## sometimes the date is printed as MM/DD/YYYY and others as YYYY-MM-DD
    ## I have not gotten to the bottom of this yet, hence the try/ except logic...
    try:
        date = datetime.strptime(dt[:10], "%m/%d/%Y").strftime("%Y_%m%d")

    except:
        
        date = datetime.strptime(dt[:10], "%Y-%m-%d").strftime("%Y_%m%d")
    
    #date = datetime.strftime("%y%m%d")
    print(meas, gage_no, insp_type, date)

    return meas, gage_no, insp_type , date


def archive_files(files):
    """ 
    Archiving site visit files as necessary
    """

    wells = "../data/OKI_wells.csv"
    gages = "../data/OKI_gage.csv"

    dest = "../OKI/"
    #source = "examples/"
    #files = os.listdir(source)
    
    gw_ID, gw_state = gw_data(wells)
    sw_ID, sw_state = sw_data(gages)

    ## Looping over files
    for file in files:
        source = os.path.split(file)[0]
        f = os.path.split(file)[1]
        ## Getting data from above functions
        xml_tree = get_tree(source + "/" + f)
        meas, gage_no, insp_type, date = xml_data(xml_tree)
        
        # Matching gage number with state ID from ancillary datasets
        if len(gage_no) == 15:
            for i in range(len(gw_ID)):
                if gage_no == gw_ID[i]:
                    state = gw_state[i]

        else:
            for i in range(len(sw_ID)):
                if gage_no == sw_ID[i]:
                    state = sw_state[i].upper()

        if state not in os.listdir(dest):
            os.mkdir(dest + state)
        
        ## Checking for existing gage dir
        if gage_no not in os.listdir(dest + state):
            os.mkdir(dest + state + "/" + gage_no)
       
        if date.split("_")[1][0] == 1:
            wy = date.split("_")[0][-2:] + 1
        else:
            wy = date.split("_")[0][-2:]

        if "WY" + wy not in os.listdir(dest + state + "/" + gage_no):
            os.mkdir(dest + state + "/" + gage_no + "/WY" + wy)

        ## Checking for existing date dir
        if date not in os.listdir(dest + state + "/" + gage_no + "/WY" + wy):
            os.mkdir(dest + state + "/" + gage_no +  "/WY" + wy + "/" + date)

        ## Checking for measurements
        #if meas == ""
        if len(meas) == 0:
            
            ## Checking for special inspection type
            for insp in insp_type:
                if insp != "None":
                    try:
                        os.mkdir(dest + state + "/" + gage_no + "/WY" + wy + "/" + date + "_insp")
                        shutil.copy(source + "/" + f, dest + state + "/" + 
                                gage_no + "/WY" + wy + "/" + date + "_insp")
                        break
                    
                    except:
                        print("ERROR: File may already exist!")
                        continue
                else:
                    try:
                        shutil.copy(source + "/" + f, dest + state + "/" + 
                                gage_no + "/WY" + wy + "/" + date)
                    except:
                        print("ERROR: File may already exist!")
                        continue
        else:
            ## appending measurement numbers to directory name
            meas_nos = ""
            for m in meas:
              meas_nos += "_" + m  
            
            try:
                os.mkdir(dest + state + "/" +gage_no + "/WY" + wy + "/" + date + "_"  + m)
                shutil.copy( source + "/" + f, dest + state + "/" + gage_no + 
                        "/WY"+ wy + "/" + date + meas_nos)

            except:
                print("ERROR: File may already exist!")
                continue
