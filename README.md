# Leo Tapie's Portfolio

Welcome to my GitHub portfolio! You'll find a collection of some of my projects and contributions. Feel free to explore and get in touch.

## Table of Contents

- [Projects](#projects)
- [About Me](#about-me)
- [Contact](#contact)

---

## Projects

My main focus for these projects has been to:
- learn about best practices associated with data extraction, cleaning, transformation and predictive modelling
- demonstrate my programming, querying, and visualisation skills
- work on topics I'm interested in

I've added a short description of each project below so you can get an idea of the concepts and skills I've applied - and choose what you wish to look at. 
My thought process and workflow is always explained (in the notebooks or README sections of each projects) and all scripts are thoroughly commented.

### Project 1: [NBA MVP prediction](https://github.com/leotapie/portfolio_projects/tree/main/MVP%20prediction%20project) - Predicting the next MVP based on historical stats data. 

Steps:
  1) Scrapping data from the web
  2) Cleaning and combining the data, as well as exploratory anaysis (EDA)
  3) Building 2 predictive models (Ridge Regression and Random Forest). Success was measured by the ability to predict the Top 5 (assessed through back testing). 

Key tools/library/concepts used:
- Scraping: `request`, `bs4`, `selenium` and `pandas` libraries. Simple and more complex data parsing (i.e., using browser driver).
- Clean Up: `pandas` library and data cleansing procedures. EDA: **correlation analysis**.
- Modemming: `pandas` and `sklearn` libraries. Concepts: **Machine learning, error metric & back testing**.


### Project 2: [Citi Bike Rental](https://github.com/leotapie/portfolio_projects/tree/main/Citi%20Bike%20Rides) - Analyse NYC's city bike trips from 2016.

Steps:
  1) Cleaning and combining the data
  2) Load the data into a Postgre database and create views
  3) Visualise the the data in Tableau

Key tools/library/concepts used:
- Cleaning and loading data: `pandas` and `sqlalchemy` libraries.
- Databse creation: `PostgreSQL` through the `Postbird` client. 
- Visualisation: `Tableau`.


### Project 3: [Subscriber Cancellations Data Pipeline](https://github.com/leotapie/portfolio_projects/tree/main/Subscriber%20Cancellations%20Data%20Pipeline) - Automated bash+python pipeline to clean SQLite database. 

Steps:
  1) Explore starting database, determine data cleaning steps and table formats for cleaned database.
  2) Write the main script: `cleanse_data.py` - which extracts, transforms and load the data, and contains unit tests and error/updates logging.
  3) Write the bash script: `script.sh` - which calls on the python cleansing script and moves/updates the final cleased database in the `/prod`folder (through user prompts)
 
Key tools/library/concepts used:
- Cleaning and loading data: `pandas` and `sqlite3` libraries
- Checks and error handling: unit tests and logger (automated updates to changelog)
- Computational efficiency: clean and load new data only to production database
- bash scripting


---

## About Me

I'm French but have been living in England for the last 8 years (London based these days). I've had the chance to grow up in Poland, Czech Republic and France, and
come from a multi-cultural familly - that's probably why I love travelling and meeting people with different backgrounds! 

I'm a mechanical engineer by education - I studied in Leeds for 4 years. And a system engineer by trade - I worked at Jaguar Land Rover (JLR) for 3.5 years. I worked in multiple teams during my time at JLR, but most relevantly worked on system integration for hybrid and future zero-carbon powertrains (BEV and FCEV for those interested in the autimotive industry!). My interest in data anlysis and modelling really began then, where I was responsible for building a tool designed to draw insights from drive cycles test data. The tool's key outputs included a structured report and an interactive interface that contained visualisation graphs. Unfortunately, I can't share any of this publicly but would be more than happy to chat about it if anyone out there is interested! 

For both personal (I travelled around Asia for 6 months and relocated to London) and professional (I realised that I wanted to work in Data) reasons I decided to leave JLR after 3.5 years - I learnt a lot and got to work on cool forward-thinking projects in an industry I'm passionat about, but it was time to move on! 

Here we are... I'm looking for my first data analyst/scientist job! I've always been fascinated by the challenge of finding solutions to a problem (and the satisfaction it brings!). Finding the *right* visualisation to illustrate an inisght or message is also something I enjoy. And I like understanding how things work (no suprise there, engineer!) - mainly: complex interactions in a system, influences and correlations between variables and the big picture. The previous statement equally applies to: optimising energy usage in a hybrid vehicle, people's acceptance of sustainable alternatives (products, services and behavioural), and the holistic approach required of a energy system with a high proportion of renewables - all personnal interest of mine!

---

## Contact

- Email: leotapie(at)gmail(dot)com
- LinkedIn: [Leo Tapie](https://www.linkedin.com/in/leo-tapie-81a101132/)

---

Thank you for visiting my portfolio, feel free to reach out!
