
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
            dcc.Store(id='form_up_cons_toload', storage_type='memory', data=0), 
            html.H5("Add UP Constituent"),
            html.Hr(),
            dbc.Alert('Please supply information in input field.', color="danger", id='cons_inputs_alert', is_open=False),
            dbc.Row( 
                [ 
                    dbc.Row(
                        [
                            dbc.Label("UP Constituent", width=2), 
                            dbc.Col(  
                                dbc.Input( 
                                    id='form_up_cons_title', type = "text", placeholder="Enter UP constituent" 
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
        id = 'form_up_cons' 
        ),
        html.Div( 
            dbc.Row( 
                [ 
                    dbc.Label("Wish to delete?", width=2), 
                    dbc.Col( 
                        dbc.Checklist( 
                            id='form_up_cons_removerecord', 
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
            id = 'form_up_cons_removerecord_div' 
        ), 
        html.Hr(),
        html.Div(
            [
                dbc.Button('Submit', color="danger", id='form_up_cons_submitbtn', size='lg', className="me-md-2"),
            ],
            # className="d-grid d-md-flex justify-content-md-end",
        ),
        dbc.Modal( 
            [    
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress"), style=mod_style),  
                dbc.ModalBody("tempmessage", id='form_up_cons_feedback_message'), 
                dbc.ModalFooter( 
                    dbc.Button("Okay", color='secondary', id="form_up_cons_closebtn", className="ms-auto", n_clicks=0) 
                ),           
            ], 
            centered=True, 
            id="form_up_cons_modal", 
            is_open=False, 
        ),
    ]
)

# Delete Div
@app.callback (
    [
        Output('form_up_cons_toload', 'data'), 
        Output('form_up_cons_removerecord_div', 'style')
    ], 
    [
        Input('url', 'pathname')
    ], 
    [
        State('url', 'search')
    ]
)

def load_delete_div(pathname, search): 
    if pathname == '/form_up_constituent': 
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
        Output('form_up_cons_title', 'value')
    ], 
    [
        Input('form_up_cons_toload', 'modified_timestamp')
    ], 
    [
        State('form_up_cons_toload', 'data'), 
        State('url', 'search')
    ]
)

def form_up_cons_load (timestamp, to_load, search): 
    if to_load == 1: 
        form_up_cons = """SELECT
        cons_id, cons_name
        FROM up_system
        ORDER BY cons_id
        """
        
        parsed = urlparse(search)
        form_up_cons_id = parse_qs(parsed.query)['id'][0]
        
        form_up_cons_val = []
        form_up_cons_col = ['cons_id', 'cons_name']
        form_up_cons_df = db.querydatafromdatabase(form_up_cons, form_up_cons_val, form_up_cons_col)
        
        counter = 0 
        counted = 0 
        
        for i in range (len(form_up_cons_df['cons_id'])): 
            if form_up_cons_df['cons_id'][i] != int(form_up_cons_id):
                form_up_cons_df = form_up_cons_df.drop(i)
            else: 
                counted = counter 
            counter += 1 
        
        form_up_cons_id = form_up_cons_df['cons_id'][counted]
        form_up_cons_title = form_up_cons_df['cons_name'][counted]
    else: 
        raise PreventUpdate
    return [form_up_cons_title]

#submit Process
@app.callback(
    [
        Output('form_up_cons_modal', 'is_open'), 
        Output('form_up_cons_feedback_message', 'children'), 
        Output('cons_inputs_alert', 'is_open'),
        Output('form_up_cons_closebtn', 'href')
    ], 
    [
        Input('form_up_cons_submitbtn', 'n_clicks'), 
        Input('form_up_cons_closebtn', 'n_clicks')
    ], 
    [
        State('form_up_cons_title', 'value'), 
        State('url', 'search'), 
        State('form_up_cons_removerecord', 'value'), 
    ]
)

def form_up_cons_submit (submit_btn, close_btn, title,search, removerecord): 
    ctx = dash.callback_context
    if ctx.triggered: 
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False 
        inputsopenalert = False
        feedbackmessage  = ' '
        okay_href = None 
    else: 
        raise PreventUpdate
    
    if eventid == 'form_up_cons_submitbtn' and submit_btn: 
        inputs = [title]
        
        if not all(inputs): 
            inputsopenalert = True
        else: 
            openmodal = True 
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]
            
            if mode == 'add': 
                sql_max_inquiry = """SELECT MAX(cons_id) from up_system
                """
                sql_max_val = []
                max_colname = ['max']
                up_cons_max_db = db.querydatafromdatabase(sql_max_inquiry, sql_max_val, max_colname)
                up_cons_max = int(up_cons_max_db['max'][0]) + 1 
                
                form_up_cons_sql = """INSERT INTO up_system(
                    cons_id, 
                    cons_name
                )
                VALUES (%s, %s)
                """
                
                form_up_cons_add = (up_cons_max, title)
                db.modifydatabase(form_up_cons_sql, form_up_cons_add)
                
                feedbackmessage = 'UP Constituent added to database.'
                okay_href  = '/settings'
            
            elif mode == 'edit': 
                parsed = urlparse(search)
                form_up_cons_editmodeid = parse_qs(parsed.query)['id'][0]
                
                sql_update_up_cons = """UPDATE up_system
                SET 
                    cons_name = %s, 
                    cons_delete_ind = %s 
                WHERE
                    cons_id = %s
                """
                
                to_delete  = bool(removerecord)
                
                values_update_up_cons = [title, to_delete, form_up_cons_editmodeid]
                db.modifydatabase(sql_update_up_cons,values_update_up_cons)
                
                feedbackmessage = 'UP Constituent updated.'
                okay_href = '/settings'
            
            else: 
                raise PreventUpdate
    elif eventid == 'form_up_cons_closebtn' and close_btn: 
        pass
    else: 
        raise PreventUpdate
    return [openmodal, feedbackmessage, inputsopenalert, okay_href]

                
                

            