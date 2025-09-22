# Premier League Player Statistics Dataset ⚽️
#### Streamlit Dasboard Link: https://ncashy--usage-dashboard-run.modal.run/#premier-league-players-dashboard
---
### I’ve always been fascinated by player insights in the Premier League, especially since my father and I share a passion for watching the matches together. We’re both big Liverpool fans, Go Reds!❤️‍🔥 This project gave me a chance to dive deeper into the stats behind the game we love and build something meaningful from it. I'm also hoping to expand on this project later with more datasets and predictive analytics, but just starting with this for now. 

## About the Dataset

This dataset contains detailed player statistics from the Premier League — one of the world’s most-watched football leagues. It covers multiple seasons and tracks various player metrics including goals, assists, nationality, and playing positions.

> **Note:** This dataset is **not authored by me**. It was originally created by a contributor on [Kaggle](https://www.kaggle.com/), a popular platform for datasets and data science projects.

---

## Context

The Premier League (English Premier League or EPL) is the top tier of English football, with 20 clubs competing from August to May.

- Teams play 380 matches (home and away fixtures).
- Points system: 3 for a win, 1 for a draw, 0 for a loss.
- Bottom 3 teams relegated; replaced by 3 promoted teams from the Championship.

This dataset allows exploration of how player factors like age, nationality, and club influence performance.

---

## Dataset Details

- Data scraped via Python using BeautifulSoup4.
- Weekly updates to reflect real-time player stats.
- Some stats missing for specific positions (e.g., goalkeepers lack shooting accuracy).

---

## Data Source & Credits

- **Data Source:** [PremierLeague.com](https://www.premierleague.com/)  
- **Original Dataset Author:** Rishikesh Kanabar

---

## ⚠️ Known Issues

- "Goals per match" has some anomalously high values due to initial HTML load errors during scraping.
- Fixes are planned analytically, avoiding direct scraping fixes.
- The dataset is not currently up to date and was last updated 5 years ago.

---

## My Project Workflow

This is my **very first dashboard project**, and I’m really proud of what I’ve learned throughout the process! Here’s a quick overview of how I built this:

1. **Dataset Acquisition**  
   I downloaded the Premier League player statistics dataset from Kaggle, which provided a rich set of football player data.

2. **Data Cleaning**  
   I cleaned and organized the data using Microsoft Excel — fixing headers, formatting columns, and preparing the dataset for analysis.

3. **Database Creation**  
   Using the cleaned CSV file, I created a relational database in **Supabase** with SQL, which allowed me to store, query, and manage the data efficiently.

4. **Development Environment**  
   I connected the Supabase database to **VSCode**, which made it easy to manage both the backend database and frontend code in one place.

5. **Dashboard Creation**  
   I built an interactive dashboard using **Streamlit**, where I visualized player statistics, nationalities, positions, and key performance metrics in charts.

6. **API and Deployment**  
   To handle API keys and secure environment variables, I used **Modal**, which simplified deployment and management of secrets.

---

### Reflection

This project taught me a lot about data cleaning, database management, connecting backend services, and frontend dashboard development — a solid foundation for future data science and web app projects. I’m excited to continue learning and improving!


## Contributions & Feedback

Feel free to open issues, submit pull requests, or suggest improvements!

---


