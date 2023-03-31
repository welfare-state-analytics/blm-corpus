# BLM-corpus

## Quality annotation of Headers in the corpus (#1)

* Precision = TP / (TP + FP) = Correct Classified Headers / (Correct Classified Headers + Incorrect Classified Headers) = 28 / (28+3) = **0.9**

* Recall = TP / (TP + FN) = Correct Classified Headers / (Correct Classified Headers + Incorrect Non-Classified Headers) = 28 / (28+11) = **0.72**

* F1 = 2TP / (2TP + FP + FN) = 56 / (56 + 3 + 11) = **0.8**


Reflection:
* The false positives in this case are related to the fact that one image is OCR:ed as text and thereby large text. This is why the algorithm claassifies these three lines as headers. 

* The false negatives are beacause this algorithm misses page-headers that often are equal in terms of size as the regular text.



## Quality annotation of Headers and Page Headers in the corpus (#2)
* Precision = TP / (TP + FP) = 38 / (38+3) = **0.93**

* Recall = TP / (TP + FN) = 38 / (38+1) = **0.97**

* F1 = 2TP / (2TP + FP + FN) = 76 / (76+3+1) = **0.95**
