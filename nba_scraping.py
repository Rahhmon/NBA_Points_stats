import requests
import bs4
import time
import pandas as pd

#Get all the matches links, from a given list of schedule games
def get_matches_links():

    month_schedule = [
        "https://www.basketball-reference.com/leagues/NBA_2023_games-october.html",
        "https://www.basketball-reference.com/leagues/NBA_2023_games-november.html",
        "https://www.basketball-reference.com/leagues/NBA_2023_games-december.html",
        "https://www.basketball-reference.com/leagues/NBA_2023_games-january.html",
        "https://www.basketball-reference.com/leagues/NBA_2023_games-february.html",
        "https://www.basketball-reference.com/leagues/NBA_2023_games-march.html",
        "https://www.basketball-reference.com/leagues/NBA_2023_games-april.html"]
    match_links = []

    for ms in month_schedule:
        request_result = requests.get(ms)
        soup = bs4.BeautifulSoup(request_result.text, "html.parser")

        all = soup.find("div", id="all_schedule")
        tbody = all.find("tbody")
        links = tbody.find_all("a", href=True)

        for l in links:
            if ("boxscores" in str(l['href'])) & ("index" not in str(l['href'])):
                match_links.append(("https://www.basketball-reference.com/"+l['href']))

        time.sleep(3)

    return match_links

#With the matches links taken above, get each particular match stats
def get_nba_match_scores(match_link):
    try:
        request_result = requests.get(match_link)

        soup = bs4.BeautifulSoup(request_result.text, "html.parser")
        trequest = soup.find("div", id="all_line_score")
        header = soup.find("h1")

        day_month = header.text.split(",")[1]
        year = header.text.split(",")[2]

        tags = str(trequest)

        start_at = int(tags.index('<tbody>'))+7
        ends_at = int(tags.index('</table>'))

        info = (tags[start_at:ends_at]).replace("<tr >", "")
        info.replace("</td>", "")
        extracted_tags = bs4.BeautifulSoup(info, 'html.parser')

        teams = extracted_tags.find_all("a")
        scores = extracted_tags.find_all("td")

        result_tupleA = []
        result_tupleB = []
        match_winner = ""
        first_quarter_winner = ""
        second_quarter_winner = ""
        third_quarter_winner = ""
        fourth_quarter_winner = ""

        time.sleep(3)

    except IndexError:
        return [0], [0]

    #Define os vencedores do 1º, 2º, 3º, 4º quarto e da partida - caso não haja prorrogação
    if(len(scores) == 10):
        #Define o vencedor da partida
        if(int(scores[9].text) > int(scores[4].text)):
            match_winner = teams[1].text
        else:
            match_winner = teams[0].text
        #______________________________________

        #Define o vencedor do primeiro quarto
        if(int(scores[0].text) > int(scores[5].text)):
            first_quarter_winner = teams[0].text
        else:
            first_quarter_winner = teams[1].text
        #______________________________________

        #Define o vencedor do segundo quarto
        if(int(scores[1].text) > int(scores[6].text)):
            second_quarter_winner = teams[0].text
        else:
            second_quarter_winner = teams[1].text
        #______________________________________

        #Define o vencedor do terceiro quarto
        if(int(scores[2].text) > int(scores[7].text)):
            third_quarter_winner = teams[0].text
        else:
            third_quarter_winner = teams[1].text
        #______________________________________

        #Define o vencedor do quarto quarto
        if(int(scores[3].text) > int(scores[8].text)):
            fourth_quarter_winner = teams[0].text
        else:
            fourth_quarter_winner = teams[1].text
        #______________________________________

    # Define os vencedores do 1º, 2º, 3º, 4º quarto e da partida - caso haja uma prorrogação
    elif(len(scores) == 12):
        #Define o vencedor da partida
        if (int(scores[11].text) > int(scores[5].text)):
            match_winner = teams[1].text
        else:
            match_winner = teams[0].text
        # ______________________________________

        # Define o vencedor do primeiro quarto
        if (int(scores[0].text) > int(scores[6].text)):
            first_quarter_winner = teams[0].text
        else:
            first_quarter_winner = teams[1].text
        # ______________________________________

        # Define o vencedor do segundo quarto
        if (int(scores[1].text) > int(scores[7].text)):
            second_quarter_winner = teams[0].text
        else:
            second_quarter_winner = teams[1].text
        # ______________________________________

        # Define o vencedor do terceiro quarto
        if (int(scores[2].text) > int(scores[8].text)):
            third_quarter_winner = teams[0].text
        else:
            third_quarter_winner = teams[1].text
        # ______________________________________

        # Define o vencedor do quarto quarto
        if (int(scores[3].text) > int(scores[9].text)):
            fourth_quarter_winner = teams[0].text
        else:
            fourth_quarter_winner = teams[1].text
        # ______________________________________

    # Define os vencedores do 1º, 2º, 3º, 4º quarto e da partida - caso haja duas prorrogações
    elif (len(scores) == 14):
        # Define o vencedor da partida
        if (int(scores[13].text) > int(scores[6].text)):
            match_winner = teams[1].text
        else:
            match_winner = teams[0].text
        # ______________________________________

        # Define o vencedor do primeiro quarto
        if (int(scores[0].text) > int(scores[7].text)):
            first_quarter_winner = teams[0].text
        else:
            first_quarter_winner = teams[1].text
        # ______________________________________

        # Define o vencedor do segundo quarto
        if (int(scores[1].text) > int(scores[8].text)):
            second_quarter_winner = teams[0].text
        else:
            second_quarter_winner = teams[1].text
        # ______________________________________
        # Define o vencedor do terceiro quarto
        if (int(scores[2].text) > int(scores[9].text)):
            third_quarter_winner = teams[0].text
        else:
            third_quarter_winner = teams[1].text
        # ______________________________________
        # Define o vencedor do quarto quarto
        if (int(scores[3].text) > int(scores[10].text)):
            fourth_quarter_winner = teams[0].text
        else:
            fourth_quarter_winner = teams[1].text
        # ______________________________________

    #Define as tuplas de resultados
    if(len(scores) == 10):
        result_tupleA = [teams[0].text,  # Equipe A - nome
                        scores[0].text,  # Equipe A - Pontos no 1 Quarto
                        scores[1].text,  # Equipe A - Pontos no 2 Quarto
                        scores[2].text,  # Equipe A - Pontos no 3 Quarto
                        scores[3].text,  # Equipe A - Pontos no 4 Quarto
                        0,  # Equipe A - Pontos na primeira prorrogação
                        0,  # Equipe A - Pontos na segunda prorrogação
                        scores[4].text,  # Equipe A - Pontos Totais

                        teams[1].text,  # Equipe B - nome
                        scores[5].text,  # Equipe B - Pontos no 1 Quarto
                        scores[6].text,  # Equipe B - Pontos no 2 Quarto
                        scores[7].text,  # Equipe B - Pontos no 3 Quarto
                        scores[8].text,  # Equipe B - Pontos no 4 Quarto
                        0,  # Equipe B - Pontos na primeira prorrogação
                        0,  # Equipe B - Pontos na segunda prorrogação
                        scores[9].text,  # Equipe B - Pontos Totais
                        first_quarter_winner,
                        second_quarter_winner,
                        third_quarter_winner,
                        fourth_quarter_winner,
                        match_winner,
                        "away"
                        ]
        result_tupleB = [
                        teams[1].text,  # Equipe B - nome
                        scores[5].text,  # Equipe B - Pontos no 1 Quarto
                        scores[6].text,  # Equipe B - Pontos no 2 Quarto
                        scores[7].text,  # Equipe B - Pontos no 3 Quarto
                        scores[8].text,  # Equipe B - Pontos no 4 Quarto
                        0,  # Equipe B - Pontos na primeira prorrogação
                        0,  # Equipe B - Pontos na segunda prorrogação
                        scores[9].text,  # Equipe B - Pontos Totais

                         teams[0].text,  # Equipe A - nome
                         scores[0].text,  # Equipe A - Pontos no 1 Quarto
                         scores[1].text,  # Equipe A - Pontos no 2 Quarto
                         scores[2].text,  # Equipe A - Pontos no 3 Quarto
                         scores[3].text,  # Equipe A - Pontos no 4 Quarto
                         0,  # Equipe A - Pontos na primeira prorrogação
                         0,  # Equipe A - Pontos na segunda prorrogação
                         scores[4].text,  # Equipe A - Pontos Totais
                         first_quarter_winner,
                         second_quarter_winner,
                         third_quarter_winner,
                         fourth_quarter_winner,
                         match_winner,
                         "home"
                         ]
    #Se houver uma prorrogação
    if(len(scores) == 12):
        result_tupleA = [teams[0].text,  # Equipe A - nome
                        scores[0].text,  # Equipe A - Pontos no 1 Quarto
                        scores[1].text,  # Equipe A - Pontos no 2 Quarto
                        scores[2].text,  # Equipe A - Pontos no 3 Quarto
                        scores[3].text,  # Equipe A - Pontos no 4 Quarto
                        scores[4].text,  # Equipe A - Pontos na primeira prorrogação
                        0,  # Equipe A - Pontos na segunda prorrogação
                        scores[5].text,  # Equipe A - Pontos Totais

                        teams[1].text,  # Equipe B - nome
                        scores[6].text,  # Equipe B - Pontos no 1 Quarto
                        scores[7].text,  # Equipe B - Pontos no 2 Quarto
                        scores[8].text,  # Equipe B - Pontos no 3 Quarto
                        scores[9].text,  # Equipe B - Pontos no 4 Quarto
                        scores[10].text,  # Equipe B - Pontos na primeira prorrogação
                        0,  # Equipe B - Pontos na segunda prorrogação
                        scores[11].text,  # Equipe B - Pontos Totais
                        first_quarter_winner,
                        second_quarter_winner,
                        third_quarter_winner,
                        fourth_quarter_winner,
                        match_winner,
                         "away"
                        ]
        result_tupleB = [teams[1].text,  # Equipe B - nome
                         scores[6].text,  # Equipe B - Pontos no 1 Quarto
                         scores[7].text,  # Equipe B - Pontos no 2 Quarto
                         scores[8].text,  # Equipe B - Pontos no 3 Quarto
                         scores[9].text,  # Equipe B - Pontos no 4 Quarto
                         scores[10].text,  # Equipe B - Pontos na primeira prorrogação
                         0,  # Equipe B - Pontos na segunda prorrogação

                         scores[11].text,  # Equipe B - Pontos Totais
                         teams[0].text,  # Equipe A - nome
                         scores[0].text,  # Equipe A - Pontos no 1 Quarto
                         scores[1].text,  # Equipe A - Pontos no 2 Quarto
                         scores[2].text,  # Equipe A - Pontos no 3 Quarto
                         scores[3].text,  # Equipe A - Pontos no 4 Quarto
                         scores[4].text,  # Equipe A - Pontos na primeira prorrogação
                         0,  # Equipe A - Pontos na segunda prorrogação
                         scores[5].text,  # Equipe A - Pontos Totais
                         first_quarter_winner,
                         second_quarter_winner,
                         third_quarter_winner,
                         fourth_quarter_winner,
                         match_winner,
                         "home"
                         ]
    # Se houver duas prorrogações
    if (len(scores) == 14):
        result_tupleA = [teams[0].text,  # Equipe A - nome
                            scores[0].text,  # Equipe A - Pontos no 1 Quarto
                            scores[1].text,  # Equipe A - Pontos no 2 Quarto
                            scores[2].text,  # Equipe A - Pontos no 3 Quarto
                            scores[3].text,  # Equipe A - Pontos no 4 Quarto
                            scores[4].text,  # Equipe A - Pontos na primeira prorrogação
                            scores[5].text,  # Equipe A - Pontos na segunda prorrogação
                            scores[6].text,  # Equipe A - Pontos Totais

                            teams[1].text,  # Equipe B - nome
                            scores[7].text,  # Equipe B - Pontos no 1 Quarto
                            scores[8].text,  # Equipe B - Pontos no 2 Quarto
                            scores[9].text,  # Equipe B - Pontos no 3 Quarto
                            scores[10].text,  # Equipe B - Pontos no 4 Quarto
                            scores[11].text,  # Equipe B - Pontos na primeira prorrogação
                            scores[12].text,  # Equipe B - Pontos na segunda prorrogação
                            scores[13].text,  # Equipe B - Pontos Totais
                            first_quarter_winner,
                            second_quarter_winner,
                            third_quarter_winner,
                            fourth_quarter_winner,
                            match_winner,
                            "away"
                            ]

        result_tupleB = [teams[1].text,  # Equipe B - nome
                             scores[7].text,  # Equipe B - Pontos no 1 Quarto
                             scores[8].text,  # Equipe B - Pontos no 2 Quarto
                             scores[9].text,  # Equipe B - Pontos no 3 Quarto
                             scores[10].text,  # Equipe B - Pontos no 4 Quarto
                             scores[11].text,  # Equipe B - Pontos na primeira prorrogação
                             scores[12].text,  # Equipe B - Pontos na segunda prorrogação
                             scores[13].text,  # Equipe B - Pontos Totais

                             teams[0].text,  # Equipe A - nome
                             scores[0].text,  # Equipe A - Pontos no 1 Quarto
                             scores[1].text,  # Equipe A - Pontos no 2 Quarto
                             scores[2].text,  # Equipe A - Pontos no 3 Quarto
                             scores[3].text,  # Equipe A - Pontos no 4 Quarto
                             scores[4].text,  # Equipe A - Pontos na primeira prorrogação
                             scores[5].text,  # Equipe A - Pontos na segunda prorrogação
                             scores[6].text,  # Equipe A - Pontos Totais
                             first_quarter_winner,
                             second_quarter_winner,
                             third_quarter_winner,
                             fourth_quarter_winner,
                             match_winner,
                             "home"
                            ]

    result_tupleB.append(day_month)
    result_tupleA.append(day_month)
    result_tupleB.append(year)
    result_tupleA.append(year)

    return result_tupleA, result_tupleB

def update_csv_matches():
    #Calls the function for getting the matches links, and add it to 'links' list
    links = get_matches_links()
    print(f"Total de partidas: {(len(links))}")

    #Read the csv file with the content already scraped
    old_df = pd.read_csv('C:/Users/User/Desktop/dash_points_nba/data.csv')
    #calculate the number of matches already downloaded
    n_matches = int(len(old_df['team']) / 2)

    #The new results will be save here
    results = []
    for l in links[n_matches:]:
        a, b = get_nba_match_scores(l)
        results.append(a)
        results.append(b)

    #Creates a new DataFrame with the unscraped results, append and write it to a new file
    new_df = pd.DataFrame(results)
    #old_df.append(new_df)
    new_df.to_csv('data.csv', index=False, header=False, mode='a')

