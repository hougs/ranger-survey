# BRC Ranger Retention Survey Analysis

For the last few years the Black Rock Rangers have sent out approximately
the same survey to all rangers who have volunteered in the last 5 years.
This repo contains code of intra and inter year analysis as well as some
funny processing stuff for pulling responses into google sheets for qualitative
analysis.

## How to run it
This was built using Python 3.6.8. To run it, you should install all of 
its dependencies in a new environment.

    pip install -r requirements.txt

You will also need two directories -- `img/` and `data/`. You should download
the current survey responses and put them in the `data/` directory. You can 
then run the script for generating plots:

    python RangerRetentionSurvey.py --input_data path_to_data.csv
    

## Hey! Be careful.
Source data and results are considered very sensitive. So, if you are working
on this repo, please be extra careful to not check in any data or results. If
you run the Jupyter Notebook, please clear the output before committing back
to the repo. I'll add some pre commit hooks to make sure this happens, but,
consider yourself warned.


