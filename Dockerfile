# cgi and cgitb module dependencies so using 3.12 version of python
FROM python:3.12-alpine
# setting up working directory 
WORKDIR /web
# site releated requirements maintained in the following files
COPY site-requirements.txt .
# Installing latest image
RUN pip install -r site-requirements.txt
# Ezhil Source setup in docker 
COPY ./ezhil ./ezhil
# uploading static site contents 
COPY ./dynamic/dist ./
# following python path is used to run python script from subprocess context TODO: 
ENV PYTHON3 /usr/local/bin/python3
# for readablity 
EXPOSE 8080
# Executing the command
CMD ["python3", "-m","ezhil.EZWeb"]