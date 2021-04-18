This repository contains the data and source code for my master thesis on 
"Polarisation-resolved super-resolution microscopy" at Lund University, 
which you can find [here](/latex/Wouter%20Duverger%20MSc%20thesis.pdf).

There are a couple of folders in this repository. `data/` contains all data necessary to generate the figures in my thesis. The figures themselves are created by scripts in the `code/` folder and saved in `figures_generated/`. `latex/` contains the source files for the thesis document itself, and `figures_other/` include handmade and downloaded graphics included in the thesis.

To run everything the code, you need a python environment with the packages listed in [requirements.txt](requirements.txt). Two of them can be tricky to install: `opencv-python` must be on exactly version 4.0.1.24, and `python-bioformats` requires a Java Development Kit and a C compiler ([installation instructions](https://pythonhosted.org/javabridge/installation.html)). Alternatively, you can install Docker and run the code in a container:

```bash
docker pull wduverger/msc-thesis        # Download container from DockerHub,
docker build -t wduverger/msc-thesis .  # ... or build it yourself.
docker run --rm -itv ${PWD}:/workspace wduverger/msc-thesis bash
```

You can run `make` inside a container to create all figures, or just run each of the python scripts in `code/`. Make sure to run them with `code/` as the working directory, not from the repository root.

(C) Wouter Duverger, May 2021