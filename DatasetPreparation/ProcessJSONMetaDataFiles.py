import sys
import json

# Process the Hansard JSON files into TSV files for loading into Sqlite.
# The data in Sqlite is then used for lookup during dataset processing.

class PeopleJsonFile:
    """
    Class to load people.json into memory for processing
    """

    def __init__(self, path):
        self.path = path
        self.data = self.load_json()

    def load_json(self):
        with open(self.path) as f:
            data = json.load(f)
        return data

    def get_data(self):
        return self.data

    def get_persons(self):
        return self.data["persons"]

    def get_memberships(self):
        return self.data["memberships"]

    def get_person(self, person_id):
        return self.data["persons"][person_id]

    def get_posts(self):
        return self.data["posts"]

    def get_membership(self, person_id):
        first_membership = next((m for m in self.data["memberships"] if m["person_id"] == person_id), "none")

        if first_membership == "none":
            return None
        return first_membership


class MinistersJsonFile:
    """
    Class to load ministers-2010.json into memory for processing
    """

    def __init__(self, path):
        self.path = path
        self.data = self.load_json()

    def load_json(self):
        with open(self.path) as f:
            data = json.load(f)
        return data

    def get_data(self):
        return self.data

    def get_memberships(self):
        return self.data["memberships"]

    def get_organizations(self):
        return self.data["organizations"]


if __name__ == "__main__":

    args = sys.argv[1:]
    data_to_process = "roles"
    if args is not None and len(args) > 0:
       data_to_process = args[0]

    if data_to_process == "roles":
        ministers_processing = MinistersJsonFile("ministers-2010.big.json")

        # Header
        print(f'{"id"}\t{"person_id"}\t{"role"}\t{"organization_id"}\t{"start_date"}\t{"end_date"}')

        for membership in ministers_processing.get_memberships():
            #print(membership)
            print(f'{membership["id"]}\t{membership["person_id"]}\t{membership.get("role", "")}\t{membership["organization_id"]}\t{membership["start_date"]}\t{membership.get("end_date", "")}')

        exit()

    if data_to_process == "organizations":
        organizations_processing = MinistersJsonFile("ministers-2010.big.json")

        # Header
        print(f'{"id"}\t{"name"}')

        for organization in organizations_processing.get_organizations():
            print(f'{organization["id"]}\t{organization["name"]}')

        exit()

    if data_to_process == "memberships":
        memberships_processing = PeopleJsonFile("people.big.json")

        # Header
        print(f'{"id"}\t{"label"}\t{"person_id"}\t{"on_behalf_of_id"}\t{"organization_id"}\t{"post_id"}\t{"start_date"}\t{"end_date"}')

        for membership in memberships_processing.get_memberships():
            #print(membership)

            if 'redirect' in membership.keys():
                continue

            if 'start_date' not in membership.keys():
                continue

            print(f'{membership["id"]}\t{membership.get("label", "")}\t{membership["person_id"]}\t{membership.get("on_behalf_of_id", "")}\t{membership.get("organization_id", "")}\t{membership.get("post_id", "")}\t{membership["start_date"]}\t{membership.get("end_date", "")}')

        exit()

    if data_to_process == "posts":
        memberships_processing = PeopleJsonFile("people.big.json")

        # Header
        print(f'{"id"}\t{"area_name"}\t{"label"}\t{"organization_id"}\t{"start_date"}\t{"end_date"}')

        for post in memberships_processing.get_posts():
            #print(post)

            print(f'{post["id"]}\t{post["area"]["name"]}\t{post.get("label", "")}\t{post["organization_id"]}\t{post.get("start_date", "")}\t{post.get("end_date", "")}')

        exit()

    if data_to_process == "persons":
        persons_processing = PeopleJsonFile("people.big.json")

        # Header
        print(f'{"id"}\t{"full_name"}')

        for person in persons_processing.get_persons():
            #print(person)

            # Skip redirects
            if 'redirect' in person.keys():
                continue

            name = 'NA'

            for name_dic in person["other_names"]:

                if 'given_name' in name_dic.keys() and 'family_name' in name_dic.keys():
                    name = f'{name_dic["given_name"]} {name_dic["family_name"]}'
                elif 'given_name' in name_dic.keys() and 'surname' in name_dic.keys():
                    name = f'{name_dic["given_name"]} {name_dic["surname"]}'
                elif 'name' in name_dic.keys():
                    name = f'{name_dic["name"]}'
                elif 'additional_name' in name_dic.keys():
                    name = f'{name_dic["additional_name"]}'
                elif 'given_name' in name_dic.keys() and 'lordname' in name_dic.keys():
                    name = f'{name_dic["given_name"]} {name_dic["lordname"]}'

                if name != 'NA':
                    continue

            print(f'{person["id"]}\t{name}')

        exit()
