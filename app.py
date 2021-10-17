# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import pathlib

from dash.dependencies import Input, Output
from urllib.parse import quote as urlquote
from flask import Flask, send_from_directory, send_file

from generators import generate_table, generate_world_map, generate_europe_map

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Used dataset names
DATA_ESTATES = 'estates.csv'

df = pd.read_csv('data/{}'.format(DATA_ESTATES))

# Normally, Dash creates its own Flask server internally. By creating our own,
# we can create a route for downloading files directly:
server = Flask(__name__)


@server.route("/data/<path:path>")
def download(path):
    """Downloads the desired file from the data folder."""
    return send_file('data/' + path,
                     mimetype='text/csv',
                     attachment_filename=path,
                     as_attachment=True)


# Download link generation
def file_download_link(filename):
    """Creates a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/data/{}".format(urlquote(filename))
    return html.Div(
        [
            html.A(
                html.Button("Stáhnout kompletní dataset: " + filename),
                href=location,
            )
        ],
        className="download-button"
    )


app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=server)

server = app.server

app.layout = html.Div(
    children=[
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src='assets/Logo-text.png',
                            draggable='False',
                            id="logo",
                            height='auto',
                            width=170,
                        ),
                    ],
                    className="three columns",
                ),
                html.Div(
                    [
                        html.H3(
                            "Mapa cen nemovitostí",
                            style={"margin-bottom": "0px"},
                        ),
                        html.H5(
                            "Dashboard pro usnadnění výběru nemovitosti",
                            style={"margin-top": "0px"}
                        ),

                    ],
                    className="eight columns",
                    id="title",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Kontaktovat autora", id="contact-button"),
                            href="mailto:marek.szeles@eforce.cvut.cz",
                        )
                    ],
                    className="two columns",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),

        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    children=[
                                        # Paste input map
                                        html.Img(
                                            src="assets/map-showcase.png",
                                            draggable='False',
                                            id="map_showcase",
                                            #height=150,
                                            width='auto',
                                        ),
                                        html.Div(
                                            # px.set_mapbox_access_token(open(".mapbox_token").read())
                                            # df = px.data.carshare()
                                            # fig = px.scatter_mapbox(df, lat="centroid_lat", lon="centroid_lon",     color="peak_hour", size="car_hours",
                                            #                   color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)
                                            # fig.show()
                                        )
                                    ],
                                    id="un_description",
                                    className="pretty_container description twelve columns flex-display"
                                ),
                            ],
                            className="content_holder row twelve columns flex-display"
                        ),
                    ],
                    className="pretty_container_bg twelve columns",
                ),
            ],
            className="row flex-display",
        ),


    ],
    id="mainContainer",
    style={'columnCount': 1, "display": "flex", "flex-direction": "column"},
)

app.title = 'Get Real dashboard'



if __name__ == '__main__':
    app.run_server(debug=True)
