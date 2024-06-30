import duckdb
import pandas as pd
import requests
import os
import re

# -------------------------------------- VARS -----------------------------------------------------

RACE_INFO_DIR = "raw/output"
URI = "http://localhost:3000"
con = duckdb.connect("db/database.db")

# -------------------------------- CHECK SERVER AVAILABILITY --------------------------------------

try:
    response = requests.get(URI)
    if response.status_code == 200:
        print(f"Server at {URI} is available.")
    else:
        print(f"Server at {URI} responded with status code {response.status_code}.")
        exit()
except requests.ConnectionError:
        print(f"Failed to connect to the server at {URI}.")
        exit()
except Exception as e:
        print(f"An error occurred: {e}")
        exit()

# ------------------------------- INCIDENTS (RACE CONTROL) ----------------------------------------

print("Processing incidents from race control...")
incidents_lines = []

for filename in os.listdir(RACE_INFO_DIR):  # grab all files at location
    if "Race_racecontrol.txt" not in filename:  # only want races, no quals or practices, and the files that are race control logs
        continue
    file_path = os.path.join(RACE_INFO_DIR, filename)  # get the path to that file
    with open(file_path, "r") as file:  # open it
        for line in file:  # read every line
            if "NOTED" not in line or "INCIDENT" not in line:  # skip if not an incident or not noted
                continue
            # ---------- get datetime and split ------------
            datetime_match = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", line)
            if not datetime_match:
                continue
            datetime = datetime_match.group(1)  # split it into date and time
            date = datetime.split()[0]
            time = datetime.split()[1]
            line = line[len(datetime) + 1 :].strip()  # remove the date and time
            
            # -------------- get driver numbers ------------
            drivers_nums = re.findall( r"\b(\d+)\s*\([A-Z]+\)", line )  # driver numbers, every digit sequence before (XXX) things
            if not drivers_nums:
                continue
            driver_one_num = drivers_nums[0]
            driver_two_num = ( drivers_nums[1] if len(drivers_nums) > 1 else None )  # there are incidents with only one guy, so can remove the second
            
            # ------------ get driver codes ---------------

            drivers_codes = re.findall(
                r"\((\w{3})\)", line
            )  # driver codes, every 3 character sequence in brackets
            if not drivers_codes:
                continue
            driver_one_code = drivers_codes[0]
            driver_two_code = ( drivers_codes[1] if len(drivers_codes) > 1 else None )  # there are incidents with only one guy, so can remove the second

            # ------------ get race name ---------------
            race_match = re.search(
                r"\d+_(.*?)_Race_.*\.txt", filename
            )  # race name from the filename
            if not race_match:
                continue
            race = race_match.group(1).replace("_", " ")

            # ------- bring it all together ------------
            incidents_lines.append(
                {
                    "date": date,
                    "time": time,
                    "driver_one_num": driver_one_num,
                    "driver_two_num": driver_two_num,
                    "driver_one_code": driver_one_code,
                    "driver_two_code": driver_two_code,
                    "race": race
                }
            )

incidents_df = pd.DataFrame(incidents_lines)
print("Finished processing incidents from race control!")

# ------------------------------- RACE INFORMATION (RACE CONTROL TXT) ---------------------------------------------------

print("Processing races from race control...")
races_lines=[]

for filename in os.listdir(RACE_INFO_DIR):  # grab all files at location
    if "Race_racecontrol.txt" not in filename:  # only want races, no quals or practices, and the files that are race control logs
        continue
    
    file_path = os.path.join(RACE_INFO_DIR, filename)  # get the path to that file
    first_line=''
    with open(file_path, "r") as file:  # open it
        for line in file:  # read every line
            first_line=line
            break     
        
    # ------------ get race date ---------------
    date_match = re.match(r"\d{4}-\d{2}-\d{2}", line)
    if not date_match:
        continue
    date = date_match.group(0)    
    
    # ------------ get race name ---------------
    race_match = re.search(r"\d+_(.*?)_Race_.*\.txt", filename)  # race name from the filename
    if not race_match:
        continue
    race = race_match.group(1).replace("_", " ")
    
    races_lines.append(
                {
                    "date": date,
                    "race": race
                }
            )      

races_df = pd.DataFrame(races_lines)
print("Finished processing races from race control!")

# ------------------------------- DRIVERS (API) ---------------------------------------------------

print("Processing drivers from endpoints...")
drivers_df = None
response = requests.get(f"{URI}/drivers")
if response.status_code == 200:
    data = response.json()
    drivers_details = []
    for driver in data:
        response = requests.get(f"{URI}/drivers/{driver}")
        if response.status_code == 200:
            drivers_details.append(response.json())
        else:
            print(f"Failed to fetch driver {driver}. Status code: {response.status_code}")
    drivers_df = pd.DataFrame(drivers_details)
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
print("Fished processing drivers from the endpoints!")

# ------------------------------- TEAMS (API) ----------------------------------------------------

print("Processing teams from endpoints...")
teams_df = None
response = requests.get(f"{URI}/teams")
if response.status_code == 200:
    data = response.json()
    teams_details = []
    for team in data:
        response = requests.get(f"{URI}/teams/{team}")
        if response.status_code == 200:
            teams_details.append(response.json())
        else:
            print(f"Failed to fetch driver {team}. Status code: {response.status_code}")
    teams_df = pd.DataFrame(teams_details)
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
print("Finished processing teams from endpoints!")

# ------------------------------- LAPS CSV -------------------------------------------------------

print("Processing laps from csv...")
laps_dfs = []
for filename in os.listdir(RACE_INFO_DIR):
    if filename.endswith("Race_laps.csv"):
        file_path = os.path.join(RACE_INFO_DIR, filename)
        df = pd.read_csv(file_path)

        race_match = re.search(r"^[^_]*_([^_]*_[^_]*_[^_]*)_", filename)  # race name from the filename
        if not race_match:
            continue
        race = race_match.group(1).replace("_", " ")

        df["race"] = race
        laps_dfs.append(df)

laps_df = pd.concat(laps_dfs, ignore_index=True)
print("Finished processing laps from csv!")

# ------------------------------- WEATHER CSV --------------------------------------------

print("Processing weather from csv...")
weather_dfs = []
for filename in os.listdir(RACE_INFO_DIR):
    if filename.endswith("weather.csv"):
        file_path = os.path.join(RACE_INFO_DIR, filename)
        df = pd.read_csv(file_path)
        
        race_match = re.search(r"^[^_]*_([^_]*_[^_]*_[^_]*)_", filename)  # race name from the filename
        if not race_match:
            continue
        race = race_match.group(1).replace("_", " ")

        df["race"] = race
        weather_dfs.append(df)

weather_dfs = pd.concat(weather_dfs, ignore_index=True)
print("Finished processing weather from csv!")

# ------------------------------- CONSTRUCTOR RESULTS CSV ----------------------------------------

print("Processing constructor results from csv...")
constructor_results_df = pd.read_csv(RACE_INFO_DIR + "/constructor_results.csv")
print("Finished processing constructor results from csv!")

# ------------------------------- DRIVER RESULTS CSV ----------------------------------------

print("Processing driver results from csv...")
driver_results_df = pd.read_csv(RACE_INFO_DIR + "/driver_results.csv")
print("Finished driver results from csv!")

# ------------------------------- DRIVER SPRINT RESULTS CSV ----------------------------------------

print("Processing driver sprint results from csv...")
driver_sprint_results_df = pd.read_csv(RACE_INFO_DIR + "/driver_sprint_results.csv")
print("Finished driver sprint results from csv!")

# ------------------------------- CIRCUITS CSV ----------------------------------------

print("Processing circuits from csv...")
circuits_df = pd.read_csv(RACE_INFO_DIR + "/circuits.csv")
print("Finished circuits from csv!")

# ------------------------------- DRIVERS TEAMS CSV ----------------------------------------

print("Processing drivers teams from csv...")
drivers_teams_df = pd.read_csv(RACE_INFO_DIR + "/drivers_teams.csv")
print("Finished drivers teams from csv!")

# ------------------------------- LAP TIMES CSV ----------------------------------------

print("Processing lap times from csv...")
lap_times_df = pd.read_csv(RACE_INFO_DIR + "/lap_times.csv")
print("Finished lap times from csv!")

# ------------------------------- RACES CARRIED OUT CSV ----------------------------------------

print("Processing races carried out from csv...")
races_carried_out_df = pd.read_csv(RACE_INFO_DIR + "/races_carried_out.csv")
print("Processing races carried out from csv...")


# ------------------------------- ADD THOSE TO DUCKDB --------------------------------------------

# txt
con.execute("CREATE TABLE IF NOT EXISTS raw_incidents AS SELECT ROW_NUMBER() OVER () AS id, * FROM incidents_df")
con.execute("CREATE TABLE IF NOT EXISTS raw_races AS SELECT ROW_NUMBER() OVER () AS id, * FROM races_df")
# api
con.execute("CREATE TABLE IF NOT EXISTS raw_drivers AS SELECT * FROM drivers_df")
con.execute("CREATE TABLE IF NOT EXISTS raw_teams AS SELECT * FROM teams_df")
# multiple csv
con.execute("CREATE TABLE IF NOT EXISTS raw_laps AS SELECT * FROM laps_df")
con.execute("CREATE TABLE IF NOT EXISTS raw_weather AS SELECT * FROM weather_dfs")
# single csv
con.execute("CREATE TABLE IF NOT EXISTS raw_circuits AS SELECT * FROM circuits_df")
con.execute("CREATE TABLE IF NOT EXISTS raw_constructors_results AS SELECT * FROM constructor_results_df")
con.execute("CREATE TABLE IF NOT EXISTS raw_driver_results AS SELECT * FROM driver_results_df")
con.execute("CREATE TABLE IF NOT EXISTS raw_driver_sprint_results AS SELECT * FROM driver_sprint_results_df")
con.execute("CREATE TABLE IF NOT EXISTS raw_drivers_teams AS SELECT * FROM drivers_teams_df")
con.execute("CREATE TABLE IF NOT EXISTS raw_lap_times AS SELECT * FROM lap_times_df")
con.execute("CREATE TABLE IF NOT EXISTS raw_races_carried_out AS SELECT * FROM races_carried_out_df")
