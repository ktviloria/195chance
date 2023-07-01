from dash import dcc
from dash import html
from dash import dash_table
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd
from datetime import date
import plotly.express as px
 
from app import app
from apps import dbconnect as db
 
layout = html.Div(
    [
        dbc.Card(
            [
                dbc.CardHeader(html.H2("Reports")),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                # tabs
                                dbc.Col(
                                    [
                                        dcc.Tabs(
                                            children =[
                                                dcc.Tab(label="PBB", value="tab_pbb", style={"color": "#800000"}, selected_style={'font-weight': 'bold', "color": "#800000"}),
                                                dcc.Tab(label="Promotion", value="tab_prom", style={"color": "#800000"}, selected_style={'font-weight': 'bold', "color": "#800000"}),
                                            ],
                                            id='tabs',
                                            value='tab_pbb',
                                            vertical = True
                                        ),
                                    ],
                                    width=2
                                ),
                                dbc.Col(
                                    html.Div(id='reports'),
                                    width=10
                                ),
                            ],
                            className="mb-3",
                        ),
                        
                    ]
                ),
            ]
        ),
    ]
) 

#reports creation callback
@app.callback( 
    [
        Output('reports', 'children'),
    ], 
    [ 
        Input('url', 'pathname'),
        Input('tabs', 'value'),
    ]
) 

def reports_loadrep(pathname, tabrep): 
    if pathname == '/reports': 
        #pbb reports
        if tabrep == 'tab_pbb':
            sql_pbb = "SELECT pbb_name FROM pbb_reports"
            values_pbb = []
            cols_pbb = ["PBB Reports Created"]
            pbb = db.querydatafromdatabase(sql_pbb, values_pbb, cols_pbb)

            if pbb.shape[0]: 
                reports_list = [
                    html.Div( 
                        [ 
                            dcc.Store(id='pbb_toload', storage_type='memory', data=0), 
                            html.H5("Add Performance-Based Bonus Report"),
                            html.Hr(),
                            dbc.Row( 
                                [ 
                                    dbc.Row(
                                        [
                                            dbc.Label("Report Name", width=2), 
                                            dbc.Col(  
                                                dbc.Input( 
                                                    id='form_pbb_name', type = "text", placeholder="Enter report name" 
                                                ),
                                                width= 8,
                                                className="mb-3",
                                            ), 
                                        ]
                                    ),
                                ], 
                                className="mb-3",
                            ),
                        ],
                        id = 'pbb_rep' 
                    ),
                    html.Div(
                        [
                            dbc.Button('Submit', color="danger", id='pbb_submitbtn', size='lg', className="me-md-2"),
                        ],
                        className="d-grid d-md-flex justify-content-md-end",
                    ),
                    dbc.Modal( 
                        [    
                            dbc.ModalHeader("Saving Progress"), 
                            dbc.ModalBody("tempmessage", id='pbb_feedback_message'), 
                            dbc.ModalFooter( 
                                dbc.Button("Okay", id="pbb_closebtn", className="ms-auto", n_clicks=0) 
                            ),           
                        ], 
                        centered=True, 
                        id="pbb_o_modal", 
                        is_open=False, 
                    ),
                    html.Br(),
                    dbc.Table.from_dataframe(pbb, striped=True, bordered=True, hover=True, size='sm') 
                ]            
            else: 
                reports_list = [html.Div( 
                        [ 
                            dcc.Store(id='pbb_toload', storage_type='memory', data=0), 
                            html.H5("Add Performance-Based Bonus Report"),
                            html.Hr(),
                            dbc.Row( 
                                [ 
                                    dbc.Row(
                                        [
                                            dbc.Label("Report Name", width=2), 
                                            dbc.Col(  
                                                dbc.Input( 
                                                    id='form_pbb_name', type = "text", placeholder="Enter report name" 
                                                ),
                                                width= 8,
                                                className="mb-3",
                                            ), 
                                        ]
                                    ),
                                ], 
                                className="mb-3",
                            ),
                        ],
                        id = 'pbb_rep' 
                    ),
                    html.Div(
                        [
                            dbc.Button('Submit', color="danger", id='pbb_submitbtn', size='lg', className="me-md-2"),
                        ],
                        className="d-grid d-md-flex justify-content-md-end",
                    ),
                    dbc.Modal( 
                        [    
                            dbc.ModalHeader("Saving Progress"), 
                            dbc.ModalBody("tempmessage", id='pbb_feedback_message'), 
                            dbc.ModalFooter( 
                                dbc.Button("Okay", id="pbb_closebtn", className="ms-auto", n_clicks=0) 
                            ),           
                        ], 
                        centered=True, 
                        id="pbb_o_modal", 
                        is_open=False, 
                    ),
                    html.Br(),
                    "No reports created yet."]

        elif tabrep == 'tab_prom':
            sql_prom = "SELECT prom_name FROM prom_reports"
            values_prom = []
            cols_prom = ["Promotional Reports Created"]
            prom = db.querydatafromdatabase(sql_prom, values_prom, cols_prom)

            if prom.shape[0]: 
                reports_list = [html.Div( 
                        [ 
                            dcc.Store(id='prom_toload', storage_type='memory', data=0), 
                            html.H5("Add Report for Promotions"),
                            html.Hr(),
                            dbc.Row( 
                                [ 
                                    dbc.Row(
                                        [
                                            dbc.Label("Report Name", width=2), 
                                            dbc.Col(  
                                                dbc.Input( 
                                                    id='form_prom_name', type = "text", placeholder="Enter report name" 
                                                ),
                                                width= 8,
                                                className="mb-3",
                                            ), 
                                        ]
                                    ),
                                ], 
                                className="mb-3",
                            ),
                        ],
                        id = 'prom_rep' 
                    ),
                    html.Div(
                        [
                            dbc.Button('Submit', color="danger", id='prom_submitbtn', size='lg', className="me-md-2"),
                        ],
                        className="d-grid d-md-flex justify-content-md-end",
                    ),
                    dbc.Modal( 
                        [    
                            dbc.ModalHeader("Saving Progress"), 
                            dbc.ModalBody("tempmessage", id='prom_feedback_message'), 
                            dbc.ModalFooter( 
                                dbc.Button("Okay", id="prom_closebtn", className="ms-auto", n_clicks=0) 
                            ),           
                        ], 
                        centered=True, 
                        id="prom_o_modal", 
                        is_open=False, 
                    ),
                    html.Br(),
                    dbc.Table.from_dataframe(prom, striped=True, bordered=True, hover=True, size='sm')]
            else: 
                reports_list = [html.Div( 
                        [ 
                            dcc.Store(id='prom_toload', storage_type='memory', data=0), 
                            html.H5("Add Report for Promotions"),
                            html.Hr(),
                            dbc.Row( 
                                [ 
                                    dbc.Row(
                                        [
                                            dbc.Label("Report Name", width=2), 
                                            dbc.Col(  
                                                dbc.Input( 
                                                    id='form_prom_name', type = "text", placeholder="Enter report name" 
                                                ),
                                                width= 8,
                                                className="mb-3",
                                            ), 
                                        ]
                                    ),
                                ], 
                                className="mb-3",
                            ),
                        ],
                        id = 'prom_rep' 
                    ),
                    html.Div(
                        [
                            dbc.Button('Submit', color="danger", id='prom_submitbtn', size='lg', className="me-md-2"),
                        ],
                        className="d-grid d-md-flex justify-content-md-end",
                    ),
                    dbc.Modal( 
                        [    
                            dbc.ModalHeader("Saving Progress"), 
                            dbc.ModalBody("tempmessage", id='prom_feedback_message'), 
                            dbc.ModalFooter( 
                                dbc.Button("Okay", id="prom_closebtn", className="ms-auto", n_clicks=0) 
                            ),           
                        ], 
                        centered=True, 
                        id="prom_o_modal", 
                        is_open=False, 
                    ),
                    html.Br(),
                    "No reports created yet."]

        return [reports_list]

    else:
        raise PreventUpdate
