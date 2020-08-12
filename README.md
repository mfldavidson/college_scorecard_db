# College Scorecard Database
#### _Final project for [SI 564](https://www.si.umich.edu/programs/courses/564) Winter 2020_

I created a database and loaded it with (some of) the 2014-15 US Department of Education College Scorecard data.
This data was sourced from [the US Department of Education](https://collegescorecard.ed.gov/data/) 
on March 7, 2020. I used the data in the database to answer questions using SQL queries.

This repo includes:
- `run.py`: program to run to create and load the database
- `create_db.py`: functions to create the database and tables
- `load_db.py`: functions to get the data, clean it, and load it into the database
- `vars.py`: global variables to be used in the above programs
- `QUESTIONS.md`: the questions I posed, SQL queries used to answer them, and the results
- `ERD.png`: entity relationship diagram of the database and tables
- `college_scorecard.sql`: a sample of the database created and loaded using `run.py`

## Initial Setup (First time only)

1. Clone this repo to your computer by using the command line to navigate to the directory/folder 
where you want it and entering `git clone https://github.com/mfldavidson/college_scorecard_db.git`.

1. Create a virtual environment (`python3 -m venv whateveryouwanttonameit`) wherever you keep 
your virtual environments.

1. Activate the virtual environment (`source whateveryounamedthevirtualenv/bin/activate` if you are on a Mac, 
or `source whateveryounamedthevirtualenv/Scripts/activate` if you are on a PC).

1. Install all necessary libraries by navigating to the repo and then running the command 
`pip install -r requirements.txt`.

1. Ensure your environmental variables are set with `username` and `password` corresponding to the MySQL 
Server in which you want to create the database (must have read-write access).

## Running the Program

1. Ensure your virtual environment is activated--if not, see step 3 above.

1. Ensure you are in the `college_scorecard_db` directory in your command line.

1. Enter `python run.py` in your command line.
