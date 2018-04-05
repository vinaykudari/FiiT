# FiiT - TheFinderBot
<img align="left" src='/.github/assets/logo.png'>

***

Lost anything ? I can help you find stuff :) Also you can also inform me any item you see lying around I'll help you to connect with the person who lost his.

***

## How am I created ?

**FiiT** is built using **[DialogFlow](https://dialogflow.com/)** and **Flask**

## Dependencies

- Python
- Pip
- Flask

## How to deploy ?

- Sign in to DialogFlow and create an agent
- Pack all the files in the repo except _app.py, README.md and .githum/assets_ in a zip file
- Go to setting of your agent and upload the packed zip in *Export and Import* tab
- In Fulfilment tab enter your_'public_ip'_/webhook 
- Start the **flask** server with `sudo python app.py`


