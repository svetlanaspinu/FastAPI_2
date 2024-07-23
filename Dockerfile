
# this containes all the steps necessary to creata a own custom image 
    # all this steps are on docker + python documentation
#use the python image from the docker-app the python version
FROM python:3.10.14

#setting the working directory
WORKDIR /usr/src/app_2

#copying requirement.txt file/ IF WE MAKE ANY CHANGES IN THE FILE WE DONT NEED TO RUN PIP INSTALL A SPECIFIC MODULE, BECAUSE WE ATTACH THE FILE WITH ALL THE LIBRARIES
COPY requirements.txt ./

# this command install all the requirements from .txt file
RUN pip install --no-cache-dir -r requirements.txt

#it will copy all of the code and it will paste it in the docker current directory WORKDIR /usr/src/app
COPY . .

#the command that i want to run starting the container
CMD ["uvicorn", "app_2.main:app", "--host", "0.0.0.0", "--port", "8000" ]