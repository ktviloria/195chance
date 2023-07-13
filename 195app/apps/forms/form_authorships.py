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
        dbc.Alert('Lead authors cannot be other contributing authors. Please check your selection.', color="danger", id='a_authors_alert', is_open=False),
        html.Hr(), 
        # General pub info needed
        html.Div(
            [
                #Authors involved
                dbc.Row( 
                    [ 
                        dbc.Col(
                            [
                            dbc.Label("Lead Author(s)"),
                            dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                            ), 
                        dbc.Col( 
                            dcc.Dropdown( 
                                    id='form_a_lead', multi = True, searchable = True
                                ),
                            width=6
                        ), 
                    ], 
                    className="mb-3", 
                ), 
                dbc.Row(
                    [ 
                        dbc.Col(
                            [
                            dbc.Label("Contributing Author(s)"),
                            #dbc.Label("*", style={"color": "#d9534f", "font-style": "bold"})
                            ], width=2, style={'display': 'flex', 'align-items': 'center'}
                            ), 
                        dbc.Col( 
                                dcc.Dropdown( 
                                    id='form_a_contributing', multi = True, searchable = True
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
                #Publication Date
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

# Delete Record Style
@app.callback ( 
    [
        Output('form_a_toload', 'data'),
        Output('form_a_removerecord_div', 'style'),
    ],
    [ 
        Input('url', 'pathname')
    ], 
    [ 
        State('url', 'search')
    ] 
)
def form_a_load_removerecord(pathname, search): 
    if pathname == '/form_authorships': 
        parsed = urlparse(search)
        mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if mode == 'edit' else 0 
        removerecord_div = None if to_load else {'display': 'none'}
    else: 
         raise PreventUpdate 
    return [to_load, removerecord_div]

#Dropdown
@app.callback (
    [
        # Output('form_a_toload', 'data'), 
        Output ('form_a_lead', 'options'),
        Output ('form_a_contributing', 'options'), 
        Output ('form_a_tag', 'options'),
        # Output ('form_a_involvement', 'options'), 
    ], 
    [
        Input('url', 'pathname'), 
        # Input('form_a_authorship_role', 'value') , 
        Input('form_a_lead', 'value'),
        Input('form_a_contributing', 'value')
    ], 
    [
        State('currentuserid', 'data'),  
    ]
)
def form_a_load_dropdown(pathname, lead, contributing, currentuserid): 
    if pathname == '/form_authorships': 
        sql_lead_author = """ SELECT
            DISTINCT (author_fn ||' '|| author_ln) as label, author_id as value,
			author_user_id
            from authors
            WHERE not author_delete_ind
				ORDER BY authors.author_user_id 
        """
        values_lead_author = []
        
        cols_lead_author = ['label', 'value', 'faculty_ind']
        lead_author_involved = db.querydatafromdatabase(sql_lead_author, values_lead_author, cols_lead_author)

        lead_author_opts = lead_author_involved.to_dict('records')

        sql_contributing_author = """ SELECT
            DISTINCT (author_fn ||' '|| author_ln) as label, author_id as value
            from authors
            WHERE not author_delete_ind
            ORDER BY value DESC
        """
        values_contributing_author = []
        
        cols_contributing_author = ['label', 'value']
        contributing_author_involved = db.querydatafromdatabase(sql_contributing_author, values_contributing_author, cols_contributing_author)

        contributing_author_opts = contributing_author_involved.to_dict('records')

        # for x in x in
        #     sql_contributing_author = """ SELECT DISTINCT (authors.author_fn ||' '|| authors.author_ln) as label, author_id as value
        #         from authors
        #         WHERE not author_delete_ind and not author_id = %s
        #         ORDER BY value 
        #     """
        #     values_contributing_author = [lead]
        #     contributing_author_involved = db.querydatafromdatabase(sql_contributing_author, values_contributing_author, cols_lead_author)
        
        # contributing_author_involved = [x for x in lead_author_involved
        #                                 if x[id] != lead
        #                                 and x[id] != contributing]
        
        #tag dropdown
        sql_tags = """SELECT DISTINCT (tag_title) AS label, tag_id AS value 
            from tags 
            WHERE tag_sub = 'A' and not tag_delete_ind 
                
            ORDER BY value
        """
        values_tag  = []
        cols_tag = ['label', 'value']
        tag_included = db.querydatafromdatabase(sql_tags, values_tag, cols_tag)
        tag_options = tag_included.to_dict('records')
        
        # #involvement dropdown
        # sql_involvement = """ SELECT a_author_subcat_label as label, a_author_subcat_id  as value 
        #     from authorship_subcategory
        #     WHERE not sub_delete_ind
        #     ORDER BY value 
        # """
        # values_involvement = []
        # cols_involvement = ['label', 'value']
        # involvement_included = db.querydatafromdatabase(sql_involvement, values_involvement, cols_involvement)
        # involvement_options = involvement_included.to_dict('records') 
        
    else: 
         raise PreventUpdate 
    return(lead_author_opts, contributing_author_opts, tag_options)
    
@app.callback(
    [
        Output('form_a_lead', 'value'),
        Output('form_a_contributing', 'value'),
        Output('form_a_title', 'value'),
        Output('form_a_tag', 'value'),
        Output('form_a_date', 'date'),
        Output('form_a_publisher', 'value'),
        Output('form_a_pubname', 'value'),
        Output('form_a_doi', 'value'),
        Output('form_a_isxn', 'value'),
        Output('form_a_scopus', 'value'), 
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
            form_a_sql = """ SELECT distinct authorships.pub_id,
				(select string_agg(lead_author_name, ', ')
				 from pub_lead_authors
				 where pub_lead_authors.pub_id = authorships.pub_id
				) as lead_authors, 
                (select string_agg(contributing_author_name, ', ')
				 from pub_contributing_authors
				 where pub_contributing_authors.pub_id = authorships.pub_id
				) as contributing_authors, 
                publications.pub_title, 
                publications.tag_id,
                authorships.a_date,
                authorships.a_publisher,
                authorships.a_pub_name, 
                authorships.a_doi, 
                authorships.a_isxn, 
                authorships.a_scopus

                FROM authorships 
                    INNER JOIN publications on authorships.pub_id = publications.pub_id 
					LEFT OUTER JOIN pub_lead_authors on publications.pub_id = pub_lead_authors.pub_id
					LEFT OUTER JOIN pub_contributing_authors on publications.pub_id = pub_contributing_authors.pub_id
                WHERE
                    publications.pub_delete_ind = false and authorships.pub_id = %s
                ORDER BY authorships.pub_id
            """
        
            parsed = urlparse(search)
            form_a_id = parse_qs(parsed.query)['id'][0]
            form_a_val = [int(form_a_id)]
            form_a_colname = ['form_a_pub_id',
                              'form_a_lead', 'form_a_contributing',
                              'form_a_pub_title', 'form_a_tag_id',
                              'form_a_date', 'form_a_publisher', 'form_a_pub_name', 'form_a_doi', 'form_a_isxn', 'form_a_scopus']
            form_a_df = db.querydatafromdatabase(form_a_sql,  form_a_val, form_a_colname )
            
            form_a_lead_sql = """SELECT distinct a_lead_id
                from
                    authorships
                where
                    a_lead_id in (SELECT distinct a_lead_id
                                from pub_lead_authors
                                where pub_lead_authors.pub_id = authorships.pub_id)
                    and authorships.pub_id = %s"""
            form_a_lead_val = [int(form_a_id)]
            form_a_lead_cols = ['a_lead_ids']
            form_a_lead_df = db.querydatafromdatabase(form_a_lead_sql, form_a_lead_val, form_a_lead_cols)
            form_a_lead= form_a_lead_df['a_lead_ids'][0]
            form_a_lead=[]
            for i in range(len(form_a_lead_df['a_lead_ids'])): 
                form_a_lead.append(form_a_lead_df['a_lead_ids'][i])
            
            form_a_contributing_sql = """SELECT distinct a_contributing_id
                from
                    authorships
                where
                    a_contributing_id in (SELECT distinct a_contributing_id
                                from pub_contributing_authors
                                where pub_contributing_authors.pub_id = authorships.pub_id)
                    and authorships.pub_id = %s"""
            form_a_contributing_val = [int(form_a_id)]
            form_a_contributing_cols = ['a_contributing_ids']
            form_a_contributing_df = db.querydatafromdatabase(form_a_contributing_sql, form_a_contributing_val, form_a_contributing_cols)
            
            if len(form_a_contributing_df) == 0:
                form_a_contributing = []
            else:
                form_a_contributing= form_a_contributing_df['a_contributing_ids'][0]
                form_a_contributing = []
                for i in range(len(form_a_contributing_df['a_contributing_ids'])): 
                    form_a_contributing.append(form_a_contributing_df['a_contributing_ids'][i])

            form_a_pub_id = form_a_df['form_a_pub_id'][0]
            form_a_pub_title = form_a_df['form_a_pub_title'][0]
            form_a_tag_id = form_a_df['form_a_tag_id'][0]
            form_a_date = form_a_df['form_a_date'][0]
            form_a_publisher = form_a_df['form_a_publisher'][0]
            form_a_pub_name = form_a_df['form_a_pub_name'][0]
            form_a_doi = form_a_df['form_a_doi'][0]
            form_a_isxn = form_a_df['form_a_isxn'][0]
            form_a_scopus = form_a_df['form_a_scopus'][0] 

        else: 
            raise PreventUpdate 
        onlyloadonce += 1       
        
    else: 
        raise PreventUpdate
    return [form_a_lead, form_a_contributing,
            form_a_pub_title, form_a_tag_id, form_a_date, form_a_publisher, form_a_pub_name, 
            form_a_doi, form_a_isxn, form_a_scopus, onlyloadonce ]


@app.callback(
    [
        Output('form_a_modal', 'is_open'), 
        Output('form_a_feedback_message', 'children'), 
        Output('form_a_closebtn', 'href'), 
        Output('a_inputs_alert', 'is_open'),
        Output('a_inputs_alert2', 'is_open'),
        Output('a_authors_alert', 'is_open'),
    ], 
    [
        Input('form_a_submitbtn', 'n_clicks'), 
        Input('form_a_closebtn', 'n_clicks') 
    ], 
    [
        State('form_a_lead', 'value'),
        State('form_a_contributing', 'value'),
        State('form_a_title', 'value'),
        State('form_a_tag', 'value'),
        State('form_a_date', 'date'),
        State('form_a_publisher', 'value'),
        State('form_a_pubname', 'value'),
        State('form_a_doi', 'value'),
        State('form_a_isxn', 'value'),
        State('form_a_scopus', 'value'), 
        State('url', 'search' ),
        State('form_a_removerecord', 'value'),  
        State('currentuserid', 'data')
    ]
)

def form_a_submitprocess (submit_btn, close_btn, a_lead, a_contributing, 
                          a_title, a_tag, a_date, a_publisher, a_pubname,
                          a_doi, a_isxn, a_scopus, search, removerecord, cuser_id):
    ctx = dash.callback_context
    if ctx.triggered: 
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False 
        feedbackmessage  = ' '
        inputsalert = False
        DOI_alert = False
        authoralert = False
        okay_href = None 
    else: 
        raise PreventUpdate
    
    if eventid == 'form_a_submitbtn' and submit_btn:     
        inputs = [
            a_lead,
            a_tag, 
            a_title, 
            a_date, 
            a_publisher, 
            a_pubname
        ]
        
        # inputs2 = [
        #     a_lead, 
        #     a_tag, 
        #     a_title, 
        #     a_date, 
        #     a_publisher, 
        #     a_pubname
        # ]
    
        if not all(inputs): 
            inputsalert = True
        elif (not(a_doi) and not(a_isxn)): 
            DOI_alert = True 
        elif a_contributing:
                for a_contributing in a_contributing:
                    if a_contributing in a_lead:
                        authoralert = True
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
                
            if mode == "add": 
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
                
                if type(a_lead) == int: 
                    a_lead = [a_lead]

                if a_contributing == None: 
                    a_contributing = []
                if type(a_contributing) == int: 
                    a_contributing = [a_contributing] 
                
                # form_a_author_combined = a_lead + a_contributing

                #LEAD AUTHOR ADD

                for i in range(len(a_lead)): 
                    sql_pub_lead = """INSERT INTO pub_lead_authors(
                        pub_id, 
                        a_lead_id
                    )
                    VALUES (%s, %s)
                    """
                    val_pub_lead = [sql_pub_max, a_lead[i]]
                    db.modifydatabase(sql_pub_lead, val_pub_lead)

                    sql_pub_lead_upd = """UPDATE pub_lead_authors
                        SET
                        lead_author_name = (SELECT author_fn || ' ' || author_ln FROM authors WHERE a_lead_id=author_id)
                        WHERE a_lead_id > 0;
                    """
                    val_pub_lead_upd = []
                    db.modifydatabase(sql_pub_lead_upd, val_pub_lead_upd)

                #     form_a_sqlcode_upd_publications = """UPDATE publications
                #         SET
                #         user_id = (SELECT author_user_id FROM authors WHERE author_user_id=user_id)
                #         WHERE pub_id > 0;
                # """ 
                #     form_a_values_updpub = []
                #     db.modifydatabase(form_a_sqlcode_upd_publications, form_a_values_updpub)

                    form_a_sqlcode_add_authorships_l = """INSERT INTO authorships(
                        pub_id, 
                        a_lead_id,
                        a_date, 
                        a_year, 
                        a_publisher, 
                        a_pub_name, 
                        a_doi, 
                        a_isxn, 
                        a_scopus 
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    str_to_date = datetime.strptime(a_date, '%Y-%m-%d').date()
                    a_year = str_to_date.year

                    form_a_values_addauthorship_l = [sql_pub_max, a_lead[i], a_date, a_year, a_publisher, a_pubname, a_doi, a_isxn, a_scopus]
                    db.modifydatabase(form_a_sqlcode_add_authorships_l, form_a_values_addauthorship_l)
                    
#                     sql_check = """select publications.pub_id, authors.author_user_id, publications.user_id
# from authors, publications
# where authors.author_user_id = publications.user_id and publications.tag_id <=7
# order by pub_id"""
#                     form_a_sqlcode_upd_publications = """UPDATE publications
#                         SET
#                         user_id = (select author_user_id
#                             from authors
#                             where author_id in (select publications.pub_id
#                                 from authorships
#                                 inner join publications on authorships.pub_id = publications.pub_id)
#                                 where publications.pub_id = authorships.pub_id))
#                         WHERE pub_id > 0;
#                 """ 
#                     form_a_values_updpub = []
#                     db.modifydatabase(form_a_sqlcode_upd_publications, form_a_values_updpub)

                # CONTRIBUTING AUTHOR ADD

                for i in range(len(a_contributing)): 
                    sql_pub_contributing = """INSERT INTO pub_contributing_authors(
                        pub_id, 
                        a_contributing_id
                    )
                    VALUES (%s, %s)
                    """
                    val_pub_contributing = [sql_pub_max, a_contributing[i]]
                    db.modifydatabase(sql_pub_contributing, val_pub_contributing)

                    sql_pub_contributing_upd = """UPDATE pub_contributing_authors
                        SET
                        contributing_author_name = (SELECT author_fn || ' ' || author_ln FROM authors WHERE a_contributing_id=author_id)
                        WHERE a_contributing_id > 0;
                    """
                    val_pub_contributing_upd = []
                    db.modifydatabase(sql_pub_contributing_upd, val_pub_contributing_upd)

                    form_a_sqlcode_add_authorships_c = """INSERT INTO authorships(
                        pub_id, 
                        a_contributing_id,
                        a_date, 
                        a_year, 
                        a_publisher, 
                        a_pub_name, 
                        a_doi, 
                        a_isxn, 
                        a_scopus 
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    str_to_date = datetime.strptime(a_date, '%Y-%m-%d').date()
                    a_year = str_to_date.year

                    form_a_values_addauthorship_c = [sql_pub_max, a_contributing[i], a_date, a_year, a_publisher, a_pubname, a_doi, a_isxn, a_scopus]
                    db.modifydatabase(form_a_sqlcode_add_authorships_c, form_a_values_addauthorship_c)


                # #LEAD AND CONTRIBUTING AUTHOR ADD
                
                # for i in range(len(form_a_author_combined)): 
                #     sql_pub_author_l = """INSERT INTO pub_lead_authors(
                #                 pub_id, 
                #                 a_lead_id
                #             )
                #             VALUES (%s, %s)
                #             """
                #     val_pub_author_l = [sql_pub_max, a_lead[i]]
                #     db.modifydatabase(sql_pub_author_l, val_pub_author_l)

                #     sql_pub_author_c = """
                #             INSERT INTO pub_contributing_authors(
                #                 pub_id, 
                #                 a_contributing_id
                #             )
                #             VALUES (%s, %s)
                #             """
                #     val_pub_author_c = [sql_pub_max, a_contributing[i]]
                #     db.modifydatabase(sql_pub_author_c, val_pub_author_c)

                #     sql_pub_author_upd_l ="""update pub_lead_authors
                #             set
                #             lead_author_name = (select author_fn || ' ' || author_ln from authors where a_lead_id=author_id)
                #             where a_lead_id>0;
                #         """
                #     val_pub_author_upd_l =[]
                #     db.modifydatabase(sql_pub_author_upd_l, val_pub_author_upd_l)

                #     sql_pub_author_upd_c ="""
                #         update pub_contributing_authors
                #             set
                #             contributing_author_name = (select author_fn || ' ' || author_ln from authors where a_contributing_id=author_id)
                #             where a_contributing_id>0;
                #         """
                #     val_pub_author_upd_c =[]
                #     db.modifydatabase(sql_pub_author_upd_c, val_pub_author_upd_c)
                        
                #     form_a_sqlcode_add_authorships_author_l = """INSERT INTO authorships(
                #             pub_id, 
                #             a_lead_id,
                #             a_date, 
                #             a_year, 
                #             a_publisher, 
                #             a_pub_name, 
                #             a_doi, 
                #             a_isxn, 
                #             a_scopus 
                #         )
                #         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                #         """
                #     str_to_date = datetime.strptime(a_date, '%Y-%m-%d').date()
                #     a_year = str_to_date.year
                        
                #     form_a_values_addauthorship_author_l = [sql_pub_max, a_lead[i], a_date, a_year, a_publisher, a_pubname, a_doi, a_isxn, a_scopus]
                #     db.modifydatabase(form_a_sqlcode_add_authorships_author_l, form_a_values_addauthorship_author_l)

                #     form_a_sqlcode_add_authorships_author_c = """INSERT INTO authorships(
                #             pub_id, 
                #             a_contributing_id,
                #             a_date, 
                #             a_year, 
                #             a_publisher, 
                #             a_pub_name, 
                #             a_doi, 
                #             a_isxn, 
                #             a_scopus 
                #         )
                #         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                #         """
                #     str_to_date = datetime.strptime(a_date, '%Y-%m-%d').date()
                #     a_year = str_to_date.year
                        
                #     form_a_values_addauthorship_author_c = [sql_pub_max, a_contributing[i], a_date, a_year, a_publisher, a_pubname, a_doi, a_isxn, a_scopus]
                #     db.modifydatabase(form_a_sqlcode_add_authorships_author_c, form_a_values_addauthorship_author_c)


                # # LEAD AND AUTHOR FOR I IN RANGE FOR ALL

                # for i in range(len(form_a_author_combined)):
                #     for i in range(len(a_lead)): 
                #         sql_pub_lead = """INSERT INTO pub_lead_authors(
                #                     pub_id, 
                #                     a_lead_id
                #                 )
                #                 VALUES (%s, %s)
                #                 """
                #         val_pub_lead = [sql_pub_max, a_lead[i]]
                #         db.modifydatabase(sql_pub_lead, val_pub_lead)

                #         sql_pub_lead_upd ="""update pub_lead_authors
                #             set
                #             lead_author_name = (select author_fn || ' ' || author_ln from authors where a_lead_id=author_id)
                #             where a_lead_id>0;
                #             """
                #         val_pub_lead_upd =[]
                #         db.modifydatabase(sql_pub_lead_upd, val_pub_lead_upd)
                            
                #         form_a_sqlcode_add_authorships_l = """INSERT INTO authorships(
                #                 pub_id, 
                #                 a_lead_id,
                #                 a_date, 
                #                 a_year, 
                #                 a_publisher, 
                #                 a_pub_name, 
                #                 a_doi, 
                #                 a_isxn, 
                #                 a_scopus 
                #             )
                #             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                #             """
                #         str_to_date = datetime.strptime(a_date, '%Y-%m-%d').date()
                #         a_year = str_to_date.year
                            
                #         form_a_values_addauthorship_l = [sql_pub_max, a_lead[i], a_date, a_year, a_publisher, a_pubname, a_doi, a_isxn, a_scopus]
                #         db.modifydatabase(form_a_sqlcode_add_authorships_l, form_a_values_addauthorship_l)

                #     for i in range(len(a_contributing)): 
                #         sql_pub_contributing = """INSERT INTO pub_contributing_authors(
                #                     pub_id, 
                #                     a_contributing_id
                #                 )
                #                 VALUES (%s, %s)
                #                 """
                #         val_pub_contributing = [sql_pub_max, a_contributing[i]]
                #         db.modifydatabase(sql_pub_contributing, val_pub_contributing)

                #         sql_pub_contributing_upd ="""update pub_contributing_authors
                #             set
                #             contributing_author_name = (select author_fn || ' ' || author_ln from authors where a_contributing_id=author_id)
                #             where a_contributing_id>0;
                #             """
                #         val_pub_contributing_upd =[]
                #         db.modifydatabase(sql_pub_contributing_upd, val_pub_contributing_upd)
                            
                #         form_a_sqlcode_add_authorships_l = """INSERT INTO authorships(
                #                 pub_id, 
                #                 a_contributing_id,
                #                 a_date, 
                #                 a_year, 
                #                 a_publisher, 
                #                 a_pub_name, 
                #                 a_doi, 
                #                 a_isxn, 
                #                 a_scopus 
                #             )
                #             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                #             """
                #         str_to_date = datetime.strptime(a_date, '%Y-%m-%d').date()
                #         a_year = str_to_date.year
                            
                #         form_a_values_addauthorship_l = [sql_pub_max, a_contributing[i], a_date, a_year, a_publisher, a_pubname, a_doi, a_isxn, a_scopus]
                #         db.modifydatabase(form_a_sqlcode_add_authorships_l, form_a_values_addauthorship_l)

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
                
                #LEAD AUTHOR EDIT

                if a_lead == None: 
                    a_lead = []
                if type(a_lead) == int: 
                        a_lead = [a_lead]
                
                #delete all lead
                sql_delete_lead_a = """DELETE FROM pub_lead_authors
                        WHERE pub_id = %s"""
                val_delete_lead_a =[int(form_a_editmodeid)]
                db.modifydatabase(sql_delete_lead_a, val_delete_lead_a)               
                #re-add pub w updated lead
                for i in range(len(a_lead)):
                    sql_pub_lead = """INSERT INTO pub_lead_authors(pub_id, a_lead_id)
                        VALUES (%s, %s)
                        """
                    pub_lead_values = [int(form_a_editmodeid), a_lead[i]]
                    db.modifydatabase(sql_pub_lead, pub_lead_values) 

                    sql_pub_lead_upd ="""update pub_lead_authors
                        set
                        lead_author_name = (select author_fn || ' ' || author_ln from authors where a_lead_id=author_id)
                        where a_lead_id>0;
                        """
                    val_pub_lead_upd =[]
                    db.modifydatabase(sql_pub_lead_upd, val_pub_lead_upd)

                    sql_update_authorships_l = """ INSERT INTO authorships ( 
                        pub_id,
                        a_lead_id,
                        a_date, 
                        a_year, 
                        a_publisher, 
                        a_pub_name, 
                        a_doi, 
                        a_isxn, 
                        a_scopus
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
                        """
                    str_to_date = datetime.strptime(a_date, '%Y-%m-%d').date()
                    a_year = str_to_date.year
                    values_update_authorships_l = [int(form_a_editmodeid), a_lead[i], a_date, a_year, a_publisher, a_pubname, a_doi, a_isxn, a_scopus]
                    db.modifydatabase(sql_update_authorships_l, values_update_authorships_l)
                
                #CONTRIBUTING AUTHOR EDIT

                if a_contributing == None: 
                    a_contributing = []
                if type(a_contributing) == int: 
                        a_contributing = [a_contributing]

                #delete all contributing
                sql_delete_contributing_a = """DELETE FROM pub_contributing_authors
                        WHERE pub_id = %s"""
                val_delete_contributing_a =[int(form_a_editmodeid)]
                db.modifydatabase(sql_delete_contributing_a, val_delete_contributing_a)               
                #add all new contributing
                for i in range(len(a_contributing)):
                    sql_pub_contributing = """INSERT INTO pub_contributing_authors(pub_id, a_contributing_id)
                        VALUES (%s, %s)
                        """
                    pub_contributing_values = [int(form_a_editmodeid), a_contributing[i]]
                    db.modifydatabase(sql_pub_contributing, pub_contributing_values) 

                    sql_pub_contributing_upd ="""update pub_contributing_authors
                        set
                        contributing_author_name = (select author_fn || ' ' || author_ln from authors where a_contributing_id=author_id)
                        where a_contributing_id>0;
                        """
                    val_pub_contributing_upd =[]
                    db.modifydatabase(sql_pub_contributing_upd, val_pub_contributing_upd)

                    sql_update_authorships_c = """ INSERT INTO authorships ( 
                        pub_id,
                        a_contributing_id,
                        a_date, 
                        a_year, 
                        a_publisher, 
                        a_pub_name, 
                        a_doi, 
                        a_isxn, 
                        a_scopus
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
                        """
                    str_to_date = datetime.strptime(a_date, '%Y-%m-%d').date()
                    a_year = str_to_date.year
                    values_update_authorships_c = [int(form_a_editmodeid), a_contributing[i], a_date, a_year, a_publisher, a_pubname, a_doi, a_isxn, a_scopus]
                    db.modifydatabase(sql_update_authorships_c, values_update_authorships_c)
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
    return [openmodal, feedbackmessage, okay_href, inputsalert, DOI_alert, authoralert]
