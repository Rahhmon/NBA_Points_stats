# NBA_Points_stats
Downloads the data according to each mach in this season, and shows up the result in a PLOTLY DASHBOARD.

This repository scraps data of NBA matches and pass to a csv file, where will be shown in a dashboard gerated by DASH-PLOTLY.

The general idea for the project was, to create a tool able to support sports betting analysis in fields like: Points per: Quarter/Half/Match in a range of n_matches played, either they were playing in home, away, or both.

This starting files contests the following season: 22-23 NBA Season.

Is easy to add more leagues to the repository, you just have to add more links to the web scrapping file "nba_scraping.py".

To update the file with the most recent data, just click Update Matches button, or than call the method "nba_scraping.update_csv_matches()"

The idea of the dashboard is to show the most frequent stats in the past n-th games by team. The chosen graphs were Scatter Plots, where each plot will mean a match.
