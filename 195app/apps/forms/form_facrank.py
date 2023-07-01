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
            dcc.Store(id='form_ra_toload', storage_type='memory', data=0), 
            html.H5("Add Faculty Rank"),
            html.Hr(),
            dbc.Row( 
                [ 
                    dbc.Row(
                        [
                            dbc.Label("Rank Title", width=2), 
                            dbc.Col(  
                                dbc.Input( 
                                    id='form_ra_title', type = "text", placeholder="Enter rank title" 
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
        id = 'form_ra' 
        ),
        html.Div( 
            dbc.Row( 
                [ 
                    dbc.Label("Wish to delete?", width=2), 
                    dbc.Col( 
                        dbc.Checklist( 
                            id='form_rank_removerecord', 
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
            id = 'form_rank_removerecord_div' 
        ), 
        html.Hr(),
        html.Div(
            [
                dbc.Button('Submit', color="danger", id='form_ra_submitbtn', size='lg', className="me-md-2"),
            ],
            # className="d-grid d-md-flex justify-content-md-end",
        ),
        dbc.Modal( 
            [    
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress"), style=mod_style), 
                dbc.ModalBody("tempmessage", id='form_ra_feedback_message'), 
                dbc.ModalFooter( 
                    dbc.Button("Okay", color='secondary', id="form_ra_closebtn", className="ms-auto", n_clicks=0) 
                ),           
            ], 
            centered=True, 
            id="form_ra_modal", 
            is_open=False, 
        ),
    ]
)

@app.callback (
    [
        Output('form_ra_toload', 'data'), 
        Output('form_rank_removerecord_div', 'style')
    ], 
    [
        Input('url', 'pathname')
    ], 
    [
        State('url', 'search')
    ]
)

def load_rank_delete_div(pathname, search): 
    if pathname == '/form_faculty_rank': 
        parsed = urlparse(search)
        mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if mode == 'edit' else 0 
        removerecord_div = None if to_load else {'display': 'none'}
    else: 
        raise PreventUpdate
    return(to_load, removerecord_div)


@app.callback (
    [
        Output('form_ra_title', 'value')
    ], 
    [
        Input('form_ra_toload', 'modified_timestamp')
    ], 
    [
        State('form_ra_toload', 'data'), 
        State('url', 'search')
    ]
)

def form_facrank_load (timestamp, to_load, search): 
    if to_load == 1: 
        form_rank = """SELECT rank_id, rank_title 
        FROM ranks 
        ORDER BY rank_id
        """
        
        parsed = urlparse(search)
        form_ranks_id = parse_qs(parsed.query)['id'][0]
        
        form_ranks_val = []
        form_ranks_col = ['rank_id', 'rank_title']
        form_ranks_df = db.querydatafromdatabase(form_rank, form_ranks_val, form_ranks_col)
        
        counter = 0 
        counted = 0 
        
        for i in range (len(form_ranks_df['rank_id'])): 
            if form_ranks_df['rank_id'][i] != int(form_ranks_id):
                form_ranks_df = form_ranks_df.drop(i)
            else: 
                counted = counter 
            counter += 1 
        
        form_rank_id = form_ranks_df['rank_id'][counted]
        form_rank_title = form_ranks_df['rank_title'][counted]
    else: 
        raise PreventUpdate
    return [form_rank_title]


@app.callback( 
    [
        Output('form_ra_modal', 'is_open'), 
        Output('form_ra_feedback_message', 'children'), 
        Output('form_ra_closebtn', 'href')
    ], 
    [
        Input('form_ra_submitbtn', 'n_clicks'), 
        Input('form_ra_closebtn', 'n_clicks')
    ], 
    [
        State('form_ra_title', 'value'), 
        State('url', 'search'), 
        State('form_rank_removerecord', 'value'), 
        State('currentuserid', 'data' )
    ]
)

def form_ranks_submit (submit_btn, close_btn, title,search, removerecord, cuser_id): 
    ctx = dash.callback_context
    if ctx.triggered: 
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False 
        feedbackmessage  = ' '
        okay_href = None 
    else: 
        raise PreventUpdate
    
    if eventid == 'form_ra_submitbtn' and submit_btn: 
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
            
            ranks_modifier = ""
            for i in range(len(usernames['id'])): 
                if int(usernames['id'][i]) == cuser_id: 
                    ranks_modifier = usernames['un'][i]
            
            ranks_timestamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ranks_timestamp_time = dt.datetime.strptime(ranks_timestamp,'%Y-%m-%d %H:%M:%S')
                
            if mode == 'add': 
                sql_max_inquiry = """SELECT MAX(rank_id) from ranks
                """
                sql_max_val = []
                max_colname = ['max']
                ranks_max_db = db.querydatafromdatabase(sql_max_inquiry, sql_max_val, max_colname)
                ranks_max = int(ranks_max_db['max'][0]) + 1 
                
                form_ranks_sql = """INSERT INTO ranks(
                    rank_id, 
                    rank_title, 
                    ranks_modified_by, 
                    ranks_last_upd
                )
                VALUES (%s, %s, %s, %s)
                """
                
                form_ranks_add = [ranks_max, title, ranks_modifier, ranks_timestamp_time ]
                db.modifydatabase(form_ranks_sql, form_ranks_add)
                
                feedbackmessage = 'Rank added to database'
                okay_href  = '/settings'
                
            elif mode == 'edit': 
                parsed = urlparse(search)
                form_rank_editmodeid = parse_qs(parsed.query)['id'][0]
                
                sql_update_rank = """UPDATE ranks
                SET 
                    rank_title = %s, 
                    ranks_modified_by = %s, 
                    ranks_last_upd = %s, 
                    ranks_delete_ind = %s
                WHERE
                    rank_id = %s
                """
                
                to_delete = bool(removerecord)
                
                values_update_rank = [title, ranks_modifier, ranks_timestamp_time, to_delete, form_rank_editmodeid]
                db.modifydatabase(sql_update_rank, values_update_rank )
                
                feedbackmessage = 'Ranks updated.'
                okay_href = '/settings'
                
            else: 
                raise PreventUpdate
    elif eventid == 'form_ra_closebtn' and close_btn: 
        pass
    else: 
        raise PreventUpdate
    return [openmodal, feedbackmessage, okay_href]
