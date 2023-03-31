# BLM-corpus

## Quality annotation of Headers in the corpus

* Precision = TP / (TP + FP) = Correct Classified Headers / (Correct Classified Headers + Incorrect Classified Headers) 

= 28 / (28+3) = 0.9

* Recall = TP / (TP + FN) = Correct Classified Headers / (Correct Classified Headers + Incorrect Non-Classified Headers) 

= 28 / (28+11) = 0.72

* F1 = 2 \times Precision Recall


Reflection:
* The false positives in this case are related to the fact that one image is OCR:ed as text and thereby large text. This is why the algorithm claassifies these three lines as headers. 

* The false negatives are beacause this algorithm misses page-headers that often are equal in terms of size as the regular text.
