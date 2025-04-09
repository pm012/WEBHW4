# WEBHW4

Create a web application with routing for two html pages: index.html and message.html.

Also:

Process static resources during program operation: style.css, logo.png;

Organize work with the form on the message.html page;
In case of a 404 Not Found error, return the error.html page
Your program runs on port 3000

To work with the form, create a Socket server on port 5000. The algorithm of work is as follows. You enter data into the form, it enters your web application, which forwards it for further processing using a socket (UDP protocol), to the Socket server. The Socket server translates the received byte string into a dictionary and saves it in the json file data.json in the storage folder.

The format of the data.json file is as follows:
```json
{
  "2022-10-29 20:20:58.020261": {
    "username": "krabaton",
    "message": "First message"
  },
  "2022-10-29 20:21:11.812177": {
    "username": "Krabat",
    "message": "Second message"
  }
}
'''
Where the key of each message is the time of receipt of the message: datetime.now(). That is, each new message from the web application is appended to the storage/data.json file with the time of receipt.

Use a single main.py file to create your web application.

Run the HTTP server and the Socket server in different threads.
                                    ADDITIONAL TASK
Create a Dockerfile and run your application as a Docker container
Use the voluemes mechanism to store data from storage/data.json outside the container

TIP
To implement the voluemes mechanism, you need to check for the existence of the storage directory and the data.json file when starting the application. And if they do not exist, then create them.


Instructions to test:
1. If you want to launch using docker-composer:
```bash
sudo docker-compose up --build 
```
2. If you want to launch the app using Docerfile:
```bash
docker build -t webhw4 .
docker run -p 3000:3000 -p 5000:5000/udp -v $(pwd)/storage:/app/storage webhw4
```
3. If you with to launch it locally from file just run main.py
4. When app is running navigate to http://localhost:3000
5. Click Send Message link
6. Send message and check the data.json file

