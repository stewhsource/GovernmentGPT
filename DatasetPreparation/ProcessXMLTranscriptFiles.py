import sys
from xml.dom import minidom
import re
import sqlite3
import json
from os import listdir
from os.path import isfile, join
import HansardConfig

class HansardXMLFile:
    """
    Class to load hansard transcript XML file into memory for processing
    """

    def __init__(self, path):
        self.path = path
        self.text = self.load_xml()
        self.xml = minidom.parseString(self.text)

    def load_xml(self):
        with open(self.path, 'r', encoding='latin-1') as f:
            text_data = f.read()
        return text_data

    def get_text(self):
        return self.text

    def get_speeches(self):
        return self.xml.getElementsByTagName("speech")

# Create sqlite connection
conn = sqlite3.connect('hansard.sqlite')

def get_person_details(person_identifier: str, speaker_name: str, at_iso8601_date: str, debug = True):
    """Get the person data from sqlite.
    Person identifier can be a member/ or person/ from the 1997+ Hansard data.

    If the person identifier is not present, then the speaker name must be present to attempt matching (pre-1997 Hansard data)
    """

    output = {"full_name": "Unknown", "person_id": None, "membership_id": None, "party": "Unknown", "constituency": "Unknown", "holding_roles": []} # Default to empty output

    # Create cursor
    c = conn.cursor()

    # Return empty if no person identifier and no speaker name
    if person_identifier is None and speaker_name is None:
        return output

    # Lookup the person name and find the person id
    if person_identifier is None:
        qry = (f"SELECT * FROM gov_mp_data "
               f"WHERE Name LIKE '%{speaker_name}%' ")

        if debug:
            print(f"----")
            print(f"Matching gov uk data for speaker data")
            print(f"SQL: {qry}")

        # Fetch result
        result = c.fetchone()
        if result is not None:
            columns = [description[0] for description in c.description]
            output["full_name"] = speaker_name
            output["party"] = result[columns.index("Party")]

            if debug:
                print(f"Found ")
                print(f"SQL: {qry}")
        else:
            return output # Return default empty

    # Base query for parlparse data - search by person_id or member_id (for newer hansard files > 1997)
    qry = (f"SELECT *, parties.party_name as party_name, membership.id as membership_id, membership.person_id as person_id FROM membership "
           f"LEFT JOIN persons ON membership.person_id = persons.id "
           f"LEFT JOIN parties on membership.on_behalf_of_id = parties.id "   
           f"WHERE match_person_id='{person_identifier}' "
           f"and on_behalf_of_id is not null")

    # Attempt query with timestamp
    if "member/" in person_identifier:
        qry = qry.replace('match_person_id', 'membership_id')
    elif "person/":
        qry = qry.replace('match_person_id', 'person_id')


    if debug:
        print(f"----")
        print(f"Matching parlparse data for personid/memberid")
        print(f"SQL: {qry}")

    # Query database
    c.execute(qry)

    # Fetch result
    result = c.fetchone()
    columns = [description[0] for description in c.description]

    if result is None: return output # Return default empty

    output["party"] = result[columns.index("party_name")]
    output["full_name"] = result[columns.index("full_name")]
    output["membership_id"] = result[columns.index("membership_id")]
    output["person_id"] = result[columns.index("person_id")]

    ###### Attach the parliamentary roles (eg committees)
    qry = (f"SELECT * FROM roles "
           f"WHERE person_id = '{output['person_id']}' "
           f"AND '{at_iso8601_date}' >= start_date AND '{at_iso8601_date}' <= end_date")

    # Query database
    c.execute(qry)

    # Fetch result
    result = c.fetchall()
    columns = [description[0] for description in c.description]
    roles = []
    for row in result:

        org_name = str(row[columns.index('organization_id')].replace('-', ' ')).title()

        output_text = ""
        if row[columns.index("role")] is None:
            output_text = f"Member of {org_name}"
        else:
            output_text = f"{org_name} {row[columns.index('role')]}"

        roles.append(output_text)

    output["holding_roles"] = roles

    ###### Attach the constituency
    qry = (f"SELECT *, posts.label as constituency FROM membership "
           f"INNER JOIN posts on posts.id = membership.post_id "
           f"WHERE membership.id = '{output['membership_id']}'")

    # Query database
    c.execute(qry)

    # Fetch result
    result = c.fetchone()
    columns = [description[0] for description in c.description]

    if result is None:
        output["constituency"] = "Unknown"
    else:
        output["constituency"] = result[columns.index("constituency")]
        output["constituency"] = output["constituency"].replace("Member of Parliament for ", "MP for ")

    #print(output)

    # Query

    # Close cursor
    c.close()

    return output


def parse_hansard_xml_file_to_tsv(path):
    xml_file = HansardXMLFile(path)
    file_name = xml_file.path.split("/")[-1]
    iso8601_date = file_name.replace("debates", "")[:10]

    for speech in xml_file.get_speeches():
        speech_id = speech.getAttribute("id")
        speech_speaker_name = speech.getAttribute("speakername")
        speech_type = speech.getAttribute("type")

        speech_person_identifier = speech.getAttribute("person_id") # Use person_id in newer hansard files
        if speech_person_identifier is None or len(speech_person_identifier) == 0:
            speech_person_identifier = speech.getAttribute("speakerid") # Use speakerid in older hansard files

        speech_time = speech.getAttribute("time")
        speech_text = ""

        for paragraph in speech.childNodes:
            if not paragraph.hasChildNodes(): continue # Skip empty nodes

            # Extracted any child nodes that are text nodes
            for child_node in paragraph.childNodes:
                if child_node.nodeValue is not None:
                    speech_text = speech_text + (str(child_node.nodeValue).strip())

                    speech_text = speech_text + " " # Ready for next sentence

        # Ignore empty speeches
        if len(speech_text) <= 8: continue

        # Ignore where no speaker id is available
        if len(speech_person_identifier) == 0: continue

        # Remove double spaces
        speech_text = re.sub(' +', ' ', speech_text)

        # Remove rogue newlines
        speech_text = re.sub('\n', '', speech_text)

        # Attach speaker details
        speaker_details = get_person_details(speech_person_identifier, speech_speaker_name, iso8601_date, debug=False)

        # Output speech data
        print(f"{iso8601_date}\t{speech_id}\t{json.dumps(speaker_details)}\t{speech_text}")
        #print(speech_person_identifier)
        #print(speech_speaker_name)
        #print(speech_id)
        #print(speech_text)
        #print(iso8601_date)


if __name__ == "__main__":
    hansard_xml_dump_path = f"/YOUR_DOWNLOADS_PATH/hansard/scrapedxml/debates/"

    xml_files = [f for f in listdir(hansard_xml_dump_path) if isfile(join(hansard_xml_dump_path, f))]

    for xml_file in sorted(xml_files):
        #print(xml_file)
        if xml_file.startswith("debates1998") or xml_file.startswith("debates1999") or xml_file.startswith("debates2"): # Filter to 1998 onwards data
            parse_hansard_xml_file_to_tsv(hansard_xml_dump_path + '/' + xml_file)