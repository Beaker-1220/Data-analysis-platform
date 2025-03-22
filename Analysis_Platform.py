from tkinter import ttk
import requests
import bs4
from bs4 import BeautifulSoup
import csv
import json
import tkinter as tk

# The Function to search for player information
def search_player(Name):
    Player = list()
    person_rating = list()
    # Read the Player.csv file and construct a dict map from players' id to name
    with open('Players.csv', 'r', newline='', encoding='gbk') as file:
        reader = csv.reader(file)
        next(reader)
        data = {row[1]: row[0] for row in reader}
        if Name not in data:
            return "Name not found"
    # Access player's id we can get player's url
    Player_url = 'https://www.dongqiudi.com/player/'+str(data[Name])+'.html'
    # User-Agent spoofing
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    response = requests.get(Player_url, headers=header)
    # Write html to text
    # Cited from https://blog.csdn.net/m0_38074612/article/details/130717974
    content = " "
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            content += chunk.decode("utf-8", errors='ignore')
    soup = BeautifulSoup(content, "html.parser")

    # Select the information from the text based on selector
    FC = soup.select('#__layout > div > div.player-data-wrap > div.player-con > div.player-left > div.player-info > div > div > ul:nth-child(1) > li:nth-child(1)')
    # Extract Text Part
    for s in FC:
        s = s.text
    FC = s[4:]
    Preferred_foot = soup.select('#__layout > div > div.player-data-wrap > div.player-con > div.player-left > div.player-info > div > div > ul:nth-child(3) > li:nth-child(3)')
    for s in Preferred_foot:
        s = s.text
    Preferred_foot = s[4:]
    Country = soup.select('#__layout > div > div.player-data-wrap > div.player-con > div.player-left > div.player-info > div > div > ul:nth-child(1) > li:nth-child(2)')
    for s in Country:
        s = s.text
    Country = s[6:]
    number = soup.select('#__layout > div > div.player-data-wrap > div.player-con > div.player-left > div.player-info > div > div > ul:nth-child(3) > li:nth-child(1)')
    for s in number:
        s = s.text
    number = s[6:]
    age = soup.select('#__layout > div > div.player-data-wrap > div.player-con > div.player-left > div.player-info > div > div > ul.second-ul > li:nth-child(2)')
    for s in age:
        s = s.text
    age = s[6:]
    weight = soup.select('#__layout > div > div.player-data-wrap > div.player-con > div.player-left > div.player-info > div > div > ul.second-ul > li:nth-child(3)')
    for s in weight:
        s = s.text
    weight = s[6:]
    Height = soup.select('#__layout > div > div.player-data-wrap > div.player-con > div.player-left > div.player-info > div > div > ul:nth-child(1) > li:nth-child(3)')
    for s in Height:
        s = s.text
    Height = s[6:]
    Pos = soup.select('#__layout > div > div.player-data-wrap > div.player-con > div.player-left > div.player-info > div > div > ul.second-ul > li:nth-child(1)')
    for s in Pos:
        s = s.text
    Pos = s[6:]
    Total = soup.select('#__layout > div > div.player-data-wrap > div.player-con > div.player-right > div.capability > p > b')
    PAC = soup.select('#__layout > div > div.player-data-wrap > div.player-con > div.player-right > div.capability > div.box_chart > div.item.item0 > span')
    SHO = soup.select('#__layout > div > div.player-data-wrap > div.player-con > div.player-right > div.capability > div.box_chart > div.item.item5 > span')
    DEF = soup.select('#__layout > div > div.player-data-wrap > div.player-con > div.player-right > div.capability > div.box_chart > div.item.item2 > span')
    DRI = soup.select('#__layout > div > div.player-data-wrap > div.player-con > div.player-right > div.capability > div.box_chart > div.item.item3 > span')
    PHY = soup.select('#__layout > div > div.player-data-wrap > div.player-con > div.player-right > div.capability > div.box_chart > div.item.item1 > span')
    PAS = soup.select('#__layout > div > div.player-data-wrap > div.player-con > div.player-right > div.capability > div.box_chart > div.item.item4 > span')
    person_rating_pre = [Total, PAC, SHO, DEF, DRI, PHY, PAS]
    # Put all the information into player list
    for element in person_rating_pre:
        for s in element:
            s = s.text
        person_rating.append(s)

    Player = [Name, FC, Pos, number, Country, age, Preferred_foot, Height, weight, person_rating]
    # return the player's information list
    return Player

def store_file(league):
    # Call different functions to get list
    information = league_data(league)
    goal_list = league_goal(league)
    assist_list = league_assist(league)
    Players = id_player(league)
    # Write information to CSV file
    header_list = ['Team Name', 'Plays', 'Wins', 'loses', 'Goals scored', 'Goals Allowed', 'Goals Differential', 'Points']
    headers_list_p = ['ID', 'Name']
    headers_list_g = ['Player', 'Team Name', 'Goals']
    headers_list_a = ['Player', 'Team Name', 'Assists']
    with open(""+league+"_test.csv", "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header_list)
        writer.writerows(information)
    with open("" + league + "_goals_test.csv", "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers_list_g)
        writer.writerows(goal_list)
    with open("" + league + "_assists_test.csv", "w", encoding="utf-8-sig", newline="") as k:
        writer = csv.writer(k)
        writer.writerow(headers_list_a)
        writer.writerows(assist_list)
    with open("Players "+str(league)+"_test.csv", "w", encoding="utf-8-sig", newline="") as p:
        writer = csv.writer(p)
        writer.writerow(headers_list_p)
        writer.writerows(Players)

def merge_players():
    # Create headers
    headers_list_p = ['ID', 'Name']
    csv_files = ['Players Serie A_test.csv', 'Players Fußball-Bundesliga_test.csv', 'Players La Liga_test.csv', 'Players Ligue 1_test.csv',
                 'Players Premier League_test.csv']

    merged_file = 'Players_test.csv'
    # Merge multiple csv files into one, get players' id to name
    with open(merged_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(headers_list_p)

        for filename in csv_files:
            with open(filename, 'r', encoding="utf-8-sig", newline='') as infile:
                reader = csv.reader(infile)
                next(reader)
                writer.writerows(reader)


def league_goal(league):
    goal_list = list()
    assist_list = list()
    Players = list()
    # Store leagues' name to website dict
    league_goal_dict = {
        'Premier League': 'https://www.dongqiudi.com/sport-data/soccer/biz/data/person_ranking?season_id=21198&app=dqd&version=0&platform=web&language=zh-cn&app_type=&type=goals',
        'Serie A': 'https://www.dongqiudi.com/sport-data/soccer/biz/data/person_ranking?season_id=19954&app=dqd&version=0&platform=web&language=zh-cn&app_type=&type=goals',
        'La Liga': 'https://www.dongqiudi.com/sport-data/soccer/biz/data/person_ranking?season_id=19950&app=dqd&version=0&platform=web&language=zh-cn&app_type=&type=goals',
        'Fußball-Bundesliga': 'https://www.dongqiudi.com/sport-data/soccer/biz/data/person_ranking?season_id=19918&app=dqd&version=0&platform=web&language=zh-cn&app_type=&type=goals',
        'Ligue 1': 'https://www.dongqiudi.com/sport-data/soccer/biz/data/person_ranking?season_id=19926&app=dqd&version=0&platform=web&language=zh-cn&app_type=&type=goals'}
    league_assist_dict = {
        'Premier League': 'https://www.dongqiudi.com/sport-data/soccer/biz/data/person_ranking?season_id=21198&app=dqd&version=0&platform=web&language=zh-cn&app_type=&type=assists',
        'Serie A': 'https://www.dongqiudi.com/sport-data/soccer/biz/data/person_ranking?season_id=19954&app=dqd&version=0&platform=web&language=zh-cn&app_type=&type=assists',
        'La Liga': 'https://www.dongqiudi.com/sport-data/soccer/biz/data/person_ranking?season_id=19950&app=dqd&version=0&platform=web&language=zh-cn&app_type=&type=assists',
        'Fußball-Bundesliga': 'https://www.dongqiudi.com/sport-data/soccer/biz/data/person_ranking?season_id=19918&app=dqd&version=0&platform=web&language=zh-cn&app_type=&type=assists',
        'Ligue 1': 'https://www.dongqiudi.com/sport-data/soccer/biz/data/person_ranking?season_id=19926&app=dqd&version=0&platform=web&language=zh-cn&app_type=&type=assists'}

    # Get url based on dict and league name
    url_1 = league_goal_dict[league]
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    response = requests.get(url_1,headers=header)
    # Write html to text and to json
    content =" "
    for chunk in response.iter_content(chunk_size=4096):
        if chunk:
            content += chunk.decode("utf-8",errors='ignore')
    data = json.loads(content)
    person_ranking = data["content"]["data"]

    # Distribute information of the player
    for person in person_ranking:
        person_name = person["person_name"]
        team_name = person["team_name"]
        person_id = person["person_id"]
        person_logo = person["person_logo"]
        goal = person["goal"]
        # add the player's information to goal list
        player_g = [person_name, team_name, goal]
        goal_list.append(player_g)

    return goal_list

def id_player(league):
    Players = list()
    # Store leagues' name to website dict
    league_goal_dict = {
        'Premier League': 'https://www.dongqiudi.com/sport-data/soccer/biz/data/person_ranking?season_id=21198&app=dqd&version=0&platform=web&language=zh-cn&app_type=&type=goals',
        'Serie A': 'https://www.dongqiudi.com/sport-data/soccer/biz/data/person_ranking?season_id=19954&app=dqd&version=0&platform=web&language=zh-cn&app_type=&type=goals',
        'La Liga': 'https://www.dongqiudi.com/sport-data/soccer/biz/data/person_ranking?season_id=19950&app=dqd&version=0&platform=web&language=zh-cn&app_type=&type=goals',
        'Fußball-Bundesliga': 'https://www.dongqiudi.com/sport-data/soccer/biz/data/person_ranking?season_id=19918&app=dqd&version=0&platform=web&language=zh-cn&app_type=&type=goals',
        'Ligue 1': 'https://www.dongqiudi.com/sport-data/soccer/biz/data/person_ranking?season_id=19926&app=dqd&version=0&platform=web&language=zh-cn&app_type=&type=goals'}

    league_assist_dict = {
        'Premier League': 'https://www.dongqiudi.com/sport-data/soccer/biz/data/person_ranking?season_id=21198&app=dqd&version=0&platform=web&language=zh-cn&app_type=&type=assists',
        'Serie A': 'https://www.dongqiudi.com/sport-data/soccer/biz/data/person_ranking?season_id=19954&app=dqd&version=0&platform=web&language=zh-cn&app_type=&type=assists',
        'La Liga': 'https://www.dongqiudi.com/sport-data/soccer/biz/data/person_ranking?season_id=19950&app=dqd&version=0&platform=web&language=zh-cn&app_type=&type=assists',
        'Fußball-Bundesliga': 'https://www.dongqiudi.com/sport-data/soccer/biz/data/person_ranking?season_id=19918&app=dqd&version=0&platform=web&language=zh-cn&app_type=&type=assists',
        'Ligue 1': 'https://www.dongqiudi.com/sport-data/soccer/biz/data/person_ranking?season_id=19926&app=dqd&version=0&platform=web&language=zh-cn&app_type=&type=assists'}
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

    # Get url based on dict and league name
    url_1 = league_goal_dict[league]
    url_2 = league_assist_dict[league]
    # Write html to text and to json
    response = requests.get(url_2, headers=header)
    content = " "
    for chunk in response.iter_content(chunk_size=4096):
        if chunk:
            content += chunk.decode("utf-8", errors='ignore')
    data = json.loads(content)
    person_ranking = data["content"]["data"]

    # Distribute the information of the player
    for person in person_ranking:
        person_name = person["person_name"]
        team_name = person["team_name"]
        person_id = person["person_id"]
        person_logo = person["person_logo"]
        assist = person['count']
        player_person = [person_id, person_name]

        # Add the player's id to name list into the list
        if player_person not in Players:
            Players.append(player_person)
    # Repeat the above operations but to the players on the assist list
    response = requests.get(url_1,headers=header)
    content =" "
    for chunk in response.iter_content(chunk_size=4096):
        if chunk:
            content += chunk.decode("utf-8",errors='ignore')
    data = json.loads(content)
    person_ranking = data["content"]["data"]

    for person in person_ranking:
        person_name = person["person_name"]
        team_name = person["team_name"]
        person_id = person["person_id"]
        person_logo = person["person_logo"]
        goal = person["goal"]

        player_person = [person_id, person_name]

        if player_person not in Players:
            Players.append(player_person)
    # return the players' id to name list
    return Players
def league_assist(league):
    # Store leagues' name to website dict
    league_assist_dict = {
        'Premier League': 'https://www.dongqiudi.com/sport-data/soccer/biz/data/person_ranking?season_id=21198&app=dqd&version=0&platform=web&language=zh-cn&app_type=&type=assists',
        'Serie A': 'https://www.dongqiudi.com/sport-data/soccer/biz/data/person_ranking?season_id=19954&app=dqd&version=0&platform=web&language=zh-cn&app_type=&type=assists',
        'La Liga': 'https://www.dongqiudi.com/sport-data/soccer/biz/data/person_ranking?season_id=19950&app=dqd&version=0&platform=web&language=zh-cn&app_type=&type=assists',
        'Fußball-Bundesliga': 'https://www.dongqiudi.com/sport-data/soccer/biz/data/person_ranking?season_id=19918&app=dqd&version=0&platform=web&language=zh-cn&app_type=&type=assists',
        'Ligue 1': 'https://www.dongqiudi.com/sport-data/soccer/biz/data/person_ranking?season_id=19926&app=dqd&version=0&platform=web&language=zh-cn&app_type=&type=assists'}
    # User-Agent spoofing
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

    assist_list = list()
    url_2 = league_assist_dict[league]
    # Write html to text and to json
    response = requests.get(url_2, headers=header)
    content = " "
    for chunk in response.iter_content(chunk_size=4096):
        if chunk:
            content += chunk.decode("utf-8", errors='ignore')
    data = json.loads(content)
    person_ranking = data["content"]["data"]

    # Distribute the information
    for person in person_ranking:
        person_name = person["person_name"]
        team_name = person["team_name"]
        person_id = person["person_id"]
        person_logo = person["person_logo"]
        assist = person['count']

        # add the player's information to goal list
        player_a = [person_name, team_name, assist]
        assist_list.append(player_a)
    return assist_list

def league_data(league):
    information = list()
    # Store leagues' name to website dict
    league_dict = {'Premier League':'https://www.dongqiudi.com/data/1', 'Serie A':'https://www.dongqiudi.com/data/2', 'La Liga':'https://www.dongqiudi.com/data/3', 'Fußball-Bundesliga':'https://www.dongqiudi.com/data/4','Ligue 1':'https://www.dongqiudi.com/data/10'}
    url = league_dict[league]
    # User-Agent spoofing
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    response = requests.get(url,headers=header)
    # Write html to text
    content =" "
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            content += chunk.decode("utf-8",errors='ignore')
    soup = BeautifulSoup(content, "html.parser")
    # Scraping relevant information based on selectors
    for i in range(1,21):

        team_name = soup.select('#__layout > div > div.container > div > div > div > div.data-con > div.right-con > div.tab-con > div > div > div > div > div:nth-child(3) > p:nth-child('+str(i)+') > span.team-icon > b')
        plays = soup.select('#__layout > div > div.container > div > div > div > div.data-con > div.right-con > div.tab-con > div > div > div > div > div:nth-child(3) > p:nth-child(' + str(i) + ') > span:nth-child(3)')
        wins = soup.select('#__layout > div > div.container > div > div > div > div.data-con > div.right-con > div.tab-con > div > div > div > div > div:nth-child(3) > p:nth-child(' + str(i) + ') > span:nth-child(4)')
        ties = soup.select('#__layout > div > div.container > div > div > div > div.data-con > div.right-con > div.tab-con > div > div > div > div > div:nth-child(3) > p:nth-child(' + str(i) + ') > span:nth-child(5)')
        loses = soup.select('#__layout > div > div.container > div > div > div > div.data-con > div.right-con > div.tab-con > div > div > div > div > div:nth-child(3) > p:nth-child(' + str(i) + ') > span:nth-child(6)')
        ties = soup.select('#__layout > div > div.container > div > div > div > div.data-con > div.right-con > div.tab-con > div > div > div > div > div:nth-child(3) > p:nth-child(' + str(i) + ') > span:nth-child(7)')
        goals = soup.select(
            '#__layout > div > div.container > div > div > div > div.data-con > div.right-con > div.tab-con > div > div > div > div > div:nth-child(3) > p:nth-child(' + str(
                i) + ') > span:nth-child(8)')
        lose_goals = soup.select(
            '#__layout > div > div.container > div > div > div > div.data-con > div.right-con > div.tab-con > div > div > div > div > div:nth-child(3) > p:nth-child(' + str(
                i) + ') > span:nth-child(9)')
        goals_difference = soup.select(
            '#__layout > div > div.container > div > div > div > div.data-con > div.right-con > div.tab-con > div > div > div > div > div:nth-child(3) > p:nth-child(' + str(
                i) + ') > span:nth-child(10)')
        points = soup.select(
            '#__layout > div > div.container > div > div > div > div.data-con > div.right-con > div.tab-con > div > div > div > div > div:nth-child(3) > p:nth-child(' + str(
                i) + ') > span:nth-child(11)')
        information_pre = [team_name, plays, wins, loses, ties, goals, lose_goals, goals_difference, points]
        Team = list()
        # Transform the information to text
        for element in information_pre:
            if element != []:
                for s in element:
                    s = s.text
                Team.append(s)
        # Append the team information to the list if it isn't empty
        if team_name != []:
            information.append(Team)
    return information

def start():
    global combobox
    # Select the category you want to view from the selection bar
    options = ['联赛积分榜', '联赛射手榜和助攻榜', '球员信息']
    combobox = ttk.Combobox(window, values=options)
    combobox.grid(row=0, column=3)
    # Create a button to execute function 'next_step'
    btn_next = tk.Button(window, text="确定", command=next_step)
    btn_next.grid(row=1, column=3)



def next_step():
    # Get the selected option from the combobox
    selected_option = combobox.get()
    if selected_option == '联赛积分榜':
        # Clear the previous results
        for i in range(-1, 50):
            for j in range(-1, 8):
                label_result = tk.Label(window, text='')
                label_result.grid(row=i + 6, column=3 * j + 9)
                label_result.config(text='                           ')

        # Define the search_league function
        def search_league():
            # Get the selected league name from the combobox
            league_name = combobox_s.get()
            # Call the league_data function to get the information
            information = league_data(league_name)
            if information:
                # Display the column headers
                label_result = tk.Label(window, text='俱乐部')
                label_result.grid(row=5, column=9)
                label_result = tk.Label(window, text='场次')
                label_result.grid(row=5, column=12)
                label_result = tk.Label(window, text='胜')
                label_result.grid(row=5, column=15)
                label_result = tk.Label(window, text='负')
                label_result.grid(row=5, column=18)
                label_result = tk.Label(window, text='进球')
                label_result.grid(row=5, column=21)
                label_result = tk.Label(window, text='失球')
                label_result.grid(row=5, column=24)
                label_result = tk.Label(window, text='净胜球')
                label_result.grid(row=5, column=27)
                label_result = tk.Label(window, text='积分')
                label_result.grid(row=5, column=30)
                # Display the information for each club in the league
                for i in range(0, len(information)):
                    for j in range(0,len(information[i])):
                        label_result = tk.Label(window, text='')
                        label_result.grid(row=i+6, column=3*j+9)
                        label_result.config(text=information[i][j])
            else:
                # Display a message if the league is not found
                label_result = tk.Label(window, text='')
                label_result.grid(row=5, column=9, columnspan=2)
                label_result.config(text="League not found")

        # Display the label and combobox for entering the league
        label = tk.Label(window, text="Enter the league you want to know about:")
        label.grid(row=3, column=3)
        options = ['Serie A', 'Premier League', 'Ligue 1', 'La Liga', 'Fußball-Bundesliga']  # 选择条的选项
        global combobox_s
        combobox_s = ttk.Combobox(window, values=options)
        combobox_s.grid(row=4, column=3)
        label_result = tk.Label(window, text='')
        label_result.grid(row=2, column=0)
        # Create a search button
        btn = tk.Button(window, text="Search", command=search_league)
        btn.grid(row=5, column=3, columnspan=2)

    # Define the search_league function
    if selected_option == '球员信息':
        # Clear the previous results
        for i in range(-1, 50):
            for j in range(-1, 8):
                label_result = tk.Label(window, text='')
                label_result.grid(row= i + 6, column=3 * j + 9)
                label_result.config(text='                          ')

        def display_player():
            # Get the player's name from the entry
            name = entry.get()
            player_data = search_player(name)
            if player_data:
                # Display the column headers
                label_result = tk.Label(window, text='球员')
                label_result.grid(row=5, column=9)
                label_result = tk.Label(window, text='俱乐部')
                label_result.grid(row=5, column=12)
                label_result = tk.Label(window, text='位置')
                label_result.grid(row=5, column=15)
                label_result = tk.Label(window, text='号码')
                label_result.grid(row=7, column=9)
                label_result = tk.Label(window, text='国家')
                label_result.grid(row=7, column=12)
                label_result = tk.Label(window, text='年龄')
                label_result.grid(row=7, column=15)
                label_result = tk.Label(window, text='惯用脚')
                label_result.grid(row=9, column=9)
                label_result = tk.Label(window, text='身高')
                label_result.grid(row=9, column=12)
                label_result = tk.Label(window, text='体重')
                label_result.grid(row=9, column=15)
                # Display the information of the player
                for i in range(0, 3):
                    label_result = tk.Label(window, text='')
                    label_result.grid(row=6, column=3*i+9)
                    label_result.config(text=player_data[i])
                for j in range(3, 6):
                    label_result = tk.Label(window, text='')
                    label_result.grid(row=8, column=3*j)
                    label_result.config(text=player_data[j])
                for k in range(6, 9):
                    label_result = tk.Label(window, text='')
                    label_result.grid(row=10, column=3 * k -9)
                    label_result.config(text=player_data[k])
                # Display the personal rating for the player
                label_result = tk.Label(window, text='综合评分')
                label_result.grid(row=12, column=9)
                label_result = tk.Label(window, text='速度')
                label_result.grid(row=14, column=9)
                label_result = tk.Label(window, text='射门')
                label_result.grid(row=16, column=9)
                label_result = tk.Label(window, text='防守')
                label_result.grid(row=18, column=9)
                label_result = tk.Label(window, text='盘带')
                label_result.grid(row=20, column=9)
                label_result = tk.Label(window, text='身体')
                label_result.grid(row=22, column=9)
                label_result = tk.Label(window, text='传球')
                label_result.grid(row=24, column=9)
                for i in range(len(player_data[9])):
                    label_rating = tk.Label(window, text='')
                    label_rating.grid(row=2*i+13, column=9)
                    label_rating.config(text=player_data[9][i])
            else:
                # Display a message if the player's name is not found
                label_result = tk.Label(window, text='')
                label_result.grid(row=5, column=9, columnspan=2)
                label_result.config(text="Name not found")
        label = tk.Label(window, text="Enter the player you want to know about:")
        label.grid(row=3, column=3)
        entry = tk.Entry(window)
        entry.grid(row=4, column=3)
        # Create a label for the results
        label_result = tk.Label(window, text='')
        label_result.grid(row=2, column=0, columnspan=2)
        # Create a search button
        btn = tk.Button(window, text="Search", command=display_player)
        btn.grid(row=5, column=3, columnspan=2)

    # Define the search_league function
    if selected_option == '联赛射手榜和助攻榜':
        # Clear the previous results
        for i in range(-1, 50):
            for j in range(-1, 8):
                label_result = tk.Label(window, text='')
                label_result.grid(row=i + 6, column=3 * j + 9)
                label_result.config(text='                          ')
        def search_goal_assist():
            # Get the selected league name from the combobox
            name = combobox_a.get()
            # Call the league_data function to get the information
            goal_data = league_goal(name)
            assist_data = league_assist(name)
            if goal_data:
                # Display the column headers
                label_result = tk.Label(window, text='球员')
                label_result.grid(row=5, column=9)
                label_result = tk.Label(window, text='俱乐部')
                label_result.grid(row=5, column=12)
                label_result = tk.Label(window, text='进球')
                label_result.grid(row=5, column=15)
                label_result = tk.Label(window, text='球员')
                label_result.grid(row=5, column=18)
                label_result = tk.Label(window, text='俱乐部')
                label_result.grid(row=5, column=21)
                label_result = tk.Label(window, text='助攻')
                label_result.grid(row=5, column=24)
                # Display the information for each club in the league
                for i in range(0, 30):
                    for j in range(0,len(goal_data[i])):
                        label_goal = tk.Label(window, text='')
                        label_goal.grid(row=i+6, column=3*j+9)
                        label_goal.config(text=goal_data[i][j])
                        label_assist = tk.Label(window, text='')
                        label_assist.grid(row=i+6, column=3*j+18)
                        label_assist.config(text=assist_data[i][j])
            else:
                # Display a message if the league is not found
                label_result = tk.Label(window, text='')
                label_result.grid(row=5, column=9, columnspan=2)
                label_result.config(text="League not found")

        # Display the label and combobox for entering the league
        label = tk.Label(window, text="Enter the League you want to know about:")
        label.grid(row=3, column=3)
        # Create a selection bar to choose league
        options = ['Serie A', 'Premier League', 'Ligue 1', 'La Liga', 'Fußball-Bundesliga']  # 选择条的选项
        global combobox_a
        combobox_a = ttk.Combobox(window, values=options)
        combobox_a.grid(row=4, column=3)
        # Create a label for the results
        label_result = tk.Label(window, text='')
        label_result.grid(row=2, column=0, columnspan=2)
        # Create a search button
        btn = tk.Button(window, text="Search", command=search_goal_assist)
        btn.grid(row=5, column=3, columnspan=2)

def collect_data():
    # Call the function to collect information and write into CSV file
    store_file('Ligue 1')
    store_file('Premier League')
    store_file('Serie A')
    store_file('La Liga')
    store_file('Fußball-Bundesliga')
    merge_players()

# Create a window to execute the program
window = tk.Tk()
# Set the size of the window
window.geometry('1400x1000')
# Set the title of the window
window.title("Data Analysis Platform based on The Big Five Leagues")
# Create a button to execute the function collect_data
btn_next = tk.Button(window, text="收集信息", command=collect_data)
btn_next.grid(row=10, column=3)
# execute the function start
start()
window.mainloop()



