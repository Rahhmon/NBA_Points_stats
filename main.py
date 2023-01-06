from dash import  html, dcc
import pandas as pd
import plotly.graph_objects as go

import nba_scraping
from app import *
import datetime
import plotly.express as px
import dash_bootstrap_components as dbc

##DATA TREATMENT
def get_month(month_day):
    month_day = str(month_day)

    if "January" in month_day:
       return 1
    elif "February" in month_day:
       return 2
    elif "March" in month_day:
       return 3
    elif "April" in month_day:
       return 4
    elif "May" in month_day:
       return 5
    elif "June" in month_day:
       return 6
    elif "July" in month_day:
       return 7
    elif "August" in month_day:
       return 8
    elif "September" in month_day:
       return 9
    elif "October" in month_day:
       return 10
    elif "November" in month_day:
       return 11
    elif "December" in month_day:
       return 12

def get_day(month_day):
    month_day = str(month_day)

    if "January" in month_day:
        return int(str(month_day.replace("January", "").replace(" ", "")))
    elif "February" in month_day:
        return int(str(month_day.replace("February", "").replace(" ", "")))
    elif "March" in month_day:
        return int(str(month_day.replace("March", "").replace(" ", "")))
    elif "April" in month_day:
        return int(str(month_day.replace("April", "").replace(" ", "")))
    elif "May" in month_day:
        return int(str(month_day.replace("May", "").replace(" ", "")))
    elif "June" in month_day:
        return int(str(month_day.replace("June", "").replace(" ", "")))
    elif "July" in month_day:
        return int(str(month_day.replace("July", "").replace(" ", "")))
    elif "August" in month_day:
        return int(str(month_day.replace("August", "").replace(" ", "")))
    elif "September" in month_day:
        return int(str(month_day.replace("September", "").replace(" ", "")))
    elif "October" in month_day:
        return int(str(month_day.replace("October", "").replace(" ", "")))
    elif "November" in month_day:
        return int(str(month_day.replace("November", "").replace(" ", "")))
    elif "December" in month_day:
        return int(str(month_day.replace("December", "").replace(" ", "")))

def data_treatment(df):
    df.drop_duplicates(inplace=True)
    df['month'] = df.apply(lambda x: get_month(x['month_day']), axis=1)
    df['day'] = df.apply(lambda x: get_day(x['month_day']), axis=1)

    df = df.dropna(subset=['day'])
    df = df.dropna(subset=['month'])
    df['date'] = df.apply(lambda x: datetime.datetime(int(x['year']), int(x['month']), int(x['day'])), axis=1)
    df['pts_1t'] = df['pts_1q'] + df['pts_2q']
    df['pts_adv_1t'] = df['pts_adv_1q'] + df['pts_adv_2q']
    df['pts_adv_2t'] = df['pts_adv_3q'] + df['pts_adv_4q']
    df['pts_2t'] = df['pts_3q'] + df['pts_4q']
    df['total_both_teams'] = df['pts_total'] + df['pts_adv_total']
    df['home_away'] = df['home_away'].str.replace(' ', '')

    return df

df = pd.read_csv('data.csv')
df = data_treatment(df)

button_click = 0

# =========  Layout  =========== #
font_type_size = {'font-family': 'Voltaire', 'font-size': '30px'}
graph_theme = 'simple_white'
font_theme=dict(family="Courier New, monospace",
                size=16,color="#1d428a")

app.layout = dbc.Container(children=[
    #First Row
    dbc.Row([
        #Card column
        dbc.Col([
            dbc.Card(
                [
                    html.H5("NBA POINTS SUMMARY", style=font_type_size),
                    html.Hr(),

                    html.H4("Select teams:",style={'margin-top': '20px'}),

                    #First team dropdown
                    html.H6("Select Team A: "),
                    dcc.Dropdown(
                        df['team'].unique(), 'GSW', multi=False, id='team_a_select',

                    ),
                    html.H6("Pitch team A:",style={'margin-top': '8px'}),
                    dcc.RadioItems(['Home', 'Away', 'Both'], 'Both',  id='pitch_A'),

                    #Second team dropdown
                    html.H6("Select Team B: ", style={'margin-top' : '20px'}),
                    dcc.Dropdown(
                        df['team'].unique(), 'BRK', multi=False, id='team_b_select'
                    ),
                    html.H6("Pitch team B:",style={'margin-top': '8px'}),
                    dcc.RadioItems(['Home', 'Away', 'Both'], 'Both',  id='pitch_B'),
                    dcc.Checklist(['Adversary'],['Adversary'], id='cl_adversary', style={'margin-top': '15px'}),
                    html.Hr(style={'margin-top': '40px'}),

                    html.H4("Points comparsion:",style={'margin-top': '20px'}),

                    html.H6("Per quarter: ", style={'margin-top': '10px'}),
                    dcc.Input(id="input_pts_quarter", type="number", value=35,style={'marginRight':'10px'}),
                    html.H6("Per time: ", style={'margin-top': '10px'}),
                    dcc.Input(id="input_pts_time", type="number", value=60, style={'marginRight':'10px'}),
                    html.H6("Per game: ", style={'margin-top': '10px'}),
                    dcc.Input(id="input_pts_game", type="number",  value=100,style={'marginRight':'10px'}),
                    html.H6("Per game (sum): ", style={'margin-top': '10px'}),
                    dcc.Input(id="input_pts_game2", type="number",  value=230,style={'marginRight':'10px'}),

                    html.Hr(style={'margin-top': '40px'}),
                    html.H4("Match population:",style={'margin-top': '20px'}),
                    dcc.Slider(0, 50, step=None,
                      marks={
                          1: '1',
                          5: '5',
                          10: '10',
                          20: '20',
                          50: 'All'
                      },
                      value=5,
                      id='slider_match_amount'),

                    html.Hr(style={'margin-top': '40px'}),
                    dbc.Button("Update matches", color="primary", id='update_button',style={'margin-top': '15px'})
                ], style={"margin": "5px", "padding": "20px"})
        ], lg=2),

        #Graphs column
        dbc.Col([
            dbc.Card([
            #First graph row: will content the graphs with points per quarter of team A
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Col(dcc.Graph(id='first_quarter_team_A', config={"displayModeBar": False, "showTips": False})),
                            html.P(id='first_quarter_resume_team_A')
                        ])
                    ])
                ], lg=4, sm=12),

                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Col(dcc.Graph(id='first_time_team_A',
                                              config={"displayModeBar": False, "showTips": False})),
                            html.P(id='first_time_resume_team_A')
                        ])
                    ])
                ], lg=4, sm=12),

                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Col(dcc.Graph(id='all_team_A',
                                              config={"displayModeBar": False, "showTips": False})),
                            html.P(id='all_resume_team_A')
                        ])
                    ])
                ], lg=4, sm=12),

            ], style={'margin-top': '20px'}),

            #Second graph row: will content the graphs with points per quarter of team B
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Col(dcc.Graph(id='first_quarter_team_B',
                                              config={"displayModeBar": False, "showTips": False})),
                            html.P(id='first_quarter_resume_team_B')
                        ])
                    ])
                ], lg=4, sm=12),

                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Col(dcc.Graph(id='first_time_team_B',
                                              config={"displayModeBar": False, "showTips": False})),
                            html.P(id='first_time_resume_team_B')
                        ])
                    ])
                ], lg=4, sm=12),

                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Col(dcc.Graph(id='all_team_B',
                                              config={"displayModeBar": False, "showTips": False})),
                            html.P(id='all_resume_team_B')
                        ])
                    ])
                ], lg=4, sm=12),

            ],style={'margin-top': '20px'}),

            #Fourth graph row: will content the graphs with all points of team A and B
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Col(dcc.Graph(id='all_both_teams_A',
                                              config={"displayModeBar": False, "showTips": False})),
                            html.P(id='all_sum_resume_team_A')
                        ])
                    ])
                ], lg=6, sm=12),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Col(dcc.Graph(id='all_both_teams_B',
                                              config={"displayModeBar": False, "showTips": False})),
                            html.P(id='all_sum_resume_team_B')
                        ])
                    ])
                ], lg=6, sm=12),
            ], style={'margin-top': '20px'}),
                ],style={"margin": "5px", "padding": "10px"})
        ], lg=10)
    ])
], style={"padding": "0px"}, fluid=True)

#CALLBACKS
@app.callback(
    [dash.dependencies.Output("first_quarter_team_A", "figure"),
     dash.dependencies.Output("first_quarter_team_B", "figure"),
     dash.dependencies.Output("first_time_team_A", "figure"),
     dash.dependencies.Output("first_time_team_B", "figure"),
     dash.dependencies.Output("all_team_A", "figure"),
     dash.dependencies.Output("all_team_B", "figure"),
     dash.dependencies.Output("all_both_teams_A", "figure"),
     dash.dependencies.Output("all_both_teams_B", "figure"),
     dash.dependencies.Output('first_quarter_resume_team_A', 'children'),
     dash.dependencies.Output('first_quarter_resume_team_B', 'children'),
     dash.dependencies.Output('first_time_resume_team_A', 'children'),
     dash.dependencies.Output('first_time_resume_team_B', 'children'),
     dash.dependencies.Output('all_resume_team_A', 'children'),
     dash.dependencies.Output('all_resume_team_B', 'children'),
     dash.dependencies.Output('all_sum_resume_team_A', 'children'),
     dash.dependencies.Output('all_sum_resume_team_B', 'children')],
    [dash.dependencies.Input("team_a_select", "value"),
    dash.dependencies.Input("team_b_select", "value"),
    dash.dependencies.Input("pitch_A", "value"),
    dash.dependencies.Input("pitch_B", "value"),
    dash.dependencies.Input("input_pts_quarter", "value"),
    dash.dependencies.Input("input_pts_time", "value"),
    dash.dependencies.Input("input_pts_game", "value"),
    dash.dependencies.Input("input_pts_game2", "value"),
    dash.dependencies.Input('update_button', 'n_clicks'),
    dash.dependencies.Input('slider_match_amount', 'value'),
    dash.dependencies.Input('cl_adversary', 'value')])

def display_graphs(team_a, team_b, pitch_a, pitch_b, pts_quarter, pts_time, pts_game, pts_game_sum, n_clicks, population, cl_adversary):
    if(pitch_a != 'Both'):
        if(pitch_a == 'Home'):
            dff_a = df[df['team'] == team_a]
            dff_a = dff_a[dff_a['home_away'] == 'home'].tail(population)
        else:
            dff_a = df[df['team'] == team_a]
            dff_a = dff_a[dff_a['home_away'] == 'away'].tail(population)
    else:
        dff_a = df[df['team'] == team_a].tail(population)

    if (pitch_b != 'Both'):
        if (pitch_b == 'Home'):
            dff_b = df[df['team'] == team_b]
            dff_b = dff_b[dff_b['home_away'] == 'home'].tail(population)
        else:
            dff_b = df[df['team'] == team_b]
            dff_b = dff_b[dff_b['home_away'] == 'away'].tail(population)
    else:
        dff_b = df[df['team'] == team_b].tail(population)


    #Graphs of points per quarter of team A
    first_quarter_team_A = px.scatter(dff_a, x="date", y="pts_1q", title=f'Pontos de {team_a} no primeiro quarto')
    first_quarter_team_A.add_trace(go.Line(x=dff_a['date'], y=(len(dff_a['pts_1q']) * [pts_quarter]), name=f'{pts_quarter}'))
    first_quarter_team_A.update_layout(template=graph_theme,title_x=0.5,font=font_theme)
    first_quarter_resume_A = f'{team_a} scored {pts_quarter} points \
            {len(dff_a[dff_a["pts_1q"] > pts_quarter]) / len(dff_a["pts_1q"]) * 100:.2f}% of times in the last {population} matches\n' \
                           f'{team_a} got scored by {pts_quarter} points \
            {len(dff_a[dff_a["pts_adv_1q"] > pts_quarter]) / len(dff_a["pts_adv_1q"]) * 100:.2f}% of times in the last {population} matches'

    #Graphs of points per quarter of team B
    first_quarter_team_B = px.scatter(dff_b, x="date", y="pts_1q", title=f'Pontos de {team_b} no primeiro quarto')
    first_quarter_team_B.add_trace(go.Line(x=dff_b['date'], y=(len(dff_b['pts_1q']) * [pts_quarter]), name=f'{pts_quarter}'))
    first_quarter_team_B.update_layout(template=graph_theme,title_x=0.5,font=font_theme)
    first_quarter_resume_B = f'{team_b} scored {pts_quarter} points \
                {len(dff_b[dff_b["pts_1q"] > pts_quarter]) / len(dff_b["pts_1q"]) * 100:.2f}% of times in the last {population} matches\n' \
                             f'{team_b} got scored by {pts_quarter} points \
                {len(dff_b[dff_b["pts_adv_1q"] > pts_quarter]) / len(dff_b["pts_adv_1q"]) * 100:.2f}% of times in the last {population} matches'

    #Graphs of points per half time of team A
    first_time_team_A = px.scatter(dff_a, x="date", y="pts_1t", title=f'Pontos de {team_a} no primeiro tempo')
    first_time_team_A.add_trace(go.Line(x=dff_a['date'], y=(len(dff_a['pts_1t']) * [pts_time]), name=f'{pts_time}'))
    first_time_team_A.update_layout(template=graph_theme,title_x=0.5,font=font_theme)
    first_time_resume_A = f'{team_a} scored {pts_time} points \
                {len(dff_a[dff_a["pts_1t"] > pts_time]) / len(dff_a["pts_1t"]) * 100:.2f}% of times in the last {population} matches\n' \
                             f'{team_a} got scored by {pts_time} points \
                {len(dff_a[dff_a["pts_adv_1t"] > pts_time]) / len(dff_a["pts_adv_1t"]) * 100:.2f}% of times in the last {population} matches'

    # Graphs of points per half time of team B
    first_time_team_B = px.scatter(dff_b, x="date", y="pts_1t", title=f'Pontos de {team_b} no primeiro tempo')
    first_time_team_B.add_trace(go.Line(x=dff_b['date'], y=(len(dff_b['pts_1t']) * [pts_time]), name=f'{pts_time}'))
    first_time_team_B.update_layout(template=graph_theme,title_x=0.5,font=font_theme)
    first_time_resume_B = f'{team_b} scored {pts_time} points \
                {len(dff_b[dff_b["pts_1t"] > pts_time]) / len(dff_b["pts_1t"]) * 100:.2f}% of times in the last {population} matches\n' \
                             f'\n{team_b} got scored by {pts_time} points \
                {len(dff_b[dff_b["pts_adv_1t"] > pts_time]) / len(dff_b["pts_1t"]) * 100:.2f}% of times in the last {population} matches'

    # Graphs of total points of team A
    all_team_A = px.scatter(dff_a, x="date", y="pts_total", title=f'Pontos de {team_a} no jogo')
    all_team_A.add_trace(go.Line(x=dff_a['date'], y=(len(dff_a['pts_total']) * [pts_game]), name=f'{pts_game}'))
    all_team_A.update_layout(template=graph_theme,title_x=0.5,font=font_theme)
    full_time_resume_A = f'{team_a} scored {pts_game} points \
                {len(dff_a[dff_a["pts_total"] > pts_game]) / len(dff_a["pts_total"]) * 100:.2f}% of times in the last {population} matches\n' \
                             f'\n{team_a} got scored by {pts_game} points \
                {len(dff_a[dff_a["pts_adv_total"] > pts_game]) / len(dff_a["pts_adv_total"]) * 100:.2f}% of times in the last {population} matches'

    # Graphs of total points of team A
    all_team_B = px.scatter(dff_b, x="date", y="pts_total", title=f'Pontos de {team_b} no jogo')
    all_team_B.add_trace(go.Line(x=dff_b['date'], y=(len(dff_b['pts_total']) * [pts_game]), name=f'{pts_game}'))
    all_team_B.update_layout(template=graph_theme, title_x=0.5, font=font_theme)
    full_time_resume_B = f'{team_b} scored {pts_game} points \
                    {len(dff_b[dff_b["pts_total"] > pts_game]) / len(dff_b["pts_total"]) * 100:.2f}% of times in the last {population} matches\n' \
                         f'\n{team_b} got scored by {pts_game} points \
                    {len(dff_b[dff_b["pts_adv_total"] > pts_game]) / len(dff_b["pts_adv_total"]) * 100:.2f}% of times in the last {population} matches'

    # Graphs of total points of team A
    all_both_teams_team_A = px.scatter(dff_a, x="date", y="total_both_teams", title=f'Pontos totais de {team_a} no jogo')
    all_both_teams_team_A.add_trace(go.Line(x=dff_a['date'], y=(len(dff_a['pts_total']) * [pts_game_sum]), name=f'{pts_game_sum}'))
    all_both_teams_team_A.update_layout(template=graph_theme,title_x=0.5,font=font_theme)
    total_both_resume_A = f'{team_a} got {pts_game_sum} points in sum of score (Own + Adv) in\
                    {len(dff_a[dff_a["total_both_teams"] > pts_game_sum]) / len(dff_a["total_both_teams"]) * 100:.2f}\
                    % of times in the last {population} matches'

    # Graphs of total points of team B
    all_both_teams_team_B = px.scatter(dff_b, x="date", y="total_both_teams", title=f'Pontos de {team_b} no jogo')
    all_both_teams_team_B.add_trace(go.Line(x=dff_b['date'], y=(len(dff_b['pts_total']) * [pts_game_sum]), name=f'{pts_game_sum}'))
    all_both_teams_team_B.update_layout(template=graph_theme, title_x=0.5, font=font_theme)
    total_both_resume_B = f'{team_b} got {pts_game_sum} points in sum of score (Own + Adv) in\
                        {len(dff_b[dff_b["total_both_teams"] > pts_game_sum]) / len(dff_b["total_both_teams"]) * 100:.2f}\
                        % of times in the last {population} matches'

    # Adversary marks
    if(cl_adversary != []):
        first_quarter_team_A.add_trace(
            go.Line(x=dff_a['date'], y=dff_a['pts_adv_1q'], name=f'Adversário', mode='markers', marker_color='red'))
        first_quarter_team_B.add_trace(
            go.Line(x=dff_b['date'], y=dff_b['pts_adv_1q'], name=f'Adversário', mode='markers', marker_color='red'))
        first_time_team_A.add_trace(
            go.Line(x=dff_a['date'], y=dff_a['pts_adv_1t'], name=f'Adversário', mode='markers', marker_color='red'))
        first_time_team_B.add_trace(
            go.Line(x=dff_b['date'], y=dff_b['pts_adv_1t'], name=f'Adversário', mode='markers', marker_color='red'))
        all_team_A.add_trace(
            go.Line(x=dff_a['date'], y=dff_a['pts_adv_total'], name=f'Adversário', mode='markers', marker_color='red'))
        all_team_B.add_trace(
            go.Line(x=dff_a['date'], y=dff_a['pts_adv_total'], name=f'Adversário', mode='markers', marker_color='red'))

    global button_click
    if(n_clicks is None):
        print("")
    else:
        if(n_clicks == button_click):
            print('')
        else:
            print('downloading')
            button_click = n_clicks
            nba_scraping.update_csv_matches()

    return first_quarter_team_A, first_quarter_team_B, first_time_team_A, first_time_team_B,\
           all_team_A,all_team_B, all_both_teams_team_A, all_both_teams_team_B, first_quarter_resume_A, \
           first_quarter_resume_B, first_time_resume_A, first_time_resume_B, full_time_resume_A, full_time_resume_B,\
           total_both_resume_A, total_both_resume_B

#EXECUTE
if __name__ == '__main__':
    app.run_server(debug=True)