from kblab import Archive
import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
import time
from pathlib import Path
import zipfile
from ebooklib import epub
import zipfile
from lxml import etree
import numpy as np

romaner=[{"meta.host_title": "Welfare state analytics"},"https://datalab.kb.se"]
blm=[{"label": "BONNIERS", "tags": "issue"},"https://datalab.kb.se"]
dn=[{"tags": "issue"},"https://betalab.kb.se"]


def get_size_treshold(page_string,quantile=0.95):

    xmlns='http://www.loc.gov/standards/alto/ns-v2#'
    tree= ET.ElementTree(ET.fromstring(page_string))
    styles_font={}
    styles=tree.find(('.//{%s}Styles' % xmlns))

    for children in styles.findall('{%s}TextStyle' % xmlns):
        styles_font[children.attrib.get('ID')]=children.attrib.get("FONTSIZE")
    size=[]

    for lines in tree.iterfind('.//{%s}TextLine' % xmlns):

        for line in lines.findall('{%s}String' % xmlns):
            # Check if there are no hyphenated words
            if ('SUBS_CONTENT' not in line.attrib and 'SUBS_TYPE' not in line.attrib):
            # Get value of attribute @CONTENT from all <String> elements
                style=line.attrib.get('STYLEREFS')
                size.append(styles_font[style])

            else:
                if ('HypPart1' in line.attrib.get('SUBS_TYPE')):
                    style=line.attrib.get('STYLEREFS')
                    size.append(styles_font[style])

    size=list(map(float,size))
    try:
        return np.quantile(size,quantile)
    except:
        print("Failed: probably page without text (solve this issue!)")
        
  
  def get_content(filter=blm,max_number=1):
    """API call to obtain a list of all books from kblab. 
    Args:
        filter (dictionary): A dictionary containing the filters for the packages in the betalab query.
        max_number (int): An integer specifying the highest number of packages to query.
    Returns:
        books (list): a list containing a list of responses from requests.get, containing alto-xml files.
    """
    home_dir=str(Path.home())
    with open(f'{home_dir}/Path/to/API_credentials', 'r') as file:
        pw = file.read().replace('\n', '')

    a = Archive(filter[1], auth=("demo", pw))
    books=[]
    xmlns='http://www.loc.gov/standards/alto/ns-v2#'
    for package_id in a.search(filter[0], max=max_number):
        write_root=etree.Element(package_id)
        page_index=1
        for x in a.get(package_id):
            if "alto.xml" in x:
                for i in range(5):
                    backoff_time = 0.1 * (2 ** i)
                    page=requests.get(f"{filter[1]}/{package_id}/{x}", auth=HTTPBasicAuth("demo", pw),stream=True)
                    if page.status_code == 200:
                        tree= ET.ElementTree(ET.fromstring(page.text))
                        """ Extract text content from ALTO xml file """
                        page_jp = f"{filter[1]}/{package_id}/{x[:-9]}.jp2/_view"
                        pb=etree.SubElement(write_root, "pb")
                        pb.set("n",f"{page_index}")
                        pb.set("facs",f"{page_jp}")
                        #contentinpage set here

                        #Get mappings of styles-font
                        styles_font={}
                        styles=tree.find(('.//{%s}Styles' % xmlns))
                        for children in styles.findall('{%s}TextStyle' % xmlns):
                            styles_font[children.attrib.get('ID')]=children.attrib.get("FONTSIZE")
                        
                        # Head treshold for the page
                        head_treshold = get_size_treshold(page.text)

                        # Find all <TextLine> elements
                        for lines in tree.iterfind('.//{%s}TextLine' % xmlns):
                            # New line after every <TextLine> element
                            # Find all <String> elements
                            block=[]
                            head_block=[]

                            for line in lines.findall('{%s}String' % xmlns):
                                # Check if there are no hyphenated words
                                if ('SUBS_CONTENT' not in line.attrib and 'SUBS_TYPE' not in line.attrib):
                                    style=line.attrib.get('STYLEREFS')
                                    size=float(styles_font[style])
                                    if size > head_treshold:
                                        head_block.append( line.attrib.get('CONTENT') )
                                    else:
                                        block.append( line.attrib.get('CONTENT') )
                                else:
                                    if ('HypPart1' in line.attrib.get('SUBS_TYPE')):
                                        style=line.attrib.get('STYLEREFS')
                                        size=float(styles_font[style])
                                        if size > head_treshold:
                                            head_block.append( line.attrib.get('SUBS_CONTENT') )
                                        else:
                                            block.append( line.attrib.get('SUBS_CONTENT') )

                            block=" ".join(block)
                            head_block=" ".join(head_block)

                            if block!=" " and block!="":
                                if "<" in block or ">" in block:
                                    block=block.replace("<","")
                                    block=block.replace(">","")
                                content_in_page=etree.SubElement(write_root, "p")
                                content_in_page.text=block

                            if head_block!=" " and head_block!="":
                                if "<" in head_block or ">" in head_block:
                                    head_block=head_block.replace("<","")
                                    head_block=head_block.replace(">","")
                                head = etree.SubElement(write_root, "Header")
                                head.text = head_block
                        page_index+=1
                        break
                    else:
                        print(f"{filter[1]}/{package_id}/{x} failed")
                        time.sleep(backoff_time)

        books.append(etree.tostring(write_root, pretty_print=True))
    return books
    
    
 def get_ids(filter=blm,max_number=1):
    """function to return all ids
    """
    home_dir=str(Path.home())
    with open(f'{home_dir}/Path/to/API_credentials', 'r') as file:
        pw = file.read().replace('\n', '')

    a = Archive(filter[1], auth=("demo", pw))
    ids=[]
    for package_id in a.search(filter[0], max=max_number):
        ids.append(package_id)
    return ids
    
    
    if __name__ == "__main__":
    for content,id in zip(get_content(),get_ids()):
        book = epub.EpubBook()

        # set metadata

        book = epub.EpubBook()

        # set metadata
        book.set_identifier(id)
        book.set_title("Sample book")
        book.set_language("sv")


        # create content in one chapter
        c1 = epub.EpubHtml(title=id, file_name="content.xhtml", lang="sv")
        c1.content = content
        book.add_item(c1)

        # add default NCX and Nav file
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # define CSS style
        style = "BODY {color: white;}"
        nav_css = epub.EpubItem(
            uid="style_nav",
            file_name="style/nav.css",
            media_type="text/css",
            content=style,
        )

        # add CSS file
        book.add_item(nav_css)

        # basic spine
        book.spine = ["nav", c1]

        # write to the file
        epub.write_epub(f"{id}.epub", book)
        newpath = f"../corpus/editions/{id}" 
        Path(newpath).mkdir(parents=True, exist_ok=True)


        with zipfile.ZipFile(f"{id}.epub", 'r') as zip_ref:
            zip_ref.extractall(newpath)
        Path(f"{id}.epub").unlink()
