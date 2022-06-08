.. ece229_group4_project documentation master file, created by
   sphinx-quickstart on Wed May  4 17:21:24 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ece229 group4 project's documentation!
=================================================

This project is a **US NEwborn Analysis System**
The purpose is helping users to search the trend of thier name  of each year and analyse the name by year, region and gender.

Package Dependencies
--------------------
The project depends on numpy, dash, dash-bootstrap-components

**For installing the Environment Config**
.. code-block::
   pip install numpy
   pip install dash
   pip install dash-bootstrap-components

File Structure
--------------
**Structure of the project**
.. code-block::
   - client
      - baby-names-state.csv _(should be added manually)_ 
      - app.py
      - EntryHomepage.py
      - nameTrend
      - top5Name,py
      - USHeatMap.py
   - doc

Start the project
--------------------

**For Entering the Homepage Dashboard:**
.. code-block::
   python client/EntryHomepage.py

The output will be displayed in port **8050**





Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
