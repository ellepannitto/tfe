## Step 1 - generate list of needed words:

This step generates a file called ```needed_words.txt``` that contains:
* words present in the datasets
* words present in the filler files, if they are occurring with a word present
in the datasets

This file will be used to load just the needed rows of the distributional space
afterwards, in order to reduce memory usage.

In order to do so, exec the ```extract-needed-words``` command as follows:

```
tfe extract-needed-words \
  --datasets-dirpath absolute_path_to_folder_containing_datasets \
  --fillers-dirpath absolute_path_to_folder_containing_datasets \
  --output absolute_path_to_desired_output_folder \
```

### Datasets format

Here you can find examples of how the datasets files should look like:

#### Pado
```
advise-v	banker-n	sbj	6.0
advise-v	biologist-n	sbj	5.0
advise-v	business-n	sbj	5.3
advise-v	client-n	sbj	3.7
advise-v	customer-n	sbj	3.8
```

#### McRae2
```
abandon-v	baby-n	3.0	2.8
abandon-v	cat-n	4.6	4.8
abandon-v	child-n	4.6	3.1
abandon-v	kidnapper-n	3.9	1.5
accept-v	award-n	1.1	6.6
accept-v	friend-n	6.1	5.8
```

#### Ferretti-instruments
```
serve-v	plate-n	5.9
serve-v	tray-n	6.5
serve-v	glass-n	4.9
serve-v	platter-n	5.8
serve-v	bucket-n	1.4
sweep-v	mop-n	3.7
```

#### Ferretti-locations
```
serve-v	library-n	2.4
serve-v	restaurant-n	7.0
serve-v	hospital-n	5.1
sweep-v	livingroom-n	2.3
sweep-v	bathroom-n	4.8
sweep-v	restaurant-n	6.1
```


### Fillers format

Here you can find examples of how the fillers files should look like:

#### plain format
```
crush-v cane-n 1309.1637438593705
crush-v tank-n 1293.2346720176752
crush-v truck-n 1278.9576614391194
crush-v powder-n 1258.737514156956
crush-v wall-n 1251.8576024713607
frighten-v people-n 4506.529251893827
frighten-v child-n 2490.799204977875
frighten-v horse-n 1602.341678594072
frighten-v death-n 1582.7433623824356  
```

#### deps format

```
advise-v sbj director-n 141.4141
advise-v sbj service-n 141.2552
advise-v obj client-n 1411.5521
advise-v obj government-n 692.2554
advise-v obj member-n 691.736
advise-v obj student-n 678.3795	 
```

## Step 2 - save spaces into numpy/scipy format:

This step produces ```.npz``` or ```.npy``` matrices from raw text spaces.
A ```npz``` matrix is produced from a sparse input, while a ```npy``` matrix
is produced from a dense input.

In order to do so, exec the ```generate-npz-space``` command as follows:
```
tfe extract-needed-words \
  --spaces-dirpath absolute_path_to_folder_containing_DSMs \
  --needed-words absolute_path_to_needed_words_file \
  --output absolute_path_to_desired_output_folder \
```

This will process all the files in the folder passed as ```spaces-dirpath```
parameter.
Note: raw spaces should be in gzipped format, and:
* sparse spaces should have extension ```.sparse.gz```
* dense spaces should have extension ```.dense.gz```


## Step 3 - generate prototypes:

This step produces a ```.npy``` matrix containing prototypes, given a
filler file and a distributional space.

The command works as follows:
```tfe generate-prototypes \
  --space-filepath absolute_path_to_distributional_matrix \
  --fillers-filepath absolute_path_to_fillers_file \
  --num-fillers number_of_fillers \
  --needed-words absolute_path_to_needed_words_file \
  --output absolute_path_to_desired_output_folder \
```

and will generate a file named ```prototypes.[space_filepath].[fillers_filepath].npy```
in the selected output folder.

Note: files containing fillers should have one of the following extensions:
* ```.plain.txt``` if the fillers are not typed
* ```.deps.txt``` if the fillers are typed

## Step 4 - evaluate correlation:

This step evaluates a correlation score given a dataset, a matrix containing
prototypes and a distributional space.

The command works as follows:
```tfe generate-prototypes \
  --space-filepath absolute_path_to_distributional_matrix \
  --dataset-filepath absolute_path_to_dataset_file \
  --prototypes-filepath absolute_path_to_prototypes_file \
  --output absolute_path_to_desired_output_folder \
```
and will generate a file named ```results.[dataset_filepath].[prototypes_filepath].txt```
in the selected output folder.
