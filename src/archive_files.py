import xml.etree.ElementTree as ET
import os
import sys
import shutil
from datetime import datetime
import csv
from tkinter import *
from tkinter import messagebox

def gage_data(filepath):
    """
    Gathering gage numbers and states for sites.
    Path to tab delimited file generated from SIMS for a particular state 
    is only required argument, and a list of gage numbers is returned.
    """
    gage_ID = []

    with open(filepath) as f:
        lines = f.readlines()
        for line in lines:
            line_list = line.split("\t")
            gage_ID.append(line_list[1])
    
    return gage_ID



def get_tree(filepath):
    """
    Open XML file using the ElementTree library.
    Path to an XML file is the only required argument and XML element tree is returned. 
    
    """
    xml_tree = ET.parse(filepath)
    
    return xml_tree


def xml_data(xml_tree):
    """
    XML tree from get_tree function is the only required argument.
    Parse the XML file and return data of interest as a list or string: 
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

def final_dest(files):
    """ 
    Requires a list of files as the only argument.
    Loops through files to determine if a site visit XML document is present
    and returns the appropriatedestination of the files based upon information 
    embedded in this document.
    """

    KY = "../data/Ky_sites.txt"
    IN = "../data/IN_sites.txt"

    ## DEST TO BE CHANGED TO SERVER LOCATION
    dest = "../OKI/"
    
    KY_gages = gage_data(KY)
    IN_gages = gage_data(IN)

    
    for f in files:
        ## Determine site visit master file
        
        if os.path.splitext(f)[1] == ".xml" and os.path.split(f)[1].startswith("SV"):
            print(f) 
            ## Getting data from above functions
            xml_tree = get_tree(f)
            meas, gage_no, insp_type, date = xml_data(xml_tree)
            
            ## Matching gage number with state- Data section provided comprehensive state list
            if gage_no in KY_gages:
                state = "KY"

            if gage_no in IN_gages:
                state = "IN"
            
            #if gage_no in OH_gages:
            #    state = "OH"

            print(state)
            if state not in os.listdir(dest):
                os.mkdir(dest + state)
            
            ## Checking for existing gage dir
            if gage_no not in os.listdir(dest + state):
                os.mkdir(dest + state + "/" + gage_no)
           
            if date.split("_")[1][0] == 1:
                wy = date.split("_")[0] + 1
            else:
                wy = date.split("_")[0]

            if "WY" + wy not in os.listdir(dest + state + "/" + gage_no):
                os.mkdir(dest + state + "/" + gage_no + "/WY" + wy)

            ### Checking for existing date dir
            #if date not in os.listdir(dest + state + "/" + gage_no + "/WY" + wy):
            #    os.mkdir(dest + state + "/" + gage_no +  "/WY" + wy + "/" + date)

            ## Checking for measurements
            if len(meas) == 0:
                
                ## Checking for special inspection type
                for insp in insp_type:
                    if insp != "None":
                        #try:

                        final_dest = dest + state + "/" + gage_no + "/WY" + wy + "/" + date + "_insp"
                        os.mkdir(final_dest)
                    else:
                        final_dest = dest + state + "/" + gage_no + "/WY" + wy + "/" + date
                        os.mkdir(final_dest)
            else:
                ## appending measurement numbers to directory name
                meas_nos = ""
                for m in meas:
                  meas_nos += "_" + m  
               
                final_dest = dest + state + "/" + gage_no + "/WY" + wy + "/" + date  + meas_nos
                if (date + meas_nos) not in os.listdir(dest + state + "/" + gage_no + "/WY" + wy + "/"):
                    os.mkdir(final_dest)
    
    return final_dest


def archive_files(files, dest):
    """ 
    Archiving site visit files as necessary.
    Accepts the same list of files given to the final_dest function and the destination
    returned from final_dest as arguments.
    """
    ## Checking if file has been archived
    for f in files:
        if os.path.split(f)[1] in os.listdir(dest):
            root = Tk()
            root.withdraw()
            messagebox.showerror("WARNING", f + " already archived")
            root.destroy() 
            continue
        else:
            shutil.copy( f, dest) 
