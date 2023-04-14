# BLM-corpus

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
