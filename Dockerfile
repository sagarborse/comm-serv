# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.6

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /commservice

# Set the working directory to /commservice
WORKDIR /commservice

# Copy the current directory contents into the container at /commservice
ADD . /commservice/

RUN pip install -r requirements.txt

# Install any needed packages specified in requirements.txt
#RUN chmod +x start.sh  && /commservice/start.sh
#EXPOSE 80
EXPOSE 8000
#CMD ["sh", "start.sh"]
