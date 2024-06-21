# Download the list of all the people in the house of commons
# https://github.com/mysociety/parlparse/blob/master/members/people.json

# Download the list of the ministerial roles
# https://github.com/mysociety/parlparse/blob/master/members/ministers-2010.json

# Download the Hansard debate transcripts in xml
rsync -az --progress --exclude '.svn' --exclude 'tmp/' --relative "data.theyworkforyou.com::parldata/scrapedxml/debates/debates2*" .

# Download MP data (including affiliation) from 1977 onwards (note the date above only has coverage from 1997+ so we need to use both)
# https://www.parliament.uk/business/publications/research/parliament-facts-and-figures/members-of-parliament/
# Constituencies|Parties|HouseMemberships.big.xml:
# http://data.parliament.uk/membersdataplatform/services/mnis/members/query/House=Commons%7CMembership=all%7Ccommonsmemberbetween=1979-5-4and2018-2-20/Constituencies%7CParties%7CHouseMemberships/