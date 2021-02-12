import pandas as pd
import re


def get_results(year, last_week):
	teams_url = "https://www.pro-football-reference.com/years/" + str(year) + "/"
	scraped_tables = pd.read_html(teams_url)

	# Get list of teams that participated in current league year
	afc = scraped_tables[0]
	nfc = scraped_tables[1]
	lg_team_table = afc.append(nfc)
	lg_team_table['div_name'] = lg_team_table['Tm'] == lg_team_table['W']
	lg_team_table = lg_team_table.loc[lg_team_table.div_name == False,:]
	nflteams = sorted([re.findall('^([A-z0-9. ]+)', tm)[0] for tm in lg_team_table.Tm])
	
	# Create empty graph (dict)
	nfl_graph = {}
	for tm in nflteams:
	    nfl_graph[tm] = []
	    
	score_graph = {}

	# Populate graphs with each week's results
	for week_num in range(1,last_week+1):
	    week_url = "https://www.pro-football-reference.com/years/" + str(year) + "/week_" + str(week_num) + ".htm"
	    scraped_tables = pd.read_html(week_url)
	    for table in scraped_tables:
	        if table.iloc[1,2] != 'Final':
	            continue
	        tm1 = table.iloc[1,0]
	        tm2 = table.iloc[2,0]
	        score1 = int(table.iloc[1,1])
	        score2 = int(table.iloc[2,1])

	        if score1 > score2:
	            if tm2 not in nfl_graph[tm1]:
	                nfl_graph[tm1].append(tm2)
	                score_graph[(tm1, tm2)] = (str(score1) + '-' + str(score2), 'Week ' + str(week_num))
	        elif score2 > score1:
	            if tm1 not in nfl_graph[tm2]:
	                nfl_graph[tm2].append(tm1)
	                score_graph[(tm2, tm1)] = (str(score2) + '-' + str(score1), 'Week ' + str(week_num))

	return nfl_graph, score_graph
