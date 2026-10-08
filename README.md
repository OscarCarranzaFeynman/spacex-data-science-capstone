# SpaceX Falcon 9 Landing Prediction — IBM Data Science Capstone

Completed SpaceX capstone notebooks, dashboard, datasets and verified results.

## Contents
- `notebooks/`: data wrangling, SQL EDA, visual EDA, Folium maps and classification.
- `dashboard/`: interactive Plotly Dash application and its input CSV.
- `data/`: wrangled 90-launch dataset and 80-column encoded feature matrix.
- `results/`: classifier comparison and launch-site analysis.
- `report/`: final presentation in PDF format (added when complete).

## Run
Install the packages in `requirements.txt`, then open the notebooks in Jupyter. Notebook data downloads use IBM Skills Network sources. For the dashboard, run from the `dashboard` directory:

```sh
python spacex-dash-app.py
```

Open the local address printed by Dash. Select a launch site and adjust the payload range to update the charts.

## Results and scope
The wrangling/model dataset contains 90 launches, including 60 successful landing outcomes (66.67%). The dashboard/map sample contains 56 launches; the SQL sample contains 101 records. These samples must not be treated as identical.

All four classification models achieved 83.33% on the 18-record test split. The decision tree achieved the highest cross-validation score in this run. The lab standardizes before splitting; a production workflow should fit preprocessing inside cross-validation to avoid data leakage. Results are educational, not production validation.

Data and laboratory material originate from IBM Skills Network. Assistance: ChatGPT.
