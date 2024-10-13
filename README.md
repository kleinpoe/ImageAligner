
## Introduction

In macro photography, you can use focus stacking to get larger depths of fields. For this, multiple software solutions exist. For me, this software oftens struggles with images that are not so well aligned. Fancy alignment solutions did not work for me. I think this manual solution serves this purpose just fine

## Prerequisites

- Images lie inside directory
  - Format: jpg
  - sorting by name should reflect sorting by focus (focus direction does not matter)
  - images must have same resolution
- Installed FIJI (ImageJ) https://imagej.net/software/fiji/downloads
- Installed python with packages: numpy, Pillow, os, csv

## Steps
1. Open FIJI (ImageJ)
2. File -> Import -> Image Sequence: select "sort alphabetically"
3. Search for point-like feature in the center of the stack (focus)
4. Use the Multi-Point tool to select the feature in every image, starting with the first image, marking in every successive image. Select exactly one point per image. You can move the points and delete misplaced point by STRG+Click.
5. STRG+M opens the points
6. Save the points to the same directory as the images using: File -> Save as
6. Open script replace input directory and the saved points filename
7. Run script

## Limitations

- Script can only align translations, no skewing/scaling which could be done by selecting multiple points. However for my macro stacks this is not necessary.

