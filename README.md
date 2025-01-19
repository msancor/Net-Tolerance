# Net-Tolerance
Repository made for didactic purposes. We reproduce some of the results of the research article: "Albert, R., Jeong, H. &amp; Barabási, AL. Error and attack tolerance of complex networks. Nature 406, 378–382 (2000). https://doi.org/10.1038/35019019".

--- 
## What's inside this repository?

1. `README.md`: A markdown file that explains the content of the repository.

2. ``modules/``: A folder including 2 Python modules used to construct random networks using the Erdös-Renyi model and scale-free networks using the Barabási-Albert model. The files included are:

    - `__init__.py`: A *init* file that allows us to import the modules into our Jupyter Notebook.

    - `random.py`: A Python file including the `RandomNetwork` class used to build random networks using the Erdös-Renyi model.

    - `scale_free.py`: A Python file including the `ScaleFree` class used to build scale-free networks using the Barabási-Albert model.

3. ``source/``: A folder including 4 Python modules used to make the plots presented in "Albert, R., Jeong, H. &amp; Barabási, AL. Error and attack tolerance of complex networks. Nature 406, 378–382 (2000). https://doi.org/10.1038/35019019". The files included are:

    - `__init__.py`: A *init* file that allows us to import the modules into our Jupyter Notebook.

    - `initial_plots.py`: A Python file including functions that help obtain Fig. 1 of "Albert, R., Jeong, H. &amp; Barabási, AL. Error and attack tolerance of complex networks. Nature 406, 378–382 (2000). https://doi.org/10.1038/35019019" along with their degree distribution plots.

    - `diameter.py`: A Python file including functions that help obtain Fig. 2 of "Albert, R., Jeong, H. &amp; Barabási, AL. Error and attack tolerance of complex networks. Nature 406, 378–382 (2000). https://doi.org/10.1038/35019019".

    - `components.py`: A Python file including functions that help obtain Fig. 3 of "Albert, R., Jeong, H. &amp; Barabási, AL. Error and attack tolerance of complex networks. Nature 406, 378–382 (2000). https://doi.org/10.1038/35019019".

    - `cluster_dist.py`: A Python file including functions that help obtain Fig. 4 of "Albert, R., Jeong, H. &amp; Barabási, AL. Error and attack tolerance of complex networks. Nature 406, 378–382 (2000). https://doi.org/10.1038/35019019".


4. `images/`: A folder including the obtained plots.

