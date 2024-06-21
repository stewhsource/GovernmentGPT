import sys
from xml.dom import minidom
import HansardConfig

# Process the Hansard XML files into TSV files for loading into Sqlite.
# The data in Sqlite is used for lookup during training dataset creation.

def parse_gov_xml_members_file(path):
    text = ""
    with open(path) as f:
        text = f.read()

    xml = minidom.parseString(text)

    # Header
    print("name\tconstituency\tparty\tstart_date\tend_date")

    for member in xml.getElementsByTagName("Member"):
        #print(member.toxml())

        name = str(member.getElementsByTagName("DisplayAs")[0].firstChild.nodeValue)
        party = str(member.getElementsByTagName("Party")[0].firstChild.nodeValue)
        start_date = str(member.getElementsByTagName("HouseStartDate")[0].firstChild.nodeValue).replace("T00:00:00", "")
        end_date = ""
        if member.getElementsByTagName("HouseEndDate") is not None and member.getElementsByTagName("HouseEndDate")[0].hasChildNodes():
            end_date = str(member.getElementsByTagName("HouseEndDate")[0].firstChild.nodeValue).replace("T00:00:00", "")

        # Get constituency
        constituency = "Member of Parliament for " + str(member.getElementsByTagName("Constituencies")[0].firstChild.getElementsByTagName("Name")[0].firstChild.nodeValue)

        # Remove titles from name
        name = name.replace("Mr ", "").replace("Mrs", "").replace("Ms", "").replace("Dr", "").replace("Miss", "").replace("Sir", "").replace("Lady", "").replace("Lord", "").strip()

        print(f"{name}\t{constituency}\t{party}\t{start_date}\t{end_date}")






parse_gov_xml_members_file(f'{HansardConfig.root_path}/Constituencies|Parties|HouseMemberships.big.xml')