# elections_monitoring

This apolotical project aims to analyse the various political parties with parlamentary seat that participate in the the 2024 Portuguese Parlamentary elections.

## Current package is capable of:
1. extracting all news that match a given query and store it in a sqlite db
2. extract information from the various political parties (currently only PSD is implemented)

## Next steps:
1. create a vector db with the newspaper contents and political parties site content
2. perform sentiment analysis of each party and its leader
3. implement a RAG along and use OpenAi's API to monito for contractions in politcal speech
4. once the POC for PSD is sucessful exteend it to all other parties
