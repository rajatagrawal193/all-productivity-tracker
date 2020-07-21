import os
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash
import mysql.connector
import plotly.graph_objects as go

print('running1')
# mydb = mysql.connector.connect(
#     host="sql12.freemysqlhosting.net",
#     user="sql12356238",
#     password="9DpGYUgdwW",
#     database='sql12356238'
# )
print("running2 ")
# mycursor = mydb.cursor()
# mycursor.execute("SHOW TABLES")
# for item in mycursor:
#     print(item)


def get_sql(par):
    return """select * from Sleepdata WHERE sleep_hours='%s' """ % (par)

    # sql = "SELECT * FROM Sleepdata"


# sqlite_select_query = """SELECT * from database_developers"""
# mycursor.execute(sql)

# def get_records():
#     return records = mycursor.fetchall()

# records=get_records()
# print("Total rows are:  ", len(records))
# print("Printing each row")
# for row in records:
#     print("Id: ", row[0])
#     print("Date: ", row[1])
#     print("sleep_hours: ", row[2])
#     print("\n")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server


# def get_cursor():

#     return mycursor


def get_sleep_graph(par):
    mydb = mysql.connector.connect(
        host="sql12.freemysqlhosting.net",
        user="sql12356247",
        password="Plu8n65DIm",
        database='sql12356247'
    )
    # 9DpGYUgdwW
    mycursor = mydb.cursor()
    # mycursor = get_cursor()
    sql = get_sql(par)
    mycursor.execute(sql)
    records = mycursor.fetchall()
    df = pd.DataFrame({
        "id": [item[0] for item in records],
        "date": [item[1] for item in records],
        "sleep_hours": [item[2] for item in records]
    })

    fig = px.bar(df, x="date", y="sleep_hours")
    mycursor.close()
    return fig


app.layout = html.Div([
    html.H2('Hello World'),
    dcc.Input(id="id", type="number", placeholder="13", debounce=True),
    dcc.Input(id="date", type="number", placeholder="date", debounce=True),
    dcc.Input(id="sleep_hours", type="number",
              placeholder="Sleep hours", debounce=True),
    html.Div(id="output"),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in [5, 6, 20]],
        value=6
    ),
    html.Div(id='display-value'),
    dcc.Graph(
        id='example-graph',
        figure=get_sleep_graph(6)
    )
])

@app.callback(dash.dependencies.Output('example-graph', 'figure'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return get_sleep_graph(value)


@app.callback(
    Output("output", "children"),
    [Input("id", "value"), Input("date", "value"),
     Input('sleep_hours', 'value')],
)
def update_output(id, date, sleep_hours):
    if id and date and sleep_hours:
        print("Entered")
        sql = " INSERT INTO Sleepdata (id, date, sleep_hours) VALUES (%s, %s, %s)"
        val = (id, date, sleep_hours)
        mydb = mysql.connector.connect(
            host="sql12.freemysqlhosting.net",
            user="sql12356247",
            password="Plu8n65DIm",
            database='sql12356247'
        )
        mycursor = mydb.cursor()
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
    return u'id {} and  Date {} and Sleep hours {}'.format(id, date, sleep_hours)


if __name__ == '__main__':
    app.run_server(debug=True)
