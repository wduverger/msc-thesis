#
#   Image with a python environment with bioformats, and opencv
#
#   Building the image: 
#
#       `docker build -t wduverger/msc-thesis .`
#
#       Run the command in the same directory as this Dockerfile
#
#       Explanation:
#       -  `-t wduverger/msc-thesis` names the image we built
#       -  The period `.` represents the current directory
#
#   Running the container: 
#
#       To open a terminal inside the container
#           `docker run --rm -itv ${PWD}:/workspace  wduverger/msc-thesis bash`
#
#       Run the command in a directory that contains both your source and data
#           files, or add another volume mount with a second `-v ...` Try to
#           run this command in the example_notebook folder.
#
#       Explanation:
#       -  `--rm` destroys the container on exit
#       -  `-it` opens an interactive terminal
#       -  `-v "{PWD}:/workspace` binds the host directory in which the command
#           is ran to the container directory in which Jupyter is running.
#
#   Compiled by Wouter Duverger (2021)
#


# Start from base images with Java and Python
FROM openjdk:17-slim
COPY --from=python:3.6 / /

# Set proper time zone
RUN rm -rf /etc/localtime && ln -s /usr/share/zoneinfo/Europe/Brussels /etc/localtime

# As root, install the necessary python libraries. Bioformats needs to be
# installed after numpy, otherwise the build will fail
RUN apt-get update && apt-get install -y python3-opencv
RUN pip install numpy==1.19.3
COPY ./code/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# If no arguments are supplied, run `make figures`
WORKDIR /workspace
CMD make figures