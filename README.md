# Introduction of the project

This is a Data Analysis platform for the Big Five Leagues of football,

which is based on python, and the information is from 'https://www.dongqiudi.com/'

## Usage method

To use this Data Analysis Platform, we execute the Analysis_Platform.exe.

As it open, we first select a category that we want to know about, and click the 

"确认" button, then select the league you want to know or enter the player's name you

wan to know about, and click the "search" button to get the information.


Click "搜索信息" button, it will collect the information of the league and player and write them into CSV

file.

###Usage Example

1. Select'联赛积分榜' -> Click'确定' -> Select'Serie A' -> Click'Search' -> Get information

2. Select'球员信息' -> Click'确定' -> enter'佩德里' -> Click'Search' -> Get information

3. Select'联赛射手榜和助攻榜' -> Click'确定' -> select'Ligue 1' -> Click'Search' -> Get information

4. Select'球员信息' -> Click'确定' -> enter'梅西' -> Click'Search' -> Get information

5. Select'球员信息' -> Click'确定' -> enter'本泽马' -> Click'Search' -> Get information

#### note

1. When search the information of the players, you have to enter the Chinese name of the players

2. Only the player who are on the goal list or the assist list of the Big Five Leagues of football

can be found.

3. Premier League and La Liga League data are currently all empty, because the 2022-2023 season has 

alread end. It is determined by the 'https://www.dongqiudi.com/', we can't access information from the 

season 2022-2023. In short, the function of the program works well, just the information on the website 

is empty.

##### Libraries to install

      bs4
      requests
      csv
      json
      tkinter

###### Author

Sun Weitai 孙伟太
邮箱：sun.weitai@foxmail.com
