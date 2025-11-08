
FROM mcr.microsoft.com/playwright:focal

#Update packages and install pip
RUN apt-get update && apt-get install -y python3-pip

# set working directory
WORKDIR /app

# copy files from local directory to build image
COPY ./ /app 

# install packages 
RUN pip install --no-cache -r requirements.txt

# install playwright browsers
RUN python3 -m playwright install

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py

CMD [ "python", "app.py" ]

