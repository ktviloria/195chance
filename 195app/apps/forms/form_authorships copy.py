#for adding and editing/deleting publications
#only admin users have access to this page

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

layout= html.Div( 
    [ 
        html.Div( 
            [ 
                dcc.Store(id='form_a_toload', storage_type='memory', data=0), 
            ] 
        ), 
        html.H2("Authorship Details"), 
        html.H6("* Indicates required field", style={"color": "#d9534f", "font-style": "italic"}),
        html.Hr(), 
        # General pub info needed
        html.Div(
            [
                #Faculty involved
                dbc.Row( 
                    [ 
                        dbc.Col(
                            [
                            dbc.Label("Faculty Involved"),
                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                            ], 
                            width=2, style={'display': 'flex', 'align-items': 'center'}
                            ), 
                        dbc.Col( 
                            html.Div( 
                                dcc.Dropdown( 
                                    id='form_a_fac', 
                                ),
                                className="dash-bootstrap" 
                            ), 
                            width=6
                        ), 
                    ], 
                    className="mb-3", 
                ), 
                #Publication tag
                dbc.Row( 
                    [ 
                        dbc.Col(
                            [
                            dbc.Label("Publication Criteria"),
                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                            ), 
                        dbc.Col( 
                            html.Div( 
                                dcc.Dropdown( 
                                    id='form_a_tag', 
                                ),
                                className="dash-bootstrap" 
                            ), 
                            width=6
                        ), 
                    ], 
                    className="mb-3", 
                ), 
                #Publication Title
                dbc.Row( 
                    [ 
                        dbc.Col(
                            [
                            dbc.Label("Publication Title"),
                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                            ),  
                        dbc.Col( 
                            dbc.Input( 
                                type="text", id="form_a_title", placeholder="Enter publication title", 
                            ), 
                            width=6, #className="placeholder"
                        ), 
                    ], 
                    className="mb-3", 
                ), 
            ],
            id='form_a_gen'
        ),
        # authorships
        html.Div(
            [
                #authors
                dbc.Row( 
                    [ 
                        dbc.Col(
                            [
                            dbc.Label("Authors"),
                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                            ), 
                        dbc.Col( 
                            dbc.Input( 
                                type="text", id="form_a_authors", placeholder="Enter all authors of publication" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                ),
                dbc.Row( 
                    [ 
                        dbc.Col(
                            [
                            dbc.Label("Authorship Role"),
                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                            ), 
                        dbc.Col( 
                            html.Div( 
                                dcc.Dropdown( 
                                    id='form_a_authorship_role', 
                                ),
                                className="dash-bootstrap" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                ), 
                dbc.Row( 
                    [ 
                        dbc.Label("Involvement", width=2, style={'display': 'flex', 'align-items': 'center'}), 
                        dbc.Col( 
                            html.Div( 
                                dcc.Dropdown( 
                                    id='form_a_involvement', 
                                ),
                                className="dash-bootstrap" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                ), 


                dbc.Row( 
                    [ 
                        dbc.Col(
                            [
                            dbc.Label("Publication Date"),
                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                            ), 
                        dbc.Col( 
                            html.Div(
                                dcc.DatePickerSingle(
                                    id='form_a_date',
                                    placeholder="MM/DD/YYYY",
                                    display_format="MM/DD/YYYY",
                                    min_date_allowed=date(2014, 1, 1),
                                    max_date_allowed=date.today(),
                                    initial_visible_month=date.today(),                                    
                                ), className="DateInput_input_1"
 
                            ), 
                        ), 
                    ], 
                    className="mb-3", 
                ),
                #publisher
                dbc.Row( 
                    [ 
                        dbc.Col(
                            [
                            dbc.Label("Publisher"),
                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                            ), 
                        dbc.Col( 
                            dbc.Input( 
                                type="text", id="form_a_publisher", placeholder="Enter publisher" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                ),
                #Name of Publication
                dbc.Row( 
                    [ 
                        dbc.Col(
                            [
                            dbc.Label("Name of Publication"),
                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                            ), 
                        dbc.Col( 
                            dbc.Input( 
                                type="text", id="form_a_pubname", placeholder="Enter name of publication or journal" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                ),
                #Scopus
                dbc.Row( 
                    [ 
                        dbc.Label("Scopus (Optional)", width=2, style={'display': 'flex', 'align-items': 'center'}), 
                        dbc.Col( 
                            dbc.Input( 
                                type="text", id="form_a_scopus", placeholder="Enter scopus" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                ),
                
                dbc.Row(
                    [
                    dbc.Col(
                        html.H6("Please provide at least one of the following:", style={"margin-bottom": "15px", "color": "#d9534f", "font-style": "italic"})
                        )
                    ]
                ),
                #DOI
                dbc.Row( 
                    [ 
                        dbc.Col(
                            [
                            dbc.Label("DOI"),
                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                            ),  
                        dbc.Col( 
                            dbc.Input( 
                                type="text", id="form_a_doi", placeholder="Enter DOI" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                ),
                #isxn
                dbc.Row( 
                    [ 
                        dbc.Col(
                            [
                            dbc.Label("ISBN/ISSN"),
                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                            ),  
                        dbc.Col( 
                            dbc.Input( 
                                type="text", id="form_a_isxn", placeholder="Enter ISBN/ISSN" 
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                ),
                
            ],
            id='form_a'
        ),
        html.Div( 
            dbc.Row( 
                [ 
                    dbc.Label("Wish to delete?", width=2), 
                    dbc.Col( 
                        dbc.Checklist( 
                            id='form_a_removerecord', 
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
            id = 'form_a_removerecord_div' 
        ), 
        html.Hr(), 
        dbc.Button('Submit', color='danger', id='form_a_submitbtn'), 
        dbc.Modal( 
            [    
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress"), style=mod_style), 
                dbc.ModalBody("tempmessage", id='form_a_feedback_message'), 
                dbc.ModalFooter( 
                    dbc.Button("Okay", color='secondary', id="form_a_closebtn", className="ms-auto", n_clicks=0) 
                ),           
            ], 
            centered=True, 
            id="form_a_modal", 
            is_open=False, 
        ),  
    ] 
) 

@app.callback (
    [
        Output('form_a_toload', 'data'), 
        Output('form_a_removerecord_div', 'style'),
        Output ('form_a_fac', 'options'), 
        Output ('form_a_tag', 'options'),
        Output ('form_a_authorship_role', 'options'), 
        Output ('form_a_involvement', 'options')
    ], 
    [
        Input('url', 'pathname'), 
    ], 
    [
        State('url', 'search'),
        State('currentuserid', 'data')
    ]
)

def form_a_load_dropdown(pathname, search, currentuserid): 
    if pathname == '/form_authorships': 
        sql_faculty_involved = """ SELECT DISTINCT (faculty.faculty_fn ||' '|| faculty.faculty_ln) as label, user_id as value
            from faculty
            
            ORDER BY value 
        """
        values_faculty = []
        cols_faculty = ['label', 'value']
        faculty_involved = db.querydatafromdatabase(sql_faculty_involved,values_faculty, cols_faculty)
        
        if currentuserid > 3:
            for i in range (len(faculty_involved)): 
                if faculty_involved['value'][i] != int (currentuserid): 
                    faculty_involved = faculty_involved.drop(i)
                else: 
                    pass
             
        
        faculty_opts = faculty_involved.to_dict('records')
        
        sql_tags = """SELECT DISTINCT (tag_title) AS label, tag_id AS value 
            from tags 
            WHERE tag_sub = 'A' and not tag_delete_ind 
                
            ORDER BY value
        """
        values_tag  = []
        cols_tag = ['label', 'value']
        tag_included = db.querydatafromdatabase(sql_tags, values_tag, cols_tag)
        tag_options = tag_included.to_dict('records')
        
        sql_author_roles = """SELECT a_label AS label, a_label_id AS value
            from authorship_role
            WHERE not role_delete_ind
            ORDER BY value 
        """
        values_author_roles = []
        cols_author_roles = ['label', 'value']
        author_roles_included = db.querydatafromdatabase(sql_author_roles, values_author_roles, cols_author_roles)
        author_role_options = author_roles_included.to_dict('records')
        
        sql_involvement = """ SELECT a_author_subcat_label as label, a_author_subcat_id  as value 
            from authorship_subcategory
            WHERE not sub_delete_ind
            ORDER BY value 
        """
        values_involvement = []
        cols_involvement = ['label', 'value']
        involvement_included = db.querydatafromdatabase(sql_involvement, values_involvement, cols_involvement)
        involvement_options = involvement_included.to_dict('records') 
        
        
        parsed = urlparse(search)
        mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if mode == 'edit' else 0 
        removerecord_div = None if to_load else {'display': 'none'}
    else: 
         raise PreventUpdate 
    return(to_load, removerecord_div,faculty_opts,tag_options, author_role_options, involvement_options )


@app.callback(
    [
        Output('form_a_fac', 'value'),
        Output('form_a_tag', 'value'),
        Output('form_a_title', 'value'),
        Output('form_a_authors', 'value'),
        Output('form_a_date', 'date'),
        Output('form_a_publisher', 'value'),
        Output('form_a_pubname', 'value'),
        Output('form_a_doi', 'value'),
        Output('form_a_isxn', 'value'),
        Output('form_a_scopus', 'value'), 
        Output('form_a_authorship_role', 'value'),
        Output('form_a_involvement', 'value') 
    ],
    [
        Input('form_a_toload', 'modified_timestamp')
    ],
    [
        State('form_a_toload', 'data'),
        State('url', 'search')
    ],
)

def form_a_load(timestamp, to_load, search): 
    if to_load == 1: 
        form_a_sql = """ SELECT 
            publications.pub_id,
			publications.user_id,
			publications.tag_id,
            publications.pub_title, 
            authorships.a_authors, 
            authorships.a_date,
            authorships.a_publisher,
            authorships.a_pub_name, 
            authorships.a_doi, 
            authorships.a_isxn, 
            authorships.a_scopus, 
            authorships.authorship_role, 
            authorships.authorship_subcategory
            FROM publications 
                INNER JOIN faculty on publications.user_id = faculty.user_id 
                INNER JOIN authorships on publications.pub_id = authorships.pub_id 
            WHERE 
                publications.pub_delete_ind = false
			ORDER BY publications.pub_id
        """
        
        parsed = urlparse(search)
        form_a_id = parse_qs(parsed.query)['id'][0]
        
        form_a_val = []
        form_a_colname = ['form_a_pub_id', 'form_a_pub_user_id', 'form_a_tag_id', 
                          'form_a_pub_title', 'form_a_authors', 'form_a_date', 'form_a_publisher', 
                          'form_a_pub_name', 'form_a_doi', 'form_a_isxn', 'form_a_scopus', 'form_a_authorship_role', 'form_a_involvement'  ]
        form_a_df = db.querydatafromdatabase(form_a_sql,  form_a_val, form_a_colname )
        
        counter = 0 
        counted = 0
        for i in range(len(form_a_df)): 
            if form_a_df['form_a_pub_id'][i] != int(form_a_id): 
                form_a_df = form_a_df.drop(i)
            else: 
                counted = counter 
            counter += 1
        
        form_a_pub_id = form_a_df['form_a_pub_id'][counted]
        form_a_pub_user_id = form_a_df['form_a_pub_user_id'][counted]
        form_a_tag_id = form_a_df['form_a_tag_id'][counted]
        form_a_pub_title = form_a_df['form_a_pub_title'][counted]
        form_a_authors = form_a_df['form_a_authors'][counted]
        form_a_date = form_a_df['form_a_date'][counted]
        form_a_publisher = form_a_df['form_a_publisher'][counted]
        form_a_pub_name = form_a_df['form_a_pub_name'][counted]
        form_a_doi = form_a_df['form_a_doi'][counted]
        form_a_isxn = form_a_df['form_a_isxn'][counted]
        form_a_scopus = form_a_df['form_a_scopus'][counted] 
        form_a_authorship_role = form_a_df['form_a_authorship_role'][counted]
        form_a_involvement = form_a_df['form_a_involvement'][counted]
    else: 
        raise PreventUpdate
    return [form_a_pub_user_id, form_a_tag_id,  form_a_pub_title,
            form_a_authors, form_a_date, form_a_publisher, form_a_pub_name, 
            form_a_doi, form_a_isxn, form_a_scopus, form_a_authorship_role, form_a_involvement]

@app.callback(
    [
        Output('form_a_modal', 'is_open'), 
        Output('form_a_feedback_message', 'children'), 
        Output('form_a_closebtn', 'href')
    ], 
    [
        Input('form_a_submitbtn', 'n_clicks'), 
        Input('form_a_closebtn', 'n_clicks') 
    ], 
    [
        State('form_a_fac', 'value'),
        State('form_a_tag', 'value'),
        State('form_a_title', 'value'),
        State('form_a_authors', 'value'),
        State('form_a_date', 'date'),
        State('form_a_publisher', 'value'),
        State('form_a_pubname', 'value'),
        State('form_a_doi', 'value'),
        State('form_a_isxn', 'value'),
        State('form_a_scopus', 'value'), 
        State('url', 'search' ),
        State('form_a_removerecord', 'value'), 
        State('form_a_authorship_role', 'value'), 
        State('form_a_involvement', 'value'), 
        State('currentuserid', 'data')
    ]
)

def form_a_submitprocess (submit_btn, close_btn, a_faculty, a_tag, 
                          a_title, a_authors, a_date, a_publisher, a_pubname,
                          a_doi, a_isxn, a_scopus, search, removerecord, a_author_role, a_involvement, cuser_id):
    ctx = dash.callback_context
    if ctx.triggered: 
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False 
        feedbackmessage  = ' '
        okay_href = None 
    else: 
        raise PreventUpdate
    
    if eventid == 'form_a_submitbtn' and submit_btn: 
        openmodal = True 
        inputs = [
            a_faculty, 
            a_tag, 
            a_title, 
            a_authors, 
            a_date, 
            a_publisher, 
            a_pubname, 
            a_author_role, 
            a_doi, 
            # a_isxn, 
            # a_scopus
        ]
        
        inputs2 = [
            a_faculty, 
            a_tag, 
            a_title, 
            a_authors, 
            a_date, 
            a_publisher, 
            a_pubname, 
            a_author_role, 
            # a_doi, 
            a_isxn, 
            # a_scopus
        ]
        
        if (not all(inputs) and not all(inputs2)): 
            feedbackmessage = "Please supply all needed information, and provide at least a DOI or an ISBN/ISSN."
        else: 
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]
            
            a_sqlcode_modifiedby = """SELECT
            user_id,
            user_un
            FROM users
            """
            a_vals_modifiedby = []
            a_cols_modifiedby = ['id', 'un']
            a_username = db.querydatafromdatabase(a_sqlcode_modifiedby, a_vals_modifiedby, a_cols_modifiedby)
            
            a_username_modifier = ""
            for i in range(len(a_username['id'])):
                if int(a_username['id'][i]) == cuser_id:
                    a_username_modifier = a_username['un'][i]

            a_timestamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            a_timestamp_time = dt.datetime.strptime(a_timestamp,'%Y-%m-%d %H:%M:%S')
            
            if mode == "add": 
                
                sql_max_inquiry = """SELECT MAX(pub_id) from publications
                """
                sql_max_val = []
                max_colname = ['max']
                pub_max_value_db = db.querydatafromdatabase (sql_max_inquiry, sql_max_val, max_colname)
                sql_pub_max = int(pub_max_value_db['max'][0]) + 1
                
                form_a_sqlcode_add_publications = """INSERT INTO publications(
                    pub_id, 
                    user_id, 
                    tag_id, 
                    pub_title, 
                    pub_delete_ind, 
                    pub_last_upd,
                    modified_by
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """ 
                
                form_a_values_addpub = [sql_pub_max, a_faculty, a_tag, a_title, False, a_timestamp_time, a_username_modifier]
                db.modifydatabase(form_a_sqlcode_add_publications, form_a_values_addpub)
                
                form_a_sqlcode_add_authorships = """INSERT INTO authorships(
                    pub_id, 
                    a_authors, 
                    a_date, 
                    a_year, 
                    a_publisher, 
                    a_pub_name, 
                    a_doi, 
                    a_isxn, 
                    a_scopus, 
                    authorship_role, 
                    authorship_subcategory
                )
                VALUES (%s, %s, %s, %s,%s,%s,%s,%s,%s, %s, %s)
                """
                str_to_date = datetime.strptime(a_date, '%Y-%m-%d').date()
                a_year = str_to_date.year
                
                form_a_values_addauthorship = [sql_pub_max, a_authors, a_date, a_year, a_publisher, a_pubname, a_doi, a_isxn, a_scopus, a_author_role, a_involvement]
                db.modifydatabase(form_a_sqlcode_add_authorships, form_a_values_addauthorship)
                feedbackmessage = 'Authorship entry added to database.'
                if cuser_id <= 3: 
                    okay_href = '/publications_manage'
                else: 
                    okay_href = '/my_publications'
            
            elif mode == 'edit': 
                parsed = urlparse(search)
                form_a_editmodeid = parse_qs(parsed.query)['id'][0]
                
                sql_update_publications = """UPDATE publications
                SET 
                    user_id = %s, 
                    tag_id = %s, 
                    pub_title = %s, 
                    pub_delete_ind = %s, 
                    pub_last_upd = %s,
                    modified_by = %s
                WHERE 
                    pub_id = %s
                """
                to_delete = bool(removerecord)
                
                values_update_publications = [a_faculty, a_tag, a_title, to_delete, a_timestamp_time, a_username_modifier, form_a_editmodeid]
                db.modifydatabase(sql_update_publications,values_update_publications )
                
                sql_update_authorships = """ UPDATE authorships
                SET 
                   a_authors = %s, 
                   a_date = %s, 
                   a_year= %s, 
                   a_publisher = %s, 
                   a_pub_name = %s, 
                   a_doi = %s, 
                   a_isxn = %s, 
                   a_scopus = %s, 
                   authorship_role = %s, 
                   authorship_subcategory = %s
                WHERE 
                    pub_id = %s
                """
                
                str_to_date = datetime.strptime(a_date, '%Y-%m-%d').date()
                
                
                a_year = str_to_date.year
                values_update_authorships = [a_authors, a_date, a_year, a_publisher, a_pubname, a_doi, a_isxn, a_scopus, a_author_role, a_involvement, form_a_editmodeid]
                db.modifydatabase(sql_update_authorships, values_update_authorships )
                feedbackmessage = 'Authorship details updated.'
                if cuser_id <= 3: 
                    okay_href = '/publications_manage'
                else: 
                    okay_href = '/my_publications'
                
            else: 
                raise PreventUpdate
    elif eventid == 'form_a_closebtn' and close_btn: 
        pass
    else: 
        raise PreventUpdate
    return [openmodal, feedbackmessage, okay_href]
