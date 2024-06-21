# Processing datasets
There's a mini pipeline you'll need to go through to prepare the data.

Download raw datasets locally:
bash download_hansard_data_xml.sh

Extract the
python ProcessXMLMetaDataFiles.py

python ProcessXMLTranscriptFiles.py

python ProductTrainingData.py --n_instances=50000

# Ready-to-go SQLite database
Structured Hansard metadata (eg people, positions/roles, party affiliations etc) from 1997 have been wrangled into the hansard.sqlite database.

If you open the database using SQLite tool of choice (eg Datagrip), you will be able to browse the schema and data.

It should be straightforward to write SQL queries to extract the data you need.

You can see some examples of how we used this database to prepare our datasets in ProcessJSONMetaDataFiles.py.

# Acknowledgements
Please see top-level README for acknowledgements.