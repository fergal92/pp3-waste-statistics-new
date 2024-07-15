# Annual Waste Data Analyser 
Welcome to the annual waste data analyser. This is a command line applicatoin built with Python. This program is connected to a google sheet database which stores the data for a fictional waste collection company. The purpose of the program is to anaysle the data from the command line.

Access the program here - [Waste Data Analyser](https://waste-data-analyser-3742936dc8c7.herokuapp.com/)

## Responsive image
![Responsive Image]()
## User stories

### As a user I can use the  program to enter valid data into a spreadsheet from the command line
#### Acceptance Criteria:
- Enter data via the CLI
- Ensure the data is validated appropriately
- The data is saved into the spreadsheet
#### Tasks:
- Create an input option for the program
- Create validation parameters for the data 
- Link the sheet via an API to the program to save all data entered 

### As a user I can use the  program to analyse how much profit the waste collecors made 
#### Acceptance Criteria:
- Allow the user to see how much profit was made
#### Tasks:
- Create functions that calculate the tonnes collected with the price list to find the profit
- display the profit to the user

## Agile Methodologies
### GitHub Projects
Link to the GitHub project page that was used to manage the website build. Items were added to the kanban board and worked through. Items were linked to the project repo and closed off as the project progressed. [github project board](https://github.com/users/fergal92/projects/3/views/1)

## Features
### Existing Features
#### Simple terminal menu
- Simple terminal menu has been incorporated into the project to ensure seamless and consistent navigation 

#### User input
- The user can input data into the spreadsheet in order to complete the annual waste collection data.
- The user is prompted to enter data 4 times as this corresponds to the monthly data for each waste type
- This data input is validated so that they cannot enter a negative number and they can enter a positive integer up to 400 Tonnes. 400 Tonnes is the upper limit of what the program expects
- When the user completes a successful data input of all 4 waste types, the current worksheet with the newly entered data is printed to the terminal to show the user where they are at

#### Calculate Profit
- The user can choose to calculate the profit for one of the three collector sheets.
- The profit cannot be calculated unless the waste data has been entered for the year. There is a validation in place for that
- The total waste collected and total profit for the year is calculated and input into the sheet
- At the end of the profit calculation the current worksheet is printed to the terminal to show the user the profit

### Features left to implement 
#### Data analysis
- More comprehensive data analysis features could be implemented to add further value to this project.
- Graphs could be added to visualise the data.
- Python packages like Pandas and matplotlib could be utilised to achieve this outcome.
## Technologies Used
- [GitPod](https://www.gitpod.io/) - was used as the main tool to write and edit code.
- [Git](https://git-scm.com/) - was used for the version control of the website.
- [GitHub](https://github.com/) - was used to host the code of the website.
- [Python](https://www.python.org/)
- [Am I Responsive](https://ui.dev/amiresponsive) - was used to generate an image of the website across different screen types and resolutions
- [Heroku](https://id.heroku.com/login) - Was used to deploy and host the project

## Testing
Please refer to the [TESTING.md](TESTING.md) file for all testing documentation
## Deployment

### Deployment to Heroku
The heroku app was deployed at the begonning of the project to ensure any issues were encountered early and could be resolved.

The live link to the site can be found here https://waste-data-analyser-3742936dc8c7.herokuapp.com/

## Credits
### Content

### Media

## Future improvements

## Acknowledgements
- [Iuliia Konovalova](https://github.com/IuliiaKonovalova) - My mentor Julia was very supportive during this project. She certainly pushed me to complete a high standard of project especially for the readme and testing sections. I took inspiration from her README.md and TESTING.md files for my own.
- [Happiness Generator](https://github.com/broken-helix/happiness/) - My first hackathon project. I learned so much from participating in this project and team. We won the March hackathon for 2024 and my team members were a great source of inspiration for me.