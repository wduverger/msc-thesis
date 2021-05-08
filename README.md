Polarisation-resolved super-resolution microscopy
---

[![Automated build](https://github.com/wduverger/msc-thesis/actions/workflows/main.yml/badge.svg)](https://github.com/wduverger/msc-thesis/actions/workflows/main.yml)

This repository contains the data and source code for my master thesis  at Lund University, 
which you can find [here](/MSc%20thesis%20Wouter%20Duverger.pdf). 

There are a couple of folders in this repository. `data/` contains all data necessary to generate the figures in my thesis. The figures themselves are created by scripts in the `code/` folder and saved in `figures_generated/`. `latex/` contains the source files for the thesis document itself, and `figures_other/` include handmade and downloaded graphics included in the thesis.

To run everything the code, you need a python environment with the packages listed in [requirements.txt](requirements.txt). Two of them can be tricky to install: `opencv-python` must be on exactly version 4.0.1.24, and `python-bioformats` requires a Java Development Kit and a C compiler ([installation instructions](https://pythonhosted.org/javabridge/installation.html)). Alternatively, you can install Docker and run the code in a container:

```bash
docker pull wduverger/msc-thesis        # Download container from Docker Hub,
docker build -t wduverger/msc-thesis .  # ... or build it yourself.

# Compile figures
docker run --rm -itv ${PWD}:/workspace wduverger/msc-thesis make -j8 figures

# Compile report
docker run --rm -itv ${PWD}:/workspace texlive/texlive bash -c "cd workspace && make thesis"
```

(C) Wouter Duverger, May 2021
