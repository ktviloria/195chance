
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
            dcc.Store(id='form_inv_toload', storage_type='memory', data=0), 
            html.H5("Add Faculty Authorship Involvement"),
            html.Hr(),
            dbc.Row( 
                [ 
                    dbc.Row(
                        [
                            dbc.Label("Authorship Involvement", width=2), 
                            dbc.Col(  
                                dbc.Input( 
                                    id='form_inv_title', type = "text", placeholder="Enter involvement" 
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
        id = 'form_inv' 
        ),
        html.Div( 
            dbc.Row( 
                [ 
                    dbc.Label("Wish to delete?", width=2), 
                    dbc.Col( 
                        dbc.Checklist( 
                            id='form_inv_removerecord', 
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
            id = 'form_inv_removerecord_div' 
        ), 
        html.Hr(),
        html.Div(
            [
                dbc.Button('Submit', color="danger", id='form_inv_submitbtn', size='lg', className="me-md-2"),
            ],
            # className="d-grid d-md-flex justify-content-md-end",
        ),
        dbc.Modal( 
            [    
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress"), style=mod_style),  
                dbc.ModalBody("tempmessage", id='form_inv_feedback_message'), 
                dbc.ModalFooter( 
                    dbc.Button("Okay", color='secondary', id="form_inv_closebtn", className="ms-auto", n_clicks=0) 
                ),           
            ], 
            centered=True, 
            id="form_inv_modal", 
            is_open=False, 
        ),
    ]
)

@app.callback (
    [
        Output('form_inv_toload', 'data'), 
        Output('form_inv_removerecord_div', 'style')
    ], 
    [
        Input('url', 'pathname')
    ], 
    [
        State('url', 'search')
    ]
)

def load_rank_delete_div(pathname, search): 
    if pathname == '/form_involvement': 
        parsed = urlparse(search)
        mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if mode == 'edit' else 0 
        removerecord_div = None if to_load else {'display': 'none'}
    else: 
        raise PreventUpdate
    return(to_load, removerecord_div)

@app.callback(
    [
        Output('form_inv_title', 'value')
    ], 
    [
        Input('form_inv_toload', 'modified_timestamp')
    ], 
    [
        State('form_inv_toload', 'data'), 
        State('url', 'search')
    ]
)

def form_inv_load (timestamp, to_load, search): 
    if to_load == 1: 
        form_inv = """SELECT a_author_subcat_id, a_author_subcat_label
        FROM authorship_subcategory
        ORDER BY a_author_subcat_id
        """
        
        parsed = urlparse(search)
        form_inv_id = parse_qs(parsed.query)['id'][0]
        
        form_inv_val = []
        form_inv_col = ['inv_id', 'inv_title']
        form_inv_df = db.querydatafromdatabase(form_inv, form_inv_val, form_inv_col)
        
        counter = 0 
        counted = 0 
        
        for i in range (len(form_inv_df['inv_id'])): 
            if form_inv_df['inv_id'][i] != int(form_inv_id):
                form_inv_df = form_inv_df.drop(i)
            else: 
                counted = counter 
            counter += 1 
        
        form_inv_id = form_inv_df['inv_id'][counted]
        form_inv_title = form_inv_df['inv_title'][counted]
    else: 
        raise PreventUpdate
    return [form_inv_title]

@app.callback(
    [
        Output('form_inv_modal', 'is_open'), 
        Output('form_inv_feedback_message', 'children'), 
        Output('form_inv_closebtn', 'href')
    ], 
    [
        Input('form_inv_submitbtn', 'n_clicks'), 
        Input('form_inv_closebtn', 'n_clicks')
    ], 
    [
        State('form_inv_title', 'value'), 
        State('url', 'search'), 
        State('form_inv_removerecord', 'value'), 
        State('currentuserid', 'data' )
    ]
)

def form_inv_submit (submit_btn, close_btn, title,search, removerecord, cuser_id): 
    ctx = dash.callback_context
    if ctx.triggered: 
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False 
        feedbackmessage  = ' '
        okay_href = None 
    else: 
        raise PreventUpdate
    
    if eventid == 'form_inv_submitbtn' and submit_btn: 
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
            
            inv_modifier = ""
            for i in range(len(usernames['id'])): 
                if int(usernames['id'][i]) == cuser_id: 
                    inv_modifier = usernames['un'][i]
            
            inv_timestamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            inv_timestamp_time = dt.datetime.strptime(inv_timestamp,'%Y-%m-%d %H:%M:%S')
            
            if mode == 'add': 
                sql_max_inquiry = """SELECT MAX(a_author_subcat_id) from authorship_subcategory
                """
                sql_max_val = []
                max_colname = ['max']
                inv_max_db = db.querydatafromdatabase(sql_max_inquiry, sql_max_val, max_colname)
                inv_max = int(inv_max_db['max'][0]) + 1 
                
                form_inv_sql = """INSERT INTO authorship_subcategory(
                    a_author_subcat_id, 
                    a_author_subcat_label, 
                    sub_modified_by, 
                    sub_last_upd
                )
                VALUES (%s, %s, %s, %s)
                """
                
                form_inv_add = (inv_max, title, inv_modifier, inv_timestamp_time)
                db.modifydatabase(form_inv_sql, form_inv_add)
                
                feedbackmessage = 'Faculty Authorship Involvement added to database.'
                okay_href  = '/settings'
            
            elif mode == 'edit': 
                parsed = urlparse(search)
                form_inv_editmodeid = parse_qs(parsed.query)['id'][0]
                
                sql_update_inv = """UPDATE authorship_subcategory
                SET 
                    a_author_subcat_label = %s, 
                    sub_modified_by = %s, 
                    sub_last_upd = %s,
                    sub_delete_ind = %s 
                WHERE
                    a_author_subcat_id = %s
                """
                
                to_delete  = bool(removerecord)
                
                values_update_inv = [title,inv_modifier,inv_timestamp_time,to_delete, form_inv_editmodeid]
                db.modifydatabase(sql_update_inv,values_update_inv)
                
                feedbackmessage = 'Faculty Authorship Involvement updated.'
                okay_href = '/settings'
            
            else: 
                raise PreventUpdate
    elif eventid == 'form_inv_closebtn' and close_btn: 
        pass
    else: 
        raise PreventUpdate
    return [openmodal, feedbackmessage, okay_href]

                
                

            