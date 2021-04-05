#
#   Image with a jupyter environment and the bioformats package
#
#   Building the image: 
#
#       `docker build -t bioformats-env .`
#
#       Run the command in the same directory as this Dockerfile
#
#       Explanation:
#       -  `-t bioformats-env` names the image we built
#       -  The period `.` represents the current directory
#
#   Running the container: 
#       
#       To run jupyter:
#           `docker run --rm -v ${PWD}:/home/jovyan -it -p 8888:8888 bioformats-env` (Powershell / bash?)
#           `docker run --rm -v "%cd%":/home/jovyan -it -p 8888:8888 bioformats-env` (Windows cmd.exe)
#
#       To open a terminal inside the container
#           `docker run --rm -v ${PWD}:/home/jovyan -it bioformats-env bash`
#
#       Run the command in a directory that contains both your source and data
#           files, or add another volume mount with a second `-v ...` Try to
#           run this command in the example_notebook folder.
#
#       Explanation:
#       -  `--rm` destroys the container on exit
#       -  `-d` detaches the container from this terminal, logs can be followed in
#           the Docker GUI
#       -  `-p 8888:8888` binds network ports 8888 on the host and container. This
#           is necessary to open Jupyter in your browser
#       -  `-v "${PWD}":/home/jovyan` binds the host directory in which the command
#           is ran to the container directory in which Jupyter is running.
#
#   Compiled by Wouter Duverger (2021)
#


# Start from base images with Java and Python
FROM openjdk:17-slim
COPY --from=python:3.6 / /

# Create a non-root user named jovyan (expected by Jupyter)
RUN adduser --system --group jovyan

# As root, install the necessary python libraries. Bioformats needs to be
# installed after numpy, otherwise the build will fail
COPY requirements.txt requirements.txt
RUN pip install numpy==1.19.3 && pip install -r requirements.txt

# Ensure jovyan owns all files in their home folder. Matplotlib won't run if
# that is not the case
RUN chown -R jovyan /home/jovyan

# On startup, run Jupyter Lab as the non-root user in their home directory
WORKDIR /home/jovyan
USER jovyan
CMD jupyter lab --ip=0.0.0.0
