
from dash import dcc
from dash import html
from dash import dash_table
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd
import datetime as dt
from datetime import date
 
from app import app
from apps import dbconnect as db
 
from urllib.parse import urlparse, parse_qs

mod_style = { 
 'color': '#fff',
 'background-color': '#b22222',
 'font-size': '25px'
} 

layout = html.Div(
    [
        html.Div( 
        [ 
            dcc.Store(id='form_upd_unit_toload', storage_type='memory', data=0), 
            html.H5("Add UP Diliman Unit"),
            html.Hr(),
            dbc.Alert('Please supply information in input field.', color="danger", id='upd_inputs_alert', is_open=False),
            dbc.Row( 
                [ 
                    dbc.Row(
                        [
                            dbc.Label("UP Diliman Unit", width=2), 
                            dbc.Col(  
                                dbc.Input( 
                                    id='form_upd_unit_title', type = "text", placeholder="Enter UP Diliman Unit" 
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
        id = 'form_upd_unit' 
        ),
        html.Div( 
            dbc.Row( 
                [ 
                    dbc.Label("Wish to delete?", width=2), 
                    dbc.Col( 
                        dbc.Checklist( 
                            id='form_upd_unit_removerecord', 
                            options=[ 
                                { 
                                    'label': "Mark for Deletion", 'value': 1 
                                } 
                            ], 
                            style={'fontWeight':'bold'}, 
                        ), 
                        width=6, 
                    ), 
                ], 
                className="mb-3", 
            ), 
            id = 'form_upd_unit_removerecord_div' 
        ), 
        html.Hr(),
        html.Div(
            [
                dbc.Button('Submit', color="danger", id='form_upd_unit_submitbtn', size='lg', className="me-md-2"),
            ],
            # className="d-grid d-md-flex justify-content-md-end",
        ),
        dbc.Modal( 
            [    
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress"), style=mod_style),  
                dbc.ModalBody("tempmessage", id='form_upd_unit_feedback_message'), 
                dbc.ModalFooter( 
                    dbc.Button("Okay", color='secondary', id="form_upd_unit_closebtn", className="ms-auto", n_clicks=0) 
                ),           
            ], 
            centered=True, 
            id="form_upd_unit_modal", 
            is_open=False, 
        ),
    ]
)

#Delete Div
@app.callback (
    [
        Output('form_upd_unit_toload', 'data'), 
        Output('form_upd_unit_removerecord_div', 'style')
    ], 
    [
        Input('url', 'pathname')
    ], 
    [
        State('url', 'search')
    ]
)

def load_delete_div(pathname, search): 
    if pathname == '/form_upd_unit': 
        parsed = urlparse(search)
        mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if mode == 'edit' else 0 
        removerecord_div = None if to_load else {'display': 'none'}
    else: 
        raise PreventUpdate
    return(to_load, removerecord_div)

#Load Details
@app.callback(
    [
        Output('form_upd_unit_title', 'value')
    ], 
    [
        Input('form_upd_unit_toload', 'modified_timestamp')
    ], 
    [
        State('form_upd_unit_toload', 'data'), 
        State('url', 'search')
    ]
)

def form_upd_unit_load (timestamp, to_load, search): 
    if to_load == 1: 
        form_upd_unit = """SELECT
        college_id, college_name
        FROM up_diliman
        ORDER BY college_id
        """
        
        parsed = urlparse(search)
        form_upd_unit_id = parse_qs(parsed.query)['id'][0]
        
        form_upd_unit_val = []
        form_upd_unit_col = ['college_id', 'college_name']
        form_upd_unit_df = db.querydatafromdatabase(form_upd_unit, form_upd_unit_val, form_upd_unit_col)
        
        counter = 0 
        counted = 0 
        
        for i in range (len(form_upd_unit_df['college_id'])): 
            if form_upd_unit_df['college_id'][i] != int(form_upd_unit_id):
                form_upd_unit_df = form_upd_unit_df.drop(i)
            else: 
                counted = counter 
            counter += 1 
        
        form_upd_unit_id = form_upd_unit_df['college_id'][counted]
        form_upd_unit_title = form_upd_unit_df['college_name'][counted]
    else: 
        raise PreventUpdate
    return [form_upd_unit_title]

#submit Process
@app.callback(
    [
        Output('form_upd_unit_modal', 'is_open'), 
        Output('form_upd_unit_feedback_message', 'children'), 
        Output('upd_inputs_alert', 'is_open'),
        Output('form_upd_unit_closebtn', 'href')
    ], 
    [
        Input('form_upd_unit_submitbtn', 'n_clicks'), 
        Input('form_upd_unit_closebtn', 'n_clicks')
    ], 
    [
        State('form_upd_unit_title', 'value'), 
        State('url', 'search'), 
        State('form_upd_unit_removerecord', 'value'), 
    ]
)

def form_upd_unit_submit (submit_btn, close_btn, title,search, removerecord): 
    ctx = dash.callback_context
    if ctx.triggered: 
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False 
        inputsopenalert = False
        feedbackmessage  = ' '
        okay_href = None 
    else: 
        raise PreventUpdate
    
    if eventid == 'form_upd_unit_submitbtn' and submit_btn: 
        inputs = [title]
        
        if not all(inputs): 
            inputsopenalert = True
        else: 
            openmodal = True 
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]
            
            if mode == 'add': 
                sql_max_inquiry = """SELECT MAX(college_id) from up_diliman
                """
                sql_max_val = []
                max_colname = ['max']
                upd_unit_max_db = db.querydatafromdatabase(sql_max_inquiry, sql_max_val, max_colname)
                upd_unit_max = int(upd_unit_max_db['max'][0]) + 1 
                
                form_upd_unit_sql = """INSERT INTO up_diliman(
                    college_id, 
                    college_name
                )
                VALUES (%s, %s)
                """
                
                form_upd_unit_add = (upd_unit_max, title)
                db.modifydatabase(form_upd_unit_sql, form_upd_unit_add)
                
                feedbackmessage = 'UP Diliman Unit added to database.'
                okay_href  = '/settings'
            
            elif mode == 'edit': 
                parsed = urlparse(search)
                form_upd_unit_editmodeid = parse_qs(parsed.query)['id'][0]
                
                sql_update_upd_unit = """UPDATE up_diliman
                SET 
                    college_name = %s, 
                    college_delete_ind = %s 
                WHERE
                    college_id = %s
                """
                
                to_delete  = bool(removerecord)
                
                values_update_upd_unit = [title, to_delete, form_upd_unit_editmodeid]
                db.modifydatabase(sql_update_upd_unit,values_update_upd_unit)
                
                feedbackmessage = 'UP Diliman Unit updated.'
                okay_href = '/settings'
            
            else: 
                raise PreventUpdate
    elif eventid == 'form_upd_unit_closebtn' and close_btn: 
        pass
    else: 
        raise PreventUpdate
    return [openmodal, feedbackmessage, inputsopenalert, okay_href]

                
                

            