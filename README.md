# BLM-corpus

## Quality annotation of Headres in the corpus

Precision = TP / (TP + FP) = Correct Classified Headers / (Correct Classified Headers + Incorrect Classified Headers) = 28 / (28+3) = 0.9

Recall = TP / (TP + FN) = Correct Classified Headers / (Correct Classified Headers + Incorrect Non-Classified Headers) = 28 / (28+11) = 0.72

Reflection: 
* The error for the precision in this case are related to the fact that one image is OCR:ed as text and thereby large text. This is why the algorithm claassifies these three lines as headers. 

* The error related to the Recall is beacuase this algorith misses page-headers that often are not larger than the regular text. 
