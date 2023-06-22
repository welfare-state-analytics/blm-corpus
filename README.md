# Bonniers litterära magasin (BLM)

## The curation process
This documentation contains the steps we have gone through to curate BLM.

1) From the Datalab.kb API, we retrieve all the alto.xml files for each page in every edition of BLM. There are a total of 565 editions of BLM available in Datalab, with an average of 85 pages per magazine. These BLM files are saved as unzipped epubs, where the content is stored as xhtml files.

2) Segmentation of "page breaks" is performed. Since each file represents a page in BLM, segmentation is done based on each page, and a UUID (Universally Unique Identifier) is added to enable identification of each page.

3) A test suite is constructed to ensure that all editions of BLM are saved as unzipped epubs and that each edition is represented by an xhtml file that can be opened.

4) A CSV file with metadata is created, containing information about each edition, such as publication date and magazine number. This is useful for future reference, as it allows linking information based on the edition's ID (represented by a row in the CSV file) obtained from the KBs API.

5) Headers are identified based on text size, where we have created a distribution of all word sizes on each page. Each row of words with a text size equal to or larger than the 95th percentile of the distribution is classified as a header, and the rest as body text. This resulted in misclassifications of page numbers and OCR errors as headers. To address this, we added a condition that a header cannot consist solely of numbers and/or special characters, as we identified misclassifications caused by this.

6) The next step was to differentiate between "headers" and "page headers" and distinguish "page headers" from body text. We chose a positional boundary on the vertical axis of the page to identify words in the top margin of the scanned image. Words above this boundary are classified as "page headers."

7) To assess the current model's ability to correctly classify "headers," "page headers," and body text, we randomly selected 20 pages from all editions. The purpose was to manually annotate the actual text objects that will serve as the "ground truth" for evaluating the model's ability to accurately classify the different types of text objects.

8) Subsequently, we created "articles" based on the classification of headers, assuming that a new article starts and ends with a "header." This allows for easier extraction of specific articles in the future and linking them to information available in data files, etc.

9) Two .csv-files are created to store information extracted from the registers (usually published once a year) and table of contents of the issues in the corpus. All edition-ID's are represented at least once in each of the files, but in cases where the information (such as the registers for most of the editions) is not available, the corresponding columns in the files are left empty.



## Quality annotation of Headers in the corpus (#1)

* Precision = TP/(TP+FP) = Correct Classified Headers/(Correct Classified Headers+Incorrect Classified Headers) = 28/(28+3) = **0.9**

* Recall = TP/(TP+FN) = Correct Classified Headers/(Correct Classified Headers+Incorrect Non-Classified Headers) = 28/(28+11) = **0.72**

* F1 = 2TP/(2TP+FP+FN) = 56/(56+3+11) = **0.8**


Reflection:
* The false positives in this case are related to the fact that one image is OCR:ed as text and thereby large text. This is why the algorithm claassifies these three lines as headers. 

* The false negatives are beacause this algorithm misses page-headers that often are equal in terms of size as the regular text.



## Quality annotation of Headers and Page Headers in the corpus (#2)
### Headers
* Precision = TP/(TP+FP) = 18/(18+3) = **0.86**

* Recall = TP/(TP+FN) = 18/(18+1) = **0.95**

* F1 = 2TP/(2TP+FP+FN) = 36/(36+3+1) = **0.9**

Reflection:
* The false positives are still related to the image that is OCR:ed as text and thereby large text. This is why the algorithm claassifies these three lines as headers. 

* The false negative is a Header that is just an integer, the algorithm at the moment excludes numbers as headers because of an issue that it was capturing page numbers as headers earlier. It can be fixed.

### Page Headers
* Precision = TP/(TP+FP) = 15/(18+0) = **1.0**

* Recall = TP/(TP+FN) = 15/(18+0) = **1.0**

* F1 = 2TP/(2TP+FP+FN) = 30/(30+0+0) = **1.0**
