# Pathology NLP



## Project Setup

This project relies upon Python and uses Anaconda to manage installation and dependencies.

*Note: As this project was developed on macOS, some dependencies may be overly strict for other OSes.*

```bash
conda create -n nlp python=3.8
conda env export -n nlp -f environment.yml
```

## Project Goals and Tasks

Project level tasks:

1. Identify appropriate College of American Pathologists protocol to be applied to each case
2. Identify super set of features that will be extracted

Case level tasks:

1. Identify number of synoptic reports per case
2. For each synoptic report identified, extract appropriate data elements


## Data Structure

Need to create standardized data model + bladder + prostate extensions

bladder: file:///Users/seth/OneDrive%20-%20The%20University%20of%20Colorado%20Denver/Documents/Projects/Cornish_NLP_Proposal/CAP%20ecc/ecc/html%20with%20css/Bladder.Res.180_3.002.011.REL_sdcFDF.html
prostate: file:///Users/seth/OneDrive%20-%20The%20University%20of%20Colorado%20Denver/Documents/Projects/Cornish_NLP_Proposal/CAP%20ecc/ecc/html%20with%20css/Prostate.Res.128_3.004.001.REL_sdcFDF.html

Questions:

1. Hand Extracted Reports? Adrie will work on this.
2. How many? More prostates (~1000s) than bladder. Prostate extracts more consistent
3. Where will solution live?
   1. Process to parse reports
   2. Extracted structured information
4. Do we care about Notes? e.g. "Histologic Type (Note B)" Notes are just to help fill out form, don't need to store.
5. If differeences between PDF and XML, PDF is winner as that's what people fill out.

The `diagnosticcomment`, `finaldiagnosis`, or `microscopicdescription` fields may contain synoptic reports
