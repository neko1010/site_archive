import xml.etree.ElementTree as ET
import os
import sys
import shutil
from datetime import datetime

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
    #meas = []
    ## if only one meas in xml- i think i remember multiples possible
    meas = ""
    gage_no = ""
    gage_name = ""
    insp_type= []
    dt = ""
    date = ""

    for child in xml_tree.iter():
        if "MeasurementNumber" in child.tag:
            #meas.append(child.tag)
            meas = child.text
        
        if "SiteIdentifier" in child.tag:
            gage_no = child.text
            
        if "Name" in child.tag:
            gage_name = child.text

        if "SpecialInspType" in child.tag:
            insp_type.append(child.text)

        if "StartDateTime" in child.tag:
            dt = child.text
    
    ## Something strange here: all datetime strings are YYYY-MM-DD, BUT
    ## sometimes the date is printed as MM/DD/YYYY and others as YYYY-MM-DD
    ## I have not gotten to the bottom of this yet, hence the try/ except logic...

    try:
        date = datetime.strptime(dt[:10], "%m/%d/%Y").strftime("%Y%m%d")

    except:
        
        date = datetime.strptime(dt[:10], "%Y-%m-%d").strftime("%Y%m%d")
    
    #date = datetime.strftime("%y%m%d")
    print(date)

    return meas, gage_no, gage_name, insp_type, date

## Looping over files
for f in os.listdir("examples"):
    
    ## Getting data from above functions
    xml_tree = get_tree("examples/" + f)
    meas, gage_no, gage_name, insp_type, date = xml_data(xml_tree)
    
    ## Checking for existing gage dir
    if gage_no not in os.listdir("output"):
        os.mkdir("output/" + gage_no)

    ## Checking for existing date dir
    if date not in os.listdir("output/" + gage_no):
        os.mkdir("output/" + gage_no + "/" + date)

    ## Checking for measurements
    if meas == ""
    #if len(meas) == 0:
        
        ## Checking for special inspection type
        for insp in insp_type:
            if insp != "None":
                os.mkdir("output/" + gage_no + "/" + date + "_INSP")
                shutil.copy("examples/" + f, "output/" + gage_no + "/" + date + "_INSP")
                break
            else:
                shutil.copy("examples/" + f, "output/" + gage_no + "/" + date)
                
    
    else:
        #for m in meas:
            os.mkdir("output/" + gage_no + "/" + date + "/_" + meas)# + m)
            shutil.copy( "examples/" + f, "output/" + gage_no + "/" + date + "/_" + meas)# + m)
            print(f + " " + meas + " copied")

