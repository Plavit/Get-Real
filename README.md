<img id="GetReal-logo-text" width="400" src="assets/Logo-text.png">

# Get-Real
HackPrague 2021 project

## Description
This project creates a dashboard for people to easily compare available real estate options and make better decisions
![image](https://user-images.githubusercontent.com/22589593/137628652-1964cece-dc28-4db9-9ff5-24482d285ade.png)

## Deployment
To run locally:

1) Get requirements in requirements.txt through
`npm install`
2) Run the app with:
`$ python app.py`

Can be also deployed online via Heroku or a similar online hosting service.

## Architecture
The app gets data through scrapers via Apify on bezrealitky.cz and from Flatzone, both in javascript. Using Python, we transform the data to csv files and compile via Dash Plotly to visualise as an interactive graphics map via a web app.

A further AI data processing using Python Scikit is planned, but not yet implemented. 
![image](https://user-images.githubusercontent.com/22589593/137628385-dacf80de-846f-49fa-b2a0-98b80f8b88eb.png)

## Links
Apify API store listing: https://apify.com/fcoudy/bezrealitkyscraper
Devpost link: https://devpost.com/software/get-real

## Demo
See the presentation here:
https://youtu.be/ETPGva9MdXM

## Presentation
See the [PowerPoint slides](docs/GetReal-present.pdf)

## Team
Created by Small Side Devs, a team formed at HackPrague 2021

![image](https://user-images.githubusercontent.com/22589593/137628346-7735ff5a-01e1-4d36-9cae-bb11f63935ca.png)


## Disclaimer
Many thanks to Lukas Krivka from Apify for a huge help getting our API scraper to work and Jiri Eckstein from Flatzone for help with their platform.
