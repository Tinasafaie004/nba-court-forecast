# NBA Court Forecast

An in-progress machine learning project that will estimate, before tipoff, each NBA team's chance of winning and the likely scoring margin. It uses real game data from the [BALLDONTLIE API](https://www.balldontlie.io/).

**Status: 1 of 7 milestones complete.** There is no prediction model yet. The project can currently fetch data from the API and save it as a snapshot.

## What works today

- `fetch-teams.py` downloads team data and saves it to `data/raw/teams_response.json`.
- `fetch-games.py` downloads five games from the 2024 season and saves them to `data/raw/2024-games_response.json`.
- Each snapshot records when the data was retrieved, the endpoint, and the query used, so later work can start from a known copy of the data.

## Roadmap

- [x] **Milestone 1:** Connect to the API, inspect five games, and save a snapshot
- [ ] **Milestone 2:** Collect historical games and create a clean game table *(next)*
- [ ] **Milestone 3:** Create features using information available before tipoff
- [ ] **Milestone 4:** Explore team performance and explain patterns
- [ ] **Milestone 5:** Compare baseline predictions with initial ML models
- [ ] **Milestone 6:** Evaluate on later games and check probability quality
- [ ] **Milestone 7:** Build a dashboard and document the findings

## Two rules for the model

- **Only use what was known before the game.** A pregame prediction can't use that game's final score or stats, because that information wouldn't exist yet.
- **Test on later games.** Training on earlier games and testing on later ones matches how the model would really be used.

## Tech stack

Python, Pandas, Requests, and the BALLDONTLIE API. scikit-learn is planned for the modeling milestones.

## Run it

You'll need Python and a BALLDONTLIE API key.

1. Install the dependencies:

   ```bash
   pip install requests python-dotenv pandas
   ```

2. Create a file named `.env` in the project folder. Git ignores this file, so your key stays private:

   ```text
   BALLDONTLIE_API_KEY=your_key_here
   ```

3. Run either script:

   ```bash
   python fetch-teams.py
   python fetch-games.py
   ```

Running a script replaces its saved snapshot in `data/raw/`.

## Project files

```text
nba-court-forecast/
├── data/raw/
│   ├── 2024-games_response.json
│   └── teams_response.json
├── fetch-games.py
├── fetch-teams.py
└── README.md
```
