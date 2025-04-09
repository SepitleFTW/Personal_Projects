"""
this is the sqlite datatbase for my
project that will store all the race events, names
etc
"""

import sqlite3 

regatta_data = {
    "Home": "https://www.regattaresults.co.za/",
    "Results": "https://www.regattaresults.co.za/",
    "2025": "https://www.regattaresults.co.za/home/2025-results/",
    # ... other years ...
    "Buffalo Regatta - 6 & 8 February": "https://www.regattaresults.co.za/Results/Results2025/2025-Feb-Buffalo/results.htm",
    "Selborne Sprints - 7 February": "https://www.regattaresults.co.za/Results/Results2025/2025-Feb-SelborneS/results.htm",
    "ECRA Champs - 1 February": "/Results/Results2025/2025-Feb-ECRAChamps/results.htm",
    "SA Schools Champs 28 Feb - 2 March": "/Results/Results2025/2025-Mar-SAChamps/results.htm",
    
}
#filtering even entries only
event_links = {
    name: url for name, url in regatta_data.items()
    if "results" in url.lower() and "Results2025" in url
}

conn = sqlite3.connect("regatta_results.db") #connecting to the database
cursor = conn.cursor() #creating a cursor object to execute SQL commands

"""
creating the table for all
the results below (A bit of chatgpt will be used)
-event name,
-link
"""
cursor.execute('''
CREATE TABLE IF NOT EXISTS regatta_events  (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT NOT NULL,
    link TEXT
)
''')

#inserting the event names and links into the table
for event_name, url in event_links.items(): #fixing the url to be a full url
    if url.startswith("/"):
        url = "https://www.regattaresults.co.za" + url #adding the base url to the link

    cursor.execute('''
    INSERT INTO regatta_events (event_name, link)
    VALUES (?, ?)
    ''', (event_name, url)) #inserting the event name and link into the table


conn.commit() #committing the changes to the database
conn.close() #closing the connection to the database

print("Database has been created successfully!")