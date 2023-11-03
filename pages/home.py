from dash import html, register_page, dcc, Input, Output, callback  #, callback # If you need callbacks, import it here.
import pandas as pd
from dash import dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc

df = pd.read_excel("/data/dataton_2023_version2.xlsx")
df_engage = pd.read_csv("Datathon/data/df_engage.csv") #loading data
df_weights = pd.read_csv("Datathon/data/weight_df.csv")
df_score = pd.read_csv("data/engage_scoredf.csv")
categorical_variables = ["Generation","Market", "Checking_Accts_202308", "Savings_Accts_202308","CD_Accts_202308", "Loan_Accts_202308", "CreditCard_Accts_202308", "Mortgage_Accts_202308", "wealth_product_202308" ]

# Dropdown options for x-axis
dropdown_options = [{'label': col, 'value': col} for col in df_engage.columns]



fig1 = px.imshow(df_engage.corr(), x=df_engage.columns, y=df_engage.columns, color_continuous_scale='RdBu')
fig2 = px.pie(df_weights, names='Column', values='Weight', title='')
fig3 = px.scatter()  # Create an empty scatter plot initially
fig4 = px.scatter()


register_page(
    __name__,
    name='Datathon23',
    top_nav=True,
    path='/'
)



@callback(
    Output('scatter-plot', 'figure'),
    Input('dropdown-column', 'value')
)



def update_scatter_plot(selected_column):
    if selected_column:
        fig4 = px.scatter(df_score, x=selected_column, y='engament score')
        return fig4
    else:
        return fig4


@callback(
    Output('bar-plot', 'figure'),
    Input('categorical-column', 'value')
)


def update_bar_plot(selected_column):
    if selected_column:
        # Assuming df_score has a column with the name 'engament score'
        df_score[selected_column]=df[selected_column]
        group_scores = df_score.groupby(selected_column)['engament score'].mean().reset_index()
        fig5 = px.bar(group_scores, x=selected_column, y='engament score')
        return fig5
    else:
        # You can handle this case accordingly, e.g., return an empty figure
        return px.bar()

def layout():
    layout = html.Div([
        html.Hr(style={'width': '80%', 'margin': '0 auto'}),
        html.H1(
            [
               "Digital Customer Behavior Data Analysis"
            ], 
        style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
        ), 
        html.Div(style={'height': '20px'}),
        html.Hr(style={'width': '80%', 'margin': '0 auto'}),  # Horizontal line


        dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Correlation Matrix of Digital engament related variable ", style={'font-size': '18px'}),
                dbc.CardBody([
                    dcc.Graph(figure=fig1),
                ])
            ], color="light"), width=6
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Contribution of each variable to the digital engagement score", style={'font-size': '18px'}),
                dbc.CardBody([
                    dcc.Graph(figure=fig2),
                ])
            ], color="light"), width=6
        ),
    ], style={'text-align': 'center'}),

        html.Div(style={'height': '20px'}),
        html.Hr(style={'width': '80%', 'margin': '0 auto'}),  # Horizontal line


        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Scatter Plot of Digital Engagement Score", style={'font-size': '18px', 'color': 'black'}),
                    dbc.CardBody([
                        # Dropdown menu for x-axis selection
                        dcc.Dropdown(
                            id='dropdown-column',
                            options=dropdown_options,
                            value= "DigLogins_UniqDays",
                            placeholder="Select a column for X-axis"
                        ),
                        html.Div(style={'height': '20px'}),
                        html.Hr(style={'width': '80%', 'margin': '0 auto'}),
                        dcc.Graph(id='scatter-plot', figure=fig4),
                    ])
                ], color="light"),
                width=12
            ),
        ], style={'text-align': 'center'}),

        html.Div(style={'height': '20px'}),
        html.Hr(style={'width': '80%', 'margin': '0 auto'}),  # Horizontal line


        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Scatter Plot of Digital Engagement Score", style={'font-size': '18px'}),
                    dbc.CardBody([
                        # Dropdown menu for x-axis selection
                        dcc.Dropdown(
                            id='categorical-column',
                            options= categorical_variables,
                            value= "Generation",
                            placeholder="Select a categorical column for X-axis"
                        ),
                        html.Div(style={'height': '20px'}),
                        html.Hr(style={'width': '80%', 'margin': '0 auto'}),
                        dcc.Graph(id='bar-plot', figure=fig4),
                    ])
                ], color="light"),
                width=12
            ),
        ], style={'text-align': 'center'}),
])
    return layout

