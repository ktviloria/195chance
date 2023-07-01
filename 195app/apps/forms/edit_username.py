import hashlib

from dash import dcc
from dash import html
from dash import dash_table
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd
import datetime
from datetime import date

from app import app
from apps import dbconnect as db
 
from urllib.parse import urlparse, parse_qs

mod_style = { 
 'color': '#fff',
 'background-color': '#b22222',
 'font-size': '25px'
} 


layout= html.Div( 
    [ 
        html.Div( 
            [ 
                dcc.Store(id='un_toload', storage_type='memory', data=0)
            ] 
        ), 
        html.H2("Edit Username"), 
        html.Hr(),
        dbc.Alert('Check your changes. Username may already exist!', color="danger", id='username_un_alert', is_open=False),
        dbc.Row(
        [
            dbc.Col(
                dbc.Row( 
                    [ 
                        dbc.Label("Username", width=2), 
                        dbc.Col( 
                            dbc.Input( 
                                type="text", id="username_un", placeholder="Enter new username" 
                            ), 
                        ), 
                    ],  
                ),
                width=6
            ),]
        ), 
        html.Hr(), 
        dbc.Button('Submit', color='danger', id='username_submitbtn'),
        dbc.Modal( 
            [    
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress"), style=mod_style), 
                dbc.ModalBody("tempmessage", id='username_feedback_message'), 
                dbc.ModalFooter( 
                    dbc.Button("Okay", color='secondary', id="username_closebtn", className="ms-auto", n_clicks=0) 
                ),           
            ], 
        centered=True, 
        id="username_modal", 
        is_open=False, 
        ),
    ]
)

@app.callback (
    [
        Output('username_un', 'value')
    ], 
    [
        Input('url', 'pathname'), 
    ], 
    [
        State('currentuserid', 'data'), 
        State('url', 'search'), 
    ]
)

def username_load (pathname, currentuserid, search): 
    if pathname == '/edit_username': 
        if currentuserid > 3: 
            usernamesql = """SELECT user_id, user_un 
            FROM users
            where
                user_id = %s
            """
            
            username_val = [f"{currentuserid}"]
            username_col = ['user_id', 'username']
            usernamedf = db.querydatafromdatabase(usernamesql,username_val, username_col )
            
            
            username = usernamedf['username'][0]
            return [username]
        
        if currentuserid <= 3: 
            
            parsed = urlparse(search)
            idparse = parse_qs(parsed.query)['id'][0]
            
            usernamesql = """SELECT user_id, user_un 
            FROM users
            where
                user_id = %s
            """
            username_val = [f"{idparse}"]
            username_col = ['user_id', 'username']
            usernamedf = db.querydatafromdatabase(usernamesql,username_val, username_col )
            
            username = usernamedf['username'][0]
            return [username]
        else: 
            raise PreventUpdate
    else: 
        raise PreventUpdate
    

@app.callback(
    [
        Output('username_modal', 'is_open'), 
        Output('username_feedback_message', 'children'), 
        Output('username_un_alert', 'is_open'), 
        Output('username_closebtn', 'href'),
    ], 
    [
        Input('username_submitbtn', 'n_clicks'),
        Input('username_closebtn', 'n_clicks'),
    ], 
    [
        State('currentuserid', 'data'),
        State('username_un', 'value'), 
        State('url', 'search')
    ]
)

def username_submit ( submit_btn, close_btn, currentuserid,username, search): 
    ctx = dash.callback_context
    if ctx.triggered: 
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        unopenalert = False
        openmodal = False 
        feedbackmessage  = ' '
        okay_href = None 
    else: 
        raise PreventUpdate
    
    if eventid == 'username_submitbtn' and submit_btn: 
        # if currentuserid > 3: 
            existingusername_sql = """SELECT 
                users.user_un
            FROM faculty
                INNER JOIN users on faculty.user_id = users.user_id
            WHERE
                faculty_delete_ind = false
            ORDER BY
                faculty.user_id ASC
            """      
            existingusername_val = []
            existingusername_colname = ['existingun1']
            existingusername_df = db.querydatafromdatabase(existingusername_sql, existingusername_val, existingusername_colname)
            
            if username in existingusername_df['existingun1'].values: 
                unopenalert = True 
            else: 
                openmodal = True
                
                fac_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                fac_timestamp_time = datetime.datetime.strptime(fac_timestamp,'%Y-%m-%d %H:%M:%S') 
                
                
                fp_sqlcode_modifiedby = """SELECT
                user_id,
                user_un
                FROM users
                """
                fp_vals_modifiedby = []
                fp_cols_modifiedby = ['id', 'un']
                usernamed = db.querydatafromdatabase(fp_sqlcode_modifiedby, fp_vals_modifiedby, fp_cols_modifiedby)
                
                username_modifier = ""
                for i in range(len(usernamed['id'])):
                    if int(usernamed['id'][i]) == currentuserid:
                        username_modifier = usernamed['un'][i]
                print(username_modifier)
                        
                
                
                sql_fac = """UPDATE faculty
                    SET 
                        faculty_last_upd = %s,
                        faculty_modified_by = %s
                    WHERE 
                        user_id = %s
                    """   
                
                
                
                
                
                sql_users = """UPDATE users
                SET 
                    user_un = %s
                WHERE 
                    user_id = %s
                """   
                values_users = []
                values_fac = []
                if currentuserid > 3: 
                    values_users = [username, currentuserid]
                    values_fac = [fac_timestamp_time, username, currentuserid]
                    okay_href = '/my_profile'
                elif currentuserid <= 3: 
                    parsed = urlparse(search)
                    modifyid = parse_qs(parsed.query)['id'][0]
                    values_users = [username, modifyid]
                    values_fac = [fac_timestamp_time, username_modifier, modifyid]
                    okay_href = '/faculty_manage'
                    
                db.modifydatabase(sql_users, values_users)
                db.modifydatabase(sql_fac, values_fac)
                
                
                feedbackmessage = 'Username updated.'
                
        # elif currentuserid < 3: 
            
    elif eventid == 'username_closebtn' and close_btn: 
        pass
    else: 
        raise PreventUpdate
    return[openmodal,feedbackmessage, unopenalert, okay_href ]
                
            