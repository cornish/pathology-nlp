# Pathology NLP

## Project TO DO List

* Summarize unmatched concepts (similar to matched concepts)
* Create views to convert long format to wide
  * which features/concepts do you care about?
* train deep learning model based on partially matched concepts?
  * get list of unmatched concepts
  * have Toby/Adrie help with mapping (for training)
  * create classifier for unmatched phrases (extraction)
* Match based on edit distance?
  * https://www.nltk.org/api/nltk.metrics.html
  * https://github.com/seatgeek/fuzzywuzzy
  * https://python.gotrained.com/nltk-edit-distance-jaccard-distance/
* Create aliases and process to load/match them
  * Use DL instead?
* literature review
* review hand mapped reports
* Also create views with parent concepts (Show me histologic type for these reports sql)
* Some reports Q: A format per line; others different format. Find some of each
* X - Hand map one or two reports
* X - Need to process parts from columns 'Parts' and 'Final Diagnosis'; should map parts labels to final diagnosis sections
* X - multiple matches for values usually means need to use key to find correct concept
* X - key/value pair doesn't work for section headings e.g. "Pathologic Staging (pTNM)"
* X - Store matched concepts to database
  * first purge matches for given report
  * store new concepts
* X - Update parser to run over more than just 1 report (probably switch from NB to .py file)

Pathology items:
* Fixed - Some reports have “<” encoded as “&lt;”
* Fixed - What is "D;" at the beginning of DiagnosticComment colum?
* X - Send the CAP document that describes the 7 or so ways to document a CAP report
* Start paper introduction w/literature review highlighting key literature
* Hand curated reports

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

Questions:

1. Hand Extracted Reports? Path will work on this.
2. How many? More prostates (~1000s) than bladder. Prostate extracts more consistent
3. Where will solution live?
   1. Process to parse reports
   2. Extracted structured information
4. Do we care about Notes? e.g. "Histologic Type (Note B)" Notes are just to help fill out form, don't need to store.
5. If differences between PDF and XML, PDF is winner as that's what people fill out.

The `diagnosticcomment`, `finaldiagnosis`, or `microscopicdescription` fields may contain synoptic reports

## For Paper

* Need to report micro- and macro-averaged precision, recall, and F score.
* Calculate 95% confidence intervals by bootstrapping from test set

## Information Extraction References

* https://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html
* https://www.osti.gov/pages/servlets/purl/1408007
* https://academic.oup.com/jamia/article/27/1/89/5618621?guestAccessKey=815a822e-35ee-4904-a8ee-46c652ecd811#supplementary-data
* https://medium.com/@kormilitzin/med7-clinical-information-extraction-system-in-python-and-spacy-5e6f68ab1c68
* https://blogs.itemis.com/en/deep-learning-for-information-extraction
* https://www.analyticsvidhya.com/blog/2019/09/introduction-information-extraction-python-spacy/