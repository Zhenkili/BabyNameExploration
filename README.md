# ece229
Project Repo for Computational Data Analysis Course

This project is a US NEwborn Analysis System. The purpose is helping users to search the trend of thier name of each year and analyse the name by year, region and gender.

visit the project website http://34.212.234.66:8050

## Table of Contents  
1. [Package Dependencies](#PackageDependencies)
2. [File Structure](#FileStructure)
3. [Run Code](#run)
4. [User Story](#story)
5. [About Dataset](#data)
6. [Testing](#TestEnv)
7. [Documentation](#doc)

<a name="PackageDependencies"></a>

## Package Dependencies

To run any of the module in this codebase, ensure the newest version of [python3](https://www.python.org/downloads/) or the newest version of [Anaconda](https://docs.anaconda.com/anaconda/install/) is installed on the machine. Further, ensure the respective binary is in the list of PATH variables. 

The project depends on numpy, dash, dash-bootstrap-components

For installing the Environment Config:
<pre>
$ pip install numpy
$ pip install dash
$ pip install dash-bootstrap-components
</pre>

<a name="FileStructure"></a>

## File Structure
   - client
      - baby-names-state.csv _(should be added manually)_ 
      - app.py
      - EntryHomepage.py
      - nameTrend
      - top5Name,py
      - USHeatMap.py
   - test
      - \_\_init\_\_.py
      - test_callback.py
      - test_ui.py
   - doc
      - build
      - source
   - EntryHomepage.py

<a name="run"></a>

## Run Code

1. Download or git clone this github repository. 
<pre>
git clone https://github.com/js-konda/ece229.git
</pre>

2. Install the necessary dependencies:
#### Using Pip
<pre>
pip install -r requirements.txt
</pre>

3. Download the [dataset](https://www.kaggle.com/datasets/ironicninja/baby-names) and place unzipped dataset into the client directory

3. For Entering the Homepage Dashboard:
<pre>
python client/EntryHomepage.py
</pre>

4. The output will be displayed in port **8050**

<a name="story"></a>

## User Story
Choosing a name is one of the most important decisions parents have to make. It is one
of the child’s first milestones and can shape its future. A name can signify that the baby
is accepted as one of the family members.
By checking the trend of names in the specific area, one can draw inspiration from it
which makes it easier to name the child. For those who already have several options,
we can help them make the desicion based on the data we have.

Our proposed solution is to analyze the differences in naming between regions and the
trend of naming from 1910 to 2021. We try to answer questions like which name is most
popular in the past 10 years in California, does there exist an obvious distinction
between east and west or when did my name become a hit nationwide. We will create
interactive histograms and plots to allow users to find the trend of a specific name
during a specific time period within a state/nationwide. We will also make a
recommendation by showing the trend changes of top 5 most popular baby names over
the years.

The real world application of this solution is that it can serve as a reference that helps
parents better name their children, such as avoiding the most popular names, finding
gender-neutral names, etc.

<a name="data"></a>

## About Dataset

This [dataset](https://www.kaggle.com/datasets/ironicninja/baby-names) consists of American newborn babies' names statistics from 1910 to 2021.
It contains important information for those names including gender, state and number of
those names in a given area during a certain year.
<a name="TestEnv"></a>

### Testing
1. Test Environment
<pre>
$ pip install pytest
</pre>

2. Run test
To run pytest, you will need to navigate to root directory and type the following command
<pre>
$ pytest -v
</pre>

<a name="doc"></a>

## Documentation
Our project used Sphinx to create a documentation static website as an ongoing part of development. Open **./docs/_build/html/index.html** file in web browser to see the docs.

or visit [doc](./doc/build/html/index.html)



