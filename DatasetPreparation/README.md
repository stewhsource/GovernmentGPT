# Processing datasets
There's a mini pipeline you'll need to go through to prepare the data.

Download raw datasets locally:
bash download_hansard_data_xml.sh

python ProcessXMLMetaDataFiles.py

python ProcessXMLTranscriptFiles.py

python ProductTrainingData.py --n_instances=50000

# Ready-to-go SQLite database
Structured Hansard metadata (eg people, positions/roles, party affiliations etc) from 1997 have been wrangled into the hansard.sqlite database.

If you open the database using SQLite tool of choice (eg Datagrip), you will be able to browse the schema and data.

It should be straightforward to write SQL queries to extract the data you need.

You can see some examples of how we used this database to prepare our datasets in ProcessJSONMetaDataFiles.py.

# Datasets
You can download the datasets referenced in the these data processing scripts from s3:

- https://stewh-publicdata.s3.eu-west-2.amazonaws.com/governmentgpt/2024-06-07/raw_datasets/1998OnwardsHansardData.big.tsv
- https://stewh-publicdata.s3.eu-west-2.amazonaws.com/governmentgpt/2024-06-07/raw_datasets/1998OnwardsHansardData_sample.big.tsv
- https://stewh-publicdata.s3.eu-west-2.amazonaws.com/governmentgpt/2024-06-07/raw_datasets/Constituencies%7CParties%7CHouseMemberships.big.xml
- https://stewh-publicdata.s3.eu-west-2.amazonaws.com/governmentgpt/2024-06-07/raw_datasets/gov_mp_data.tsv
- https://stewh-publicdata.s3.eu-west-2.amazonaws.com/governmentgpt/2024-06-07/raw_datasets/hansard.sqlite
- https://stewh-publicdata.s3.eu-west-2.amazonaws.com/governmentgpt/2024-06-07/raw_datasets/members-since-1979.big.json
- https://stewh-publicdata.s3.eu-west-2.amazonaws.com/governmentgpt/2024-06-07/raw_datasets/membership.big.tsv
- https://stewh-publicdata.s3.eu-west-2.amazonaws.com/governmentgpt/2024-06-07/raw_datasets/ministers-2010.big.json
- https://stewh-publicdata.s3.eu-west-2.amazonaws.com/governmentgpt/2024-06-07/raw_datasets/organizations.big.tsv
- https://stewh-publicdata.s3.eu-west-2.amazonaws.com/governmentgpt/2024-06-07/raw_datasets/people.big.json
- https://stewh-publicdata.s3.eu-west-2.amazonaws.com/governmentgpt/2024-06-07/raw_datasets/persons.big.tsv
- https://stewh-publicdata.s3.eu-west-2.amazonaws.com/governmentgpt/2024-06-07/raw_datasets/posts.big.tsv
- https://stewh-publicdata.s3.eu-west-2.amazonaws.com/governmentgpt/2024-06-07/raw_datasets/roles.big.tsv


# Acknowledgements
Please see top-level README for acknowledgements.