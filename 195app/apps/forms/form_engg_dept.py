
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
            dcc.Store(id='form_engg_dept_toload', storage_type='memory', data=0), 
            html.H5("Add UPD Engineering Department"),
            html.Hr(),
            dbc.Alert('Please supply information in input field.', color="danger", id='engg_inputs_alert', is_open=False),
            dbc.Row( 
                [ 
                    dbc.Row(
                        [
                            dbc.Label("UPD Engineering Department", width=2), 
                            dbc.Col(  
                                dbc.Input( 
                                    id='form_engg_dept_title', type = "text", placeholder="Enter UPD Engineering Unit" 
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
        id = 'form_engg_dept' 
        ),
        html.Div( 
            dbc.Row( 
                [ 
                    dbc.Label("Wish to delete?", width=2), 
                    dbc.Col( 
                        dbc.Checklist( 
                            id='form_engg_dept_removerecord', 
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
            id = 'form_engg_dept_removerecord_div' 
        ), 
        html.Hr(),
        html.Div(
            [
                dbc.Button('Submit', color="danger", id='form_engg_dept_submitbtn', size='lg', className="me-md-2"),
            ],
            # className="d-grid d-md-flex justify-content-md-end",
        ),
        dbc.Modal( 
            [    
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress"), style=mod_style),  
                dbc.ModalBody("tempmessage", id='form_engg_dept_feedback_message'), 
                dbc.ModalFooter( 
                    dbc.Button("Okay", color='secondary', id="form_engg_dept_closebtn", className="ms-auto", n_clicks=0) 
                ),           
            ], 
            centered=True, 
            id="form_engg_dept_modal", 
            is_open=False, 
        ),
    ]
)

#Delete Div
@app.callback (
    [
        Output('form_engg_dept_toload', 'data'), 
        Output('form_engg_dept_removerecord_div', 'style')
    ], 
    [
        Input('url', 'pathname')
    ], 
    [
        State('url', 'search')
    ]
)

def load_delete_div(pathname, search): 
    if pathname == '/form_engg_dept': 
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
        Output('form_engg_dept_title', 'value')
    ], 
    [
        Input('form_engg_dept_toload', 'modified_timestamp')
    ], 
    [
        State('form_engg_dept_toload', 'data'), 
        State('url', 'search')
    ]
)

def form_engg_dept_load (timestamp, to_load, search): 
    if to_load == 1: 
        form_engg_dept = """SELECT
        dept_id, dept_name
        FROM engineering_departments
        ORDER BY dept_id
        """
        
        parsed = urlparse(search)
        form_engg_dept_id = parse_qs(parsed.query)['id'][0]
        
        form_engg_dept_val = []
        form_engg_dept_col = ['dept_id', 'dept_name']
        form_engg_dept_df = db.querydatafromdatabase(form_engg_dept, form_engg_dept_val, form_engg_dept_col)
        
        counter = 0 
        counted = 0 
        
        for i in range (len(form_engg_dept_df['dept_id'])): 
            if form_engg_dept_df['dept_id'][i] != int(form_engg_dept_id):
                form_engg_dept_df = form_engg_dept_df.drop(i)
            else: 
                counted = counter 
            counter += 1 
        
        form_engg_dept_id = form_engg_dept_df['dept_id'][counted]
        form_engg_dept_title = form_engg_dept_df['dept_name'][counted]
    else: 
        raise PreventUpdate
    return [form_engg_dept_title]

#Submit Process
@app.callback(
    [
        Output('form_engg_dept_modal', 'is_open'), 
        Output('form_engg_dept_feedback_message', 'children'), 
        Output('engg_inputs_alert', 'is_open'),
        Output('form_engg_dept_closebtn', 'href')
    ], 
    [
        Input('form_engg_dept_submitbtn', 'n_clicks'), 
        Input('form_engg_dept_closebtn', 'n_clicks')
    ], 
    [
        State('form_engg_dept_title', 'value'), 
        State('url', 'search'), 
        State('form_engg_dept_removerecord', 'value'), 
    ]
)

def form_engg_dept_submit (submit_btn, close_btn, title,search, removerecord): 
    ctx = dash.callback_context
    if ctx.triggered: 
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False 
        inputsopenalert = False
        feedbackmessage  = ' '
        okay_href = None 
    else: 
        raise PreventUpdate
    
    if eventid == 'form_engg_dept_submitbtn' and submit_btn: 
        inputs = [title]
        
        if not all(inputs): 
            inputsopenalert = True
        else: 
            openmodal = True 
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]
            
            if mode == 'add': 
                sql_max_inquiry = """SELECT MAX(dept_id) from engineering_departments
                """
                sql_max_val = []
                max_colname = ['max']
                engg_dept_max_db = db.querydatafromdatabase(sql_max_inquiry, sql_max_val, max_colname)
                engg_dept_max = int(engg_dept_max_db['max'][0]) + 1 
                
                form_engg_dept_sql = """INSERT INTO engineering_departments(
                    dept_id, 
                    dept_name
                )
                VALUES (%s, %s)
                """
                
                form_engg_dept_add = (engg_dept_max, title)
                db.modifydatabase(form_engg_dept_sql, form_engg_dept_add)
                
                feedbackmessage = 'UPD Engineering Department added to database.'
                okay_href  = '/settings'
            
            elif mode == 'edit': 
                parsed = urlparse(search)
                form_engg_dept_editmodeid = parse_qs(parsed.query)['id'][0]
                
                sql_update_engg_dept = """UPDATE engineering_departments
                SET 
                    dept_name = %s, 
                    dept_delete_ind = %s 
                WHERE
                    dept_id = %s
                """
                
                to_delete  = bool(removerecord)
                
                values_update_engg_dept = [title, to_delete, form_engg_dept_editmodeid]
                db.modifydatabase(sql_update_engg_dept,values_update_engg_dept)
                
                feedbackmessage = 'UPD Engineering Department updated.'
                okay_href = '/settings'
            
            else: 
                raise PreventUpdate
    elif eventid == 'form_engg_dept_closebtn' and close_btn: 
        pass
    else: 
        raise PreventUpdate
    return [openmodal, feedbackmessage, inputsopenalert, okay_href]

                
                

            