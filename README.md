## Step 1 - generate list of needed words:

This step generates a file called 'needed_words' that contains all the targets
and fillers in the datasets and in the fillers lists.
This file will be used to load just the needed rows of the distributional space
afterwards.

In order to do so, exec the extract-needed-words command


## Step 2 - save spaces into numpy/scipy format:

This step produces .npz or .npy matrices from raw text spaces.
In order to do so, exec the generate-npz-space command

Note: raw spaces should be in gzipped format, and:
* sparse spaces should have extension .sparse.gz
* dense spaces should have extension .dense.gz


## Step 3 - generate prototypes:

This step produces a npy matrix containing prototypes, given a filler file and
a distributional space.

Note: files containing fillers should have one of the following extensions:
* .plain.txt if the fillers are not typed
* .deps.txt if the fillers are typed

## Step 4 - evaluate correlation:

This step evaluates a correlation score given a dataset, a matrix containing
prototypes and a distributional space.
