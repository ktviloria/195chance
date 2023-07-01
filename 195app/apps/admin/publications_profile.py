#for adding and editing/deleting publications
#only admin users have access to this page
#if editing, profile details of current faculty user being edited is shown

from dash import dcc
from dash import html
from dash import dash_table
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd
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
                dcc.Store(id='pubprof_toload', storage_type='memory', data=0), 
            ] 
        ), 
        html.H2("Publication Details"), 
        html.Hr(), 
        # General pub info needed
        html.Div(
            [
                #Faculty involved
                dbc.Row( 
                    [ 
                        dbc.Label("Faculty Involved", width=2), 
                        dbc.Col( 
                            html.Div( 
                                dbc.Select( 
                                    id='pubprof_fac', 
                                ),
                                className="dash-bootstrap" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                ), 
                #Publication tag
                dbc.Row( 
                    [ 
                        dbc.Label("Publication Tag", width=2), 
                        dbc.Col( 
                            html.Div( 
                                dbc.Select( 
                                    id='pubprof_tag', 
                                ),
                                className="dash-bootstrap" 
                            ), 
                            width=6, 
                        ), 
                    ], 
                    className="mb-3", 
                ), 
                #Publication Title
                dbc.Row( 
                    [ 
                        dbc.Label("Publication Title", width=2), 
                        dbc.Col( 
                            dbc.Input( 
                                type="text", id="pubprof_title", placeholder="Enter publication title" 
                            ), 
                            width=6, 
                        ), 
                    ], 
                    className="mb-3", 
                ), 
            ],
            id='pubprof_gen'
        ),
        # authorships
        html.Div(
            [
                #authors
                dbc.Row( 
                    [ 
                        dbc.Label("Authors", width=2), 
                        dbc.Col( 
                            dbc.Input( 
                                type="text", id="pubprof_a_authors", placeholder="Enter all authors of publication" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                ), 
                #pub date
                dbc.Row( 
                    [ 
                        dbc.Label("Publication Date", width=2), 
                        dbc.Col( 
                            dbc.Input( 
                                type="text", id="pubprof_a_pubdate", placeholder="Enter publication date YYYY or MM/DD/YYYY" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                ), 
                #publisher
                dbc.Row( 
                    [ 
                        dbc.Label("Publisher", width=2), 
                        dbc.Col( 
                            dbc.Input( 
                                type="text", id="pubprof_a_publisher", placeholder="Enter publisher" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                ),
                #Name of Publication
                dbc.Row( 
                    [ 
                        dbc.Label("Name of Publication", width=2), 
                        dbc.Col( 
                            dbc.Input( 
                                type="text", id="pubprof_a_pubname", placeholder="Enter name of publication" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                ),
                #DOI
                dbc.Row( 
                    [ 
                        dbc.Label("DOI", width=2), 
                        dbc.Col( 
                            dbc.Input( 
                                type="text", id="pubprof_a_doi", placeholder="Enter DOI" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                ),
                #isxn
                dbc.Row( 
                    [ 
                        dbc.Label("ISBN/ISSN", width=2), 
                        dbc.Col( 
                            dbc.Input( 
                                type="text", id="pubprof_a_isxn", placeholder="Enter ISBN/ISSN" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                ),
                #Scopus
                dbc.Row( 
                    [ 
                        dbc.Label("Scopus", width=2), 
                        dbc.Col( 
                            dbc.Input( 
                                type="text", id="pubprof_a_scopus", placeholder="Enter scopus" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                )
            ],
            id='pubprof_a'
        ),
        # presentations
        html.Div(
            [
                #authors
                dbc.Row( 
                    [ 
                        dbc.Label("Authors", width=2), 
                        dbc.Col( 
                            dbc.Input( 
                                type="text", id="pubprof_p_authors", placeholder="Enter all authors of publication" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                ), 
                #conference
                dbc.Row( 
                    [ 
                        dbc.Label("Conference", width=2), 
                        dbc.Col( 
                            dbc.Input( 
                                type="text", id="pubprof_p_conf", placeholder="Enter conference" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                ),
                #location
                dbc.Row( 
                    [ 
                        dbc.Label("Location", width=2), 
                        dbc.Col( 
                            dbc.Input( 
                                type="text", id="pubprof_p_loc", placeholder="Enter location of conference" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                ),
                #pres date
                dbc.Row( 
                    [ 
                        dbc.Label("Presentation Date", width=2), 
                        dbc.Col( 
                            dbc.Input(
                                type="text", id="pubprof_p_presdate", placeholder="Enter date(s) of presentation YYYY or MM/DD/YYYY" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                ),
                #pres add info
                dbc.Row( 
                    [ 
                        dbc.Label("Additional Information", width=2), 
                        dbc.Col( 
                            dbc.Input( 
                                type="text", id="pubprof_p_addinfo", placeholder="Enter any additional information" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                )
            ],
            id='pubprof_p'
        ),
        # projects
        html.Div(
            [
                #roles
                dbc.Row( 
                    [ 
                        dbc.Label("Role", width=2), 
                        dbc.Col( 
                            dbc.Input( 
                                type="text", id="pubprof_r_role", placeholder="Enter role in project" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                ), 
                #start date
                dbc.Row( 
                    [ 
                        dbc.Label("Project Start Date", width=2), 
                        dbc.Col( 
                            dbc.Input( 
                                type="text", id="pubprof_r_start", placeholder="Enter start date of project" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                ),
                #end date
                dbc.Row( 
                    [ 
                        dbc.Label("Project End Date", width=2), 
                        dbc.Col( 
                            dbc.Input( 
                                type="text", id="pubprof_r_end", placeholder="Enter end date of project" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                ),
                #timeframe
                dbc.Row( 
                    [ 
                        dbc.Label("Timeframe", width=2), 
                        dbc.Col( 
                            dbc.Input( 
                                type="text", id="pubprof_r_timeframe", placeholder="Enter timeframe of project YYYY or MM/DD/YYYY" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                ),
                #fund org
                dbc.Row( 
                    [ 
                        dbc.Label("Funding Organization", width=2), 
                        dbc.Col( 
                            dbc.Input(
                                type="text", id="pubprof_r_fundorg", placeholder="Enter funding organization" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                )
            ],
            id='pubprof_r'
        ),
        # others
        html.Div(
            [
                #date
                dbc.Row( 
                    [ 
                        dbc.Label("Date", width=2), 
                        dbc.Col( 
                            dbc.Input( 
                                type="text", id="pubprof_o_date", placeholder="Enter date of publication YYYY or MM/DD/YYYY" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                ),
                #others add info
                dbc.Row( 
                    [ 
                        dbc.Label("Additional Information", width=2), 
                        dbc.Col( 
                            dbc.Input( 
                                type="text", id="pubprof_p_addinfo", placeholder="Enter any additional information" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                )
            ],
            id='pubprof_o'
        ),
        #delete
        html.Div( 
            dbc.Row( 
                [ 
                    dbc.Label("Wish to delete?", width=2), 
                    dbc.Col( 
                        dbc.Checklist( 
                            id='pubprof_removerecord', 
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
            id = 'pubprof_removerecord_div' 
        ), 
        html.Hr(), 
        dbc.Button('Submit', color='danger', id='pubprof_submitbtn'), 
        dbc.Modal( 
            [    
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress"), style=mod_style), 
                dbc.ModalBody("tempmessage", id='pubprof_feedback_message'), 
                dbc.ModalFooter( 
                    dbc.Button("Okay", color='secondary', id="pubprof_closebtn", className="ms-auto", n_clicks=0) 
                ),           
            ], 
            centered=True, 
            id="pubprof_modal", 
            is_open=False, 
        ), 
    ] 
) 

@app.callback( 
        [ 
            Output('pubprof_toload', 'data'), 
            Output('pubprof_fac', 'options'), 
            Output('pubprof_tag', 'options'), 
            Output('pubprof_removerecord_div', 'style'),
        ], 
        [ 
            Input('url', 'pathname') 
        ], 
        [ 
            State('url', 'search') 
        ] 
    ) 

def facprof_load(pathname, search): 
    if pathname == '/publications_profile': 
        sql = """SELECT
                faculty_fn || ' ' || faculty_ln AS faculty_full_name,
                rank_title,
                faculty_bdate,
                faculty_mail,
                faculty_contact,
                faculty_emp_num,
                faculty_expert1,
                faculty_expert2,
                faculty_expert3,
                faculty_expert4,
                faculty_expert5
            FROM faculty
                INNER JOIN ranks ON faculty.rank_id = ranks.rank_id
                INNER JOIN users on faculty.user_id = users.user_id
            WHERE
                faculty_delete_ind = false
            ORDER BY
                faculty_last_upd DESC
            """
        values = []
        cols = ['Full Name', 'Rank', 'Birthdate', 'Mail', 'Contact number', 'Employee #', 'Expertise 1', 'Expertise 2', 'Expertise 3', 'Expertise 4', 'Expertise 5'] 
        faculty = db.querydatafromdatabase(sql, values, cols)
        rank_opts = faculty.to_dict('records') 

        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
 
        to_load = 1 if create_mode == 'edit' else 0
        removerecord_div = None if to_load else {'display':'none'}
        # if style = None, then we get the default value
    else:
        raise PreventUpdate
    return [to_load, rank_opts, removerecord_div]
 

# #define submission for adding and editing faculty 
