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
            dcc.Store(id='form_pc_toload', storage_type='memory', data=0), 
            html.H5("Add Publication Criteria"),
            html.Hr(),
            dbc.Row( 
                [ 
                    dbc.Row(
                        [
                            dbc.Label("Criteria Title", width=2), 
                            dbc.Col(  
                                dbc.Input( 
                                    id='form_pc_tag', type = "text", placeholder="Enter criteria title" 
                                ),
                                width= 8,
                                className="mb-3",
                            ), 
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Label("Type", width=2), 
                            dbc.Col(  
                                html.Div( 
                                    dcc.Dropdown( 
                                        # [
                                        #     'A (Authorships)',
                                        #     'P (Presentations)',
                                        #     'R (Projects)',
                                        #     'O (Others)'
                                        # ],
                                        id='form_criteria_type', 
                                        options = [{'label':'A (Publications/Authorships)', 'value': 'A'},
                                                    {'label':'P (Presentations)','value': 'P'},
                                                    {'label':'R (Projects)', 'value': 'R'},
                                                    {'label':'O (Other Academic Merits)', 'value': 'O'}, 
                                        ]
                                    ),
                                    className="dash-bootstrap" 
                                ), 
                                width=8,
                                className="mb-3",
                            ), 
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Label("Short Criteria Title", width=2), 
                            dbc.Col(  
                                dbc.Input( 
                                    id='form_pc_short', type = "text", placeholder="Enter shortened criteria name" 
                                ),
                                width=8,
                                className="mb-3",
                            ),
                        ]
                    )
                ], 
                className="mb-3",
            ),
        ],
        id = 'form_pc' 
        ),
        html.Div( 
            dbc.Row( 
                [ 
                    dbc.Label("Wish to delete?", width=2), 
                    dbc.Col( 
                        dbc.Checklist( 
                            id='form_criteria_removerecord', 
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
            id = 'form_criteria_removerecord_div' 
        ), 
        html.Hr(),
        html.Div(
            [
                dbc.Button('Submit', color="danger", id='form_pc_submitbtn', size='lg', className="me-md-2"),
            ],
            # className="d-grid d-md-flex justify-content-md-end",
        ),
        
        dbc.Modal( 
            [    
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress"), style=mod_style),
                dbc.ModalBody("tempmessage", id='form_pc_feedback_message'), 
                dbc.ModalFooter( 
                    dbc.Button("Okay", color='secondary', id="form_pc_closebtn", className="ms-auto", n_clicks=0) 
                ),           
            ], 
            centered=True, 
            id="form_criteria_modal", 
            is_open=False, 
        ),
    ]
)

@app.callback(
    [
        Output('form_pc_toload', 'data'), 
        Output('form_criteria_removerecord_div', 'style'), 
    ], 
    [
        Input('url', 'pathname'), 
    ], 
    [
        State('url', 'search')
    ]
)

def load_delete_div (pathname, search): 
    if pathname == '/form_criteria': 
        parsed = urlparse(search)
        mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if mode == 'edit' else 0 
        removerecord_div = None if to_load else {'display': 'none'}
    else: 
        raise PreventUpdate
    return(to_load, removerecord_div)

@app.callback(
    [
       Output('form_pc_tag', 'value'),
       Output('form_criteria_type', 'value'),
       Output('form_pc_short', 'value')  
    ], 
    [
        Input('form_pc_toload', 'modified_timestamp')
    ], 
    [
        State('form_pc_toload', 'data'), 
        State('url', 'search')
    ]
)

def form_criteria_load (timestamp, to_load, search): 
    if to_load == 1: 
        form_criteria = """SELECT 
            tag_id,
            tag_title, 
            tag_sub, 
            tag_short_title
        FROM tags
        ORDER BY tag_id
        """
        
        parsed = urlparse(search)
        form_criteria_id = parse_qs(parsed.query)['id'][0]
        
        form_criteria_val = []
        form_criteria_col = ['tag_id', 'tag_title', 'tag_sub', 'tag_short']
        form_criteria_df = db.querydatafromdatabase(form_criteria,form_criteria_val,form_criteria_col)
        
        counter = 0 
        counted = 0 
        
        for i in range (len(form_criteria_df)): 
            if form_criteria_df['tag_id'][i] != int(form_criteria_id): 
                form_criteria_df = form_criteria_df.drop(i)
            else: 
                counted = counter 
            counter += 1 
        
        form_critria_id = form_criteria_df['tag_id'][counted]
        form_critria_title = form_criteria_df['tag_title'][counted]
        form_critria_sub = form_criteria_df['tag_sub'][counted]
        form_critria_short = form_criteria_df['tag_short'][counted]
    else: 
        raise PreventUpdate
    return [ form_critria_title, form_critria_sub,form_critria_short ]

@app.callback(
    [
        Output('form_criteria_modal', 'is_open'), 
        Output('form_pc_feedback_message', 'children'), 
        Output('form_pc_closebtn', 'href')
    ], 
    [
        Input('form_pc_submitbtn', 'n_clicks'), 
        Input('form_pc_closebtn', 'n_clicks')
    ], 
    [
        State('form_pc_tag', 'value'), 
        State('form_criteria_type', 'value'),
        State('form_pc_short', 'value'), 
        State('url', 'search'), 
        State('form_criteria_removerecord', 'value'), 
        State('currentuserid', 'data')
    ]
)

def form_criteria_submit (submit_btn, close_btn, tag, type, short, search, removerecord, cuser_id): 
    ctx = dash.callback_context
    if ctx.triggered: 
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False 
        feedbackmessage  = ' '
        okay_href = None 
    else: 
        raise PreventUpdate
    
    if eventid == 'form_pc_submitbtn' and submit_btn: 
        openmodal = True 
        inputs = [ 
            tag, 
            type, 
            short
        ]
        
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
            
            criteria_modifier = ""
            for i in range(len(usernames['id'])): 
                if int(usernames['id'][i]) == cuser_id: 
                    criteria_modifier = usernames['un'][i]
            
            criteria_timestamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            criteria_timestamp_time = dt.datetime.strptime(criteria_timestamp,'%Y-%m-%d %H:%M:%S')            
            
        
            if mode == 'add': 
                sql_max_inquiry = """SELECT MAX(tag_id) from tags
                """
                sql_max_val = []
                max_colname = ['max']
                tag_max_db = db.querydatafromdatabase(sql_max_inquiry,sql_max_val,max_colname )
                tag_max = int(tag_max_db['max'][0]) + 1 
                
                form_criteria_sql = """INSERT INTO tags( 
                    tag_id, 
                    tag_title, 
                    tag_sub, 
                    tag_short_title, 
                    tag_modified_by, 
                    tag_last_upd 
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """ 
                
                form_criteria_add = [tag_max,tag, type, short,criteria_modifier , criteria_timestamp_time ]
                db.modifydatabase(form_criteria_sql, form_criteria_add)
                
                feedbackmessage = 'Criteria added to database.'
                okay_href ='/settings'
            
            elif mode == 'edit': 
                parsed = urlparse(search)
                form_criteria_editmodeid = parse_qs(parsed.query)['id'][0]
                
                sql_update_criteria = """UPDATE tags
                SET
                    tag_title = %s, 
                    tag_sub = %s, 
                    tag_short_title = %s, 
                    tag_delete_ind = %s, 
                    tag_modified_by = %s, 
                    tag_last_upd  = %s
                    
                WHERE 
                    tag_id = %s 
                """
                
                to_delete = bool(removerecord)
                
                values_update_criteria = [tag, type, short, to_delete, criteria_modifier, criteria_timestamp_time, form_criteria_editmodeid ]
                db.modifydatabase(sql_update_criteria,values_update_criteria )
                
                feedbackmessage = 'Criteria updated.'
                okay_href = '/settings'
                
            else: 
                raise PreventUpdate
    elif eventid == 'form_pc_closebtn' and close_btn: 
        pass
    else: 
        raise PreventUpdate
    return [openmodal, feedbackmessage, okay_href]
            