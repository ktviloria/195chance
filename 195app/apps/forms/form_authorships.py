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
                dcc.Store(id ='onlyloadonce', storage_type='memory', data=1), 
                dcc.Store(id = 'dummy', storage_type='memory', data='')
            ] 
        ), 
        html.H2("Publication Details"), 
        html.H6("* Indicates required field", style={"color": "#d9534f", "font-style": "italic"}),
        dbc.Alert('Please supply required fields.', color="danger", id='a_inputs_alert', is_open=False),
        dbc.Alert('Please supply either a DOI or ISXN', color="danger", id='a_inputs_alert2', is_open=False),
        html.Hr(), 
        # General pub info needed
        html.Div(
            [
                #Faculty involved
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
                            width=4,
                        ),
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
                                    id='form_a_fac', multi = False
                                ),
                                className="dash-bootstrap" 
                            ), 
                            width=4
                        ), 
                        
                    ], 
                    className="mb-3", 
                ), 
                html.Div(
                    dbc.Row(
                        [ 
                        dbc.Col(
                            [
                            dbc.Label("Authorship Role"),
                            #dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                            ), 
                        dbc.Col( 
                            html.Div( 
                                dcc.Dropdown( 
                                    id='form_a_authorship_role2', 
                                ),
                                className="dash-bootstrap" 
                            ), 
                            width=4,
                        ),
                        dbc.Col(
                            [
                            dbc.Label("Faculty Involved"),
                            #dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                            ], 
                            width=2, style={'display': 'flex', 'align-items': 'center'}
                            ), 
                        dbc.Col( 
                            html.Div( 
                                dcc.Dropdown( 
                                    id='form_a_fac2', multi = True
                                ),
                                className="dash-bootstrap" 
                            ), 
                            width=4
                        ), 
                        
                    ], 
                    className="mb-3", 
                        
                    ),
                    id = 'secondrow'
                ), 
                #Publication tag
                dbc.Row( 
                    [ 
                        dbc.Col(
                            [
                            dbc.Label("Criteria"),
                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                            ), 
                        dbc.Col( 
                            html.Div( 
                                dcc.Dropdown( 
                                    id='form_a_tag', optionHeight=60
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
                        dbc.Col(
                            [
                            dbc.Label("Publication Title"),
                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                            ),  
                        dbc.Col( 
                            dbc.Textarea( 
                                #type="text", 
                                id="form_a_title", placeholder="Enter title",
                            ), 
                            width=6,
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
                            dbc.Textarea( 
                                #type="text", 
                                id="form_a_authors", placeholder="Enter all authors of publication",
                            ), 
                            width=6,
                        ), 
                    ], 
                    className="mb-3", 
                ),
                # dbc.Row( 
                #     [ 
                #         dbc.Col(
                #             [
                #             dbc.Label("Authorship Role"),
                #             dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                #             ], width=2, style={'display': 'flex', 'align-items': 'center'}
                #             ), 
                #         dbc.Col( 
                #             html.Div( 
                #                 dcc.Dropdown( 
                #                     id='form_a_authorship_role', 
                #                 ),
                #                 className="dash-bootstrap" 
                #             ), 
                #             width=6,
                #         ), 
                #     ], 
                #     className="mb-3", 
                # ), 
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
                            dbc.Textarea( 
                                #type="text", 
                                id="form_a_publisher", placeholder="Enter publishing house or publishing company", style={"height":"15px"}  
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
                            dbc.Label("Name of Journal"),
                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                            ), 
                        dbc.Col( 
                            dbc.Textarea( 
                                #type="text", 
                                id="form_a_pubname", placeholder="Enter name of publication or journal",
                                style={"height":"15px"}
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
                                type="text", 
                                id="form_a_doi", placeholder="Enter DOI"
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
                                type="text", 
                                id="form_a_isxn", placeholder="Enter ISBN/ISSN"
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
                        width=4, 
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
        # Output('form_a_toload', 'data'), 
        Output('form_a_removerecord_div', 'style'),
        Output ('form_a_fac', 'options'),
        Output ('form_a_fac2', 'options'), 
        Output ('form_a_tag', 'options'),
        Output ('form_a_authorship_role', 'options'), 
        Output ('form_a_authorship_role2', 'options'), 
        Output ('form_a_involvement', 'options'), 
    ], 
    [
        Input('url', 'pathname'), 
        Input('form_a_authorship_role', 'value') , 
        Input('form_a_fac', 'value')
    ], 
    [
        State('url', 'search'),
        State('currentuserid', 'data'), 
        
    ]
)

def form_a_load_dropdown(pathname, role, lead, search, currentuserid): 
    if pathname == '/form_authorships': 
        sql_faculty_involved = """ SELECT DISTINCT (faculty.faculty_fn ||' '|| faculty.faculty_ln) as label, user_id as value
            from faculty
            WHERE not faculty_delete_ind  and faculty_active_ind = true
            ORDER BY value 
        """
        values_faculty = []
        
        cols_faculty = ['label', 'value']
        faculty_involved = db.querydatafromdatabase(sql_faculty_involved,values_faculty, cols_faculty)

        roles = ''
        if role != None : 
            sql_author_roles = """SELECT a_label AS label, a_label_id AS value
                from authorship_role
                WHERE not role_delete_ind and a_label_id = %s 
                ORDER BY value 
            """
            values_author_roles = [role]
            cols_author_roles = ['label', 'value']
            author_roles_included = db.querydatafromdatabase(sql_author_roles, values_author_roles, cols_author_roles)
            roles = author_roles_included['label'][0]
        
        # if roles != 'Co-Author': 
        #     if int(currentuserid) > 3:
        #         for i in range (len(faculty_involved)): 
        #             if faculty_involved['value'][i] != int (currentuserid): 
        #                 faculty_involved = faculty_involved.drop(i)
        #             else: 
        #                 pass
        

        if roles != 'Co-Author': 
            if type(lead)==int:
                sql_faculty_involved2 = """ SELECT DISTINCT (faculty.faculty_fn ||' '|| faculty.faculty_ln) as label, user_id as value
                    from faculty
                    WHERE not faculty_delete_ind  and not user_id = %s
                    ORDER BY value 
                """
                values_faculty2 = [lead]
                faculty_involved2 = db.querydatafromdatabase(sql_faculty_involved2,values_faculty2, cols_faculty)
            else:
                faculty_involved2 = faculty_involved 
        else: 
            faculty_involved2 = faculty_involved
        
        
        
             
        faculty_opts = faculty_involved.to_dict('records')
        faculty_opts2 = faculty_involved2.to_dict('records')
        
        
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
        
        author_roles_included2 = author_roles_included
        for i in range (len(author_roles_included2)): 
            if author_roles_included2['label'][i] != 'Contributing Author':
                author_roles_included2 = author_roles_included2.drop(i)
                
        author_role_options2 = author_roles_included2.to_dict('records')
        
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
    return(removerecord_div,faculty_opts, faculty_opts2,tag_options, author_role_options,author_role_options2, involvement_options )

@app.callback(
    [
        Output('secondrow','style'), 
        Output('form_a_fac','multi'),
        
    ], 
    [
        Input('url', 'pathname'),
        Input('form_a_toload', 'modified_timestamp'), 
        Input('form_a_authorship_role', 'value')  
    ]
)
def secondrow_stuff (pathname, timestamp, role):
    if pathname == '/form_authorships': 
        roles = ''
        if role != None: 
            sql_author_roles = """SELECT a_label AS label, a_label_id AS value
                from authorship_role
                WHERE not role_delete_ind and a_label_id = %s 
                ORDER BY value 
            """
            values_author_roles = [role]
            cols_author_roles = ['label', 'value']
            author_roles_included = db.querydatafromdatabase(sql_author_roles, values_author_roles, cols_author_roles)
            roles = author_roles_included['label'][0]

        
        # roles = ''
        # for i in range(len(author_roles_included)): 
        #     if author_roles_included['value'][i] == role: 
        #         roles = author_roles_included['label'][i]
        #     else: 
        #         roles = None
        # print(roles == 'Lead Author')
        # print(roles)
        # print('Lead Author')
        if roles == 'Lead Author': 
            remove_secondrow = None 
            multi = False
        elif  roles == 'Co-Author': 
            remove_secondrow = {'display': 'none'}
            multi = True
        elif roles == 'Contributing Author': 
            remove_secondrow = {'display': 'none'}
            multi = True
        else: 
            remove_secondrow = {'display': 'none'}
            multi = False
            
    else: 
        raise PreventUpdate
    return [remove_secondrow, multi]
    

@app.callback(
    [
        Output('form_a_tag', 'value'),
        Output('form_a_title', 'value'),
        Output('form_a_authors', 'value'),
        Output('form_a_date', 'date'),
        Output('form_a_publisher', 'value'),
        Output('form_a_pubname', 'value'),
        Output('form_a_doi', 'value'),
        Output('form_a_isxn', 'value'),
        Output('form_a_scopus', 'value'), 
        Output('form_a_involvement', 'value'), 
        Output('form_a_authorship_role', 'value'),
        Output('form_a_authorship_role2', 'value'), 
        Output('form_a_fac', 'value'),
        Output('form_a_fac2', 'value'),
        # Output('form_a_fac', 'persistence'), 
        # Output('form_a_fac', 'persistence-type'), 
        Output('onlyloadonce','data' )
    ],
    [
        Input('form_a_toload', 'modified_timestamp'), 
    ],
    [
        State('form_a_toload', 'data'),
        State('url', 'search'), 
        State('onlyloadonce', 'data')
    ],
)

def form_a_load(timestamp, to_load, search, onlyloadonce): 
    parsed = urlparse(search)
    mode = parse_qs(parsed.query)['mode'][0]
    to_load = 1 if mode == 'edit' else 0 
    
    if onlyloadonce == 1: 
        if to_load == 1: 
            form_a_sql = """ SELECT 
                publications.pub_id,
                publications.tag_id,
                publications.pub_title, 
                authorships.a_authors, 
                authorships.a_date,
                authorships.a_publisher,
                authorships.a_pub_name, 
                authorships.a_doi, 
                authorships.a_isxn, 
                authorships.a_scopus, 
                authorships.authorship_subcategory
                FROM publications 
                    LEFT OUTER JOIN faculty on publications.user_id = faculty.user_id 
                    LEFT OUTER JOIN authorships on publications.pub_id = authorships.pub_id 
                WHERE 
                    publications.pub_delete_ind = false and publications.pub_id = %s 
                ORDER BY publications.pub_id
            """
        
            
            parsed = urlparse(search)
            form_a_id = parse_qs(parsed.query)['id'][0]
            
            form_a_val = [int(form_a_id)]
            form_a_colname = ['form_a_pub_id',  'form_a_tag_id', 
                            'form_a_pub_title', 'form_a_authors', 'form_a_date', 'form_a_publisher', 
                            'form_a_pub_name', 'form_a_doi', 'form_a_isxn', 'form_a_scopus', 'form_a_involvement']
            form_a_df = db.querydatafromdatabase(form_a_sql,  form_a_val, form_a_colname )
            
            form_au_us = """SELECT 
                authorships_users.user_id, 
                authorships_users.authorship_role, 
                authorship_role.a_label
                
            
            FROM authorships_users
            LEFT OUTER JOIN authorship_role ON authorships_users.authorship_role = authorship_role.a_label_id
            WHERE authorships_users.pub_id = %s
            ORDER BY authorships_users.authorship_role
            """
            form_au_us_val = [int(form_a_id)]
            form_au_us_col = ['user_ids', 'role_id', 'roles']
            form_au_us_df = db.querydatafromdatabase(form_au_us,  form_au_us_val, form_au_us_col)
            
            author_r1 = ''
            author_r2 = ''
            author1 = []
            author2 = []
            if len(form_au_us_df['roles']) > 1: 
                author_r1 = form_au_us_df['role_id'][0]
                if form_au_us_df['roles'][0] != form_au_us_df['roles'][1]: 
                    author_r2 = form_au_us_df['role_id'][1]
                    author1 = form_au_us_df['user_ids'][0]
                    for i in range(len(form_au_us_df['user_ids'])): 
                        if i > 0: 
                            author2.append(form_au_us_df['user_ids'][i])
                        else: 
                            pass
                elif form_au_us_df['roles'][0] == form_au_us_df['roles'][1]:
                    for i in range(len(form_au_us_df['user_ids'])): 
                        author1.append(form_au_us_df['user_ids'][i])
                else: 
                    pass
            elif len(form_au_us_df['roles']) == 1:
                author_r1 = author_r1 = form_au_us_df['role_id'][0]
                author1 = form_au_us_df['user_ids'][0]
                
                author_r2 = None 
                author2 = None
                    
                        
                    
                    
                
            
            
            form_a_pub_id = form_a_df['form_a_pub_id'][0]
            form_a_tag_id = form_a_df['form_a_tag_id'][0]
            form_a_pub_title = form_a_df['form_a_pub_title'][0]
            form_a_authors = form_a_df['form_a_authors'][0]
            form_a_date = form_a_df['form_a_date'][0]
            form_a_publisher = form_a_df['form_a_publisher'][0]
            form_a_pub_name = form_a_df['form_a_pub_name'][0]
            form_a_doi = form_a_df['form_a_doi'][0]
            form_a_isxn = form_a_df['form_a_isxn'][0]
            form_a_scopus = form_a_df['form_a_scopus'][0] 
            form_a_involvement = form_a_df['form_a_involvement'][0]

        else: 
            raise PreventUpdate 
        onlyloadonce += 1
        
        
    else: 
        raise PreventUpdate
    return [form_a_tag_id,  form_a_pub_title,
            form_a_authors, form_a_date, form_a_publisher, form_a_pub_name, 
            form_a_doi, form_a_isxn, form_a_scopus,  form_a_involvement, author_r1, author_r2, author1, author2, onlyloadonce ]

# tester 
# @app.callback(
#     [
#         Output('dummy', 'data')
#     ],
#     [
#          Input('form_a_submitbtn', 'n_clicks'), 
#          Input('form_a_closebtn', 'n_clicks') 
#     ], 
#     [
#         State('form_a_fac', 'value'), 
#         State('form_a_fac2', 'value'),
#         State('form_a_authorship_role2', 'value'),
#     ]
# )

# def submit(submit_btn, close_btn, form_a_fac, form_a_fac2, author2): 
#     ctx = dash.callback_context
#     ctx = dash.callback_context
#     if ctx.triggered: 
#         eventid = ctx.triggered[0]['prop_id'].split('.')[0]
#     else: 
#         raise PreventUpdate
    
#     print(author2)
    
#     if eventid == 'form_a_submitbtn' and submit_btn: 
#         if form_a_fac2 == None: 
#             form_a_fac2 = []
#         if form_a_fac == None: 
#             form_a_fac = []
#         if type(form_a_fac) == int: 
#             form_a_fac = [form_a_fac]
#         form_a_fac_combined = form_a_fac + form_a_fac2
#         print(form_a_fac_combined)
#         print(form_a_fac_combined[0])
#     return [form_a_fac_combined]
        


@app.callback(
    [
        Output('form_a_modal', 'is_open'), 
        Output('form_a_feedback_message', 'children'), 
        Output('form_a_closebtn', 'href'), 
        Output('a_inputs_alert', 'is_open'),
        Output('a_inputs_alert2', 'is_open')
    ], 
    [
        Input('form_a_submitbtn', 'n_clicks'), 
        Input('form_a_closebtn', 'n_clicks') 
    ], 
    [
        State('form_a_fac', 'value'),
        State('form_a_fac2', 'value'),
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
        State('form_a_authorship_role2', 'value'), 
        State('form_a_involvement', 'value'), 
        State('currentuserid', 'data')
    ]
)

def form_a_submitprocess (submit_btn, close_btn, a_faculty, a_faculty2, a_tag, 
                          a_title, a_authors, a_date, a_publisher, a_pubname,
                          a_doi, a_isxn, a_scopus, search, removerecord, a_author_role, a_author_role2, a_involvement, cuser_id):
    ctx = dash.callback_context
    if ctx.triggered: 
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False 
        feedbackmessage  = ' '
        all_inputsalert = False
        DOI_alert = False 
        okay_href = None 
    else: 
        raise PreventUpdate
    
    if eventid == 'form_a_submitbtn' and submit_btn: 
        
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
        if (not(a_doi) and not(a_isxn)): 
            DOI_alert = True 
        
        if (not all(inputs) and not all(inputs2)): 
            all_inputsalert = True
        else:
            openmodal = True  
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
            
            roles = ''
            if a_author_role != None: 
                sql_author_roles = """SELECT a_label AS label, a_label_id AS value
                    from authorship_role
                    WHERE not role_delete_ind and a_label_id = %s 
                    ORDER BY value 
                """
                values_author_roles = [a_author_role]
                cols_author_roles = ['label', 'value']
                author_roles_included = db.querydatafromdatabase(sql_author_roles, values_author_roles, cols_author_roles)
                roles = author_roles_included['label'][0]
                
                
            if mode == "add": 
                print(a_author_role2)

                sql_max_inquiry = """SELECT MAX(pub_id) from publications
                """
                sql_max_val = []
                max_colname = ['max']
                pub_max_value_db = db.querydatafromdatabase (sql_max_inquiry, sql_max_val, max_colname)
                sql_pub_max = int(pub_max_value_db['max'][0]) + 1
                
                form_a_sqlcode_add_publications = """INSERT INTO publications(
                    pub_id,  
                    tag_id, 
                    pub_title, 
                    pub_delete_ind, 
                    pub_last_upd,
                    modified_by
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """ 
                
                form_a_values_addpub = [sql_pub_max, a_tag, a_title, False, a_timestamp_time, a_username_modifier]
                db.modifydatabase(form_a_sqlcode_add_publications, form_a_values_addpub)
                

                # if a_faculty2 == None: 
                #     a_faculty2 = []
                # if type(a_faculty) == int: 
                #     a_faculty = [a_faculty]
                # form_a_fac_combined = a_faculty + a_faculty2
                
                # roles = ''
                # if a_author_role != None: 
                #     sql_author_roles = """SELECT a_label AS label, a_label_id AS value
                #         from authorship_role
                #         WHERE not role_delete_ind and a_label_id = %s 
                #         ORDER BY value 
                #     """
                #     values_author_roles = [a_author_role]
                #     cols_author_roles = ['label', 'value']
                #     author_roles_included = db.querydatafromdatabase(sql_author_roles, values_author_roles, cols_author_roles)
                #     roles = author_roles_included['label'][0]
                if a_faculty2 == None: 
                    a_faculty2 = []
                if roles == 'Co-Author': 
                    a_faculty2 = []
                if a_faculty == None: 
                        a_faculty = []
                if type(a_faculty) == int: 
                        a_faculty = [a_faculty]
                form_a_fac_combined = a_faculty + a_faculty2
                
                for i in range(len(form_a_fac_combined)): 
                    sql_authorships_users = """INSERT INTO authorships_users(
                        pub_id, 
                        user_id, 
                        authorship_role 
                    )
                    VALUES (%s, %s, %s)
                    """
                    role_num = ''
                    

                    
                    if roles == 'Co-Author' or roles =='Contributing Author':
                        role_num = a_author_role
                    if roles == 'Lead Author': 
                        
                        if int(i) == 0: 
                            role_num = a_author_role
                        elif int(i) > 0:  
                            role_num = a_author_role2
                    
                    
                        
                    authorships_users_values = [sql_pub_max,form_a_fac_combined[i],role_num ]
                    db.modifydatabase(sql_authorships_users, authorships_users_values)
                
                
                
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
                    authorship_subcategory
                )
                VALUES (%s, %s, %s, %s,%s,%s,%s,%s,%s, %s)
                """
                str_to_date = datetime.strptime(a_date, '%Y-%m-%d').date()
                a_year = str_to_date.year
                
                
                
                form_a_values_addauthorship = [sql_pub_max, a_authors, a_date, a_year, a_publisher, a_pubname, a_doi, a_isxn, a_scopus, a_involvement]
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
                    tag_id = %s, 
                    pub_title = %s, 
                    pub_delete_ind = %s, 
                    pub_last_upd = %s,
                    modified_by = %s
                WHERE 
                    pub_id = %s
                """
                to_delete = bool(removerecord)
                
                values_update_publications = [a_tag, a_title, to_delete, a_timestamp_time, a_username_modifier, form_a_editmodeid]
                db.modifydatabase(sql_update_publications,values_update_publications )
                
                
                if a_faculty2 == None: 
                    a_faculty2 = []
                if roles == 'Co-Author': 
                    a_faculty2 = []
                if a_faculty == None: 
                        a_faculty = []
                if type(a_faculty) == int: 
                        a_faculty = [a_faculty]
                form_a_fac_combined = a_faculty + a_faculty2
                                
                sql_authorships_users = """DELETE FROM authorships_users
                        WHERE pub_id = %s      
                """
                authorships_users_values = [int(form_a_editmodeid)]
                db.modifydatabase(sql_authorships_users, authorships_users_values)
                role_num = ''
                for i in range(len(form_a_fac_combined)): 
                    print(i)
                    sql_authorships_users =  """INSERT INTO authorships_users(
                        pub_id, 
                        user_id, 
                        authorship_role 
                    )
                    VALUES (%s, %s, %s)
                    """
                    
                    if roles == 'Co-Author' or 'Contributing Author': 
                        role_num = a_author_role
                    if roles == 'Lead Author': 
                        if i == 0: 
                            role_num = a_author_role
                        else: 
                            role_num = a_author_role2
                    
                    authorships_users_values = [int(form_a_editmodeid), form_a_fac_combined[i],role_num ]
                    db.modifydatabase(sql_authorships_users, authorships_users_values)
                
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
                   authorship_subcategory = %s
                WHERE 
                    pub_id = %s
                """
                
                str_to_date = datetime.strptime(a_date, '%Y-%m-%d').date()
                
                
                a_year = str_to_date.year
                values_update_authorships = [a_authors, a_date, a_year, a_publisher, a_pubname, a_doi, a_isxn, a_scopus, a_involvement, form_a_editmodeid]
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
    return [openmodal, feedbackmessage, okay_href, all_inputsalert,DOI_alert ]
