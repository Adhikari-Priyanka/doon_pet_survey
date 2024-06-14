import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# Sample DataFrame
df = pd.read_csv("F:\\github\\doon_pet_survey\\cat_combine_nona.csv")

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    dcc.Dropdown(
        id='column-dropdown',
        options=[{'label': col, 'value': col} for col in df.columns],
        value=df.columns[0]  # Default value
    ),
    dcc.Graph(id='histogram')
])

# Callback to update the histogram based on selected column
@app.callback(
    Output('histogram', 'figure'),
    [Input('column-dropdown', 'value')]
)
def update_histogram(selected_column):

    # Create histogram
    fig = go.Figure(data=[go.Histogram(x=df[selected_column])])

    fig.update_layout(
    # Set the global font
    font = {
        "family":"Arial",
        "size":16
    },
    # Update title font
    title = {
        "text": f"Distribution of {selected_column.replace('_', ' ')}",
        "y": 0.9, # Sets the y position with respect to `yref`
        "x": 0.5, # Sets the x position of title with respect to `xref`
        "xanchor":"center", # Sets the title's horizontal alignment with respect to its x position
        "yanchor": "top", # Sets the title's vertical alignment with respect to its y position. "      
        "font": { # Only configures font for title
            "family":"Arial",
            "size":20,
            "color": "Black"
        }
    }
)

    # Add X and Y labels
    fig.update_xaxes(title_text="Ages")
    fig.update_yaxes(title_text="Number of cats")

    # Display plot
    #fig.show()
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
