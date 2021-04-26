# The Code Directory

This directory should store all code for the respective repository project. Also, keep data cleaning and analyses separate for example:  

## Protocol

To ensure replicability, we want to keep a clean and easy to read/understand filing structure. To do this, we want to create separate files for data cleaning, analysis, and presentation (e.g. mapping or html files) 

### File naming conventions

`type_content.extension`

#### Data files
* `data.r` or `data.py` should be where you clean, download, merge, or do any work on the data. If you require multiple data cleaning files, prefix the script with the word `data`. For example: 
	* `data_infogroup.py` would refer to working with infogroup data.
	* `data_census.r` would refer to working on census data.

#### Analysis files
* `analysis.r` or `analysis.py` are file names for doing your analysis. 
	* If you are running different types of analyses, make sure to prefix the file name with `analysis` (e.g. `analysis_regressions.r`, `analysis_pca.py`)

#### Mapping files
* `map.r` or `map.py` and follow the same structure as above if you need more than one mapping file. 