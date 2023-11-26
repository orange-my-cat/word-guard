import os
import zipfile
from lxml import etree
import json 
import math
from datetime import datetime


file_directory = os.getcwd() + "\\uploads"
files = os.listdir(file_directory)


prefix = """{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"""
results = {}
authors = []
doc_data = {}

if __name__ == "__main__":
# This function is heavily influenced by this source https://stackoverflow.com/questions/7021141/how-to-retrieve-the-author-of-an-office-file-in-python
    def get_authors(zip):
        #T his contains the returned dictionary containing both an id associated with the author and the author name for the given document. 
       

        # Gets the xml contents that contain the 'creator'/author(s) within the zipped file. 
        document = etree.fromstring(zip.read('docProps/core.xml'))
        # The dictionary with dc as the key and the value as the object tag associated with the creator. 
        ns={'dc': 'http://purl.org/dc/elements/1.1/'}
        # This obtains a list of creators for the given document. 
        creators = document.xpath('//dc:creator', namespaces=ns)[0].text
        
        
        #Since creators is a string of authors separated by ';', the split function is done to create a list of separate users to loop through. 
        creators = creators.split(';')
        authors.append((creators, len(creators)))
        return authors
   
    # unzip and read document.xml
    def get_word_xml(docx_filename):
        with open(docx_filename, 'rb') as f:
            zip = zipfile.ZipFile(f)
            get_authors(zip)
            xml_content = zip.read('word/document.xml')
            xml_core = zip.read('docProps/core.xml')
            xml_app = zip.read('docProps/app.xml')
            #we need to open docProps/core.xml & docProps/app.xml
            #to get the modfication dates, authors, version number
        return xml_content, xml_core, xml_app
    
    def extract_core(xml_core):
        root = etree.fromstring(xml_core)

        creator = ""
        lastmodifiedby = ""
        revisions = ""
        createdDate = ""
        modifiedDate = ""

        for child in root.iter():
            attribute  = child.tag
            if "creator" in attribute:
                creator = child.text
                continue
            elif "lastModifiedBy" in attribute:
                lastmodifiedby = child.text
                continue
            elif "revision" in attribute:
                revisions = child.text
                continue
            elif "created" in attribute: 
                createdDate = child.text
                continue
            elif "modified" in attribute:  
                modifiedDate = child.text
                continue
                        

        #print(creator + ", " + lastmodifiedby + ", " + revisions + ", " + createdDate + ", " + modifiedDate) 

        return creator, lastmodifiedby, createdDate, modifiedDate

    def extract_app(xml_app):
        root = etree.fromstring(xml_app)
        
        versionstr = ""
        versionnum = ""
        wordcount = ""
        charactercount = ""

        for child in root.iter():
            attribute  = child.tag
            if "Application" in attribute:
                versionstr = child.text
            elif "AppVersion" in attribute:
                versionnum = child.text
            elif "Words" in attribute:
                wordcount = child.text
            elif "Characters" in attribute: 
                charactercount = child.text
            elif "TotalTime" in attribute:
                edittime = child.text
        
        #print(versionstr + ", " + versionnum + ", " + wordcount + ", " + charactercount) 

        return versionstr + " " + versionnum, wordcount, charactercount, edittime

    #debugging function - writes to json file
    def writejson(results):
        json_object = json.dumps(results, indent=4)
        with open("results.json", "w") as rf:
            rf.write(json_object)
            rf.close()

    #calculate cheating probability
    def cheating_prob(results):
        word_per_unique_rsid = int(results["words"])/len(results["rsidR"].keys())
        word_per_rsidr = int(results["words"])/sum(results["rsidR"].values())
        word_per_minute = int(results["words"])/max(int(results["edit_time"]), 1)
        log_odds = -0.48452-0.16014*word_per_unique_rsid + 0.42515*word_per_rsidr + 0.02672*word_per_minute
        prob = math.exp(log_odds)/(math.exp(log_odds)+1)

        # Catching documents which are completely/majority content copied
        if int(word_per_unique_rsid) in range(70, 10001) and max(int(results["edit_time"]), 1) in range(0, 30):
            # Almost certain as only other alternative is for the document to be copied content of the author's original work (transferring) 
            prob = 0.99
            return prob
        
        return min(0.99, round(prob, 2))

    for file in files:
        xml_content, xml_core, xml_app = get_word_xml(f'{file_directory}\\{file}')
        
        cr, mb, crD, lmD = extract_core(xml_core) #creator, lastmodifiedby, createdDate, modifiedDate
        ver, wc, cc, et = extract_app(xml_app) #Version, Word Count, Character COunt
        root = etree.fromstring(xml_content) # create tree based on xml
        
        rsids = {}

        # get every occurance of rsid in the xml
        for child in root.iter():

            #print(child.attrib.items())
            for attribute, val in child.attrib.items():
                if "rsid" in attribute:
                    rsidtype = attribute.replace(prefix, "")
                    rsids[rsidtype] = rsids.get(rsidtype, []) + [val]                        

        text = "" # init text

        # get body element
        body = root.xpath('//w:body', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
        
        # get paragrahs
        for paragraph in body[0].getchildren():
            for node in paragraph.iter():
                if node.text is not None:
                    text += node.text
            text += " "

        # count words
        word_count = len([x for x in text.split(" ") if x != ''])

        doc_data = {}

        # count rsids based on type and id
        for key, value in rsids.items():
            unique = {}
            for item in value:
                if item in unique:
                    unique[item] += 1
                else:
                    unique[item] = 1
            doc_data[key] = unique

        doc_data["words"] = word_count # can also use 'wc'
        #print("authors", authors)
        # TO DO
        #doc_data["version"] = 16.0000
        #doc_data["tval"] = 0.123
        #doc_data["suspicious"] = True
        #doc_data["created"] = "12/03/23"
        #doc_data["last_modified"] = "23/04/23"
        #doc_data["edit_time"] = 20
          
        #Done

        crDf = datetime.strptime(crD, "%Y-%m-%dT%H:%M:%SZ")
        lmDf = datetime.strptime(lmD, "%Y-%m-%dT%H:%M:%SZ")        

        doc_data["authors"] = authors
        doc_data["version"] = ver
        doc_data["created"] = crDf.strftime("%H:%M:%S, %d/%m/%Y")
        doc_data["last_modified"] = lmDf.strftime("%H:%M:%S, %d/%m/%Y")
        doc_data["edit_time"] = et
        doc_data["probability"] = cheating_prob(doc_data)
        doc_data["suspicious"] = doc_data["probability"] > 0.5

        results[file] = doc_data
        authors = []
    
    #writejson(results)
    json_object = json.dumps(results, indent=4)
    # This code works to delete files in the directory, However it breaks the page?
    #remove the files in the upload folder
    for file in files:
        os.remove(file_directory + "\\"  + file)
        
    print(json_object)