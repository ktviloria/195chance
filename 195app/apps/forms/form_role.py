from dash import dcc
from dash import html
from dash import dash_table
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd
import datetime as dt
from datetime import date, datetime
 
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
            dcc.Store(id='form_ro_toload', storage_type='memory', data=0), 
            html.H5("Add Faculty Authorship Role"),
            html.Hr(),
            dbc.Row( 
                [ 
                    dbc.Row(
                        [
                            dbc.Label("Authorship Role", width=2), 
                            dbc.Col(  
                                dbc.Input( 
                                    id='form_ro_title', type = "text", placeholder="Enter role" 
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
        id = 'form_ro' 
        ),
        html.Div( 
            dbc.Row( 
                [ 
                    dbc.Label("Wish to delete?", width=2), 
                    dbc.Col( 
                        dbc.Checklist( 
                            id='form_ro_removerecord', 
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
            id = 'form_ro_removerecord_div' 
        ), 
        html.Hr(),
        html.Div(
            [
                dbc.Button('Submit', color="danger", id='form_ro_submitbtn', size='lg', className="me-md-2"),
            ],
            # className="d-grid d-md-flex justify-content-md-end",
        ),
        dbc.Modal( 
            [    
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress"), style=mod_style), 
                dbc.ModalBody("tempmessage", id='form_ro_feedback_message'), 
                dbc.ModalFooter( 
                    dbc.Button("Okay", color='secondary', id="form_ro_closebtn", className="ms-auto", n_clicks=0) 
                ),           
            ], 
            centered=True, 
            id="form_ro_modal", 
            is_open=False, 
        ),
    ]
)

@app.callback(
    [
        Output('form_ro_toload', 'data'), 
        Output('form_ro_removerecord_div', 'style')
    ], 
    [
        Input('url', 'pathname')
    ], 
    [
        State('url', 'search')
    ]
)

def load_role_delete_div(pathname, search): 
    if pathname == '/form_role': 
        parsed = urlparse(search)
        mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if mode == 'edit' else 0 
        removerecord_div = None if to_load else {'display': 'none'}
    else: 
        raise PreventUpdate
    return(to_load, removerecord_div)

@app.callback(
    [
        Output('form_ro_title', 'value')
    ], 
    [
        Input('form_ro_toload', 'modified_timestamp')
    ], 
    [
        State('form_ro_toload', 'data'), 
        State('url', 'search')
    ]
)

def form_role_load (timestamp, to_load, search): 
    if to_load == 1: 
        form_role = """SELECT a_label_id, a_label 
        from authorship_role 
        Order by a_label_id
        """
        
        parsed = urlparse(search)
        form_roles_id = parse_qs(parsed.query)['id'][0]
        
        form_role_val = []
        form_role_col = ['role_id', 'role_title']
        
        form_role_df = db.querydatafromdatabase (form_role, form_role_val, form_role_col)
        
        counter = 0 
        counted = 0 
        
        for i in range (len(form_role_df['role_id'])): 
            if form_role_df['role_id'][i] != int(form_roles_id):
                form_role_df = form_role_df.drop(i)
            else: 
                counted = counter 
            counter += 1 
        
        form_role_id = form_role_df['role_id'][counted]
        form_role_title = form_role_df['role_title'][counted]
    else: 
        raise PreventUpdate
    return [form_role_title]

@app.callback(
    [
        Output('form_ro_modal', 'is_open'),
        Output('form_ro_feedback_message', 'children'), 
        Output('form_ro_closebtn', 'href')
    ], 
    [
        Input('form_ro_submitbtn', 'n_clicks'), 
        Input('form_ro_closebtn', 'n_clicks')
    ], 
    [
        State('form_ro_title', 'value'), 
        State('url', 'search'), 
        State('form_ro_removerecord', 'value'), 
        State('currentuserid', 'data')
    ]
)

def form_roles_submit(submit_btn, close_btn, title,search, removerecord, cuser_id): 
    ctx = dash.callback_context
    if ctx.triggered: 
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False 
        feedbackmessage  = ' '
        okay_href = None 
    else: 
        raise PreventUpdate
    
    if eventid == 'form_ro_submitbtn' and submit_btn: 
        openmodal = True 
        inputs = [title]
        
        if not all(inputs): 
            feedbackmessage = "Please supply all needed information."
        else: 
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]

            username_modify = """SELECT 
                    user_id, 
                    user_un
                    FROM users 
                """
            vals_username = []
            cols_username = ['id', 'un']
            usernames = db.querydatafromdatabase(username_modify, vals_username, cols_username)
    
            roles_modifier = ""
            for i in range(len(usernames['id'])): 
                if int(usernames['id'][i]) == cuser_id: 
                    roles_modifier = usernames['un'][i]
            
            roles_timestamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            roles_timestamp_time = dt.datetime.strptime(roles_timestamp,'%Y-%m-%d %H:%M:%S')
            
            if mode == 'add': 
                sql_max_inquiry = """SELECT MAX(a_label_id) from authorship_role
                """
                sql_max_val = []
                max_colname = ['max']
                role_max_db = db.querydatafromdatabase(sql_max_inquiry, sql_max_val, max_colname)
                role_max = int(role_max_db['max'][0]) + 1
                
                form_roles_sql = """INSERT INTO authorship_role(
                    a_label_id, 
                    a_label, 
                    role_modified_by, 
                    role_last_upd
                )
                VALUES(%s, %s, %s, %s)
                """
                
                form_role_add = [role_max, title, roles_modifier,roles_timestamp_time]
                db.modifydatabase(form_roles_sql,form_role_add )
                
                feedbackmessage = 'Role added to database.'
                okay_href  = '/settings'
                
            elif mode == 'edit': 
                parsed = urlparse(search)
                form_role_editmodeid = parse_qs(parsed.query)['id'][0]
                
                sql_update_role = """UPDATE authorship_role
                SET
                    a_label = %s, 
                    role_modified_by = %s, 
                    role_last_upd = %s, 
                    role_delete_ind = %s
                WHERE
                    a_label_id = %s
                """
                
                to_delete = bool(removerecord)
                
                values_update_role = [title, roles_modifier, roles_timestamp_time, to_delete, form_role_editmodeid]
                db.modifydatabase(sql_update_role,values_update_role )
                
                feedbackmessage = 'Role updated.'
                okay_href = '/settings'
          
            else: 
                raise PreventUpdate
    elif eventid == 'form_ro_closebtn' and close_btn: 
        pass
    else: 
        raise PreventUpdate
    return [openmodal, feedbackmessage, okay_href]
                
                


    
        