#for adding author and editing/deleting author profile
#only admin users have access to this page
#if editing a faculty member, profile details of current faculty user being edited is shown

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
from dash.dash import no_update
import re

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
                dcc.Store(id='authorprof_toload', storage_type='memory', data=0), 
            ] 
        ), 
        html.H2("Profile Details"), 
        html.H6("* Indicates required field", style={"color": "#d9534f", "font-style": "italic"}),
        html.Hr(), 
        dbc.Alert('Please supply required fields.', color="danger", id='authorprof_inputs_alert', is_open=False),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        # Last Name Input
                        dbc.Row( 
                            [ 
                                dbc.Col(
                                    [
                                        dbc.Label("Last Name",), 
                                        dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"}),
                                    ],
                                    width=3
                                ),
                                dbc.Col( 
                                    dbc.Input( 
                                        type="text", id="authorprof_ln", placeholder="Enter last name of author" 
                                    ), 
                                ), 
                            ], 
                            className="mb-3", 
                        ), 
                        # First Name Input
                        dbc.Row( 
                            [ 
                                dbc.Col(
                                    [
                                        dbc.Label("First Name",), 
                                        dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"}),
                                    ],
                                    width=3
                                ),
                                dbc.Col( 
                                    dbc.Input( 
                                        type="text", id="authorprof_fn", placeholder="Enter first name of author" 
                                    ), 
                                ), 
                            ], 
                            className="mb-3", 
                        ), 
                        # Email Input
                        dbc.Row( 
                            [ 
                                dbc.Col([
                                    dbc.Label("Email")                                ],
                                width=3), 
                                dbc.Col( 
                                    dbc.Input( 
                                        type="text", id="authorprof_mail", placeholder="Enter email" 
                                    ), 
                                ), 
                            ], 
                            className="mb-3", 
                        ), 
                        # Contact Number Input
                        dbc.Row( 
                            [ 
                                dbc.Label("Contact number", width=3), 
                                dbc.Col( 
                                    dbc.Input( 
                                        type="text", id="authorprof_contact", placeholder="Enter contact number" 
                                    ), 
                                ), 
                            ], 
                            className="mb-3", 
                        ),
                        # Author Affiliation Dropdown
                        html.Div(
                            dbc.Row( 
                                [ 
                                    dbc.Col(
                                        [
                                            dbc.Label("Author Affiliation", id = 'authorprof_affiliation_label'), 
                                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"}),
                                        ],
                                        width=3
                                    ),  
                                    dbc.Col( 
                                        html.Div( 
                                            dcc.Dropdown( 
                                                id='authorprof_affiliation', 
                                                options =[
                                                    {'label':'UP', 'value':True},
                                                    {'label':'Non-UP', 'value':False}
                                                    ]
                                            ),
                                            className="dash-bootstrap" 
                                        ), 
                                    ), 
                                ], 
                                className="mb-3", 
                            ),
                            id = 'authorprof_affiliation'
                        ),
                        # IE Faculty Indication Dropdown
                        html.Div(
                            dbc.Row( 
                                [ 
                                    dbc.Col(
                                        [
                                            dbc.Label("IE Faculty Indication", id = 'authorprof_iefacind_label'), 
                                            # dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"}, id='authorprof_iefacind_star'),
                                        ],
                                        width=3
                                    ),  
                                    dbc.Col( 
                                        [
                                            html.Div( 
                                                dcc.Dropdown( 
                                                    id='authorprof_iefacind', 
                                                    options = [
                                                        {'label':'IE Faculty', 'value':True},
                                                        {'label':'Non-IE Faculty', 'value':False},
                                                    ]
                                                ),
                                                className="dash-bootstrap",
                                            ), 
                                            html.Div( 
                                                dcc.Dropdown( 
                                                    id='authorprof_noniefacind', 
                                                    options = [
                                                        {'label': 'N/A: Non-UP Affiliated', 'value': 'Non-UP'},
                                                    ]
                                                ),
                                                className="dash-bootstrap",
                                            ), 
                                        ]
                                    ), 
                                ], 
                                className="mb-3", 
                            ),
                            id = 'authorprof_iefacind_div'
                        ),
                        # Delete Indicator
                        html.Div( 
                            dbc.Row( 
                                [ 
                                    dbc.Label("Wish to delete?", width=3), 
                                    dbc.Col( 
                                        dbc.Checklist( 
                                            id='authorprof_removerecord', 
                                            options=[ 
                                                { 
                                                    'label': "Mark for Deletion", 'value': 1 
                                                } 
                                            ], 
                                            style={'fontWeight':'bold'}, 
                                        ), 
                                    ), 
                                ], 
                                className="mb-3", 
                            ), 
                            id = 'authorprof_removerecord_div' 
                        ), 
                    ],
                    width=6
                )
            ]
        ),
        html.Hr(), 
        dbc.Button('Submit', color='danger', id='authorprof_submitbtn'), 
        dbc.Modal( 
            [    
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress"), style=mod_style), 
                dbc.ModalBody("temp message", id = 'authorprof_feedback_message'),  
                dbc.ModalFooter( 
                    dbc.Button("Okay", id="authorprof_closebtn", color='secondary', className="ms-auto", n_clicks=0) 
                ),           
            ], 
            centered=True, 
            id="authorprof_modal", 
            is_open=False, 
        ), 
    ] 
) 

# Delete Record Style
@app.callback ( 
    [
        Output('authorprof_toload', 'data'), 
        Output('authorprof_removerecord_div', 'style')
    ],
    [ 
        Input('url', 'pathname'),
    ], 
    [ 
        State('url', 'search')
        
    ] 
)
def authorprof_load_removerecord(pathname, search): 
    if pathname == '/author_profile': 
        parsed = urlparse(search)
        mode = parse_qs(parsed.query)['mode'][0]

        to_load = 1 if mode == 'edit' else 0 

        removerecord_div = None if to_load else {'display': 'none'}

    else: 
         raise PreventUpdate 
    return [to_load, removerecord_div]

# IE Faculty Indicator Style       
@app.callback(
    [
        Output('authorprof_iefacind', 'style'), 
        Output('authorprof_noniefacind', 'style'),
        Output('authorprof_iefacind_label', 'style'),
        # Output('authorprof_iefacind_star', 'style'),
    ], 
    [
        Input('url', 'pathname'), 
        Input('authorprof_affiliation', 'value')
    ]
)
def facinddiv (pathname, aff): 
    if pathname == '/author_profile':
        if aff == '':
            aff = None
            facind = None
            nonfacind = None
            facindlabel = None
            # facindstar = None
        
        if aff == None:  
            facind = {'display': 'none'}
            nonfacind = {'display': 'none'}
            facindlabel = {'display': 'none'}
            # facindstar = {'display': 'none'}
        elif aff == False:
            facind = {'display': 'none'}
            nonfacind = None
            facindlabel = None
            # facindstar = None
        else: 
            facind = None
            nonfacind = {'display': 'none'}
            facindlabel = None
            # facindstar = None
    else: 
        raise PreventUpdate
    return [facind, nonfacind, facindlabel]


# Load Details
@app.callback (
    [
        Output('authorprof_ln', 'value'),
        Output('authorprof_fn', 'value'), 
        Output('authorprof_mail', 'value'), 
        Output('authorprof_contact', 'value'),    
        Output('authorprof_affiliation', 'value'),
        Output('authorprof_iefacind', 'value'),
    ], 
    [
        Input('authorprof_toload', 'modified_timestamp')
    ], 
    [
        State('authorprof_toload','data'), 
        State('url', 'search'), 
    ]
)
def authorprof_load (timestamp, to_load, search):
    if to_load == 1: 
        authorprof_sql = """ SELECT 
                author_id,
                author_user_id,
                author_ln, 
                author_fn,
                author_mail,
                author_contact,
                author_aff,
                author_fac_ind
            FROM authors
            WHERE
                author_delete_ind = false
            """
            
        parsed = urlparse(search)
        authorprofid = parse_qs(parsed.query)['id'][0]
            
        authorprof_val = []
        authorprof_colname = ['authorprof_id','authorprof_user_id', 'authorprof_ln', 'authorprof_fn', 'authorprof_mail', 'authorprof_contact', 'authorprof_aff', 'authorprof_fac_ind']
        authorprof_df = db.querydatafromdatabase(authorprof_sql, authorprof_val, authorprof_colname)
            
        counter = 0 
        for i in range(len(authorprof_df)):
                if authorprof_df['authorprof_id'][i] != int(authorprofid):
                    authorprof_df  = authorprof_df.drop(i)
                else: 
                    counted = counter 
                counter += 1
                    
        authorprof_ln = authorprof_df['authorprof_ln'][counted]
        authorprof_fn = authorprof_df['authorprof_fn'][counted]
        authorprof_mail = authorprof_df['authorprof_mail'][counted]
        authorprof_contact = authorprof_df['authorprof_contact'][counted]
        authorprof_aff = authorprof_df['authorprof_aff'][counted]
        authorprof_fac_ind = authorprof_df['authorprof_fac_ind'][counted]
    else:
        raise PreventUpdate
    return [authorprof_ln, authorprof_fn, authorprof_mail, authorprof_contact, authorprof_aff, authorprof_fac_ind]


# Submit Process 
@app.callback(
    [
        Output('authorprof_modal', 'is_open'), 
        Output('authorprof_feedback_message', 'children'), 
        Output('authorprof_inputs_alert', 'is_open'), 
        Output('authorprof_closebtn', 'href')
    ], 
    [
        Input('authorprof_submitbtn', 'n_clicks'), 
        Input('authorprof_closebtn', 'n_clicks')
    ],
    [
        State('authorprof_ln', 'value'), 
        State('authorprof_fn', 'value'),
        State('authorprof_mail', 'value'),
        State('authorprof_contact', 'value'),
        State('url', 'search'), 
        State('authorprof_removerecord', 'value'), 
        State('authorprof_affiliation', 'value'),
        State('authorprof_iefacind', 'value'),
        State('authorprof_noniefacind', 'value'),
    ]
)

def authorprof_submitprocess (submit_btn, close_btn,
                           lastname, firstname, mail, contact,
                           search, removerecord, 
                           aff, facind, nonfacind): 
    ctx = dash.callback_context
    if ctx.triggered: 
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False 
        feedbackmessage  = ' '
        inputsopenalert = False
        okay_href = None 
    else: 
        raise PreventUpdate
        
    if eventid == 'authorprof_submitbtn' and  submit_btn:
        completename = [lastname, firstname]
        if not all (completename):
            inputsopenalert = True
        # else:
        #     if aff == True:
        #         up_required = [aff, facind]
        #         if not all(up_required): 
        #             inputsopenalert = True
        #     elif aff == False:
        #         nonup_required = [aff, nonfacind]
        #         if not all(nonup_required): 
        #             inputsopenalert = True
        else: 
                openmodal = True 
                parsed = urlparse(search)
                mode = parse_qs(parsed.query)['mode'][0]
                
                author_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                author_timestamp_time = datetime.datetime.strptime(author_timestamp,'%Y-%m-%d %H:%M:%S')

                if mode == "add":
                    sql_add = """INSERT INTO authors(
                        author_ln, 
                        author_fn, 
                        author_mail,
                        author_contact,
                        author_aff,
                        author_fac_ind,
                        author_delete_ind, 
                        author_last_upd
                    )
                    VALUES (%s, %s, %s, %s,%s, %s, %s, %s)
                    """
                    values_add =[lastname, firstname, mail, contact, aff, facind, False, author_timestamp_time]
                    db.modifydatabase(sql_add,values_add)
                    feedbackmessage = f"Author added to DelPHI."
                    okay_href = '/author_manage'
                
                elif mode == 'edit': 
                    parsed = urlparse(search)
                    authorprof_editmodeid = parse_qs(parsed.query)['id'][0]
                    authorprof_editmodeuserid = parse_qs(parsed.query)['id'][0]
                    
                    sql_edit = """UPDATE authors
                    SET 
                        author_ln = %s, 
                        author_fn = %s, 
                        author_mail = %s,
                        author_contact = %s, 
                        author_aff = %s,
                        author_fac_ind = %s,
                        author_last_upd = %s,
                        author_delete_ind = %s
                    WHERE 
                        author_id = %s
                    """
                    to_delete = bool(removerecord)
                    values_edit = [lastname, firstname, mail, contact, aff, facind, author_timestamp_time, to_delete, authorprof_editmodeid]
                    
                    # if aff == True and facind == True:
                    sql_author="""SELECT author_user_id FROM authors"""
                    values_author = []
                    cols_author = ['id']
                    fac_user_id = db.querydatafromdatabase(sql_author, values_author, cols_author)
                        
                    for i in range(len(fac_user_id['id'])):
                        if int(fac_user_id['id'][i]) == int(authorprof_editmodeuserid):
                            sql_fac = """UPDATE faculty
                                    SET 
                                        faculty_ln = %s, 
                                        faculty_fn = %s,
                                        faculty_mail = %s,
                                        faculty_contact = %s,
                                        faculty_delete_ind = %s, 
                                        faculty_last_upd = %s
                                    WHERE 
                                        user_id = %s
                                    """
                            to_delete = bool(removerecord)
                            values_fac = [lastname, firstname, mail, contact, to_delete, author_timestamp_time, authorprof_editmodeuserid]
                            db.modifydatabase(sql_fac, values_fac)
                            
                    db.modifydatabase(sql_edit, values_edit)

                    feedbackmessage = "Author information updated."
                    okay_href = '/author_manage'
                else: 
                    raise PreventUpdate
    elif eventid == 'authorprof_closebtn' and close_btn: 
        pass 
    else: 
        raise PreventUpdate
    return [openmodal, feedbackmessage, inputsopenalert, okay_href]
