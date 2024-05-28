FROM ultrafunk/undetected-chromedriver


WORKDIR /app

COPY ./ /app


# install packages 
RUN pip install --no-cache -r requirements.txt

#install chrome and driver
RUN python setup_chrome.py

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py


CMD [ "python", "app.py" ]
