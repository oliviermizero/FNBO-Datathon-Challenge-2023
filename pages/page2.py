
import pandas as pd
import numpy as np
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash import register_page, Input, Output, callback, State
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
from .PredictModel import PredictModel

# Load the data
df_engage = pd.read_csv("/Users/mshyaka2/Desktop/Datathon/data/df_engage.csv")

# register the page
register_page(
    __name__,
    name='Score Prediction',
    top_nav=True,
    path='/page2'
)


# Dropdown options for x-axis
dropdown_options = [{'label': col, 'value': col} for col in df_engage.columns]

# Layout for the Score Prediction page
# ... (previous code)

# Create a list of dbc.Cards for input values
input_cards = []

for option in dropdown_options:
    input_cards.append(
        dbc.Card([
            dbc.CardHeader(option['label'], style={'font-size': '18px'}),
            dbc.CardBody([
                dcc.Input(id=f'input-{option["value"]}', type='number', step=1),
            ])
        ], color="light")
    )

# Layout for the Score Prediction page
def layout():
    input_elements = []
    for column in dropdown_options:
        input_elements.append(html.Div([
            html.H5(column['label'], style={'font-size': '14px'}),  # Title with the column name
            dcc.Input(id=column["value"], type='number')
        ], className='input-card'))

    input_cards = []
    for i in range(0, len(input_elements), 3):
        input_row = html.Div([input_elements[i], input_elements[i+1], input_elements[i+2]], className='input-row')
        input_cards.append(input_row)

    return html.Div([
        html.Hr(style={'width': '80%', 'margin': '0 auto'}),
        html.H1("Digital Engagement Score Prediction",
                style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}),
        html.Div(style={'height': '20px'}),
        html.Hr(style={'width': '80%', 'margin': '0 auto'}),  # Horizontal line
       
        dbc.Card([
            dbc.CardHeader("Input Values for Prediction", style={'font-size': '18px'}),
            dbc.CardBody([
                html.Div(id="prediction-output"),
                html.Div("Enter input values for each column:"),
                 html.Div(input_cards),
                #html.Div(input_cards),  # Replace the dropdown with input cards
                html.Button('Predict Score', id='predict-button', n_clicks=0),
                html.Button('Clear Inputs', id='clear-button', n_clicks=0),

            ])
        ], color="light")
    ])

# Define the callback to predict the score
# Create a list of input elements for the callback
input_elements = [Input(f'input-{option["value"]}', 'value') for option in dropdown_options]
# Create an instance of the PredictModel
predictor = PredictModel()

# In your callback function
# In your callback function
@callback(
    Output('prediction-output', 'children'),
    Output('clear-button', 'n_clicks'),
    *[Output(column["value"], 'value') for column in dropdown_options],  # Add outputs for each input
    Input('predict-button', 'n_clicks'),
    Input('clear-button', 'n_clicks'),
    *[State(column["value"], 'value') for column in dropdown_options],
)
def update_output(predict_clicks, clear_clicks, *input_values):
    if clear_clicks > 0:
        # Clear input values
        for i in range(len(dropdown_options)):
            input_id = dropdown_options[i]["value"]
            dash.callback_context.states[input_id] = None
        # Drop the last row from df_engage
        df_engage.drop(df_engage.index[-1], inplace=True)
        return "Inputs cleared", 0, *([None] * len(dropdown_options))  # Reset all input values
    elif predict_clicks > 0:
        # Update the last row of df_engage with the input values
        input_values_list = [float(value) if value else 0.0 for value in input_values]

        last_row = pd.Series(data=dict(zip([option["value"] for option in dropdown_options], input_values_list)))
        df_engage.loc[df_engage.index[-1]] = last_row
        print("Input Values List:", input_values_list)
        
        # Perform prediction using the PredictModel class
        scaled_score = predictor.fit_and_predict_score(df_engage)  # Pass the input data

        # Return the scaled score and reset all input values
        return f"Predicted Score: {scaled_score:.2f}", clear_clicks, *input_values 

    else:
        return dash.no_update, clear_clicks, *input_values  # No changes if not predicting or clearing