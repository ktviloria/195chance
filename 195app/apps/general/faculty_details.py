#for viewing faculty details with button
#all users have access to this page

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
                dcc.Store(id = 'previous2', storage_type='session', data =[]), 
                dcc.Store(id = 'firsttime2', storage_type='session', data = 1)
            ]
        ), 
        html.H2("Faculty Details"), 
        html.Hr(), 
        html.Div('', id = 'modals_fac_details_holder',  style={'display': 'none'}), 
        html.Div(
            dbc.Row(
                [
                    #Faculty picture
                    dbc.Col(
                        html.Img(id='fac_pic', height="200px"),
                        width = {"size": 3, "order": 0, "offset": 1}
                    ),
                    #Faculty details
                    dbc.Col(
                        html.Div(
                            [
                                #Name
                                dbc.Row(
                                    [
                                        dbc.Label ("Name: ", id='facdet_name'),
                                        # dbc.Col(dbc.Label(id='facdet_name1')), 
                                    ]
                                ),
                                #Rank
                                dbc.Row(
                                    [
                                        dbc.Label("Rank: ", id='facdet_rank'),
                                        # html.Div(id='facdet_rank')
                                    ]
                                ),
                                #Birthdate
                                dbc.Row(
                                    [
                                        dbc.Label("Birthdate", id='facdet_bday'),    
                                        # html.Div(id='facdet_bday')
                                    ]
                                    ),
                                #Mail
                                dbc.Row(
                                    [
                                        dbc.Label("Email: ", id='facdet_mail' ),
                                        # html.Div(id='facdet_mail')
                                    ]
                                ),
                                #Contact #
                                # dbc.Row(
                                #     [
                                #         dbc.Label("Contact Number: ", id='facdet_contact'),
                                #         # html.Div(id='facdet_contact')
                                #     ]
                                # ),
                                #Areas of expertise
                                dbc.Row(
                                    [
                                        html.Strong("Areas of Expertise: "),
                                        html.Div(id='facdet_expert1'),
                                        html.Div(id='facdet_expert2'),
                                        html.Div(id='facdet_expert3'),
                                        html.Div(id='facdet_expert4'),
                                        html.Div(id='facdet_expert5')
                                    ]
                                ),
                            ]
                        ),
                        width=8
                    )
                ]
            ),
        ),
        html.Hr(),
        html.Div( 
            [
                dbc.Row(
                    [
                        # tabs
                        dbc.Col(
                            [
                                dbc.Tabs(
                                    [
                                        dbc.Tab(label="Publications", tab_id="tab_a", label_style={"color": "#800000"}, active_tab_style={'font-weight': 'bold'}),
                                        dbc.Tab(label="Presentations", tab_id="tab_p", label_style={"color": "#800000"}, active_tab_style={'font-weight': 'bold'}),
                                        dbc.Tab(label="Projects", tab_id="tab_r", label_style={"color": "#800000"}, active_tab_style={'font-weight': 'bold'}),
                                        dbc.Tab(label="Other Academic Merits", tab_id="tab_o", label_style={"color": "#800000"}, active_tab_style={'font-weight': 'bold'})
                                    ],
                                    id='tabs',
                                    active_tab='tab_a'
                                ),
                            ],
                            width=7
                        ),
                        #date filter
                        dbc.Col(
                            html.Div(
                                [
                                dbc.FormText("Lower Year", style = {"font-style": "italic"}),    
                                dcc.Dropdown(id='facdet_date_filter', clearable=True, searchable=True, placeholder="YYYY"),
                                ]
                            ),
                            className="dash-bootstrap", 
                            style={'min-width': '8%', 'padding-left': '0.5rem', 'padding-right': '0.5rem'}
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                dbc.FormText("Upper Year",style = {"font-style": "italic"}), 
                                dcc.Dropdown(id='facdet_date_filter_upper', clearable=True, searchable=True, placeholder="YYYY"), 
                                ]   
                            ), 
                            className="dash-bootstrap",
                            style={'min-width': '8%', 'padding-left': '0.5rem', 'padding-right': '0.5rem'}
                        ),
                        #search filter
                        dbc.Col(
                            [
                            dbc.FormText("Search criteria, title, or any keyword on the table or modal", style = {"font-style": "italic", "font-size":"12px"}),
                            dbc.Input(type="text", id="facdet_filter", placeholder="Enter Keyword"),
                            ], style={'min-width': '22%', 'padding-left': '0.5rem', 'padding-right': '0.5rem'}
                        ), 
                    ]
                ),
                html.Hr(),
                html.Div(id='pubsumm')
            ],
        ),
    ] 
) 

#date filter dropdowns
@app.callback(
    [
        Output('facdet_date_filter', 'options'),
        Output('facdet_date_filter_upper', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('tabs', 'active_tab'),
        Input('facdet_date_filter', 'value'),
    ]
)
def facdet_loaddropdown (pathname, tab, initial_date):
    if pathname == '/faculty_details':
        if tab == 'tab_a':
            facdet_sql_date_filter = """SELECT DISTINCT (a_year) as label, (a_year) as value
                                from authorships"""
        elif tab == 'tab_p':
            facdet_sql_date_filter = """SELECT DISTINCT (p_year) as label, (p_year) as value
                                from presentations"""
        elif tab == 'tab_r':
            facdet_sql_date_filter = """SELECT DISTINCT (r_year) as label, (r_year) as value
                                from projects"""
        elif tab == 'tab_o':
            facdet_sql_date_filter = """SELECT DISTINCT (o_year) as label, (o_year) as value
                                from others"""
        else:
            raise PreventUpdate
        
        facdet_sql_date_filter += """ ORDER BY value DESC"""
        facdet_values_date_filter = []
        facdet_cols_date_filter = ['label', 'value']
        facdet_date_filter_included = db.querydatafromdatabase(facdet_sql_date_filter, facdet_values_date_filter, facdet_cols_date_filter)
        facdet_date_filter_options = facdet_date_filter_included.to_dict('records')

        if initial_date: 
            if tab == 'tab_a':
                facdet_sql_date_filter_upper = """SELECT DISTINCT (a_year) as label, (a_year) as value
                                from authorships
                                WHERE cast(a_year as int) >=  %s 
                                ORDER BY value DESC"""
            elif tab == 'tab_p':
                facdet_sql_date_filter_upper = """SELECT DISTINCT (p_year) as label, (p_year) as value
                                    from presentations
                                    WHERE cast(p_year as int) >=  %s 
                                    ORDER BY value DESC"""
            elif tab == 'tab_r':
                facdet_sql_date_filter_upper = """SELECT DISTINCT (r_year) as label, (r_year) as value
                                    from projects
                                    WHERE cast(r_year as int) >=  %s 
                                    ORDER BY value DESC"""
            elif tab == 'tab_o':
                facdet_sql_date_filter_upper = """SELECT DISTINCT (o_year) as label, (o_year) as value
                                    from others
                                    WHERE cast(o_year as int) >=  %s 
                                    ORDER BY value DESC"""
                                    
            facdet_values_filter_upper = [initial_date]
            facdet_cols_date_filter_upper = ['label', 'value']
            
            facdet_date_filter_included_upper = db.querydatafromdatabase(facdet_sql_date_filter_upper, facdet_values_filter_upper, facdet_cols_date_filter_upper)
            facdet_date_filter_options_upper = facdet_date_filter_included_upper.to_dict('records')
        else:
            facdet_date_filter_options_upper = facdet_date_filter_options
    else:
        raise PreventUpdate
    
    return [facdet_date_filter_options, facdet_date_filter_options_upper]    

#details of chosen faculty member
@app.callback( 
        [ 
            Output('fac_pic', 'src'),
            Output('facdet_name', 'children'),
            Output('facdet_rank', 'children'),
            Output('facdet_bday', 'children'),
            Output('facdet_mail', 'children'),
            Output('facdet_expert1', 'children'),
            Output('facdet_expert2', 'children'), 
            Output('facdet_expert3', 'children'), 
            Output('facdet_expert4', 'children'), 
            Output('facdet_expert5', 'children'), 
        ], 
        [ 
            Input('url', 'pathname') 
        ],
        [ 
            State('url', 'search')
        ] 
)

def facdetails_load(pathname, search): 
    if pathname == '/faculty_details': 
        sql = """SELECT
                faculty.user_id,
                faculty_fn || ' ' || faculty_ln AS faculty_full_name,
                rank_title,
                faculty_bdate,
                faculty_mail,
                faculty_expert1,
                faculty_expert2,  
                faculty_expert3,  
                faculty_expert4, 
                faculty_expert5
            FROM faculty
                INNER JOIN ranks ON faculty.rank_id = ranks.rank_id
                INNER JOIN users on faculty.user_id = users.user_id
            WHERE
                faculty_delete_ind = false AND faculty.user_id = %s 
            """
        parsed = urlparse(search)
        facdetid = parse_qs(parsed.query)['id'][0]
        values = [facdetid]
        cols = ['userID', 'Full Name', 'Rank', 'Birthdate', 'Mail', 'Expertise 1', 'Expertise 2', 'Expertise 3', 'Expertise 4', 'Expertise 5' ] 
        faculty = db.querydatafromdatabase(sql, values, cols)

        
        userID = faculty['userID'][0]
        fullname_h = " %s" % (faculty['Full Name'][0] or " ")
        fullname = [
            html.Div([
                html.Strong("Name: "),
                html.Span(f"{fullname_h}"), 
                ]
            ),
        ]
        rank_h = " %s" % (faculty['Rank'][0] or " ")
        rank = [
            html.Div([
                html.Strong("Rank: "),
                html.Span(f"{rank_h}"), 
                ]
            ),
        ]
        birthdate_h = " %s" % (faculty['Birthdate'][0] or " ")
        birthdate =  [
            html.Div([
                html.Strong("Birthdate: "),
                html.Span(f"{birthdate_h}"), 
                ]
            ),
        ]
        mail_h = " %s" % (faculty['Mail'][0] or " ")
        mail = [
            html.Div([
                html.Strong("Email: "),
                html.Span(f"{mail_h}"), 
                ]
            ),
        ]
        expertise1= faculty['Expertise 1'][0]
        expertise2= faculty['Expertise 2'][0]
        expertise3= faculty['Expertise 3'][0]
        expertise4= faculty['Expertise 4'][0]
        expertise5= faculty['Expertise 5'][0]
        fac_pic = app.get_asset_url(f"{facdetid}.png")
            
            
            
        
    else:
        raise PreventUpdate
    return [fac_pic, fullname, rank, birthdate, mail, expertise1, expertise2, expertise3, expertise4, expertise5]
        

#publications summary of chosen faculty member
@app.callback(
    [
        Output('pubsumm', 'children'), 
        Output('modals_fac_details_holder', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('tabs', 'active_tab'),
        Input('facdet_filter', 'value'),
        Input('facdet_date_filter', 'value'),
        Input('facdet_date_filter_upper', 'value')
    ],
    [ 
        State('url', 'search')
    ] 
)

def facdet_loadpublist (pathname, tab, searchterm, datefilter, datefilter_u, search):
    if pathname == '/faculty_details':
        #authorships
        if tab == 'tab_a':
            sql_a = """SELECT 
                authorships.a_year,
                publications.pub_id,
				string_agg(
				  CASE
					WHEN authorship_role.a_label IS NULL THEN faculty_fn || ' ' || faculty_ln
					ELSE faculty_fn || ' ' || faculty_ln || ' (' || authorship_role.a_label ||') '
				  END,
				  ', '
				) AS combined_values,
                tags.tag_short_title,
                pub_title, 
                a_authors, 
                To_char(a_date, 'Month YYYY'),
                a_pub_name, 
                a_publisher, 
                a_doi, 
                a_isxn, 
                a_scopus, 
                authorship_subcategory.a_author_subcat_label,
                to_char(publications.pub_last_upd::timestamp, 'Month DD YYYY HH24:MI:SS') as timestampz,
                publications.modified_by, 
                string_agg(CAST(faculty.user_ID as varchar),  ', ')
                

                FROM authorships_users
                INNER JOIN authorships on authorships_users.pub_id = authorships.pub_id
                LEFT OUTER JOIN faculty on authorships_users.user_id = faculty.user_id
                INNER JOIN publications on authorships_users.pub_id = publications.pub_id
                LEFT OUTER JOIN authorship_role on authorships_users.authorship_role = authorship_role.a_label_id
                LEFT OUTER JOIN tags on publications.tag_id = tags.tag_id
                LEFT OUTER JOIN authorship_subcategory on authorships.authorship_subcategory = authorship_subcategory.a_author_subcat_id
                WHERE publications.pub_delete_ind = false

            
            """
                            #  AND faculty.user_ID = %s
            parsed = urlparse(search)
            facdetid = parse_qs(parsed.query)['id'][0]
            # values_a = [f"{facdetid}"]
            values_a = []
            cols_a = ['Year','id', 'Faculty Involved', 'Publication Criteria', 'Title', 'All Authors',  'Date', 'Publication', 'Publisher', 'DOI','ISXN', 'Scopus',  'Involvement2', 'Last Updated', 'Last Modified By' , 'author_ids']            
            #fix additivity of searchterms and filters
            if datefilter:
                sql_a += """AND (cast (a_year as int) >= %s)"""
                values_a += [datefilter]
                if datefilter_u:
                    sql_a += """AND (cast (a_year as int) <= %s)"""
                    values_a += [datefilter_u]
                    if searchterm:
                        sql_a += """ AND (
                            ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) OR (a_year ILIKE %s)
                            OR (a_authors ILIKE %s) OR (a_pub_name ILIKE %s) OR ((To_char(a_date, 'Month YYYY')) ILIKE %s)
                            OR (a_publisher ILIKE %s) OR (a_doi ILIKE %s) OR (a_isxn ILIKE %s) OR (a_scopus ILIKE %s) OR (tag_short_title ILIKE %s)
                            OR (authorship_role.a_label ILIKE %s))"""
                        values_a += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
                if searchterm:
                    sql_a += """ AND (
                        ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) OR (a_year ILIKE %s)
                        OR (a_authors ILIKE %s) OR (a_pub_name ILIKE %s) OR ((To_char(a_date, 'Month YYYY')) ILIKE %s)
                        OR (a_publisher ILIKE %s) OR (a_doi ILIKE %s) OR (a_isxn ILIKE %s) OR (a_scopus ILIKE %s) OR (tag_short_title ILIKE %s)
                        OR (authorship_role.a_label ILIKE %s))"""
                    values_a += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                            f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                            f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
                    if datefilter_u:
                        sql_a += """AND (cast (a_year as int) <= %s)"""
                        values_a += [datefilter_u]
                else:
                    sql_a += """"""
                    values_a += [] 
                    
            elif datefilter_u: 
                sql_a += """AND (cast (a_year as int) <= %s)"""
                values_a += [datefilter_u]
                if datefilter:
                    sql_a += """AND (cast (a_year as int) >= %s)"""
                    values_a += [datefilter]
                    if searchterm:
                        sql_a += """ AND (
                            ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) OR (a_year ILIKE %s)
                            OR (a_authors ILIKE %s) OR (a_pub_name ILIKE %s) OR ((To_char(a_date, 'Month YYYY')) ILIKE %s)
                            OR (a_publisher ILIKE %s) OR (a_doi ILIKE %s) OR (a_isxn ILIKE %s) OR (a_scopus ILIKE %s) OR (tag_short_title ILIKE %s)
                            OR (authorship_role.a_label ILIKE %s))"""
                        values_a += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
                if searchterm:
                    sql_a += """ AND (
                        ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) OR (a_year ILIKE %s)
                        OR (a_authors ILIKE %s) OR (a_pub_name ILIKE %s) OR ((To_char(a_date, 'Month YYYY')) ILIKE %s)
                        OR (a_publisher ILIKE %s) OR (a_doi ILIKE %s) OR (a_isxn ILIKE %s) OR (a_scopus ILIKE %s) OR (tag_short_title ILIKE %s)
                        OR (authorship_role.a_label ILIKE %s))"""
                    values_a += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                            f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                            f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
                    if datefilter:
                        sql_a += """AND (cast (a_year as int) >= %s)"""
                        values_a += [datefilter]
                else:
                    sql_a += """"""
                    values_a += [] 
            
            elif searchterm:
                sql_a += """ AND (
                    ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) OR (a_year ILIKE %s)
                    OR (a_authors ILIKE %s) OR (a_pub_name ILIKE %s) OR ((To_char(a_date, 'Month YYYY')) ILIKE %s)
                    OR (a_publisher ILIKE %s) OR (a_doi ILIKE %s) OR (a_isxn ILIKE %s) OR (a_scopus ILIKE %s) OR (tag_short_title ILIKE %s)
                    OR (authorship_role.a_label ILIKE %s))"""
                values_a += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                        f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                        f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
                if datefilter:
                    sql_a += """AND (cast (a_year as int) >= %s)"""
                    values_a += [datefilter]
                    if datefilter_u:
                        sql_a += """AND (cast (a_year as int) <= %s)"""
                        values_a += [datefilter_u]
                elif datefilter_u:
                    sql_a += """AND (cast (a_year as int) <= %s)"""
                    values_a += [datefilter_u]
                    if datefilter:
                        sql_a += """AND (cast (a_year as int) >= %s)"""
                        values_a += [datefilter]
                else:
                    sql_a += """"""
                    values_a += []     
            else:
                sql_a += """"""
                values_a += []
            
            sql_a += """GROUP BY publications.pub_id, authorships.a_year, tags.tag_short_title, authorship_subcategory.a_author_subcat_label,
                a_authors, To_char(a_date, 'Month YYYY'),a_pub_name, a_publisher, 
                a_doi, a_isxn, a_scopus, publications.modified_by, to_char(publications.pub_last_upd::timestamp, 'Month DD YYYY HH24:MI:SS')
            ORDER BY authorships.a_year DESC"""
            pub_a = db.querydatafromdatabase(sql_a, values_a, cols_a)
            
            
            modals_a = []
            if pub_a.shape[0]: 
                buttons_a = [] 
                # pub_details = []
                # other_info = []
                
                
                #modal button generation
                for ids in pub_a['id']: 
                    buttons_a += [
                        html.Div(
                            # dbc.Button('View', id = f"modal_button_{ids}", href=f"/publication_details_a?mode=view&id={ids}", size='sm', color='primary', ), 
                            dbc.Button('View', id = f"modal_button_fac_{ids}", size='sm', color='danger', ), 
                            style={'text-align': 'center'} 
                        ) 
                    ]
                pub_a['More Details'] = buttons_a 
                #modal content
                for i in range(len(pub_a)): 
                    ids = pub_a['id'][i]
                    pub_title = pub_a['Title'][i]
                    pub_faculty_assoc = pub_a['Faculty Involved'][i]
                    pub_category = pub_a['Publication Criteria'][i]
                    pub_authors = pub_a['All Authors'][i]
                    # pub_involvement = pub_a['Involvement'][i]
                    pub_involvement2 = pub_a['Involvement2'][i]
                    pub_date = pub_a['Date'][i]
                    pub_publication = pub_a['Publication'][i]
                    pub_publisher = pub_a['Publisher'][i]
                    pub_DOI = pub_a['DOI'][i]
                    pub_ISXN = pub_a['ISXN'][i]
                    pub_Scopus = pub_a['Scopus'][i]
                    
                    modals_a += [
                        html.Div(
                            dbc.Modal(
                                [
                                    dbc.ModalHeader(dbc.ModalTitle("Record Details"), style=mod_style), 
                                    dbc.ModalBody([
                                        html.Div([
                                            html.Strong("Title: "),
                                            html.Span(f"{pub_title}"), ], id = f"modal_title_{ids}"
                                        ),
                                        html.Div([
                                            html.Strong("Faculty Involved: "),  
                                            html.Span(f"{pub_faculty_assoc}"),], id = f"modal_pub_faculty_{ids}"
                                        ),       
                                        html.Div([
                                            html.Strong("Publication Category: "), 
                                            html.Span(f"{pub_category}"),], id = f"modal_pub_category_{ids}"
                                        ), 
                                        html.Div([
                                            html.Strong("Authors: "),
                                            html.Span(f"{pub_authors}"),], id = f"modal_authors_{ids}"),
                                        html.Div([
                                            html.Strong("With Other UP Faculty: "), 
                                            html.Span(f"{pub_involvement2}"),], id = f"modal_involvement_{ids}"),
                                        html.Div([
                                            html.Strong("Date of Publication: "), 
                                            html.Span(f"{pub_date}"),], id = f"modal_date_{ids}"),
                                        html.Div([
                                            html.Strong("Publication: "),
                                            html.Span(f"{pub_publication}"),], id = f"modal_publication_{ids}"),
                                        html.Div([
                                            html.Strong("Publishing House: "),
                                            html.Span(f"{pub_publisher}"),], id = f"modal_publisher_{ids}"),
                                        html.Div([
                                            html.Strong("DOI: "),
                                            html.Span(f"{pub_DOI}"),], id = f"modal_DOI_{ids}"),
                                        html.Div([
                                            html.Strong("ISXN: "), 
                                            html.Span(f"{pub_ISXN}"),], id = f"modal_ISXN_{ids}"),
                                        html.Div([
                                            html.Strong("Scopus: "), 
                                            html.Span(f"{pub_Scopus}"),], id = f"modal_scopus_{ids}"), 
                                    ],), 
                                    # dbc.ModalFooter(
                                    #     dbc.Button("Close", id= f'modal_close_{ids}', n_clicks = 0)
                                    # )
                                ], 
                                id = f"modal_a_fac_{ids}", size ='lg',
                                centered=True, is_open = False
                            ),  id= f'div_modal_fac_{ids}', style={'display': 'none'}
                        )
                    ]

                #publication details content
                # for i in range(len(pub_a)): 
                #     inputs_1 = [pub_a['Date'][i], pub_a['Publication'][i], pub_a['Publisher'][i]]
                #     if not all (inputs_1) :  
                #         pub_details += " "
                #     else: 
                #         pub_details += [("Published in/on: %s in %s by %s" % (pub_a['Date'][i], pub_a['Publication'][i], pub_a['Publisher'][i]))] 
                #     # inputs_2 = [pub_a['DOI'][i], pub_a['ISXN'][i], pub_a['Scopus'][i]]
                #     # if not all (inputs_2): 
                #     #     other_info += " "
                #     # else: 
                #     other_info += [("DOI: %s \n Issue Number: %s \n Scopus: %s"  % (pub_a['DOI'][i], pub_a['ISXN'][i], pub_a['Scopus'][i]) or " " )]

                # pub_a['Publication Details'] = pub_details
                # pub_a['Other Information'] = other_info
                
            
            
            for j in range(len(pub_a['author_ids'])):
                # print(list(((pub_a)['author_ids'][i])))
                string = pub_a['author_ids'][j]
                listed = string.split(', ')
                if facdetid not in listed: 
                    pub_a = pub_a.drop(j)
                else: 
                    pass
            
            pub_a.drop(['Last Updated'],axis=1,inplace=True)     
            pub_a.drop(['Last Modified By'],axis=1,inplace=True)     
            pub_a.drop(['author_ids'],axis=1,inplace=True) 
            pub_a.drop(['Faculty Involved'],axis=1,inplace=True)
            pub_a.drop(['id'],axis=1,inplace=True)
            pub_a.drop(['Date'],axis=1,inplace=True)
            pub_a.drop(['Publication'],axis=1,inplace=True)
            pub_a.drop(['Publisher'],axis=1,inplace=True)
            pub_a.drop(['DOI'],axis=1,inplace=True)
            pub_a.drop(['ISXN'],axis=1,inplace=True)
            pub_a.drop(['Scopus'],axis=1,inplace=True)
            pub_a.drop(['Involvement2'],axis=1,inplace=True)
            
            if pub_a.shape[0]:
                table_a = dbc.Table.from_dataframe(pub_a, striped=True, bordered=True, hover=True, size='sm', style={"whiteSpace": "pre-line"}) 
            else:
                table_a = "No records to display"
            return [table_a, modals_a] 

        #presentations
        elif tab == 'tab_p':
            sql_p = """SELECT
                presentations.p_year,
                publications.pub_id,
				string_agg(
				  CASE
					WHEN presentations_users.pres_role IS NULL THEN faculty_fn || ' ' || faculty_ln
					ELSE faculty_fn || ' ' || faculty_ln || ' (' || presentations_users.pres_role ||') '
				  END,
				  ', '
				) AS combined_values,
                tags.tag_short_title,
                pub_title,
                p_authors,
                to_char(p_start_date, 'Month DD, YYYY'), 
                to_char(p_end_date, 'Month  DD, YYYY'), 
                p_conf, 
                p_loc, 
                p_add_info, 
                string_agg(CAST(faculty.user_ID as varchar),  ', ')
            FROM presentations_users
				INNER JOIN presentations on presentations_users.pub_id = presentations.pub_id
                LEFT OUTER JOIN faculty on presentations_users.user_id = faculty.user_id
				INNER JOIN publications on presentations_users.pub_id = publications.pub_id
                INNER JOIN tags on publications.tag_id = tags.tag_id
            WHERE
                pub_delete_ind = false
            """
            parsed = urlparse(search)
            facdetid = parse_qs(parsed.query)['id'][0]
            values_p = []
            cols_p = ['Year', 'id', 'Faculty Involved', 'Criteria', 'Title', 'All Authors', 'Start Date', 'End Date', 'Conference',
                      'Location', 'Other Info', 'presenters_ids'] 
            
            if datefilter:
                sql_p += """AND (cast (p_year as int) >= %s)"""
                values_p += [datefilter]
                if datefilter_u:
                    sql_p += """AND (cast (p_year as int) <= %s)"""
                    values_p += [datefilter_u]
                    if searchterm:
                        sql_p += """ AND (
                            ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                            OR (p_authors ILIKE %s) OR (p_year ILIKE %s) OR (p_conf ILIKE %s)
                            OR (p_loc ILIKE %s) OR (p_add_info ILIKE %s) OR (tag_short_title ILIKE %s)
                            OR (to_char(p_start_date, 'Month DD, YYYY') ILIKE %s) OR (to_char(p_end_date, 'Month DD, YYYY')ILIKE %s)
                            OR (presentations_users.pres_role ILIKE %s))"""
                        values_p += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                                f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%",f"%{searchterm}%"]
                if searchterm:
                    sql_p += """ AND (
                        ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                        OR (p_authors ILIKE %s) OR (p_year ILIKE %s) OR (p_conf ILIKE %s)
                        OR (p_loc ILIKE %s) OR (p_add_info ILIKE %s) OR (tag_short_title ILIKE %s)
                        OR (to_char(p_start_date, 'Month DD, YYYY') ILIKE %s) OR (to_char(p_end_date, 'Month DD, YYYY')ILIKE %s)
                        OR (presentations_users.pres_role ILIKE %s))"""
                    values_p += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                            f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                            f"%{searchterm}%", f"%{searchterm}%",f"%{searchterm}%"]
                    if datefilter_u:
                        sql_p += """AND (cast (p_year as int) <= %s)"""
                        values_p += [datefilter_u]
                else:
                    sql_p += """"""
                    values_p += [] 
            
            elif datefilter_u: 
                sql_p += """AND (cast (p_year as int) <= %s)"""
                values_p += [datefilter_u]
                if datefilter:
                    sql_p += """AND (cast (p_year as int) >= %s)"""
                    values_p += [datefilter]
                    if searchterm:
                        sql_p += """ AND (
                            ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                            OR (p_authors ILIKE %s) OR (p_year ILIKE %s) OR (p_conf ILIKE %s)
                            OR (p_loc ILIKE %s) OR (p_add_info ILIKE %s) OR (tag_short_title ILIKE %s)
                            OR (to_char(p_start_date, 'Month DD, YYYY') ILIKE %s) OR (to_char(p_end_date, 'Month DD, YYYY')ILIKE %s)
                            OR (presentations_users.pres_role ILIKE %s))"""
                        values_p += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                                f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%",f"%{searchterm}%"]
                if searchterm:
                    sql_p += """ AND (
                        ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                        OR (p_authors ILIKE %s) OR (p_year ILIKE %s) OR (p_conf ILIKE %s)
                        OR (p_loc ILIKE %s) OR (p_add_info ILIKE %s) OR (tag_short_title ILIKE %s)
                        OR (to_char(p_start_date, 'Month DD, YYYY') ILIKE %s) OR (to_char(p_end_date, 'Month DD, YYYY')ILIKE %s)
                        OR (presentations_users.pres_role ILIKE %s))"""
                    values_p += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                            f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                            f"%{searchterm}%", f"%{searchterm}%",f"%{searchterm}%"]
                    if datefilter:
                        sql_p += """AND (cast (p_year as int) >= %s)"""
                        values_p += [datefilter]
                        
                else:
                    sql_p += """"""
                    values_p += [] 
            
            elif searchterm:
                sql_p += """ AND (
                    ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                    OR (p_authors ILIKE %s) OR (p_year ILIKE %s) OR (p_conf ILIKE %s)
                    OR (p_loc ILIKE %s) OR (p_add_info ILIKE %s) OR (tag_short_title ILIKE %s)
                    OR (to_char(p_start_date, 'Month DD, YYYY') ILIKE %s) OR (to_char(p_end_date, 'Month DD, YYYY')ILIKE %s)
                    OR (presentations_users.pres_role ILIKE %s))"""
                values_p += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                        f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                        f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
                if datefilter:
                    sql_p += """AND (cast (p_year as int) >= %s)"""
                    values_p += [datefilter]
                    if datefilter_u:
                        sql_p += """AND (cast (p_year as int) <= %s)"""
                        values_p += [datefilter_u]
                if datefilter_u:
                        sql_p += """AND (cast (p_year as int) <= %s)"""
                        values_p += [datefilter_u]
                        if datefilter:
                            sql_p += """AND (cast (p_year as int) >= %s)"""
                            values_p += [datefilter]
                else:
                    sql_p += """"""
                    values_p += []     
            else:
                sql_p += """"""
                values_p += []

            sql_p += """GROUP BY p_year, publications.pub_id, tags.tag_short_title, pub_title, p_authors, to_char(p_start_date, 'Month DD, YYYY'), 
                to_char(p_end_date, 'Month  DD, YYYY'), p_conf, p_loc, p_add_info
            ORDER BY presentations.p_year DESC"""
            pub_p = db.querydatafromdatabase(sql_p, values_p, cols_p)
            
            modals_p = []
            if pub_p.shape[0]:
                buttons_p = [] 
                # pres_details = []
                # other_details = []
                
                
                #modal button generation
                for id in pub_p['id']: 
                    buttons_p += [
                        html.Div(
                            dbc.Button('View', id = f"modal_button_fac_{id}", size='sm', color='danger', ), 
                            style={'text-align': 'center'} 
                        ) 
                    ]
                pub_p['More Details'] = buttons_p
                
                #modal content
                for i in range(len(pub_p)): 
                    ids = pub_p['id'][i]
                    pub_title = pub_p['Title'][i]
                    pres_fac = pub_p['Faculty Involved'][i]
                    pres_category = pub_p['Criteria'][i]
                    pres_conf = pub_p['Conference'][i]
                    pres_start = pub_p['Start Date'][i]
                    pres_end = pub_p['End Date'][i]
                    pres_loc = pub_p['Location'][i]
                    pres_other = pub_p['Other Info'][i]
                    
                    modals_p += [
                        html.Div(
                            dbc.Modal(
                                [
                                    dbc.ModalHeader(dbc.ModalTitle("Record Details"), style=mod_style), 
                                    dbc.ModalBody([
                                        html.Div([
                                            html.Strong("Title: "), 
                                            html.Span(f"{pub_title}"),],id = f"modal_title_{ids}"),
                                        html.Div([
                                            html.Strong("Faculty Involved: "), 
                                            html.Span(f"{pres_fac}"),], id = f"modal_pres_fac_{ids}"),
                                        html.Div([
                                            html.Strong("Presentation Category: "), 
                                            html.Span(f"{pres_category}"),],  id = f"modal_pres_cat_{ids}"),
                                        html.Div([
                                            html.Strong("Conference: "), 
                                            html.Span(f"{pres_conf}"),], id = f"modal_pres_conf_{ids}"),
                                        html.Div([
                                            html.Strong("Presentation Date: "),
                                            html.Span(f"{pres_start} to {pres_end}"),], id = f"modal_pres_date_{ids}"),
                                        html.Div([
                                            html.Strong("Presentation Location: "),
                                            html.Span(f"{pres_loc}"),], id = f"modal_pres_loc_{ids}"),
                                        html.Div([
                                            html.Strong("Additional Information: "), 
                                            html.Span(f"{pres_other}"),], id = f"modal_pres_other_{ids}")
                                    ],), 
                                    # dbc.ModalFooter(
                                    #     dbc.Button("Close", id= f'modal_close_{ids}', n_clicks = 0)
                                    # )
                                ], 
                                id = f"modal_a_fac_{ids}", size ='lg',
                                centered=True, is_open = False
                            ),  id= f'div_modal_fac_{ids}', style={'display': 'none'}
                        )
                    ]
                
                #publication details content
                # for i in range(len(pub_p)): 
                #     pres_details += [("Presented from: %s to %s \n Presented at: %s (%s)" % (pub_p['Start Date'][i], pub_p['End Date'][i], pub_p['Conference'][i], pub_p['Location'][i]) or "No Details Provided")]
                #     other_details += [pub_p['Other Info'][i]]
            
                
                # pub_p['Presentation Details'] = pres_details
                # pub_p['Additional Info'] = other_details
                
                
            for j in range(len(pub_p['presenters_ids'])):
                string = pub_p['presenters_ids'][j]
                listed = string.split(', ')
                if facdetid not in listed: 
                    pub_p = pub_p.drop(j)
                else: 
                    pass
                
            pub_p.drop(['id'],axis=1,inplace=True)  
            pub_p.drop(['presenters_ids'],axis=1,inplace=True)    
            pub_p.drop(['Start Date'],axis=1,inplace=True)
            pub_p.drop(['End Date'],axis=1,inplace=True)
            pub_p.drop(['Conference'],axis=1,inplace=True)
            pub_p.drop(['Location'],axis=1,inplace=True)
            pub_p.drop(['Other Info'],axis=1,inplace=True)
            
            if pub_p.shape[0]:
                table_p = dbc.Table.from_dataframe(pub_p, striped=True, bordered=True, hover=True, size='sm', style={"whiteSpace": "pre-line"}) 
            else:
                table_p = "No records to display"
            return [table_p, modals_p]  
    
        #projects
        elif tab == 'tab_r':
            sql_r = """SELECT
                r_year,
                publications.pub_id,
                string_agg(
                    CASE
                    WHEN projects_users.r_roles IS NULL THEN faculty_fn || ' ' || faculty_ln
                    ELSE faculty_fn || ' ' || faculty_ln || ' (' || projects_users.r_roles ||') '
                END,
                ', '
                ) AS combined_values,
                tag_short_title,
                pub_title,
                r_timeframe, 
                to_char(r_start_date, 'Month DD YYYY'),
                to_char(r_end_date, 'Month DD YYYY'), 
                r_fund_org, 
                string_agg(
                    CASE
                    WHEN projects_users.r_roles IS NULL THEN faculty_fn || ' ' || faculty_ln
                    ELSE faculty_fn || ' ' || faculty_ln || ' [' || projects_users.r_contract_link ||'] '
                END,
                ', '
                ) AS combined_values, 
                string_agg(CAST(faculty.user_ID as varchar),  ', ')
            FROM projects_users
                INNER JOIN projects on projects_users.pub_id = projects.pub_id
                LEFT OUTER JOIN faculty on projects_users.user_id = faculty.user_id
                INNER JOIN publications on projects_users.pub_id = publications.pub_id
                INNER JOIN tags on publications.tag_id = tags.tag_id
            WHERE
                pub_delete_ind = false

            """
            parsed = urlparse(search)
            facdetid = parse_qs(parsed.query)['id'][0]
            values_r = []
            cols_r = ['Year', 'id', 'Faculty Involved', 'Criteria', 'Title', 'Timeframe', 'Start Date', 'End Date', 'Funding Organization', 'Contract', 'projteam']
            
            if datefilter:
                sql_r += """AND (cast (r_year as int) >= %s)"""
                values_r += [datefilter]
                if datefilter_u:
                    sql_r += """AND (cast (r_year as int) <= %s)"""
                    values_r += [datefilter_u]
                    if searchterm:
                        sql_r += """ AND (
                            (r_year ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                            OR (projects_users.r_roles ILIKE %s) OR (r_timeframe ILIKE %s) OR (r_fund_org ILIKE %s) OR (tag_short_title ILIKE %s)
                            OR ((To_char(r_start_date, 'Month DD, YYYY')) ILIKE %s) OR ((To_char(r_end_date, 'Month DD, YYYY')) ILIKE %s)
                            )"""
                        values_r += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                            f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                            ]  
                if searchterm:
                    sql_r += """ AND (
                        (r_year ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                        OR (projects_users.r_roles ILIKE %s) OR (r_timeframe ILIKE %s) OR (r_fund_org ILIKE %s) OR (tag_short_title ILIKE %s)
                        OR ((To_char(r_start_date, 'Month DD, YYYY')) ILIKE %s) OR ((To_char(r_end_date, 'Month DD, YYYY')) ILIKE %s)
                        )"""
                    values_r += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                        f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                    ]  
                    if datefilter_u:
                        sql_r += """AND (cast (r_year as int) <= %s)"""
                        values_r += [datefilter_u]
                else:
                    sql_r += """"""
                    values_r += [] 
                    
            elif datefilter_u: 
                sql_r += """AND (cast (r_year as int) <= %s)"""
                values_r += [datefilter_u]
                if datefilter:
                    sql_r += """AND (cast (r_year as int) >= %s)"""
                    values_r += [datefilter]
                    if searchterm:
                        sql_r += """ AND (
                            (r_year ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                            OR (projects_users.r_roles ILIKE %s) OR (r_timeframe ILIKE %s) OR (r_fund_org ILIKE %s) OR (tag_short_title ILIKE %s)
                            OR ((To_char(r_start_date, 'Month DD, YYYY')) ILIKE %s) OR ((To_char(r_end_date, 'Month DD, YYYY')) ILIKE %s)
                            )"""
                        values_r += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
                if searchterm:
                    sql_r += """ AND (
                        (r_year ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                        OR (projects_users.r_roles ILIKE %s) OR (r_timeframe ILIKE %s) OR (r_fund_org ILIKE %s) OR (tag_short_title ILIKE %s)
                        OR ((To_char(r_start_date, 'Month DD, YYYY')) ILIKE %s) OR ((To_char(r_end_date, 'Month DD, YYYY')) ILIKE %s)
                        )"""
                    values_r += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                            f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
                    if datefilter:
                        sql_r += """AND (cast (r_year as int) >= %s)"""
                        values_r += [datefilter]

                else:
                    sql_r += """"""
                    values_r += [] 
                    
            elif searchterm:
                sql_r += """ AND (
                        (r_year ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                        OR (projects_users.r_roles ILIKE %s) OR (r_timeframe ILIKE %s) OR (r_fund_org ILIKE %s) OR (tag_short_title ILIKE %s)
                        OR ((To_char(r_start_date, 'Month DD, YYYY')) ILIKE %s) OR ((To_char(r_end_date, 'Month DD, YYYY')) ILIKE %s)
                        )"""
                values_r += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                        f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                        ]  
                if datefilter:
                    sql_r += """AND (cast (r_year as int) >= %s)"""
                    values_r += [datefilter]
                    if datefilter_u:
                        sql_r += """AND (cast (r_year as int) <= %s)"""
                        values_r += [datefilter_u]
                if datefilter_u:
                    sql_r += """AND (cast (r_year as int) <= %s)"""
                    values_r += [datefilter_u]
                    if datefilter:
                        sql_r += """AND (cast (r_year as int) >= %s)"""
                        values_r += [datefilter]
                    
                else:
                    sql_r += """"""
                    values_r += []     
            else:
                sql_r += """"""
                values_r += []   

            sql_r += """GROUP BY r_year, publications.pub_id, tags.tag_short_title, pub_title, r_timeframe, to_char(r_start_date, 'Month DD, YYYY'), 
            to_char(r_end_date, 'Month  DD, YYYY'), r_fund_org, r_end_date, r_start_date
            ORDER BY projects.r_year DESC"""
            pub_r = db.querydatafromdatabase(sql_r, values_r, cols_r)
            
            modals_r = []
            if pub_r.shape[0]:
                buttons_r=[] 
                # proj_details1 = []
                # proj_details2 = [] 
                # proj_details = []
                
                
                #modal button generation
                for id in pub_r['id']: 
                    buttons_r += [
                        html.Div(
                            dbc.Button('View', id = f"modal_button_fac_{id}", size='sm', color='danger', ), 
                            style={'text-align': 'center'} 
                        ) 
                    ]
                
                pub_r['More Details'] = buttons_r
                
                #modal content
                for i in range(len(pub_r)): 
                    ids = pub_r['id'][i]
                    pub_title = pub_r['Title'][i]
                    proj_fac = pub_r['Faculty Involved'][i]
                    proj_tag = pub_r['Criteria'][i]
                    proj_start = pub_r ['Start Date'][i]
                    proj_end = pub_r['End Date'][i]
                    proj_timeframe = pub_r['Timeframe'][i]
                    proj_org = pub_r['Funding Organization'][i]
                    proj_contract = pub_r['Contract'][i]
                    
                    modals_r += [
                        html.Div(
                            dbc.Modal(
                                [
                                    dbc.ModalHeader(dbc.ModalTitle("Record Details"), style=mod_style), 
                                    dbc.ModalBody([
                                        html.Div([
                                            html.Strong("Title: "),
                                            html.Span(f"{pub_title}"),], id = f"modal_title_{ids}"),
                                        html.Div([
                                            html.Strong("Faculty Involved: "), 
                                            html.Span(f"{proj_fac}"),], id = f"modal_proj_fac_{ids}"),
                                        html.Div([
                                            html.Strong("Project Category: "), 
                                            html.Span(f"{proj_tag}"),], id = f"modal_proj_tag_{ids}"),
                                        html.Div([
                                            html.Strong("Project Duration: "), 
                                            html.Span(f"{proj_start} to {proj_end}. Completed in {proj_timeframe}"),], id = f"modal_proj_duration_{ids}"),
                                        html.Div([
                                            html.Strong("Funding Organization: "), 
                                            html.Span(f"{proj_org}"),], id = f"modal_proj_org_{ids}"),
                                        html.Div([
                                            html.Strong("Contract Copy: "), 
                                            html.Span(f"{proj_contract}"),], id = f"modal_proj_contract_{ids}"),
                                    ],), 
                                    # dbc.ModalFooter(
                                    #     dbc.Button("Close", id= f'modal_close_{ids}', n_clicks = 0)
                                    # )
                                ], 
                                id = f"modal_a_fac_{ids}", size ='lg',
                                centered=True, is_open = False
                            ),  id= f'div_modal_fac_{ids}', style={'display': 'none'}
                        )
                    ]

                #publication details content
                # for i in range(len(pub_r)):
                #     if pub_r['Role'][i] == None:
                #         proj_details1 += [" "] 
                #     else:     
                #         proj_details1 += [("Executed project as  %s \n"  % (pub_r['Role'][i])) or " "]
                    
                #     if pub_r['Timeframe'][i] == None:
                #         proj_details2 += [" "] 
                #     else: 
                #         proj_details2 += [("Executed project in %s months from %s to %s" % (pub_r['Timeframe'][i],pub_r['Start Date'][i], pub_r['End Date'][i])) or " "]
                #     proj_details += [proj_details1[i] + proj_details2[i]]
                # pub_r['Project Details'] = proj_details
            for j in range(len(pub_r['projteam'])):
                string = pub_r['projteam'][j]
                listed = string.split(', ')
                if facdetid not in listed: 
                    pub_r = pub_r.drop(j)
                else: 
                    pass    
            
            pub_r.drop(['projteam'],axis=1,inplace=True)
            pub_r.drop(['id'],axis=1,inplace=True)
            pub_r.drop(['Contract'],axis=1,inplace=True)
            pub_r.drop(['Start Date'],axis=1,inplace=True)
            pub_r.drop(['End Date'],axis=1,inplace=True)
            pub_r.drop(['Timeframe'],axis=1,inplace=True)
            pub_r.drop(['Funding Organization'],axis=1,inplace=True)
            
            if pub_r.shape[0]:
                table_r = dbc.Table.from_dataframe(pub_r, striped=True, bordered=True, hover=True, size='sm', style={"whiteSpace": "pre-line"}) 
            else:
                table_r = "No records to display"
            return [table_r, modals_r] 

        #others
        elif tab == 'tab_o':
            sql_o = """SELECT
                    o_year,
                    publications.pub_id,
                    string_agg(
                        CASE
                        WHEN others_users.o_add_info IS NULL THEN faculty_fn || ' ' || faculty_ln
                        ELSE faculty_fn || ' ' || faculty_ln || ' [' || others_users.o_add_info ||'] '
                    END,
                    ', '
                    ) AS combined_values,
                    tags.tag_short_title,
                    pub_title,
                    to_char(o_date, 'Month YYYY'), 
                    string_agg(CAST(faculty.user_ID as varchar),  ', ')
                FROM others_users
                    INNER JOIN others on others_users.pub_id = others.pub_id
                    LEFT OUTER JOIN faculty on others_users.user_id = faculty.user_id
                    INNER JOIN publications on others_users.pub_id = publications.pub_id
                    INNER JOIN tags on publications.tag_id = tags.tag_id  
                WHERE
                    pub_delete_ind = false
                """
            parsed = urlparse(search)
            facdetid = parse_qs(parsed.query)['id'][0]
            values_o = []
            cols_o = ['Year', 'id', 'Faculty Involved', 'Criteria', 'Title', 'Date', 'together'] 

            if datefilter:
                sql_o += """AND (cast (o_year as int) >= %s)"""
                values_o += [datefilter]
                if datefilter_u:
                    sql_o += """AND (cast (o_year as int) <= %s)"""
                    values_o += [datefilter_u]
                    if searchterm:
                        sql_o += """ AND (
                            (o_year ILIKE %s) OR (pub_title ILIKE %s) OR ((To_char(o_date, 'Month DD, YYYY')) ILIKE %s)
                            OR (others_users.o_add_info ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (tag_short_title ILIKE %s)
                            )"""
                        values_o += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                            f"%{searchterm}%",]
                if searchterm:
                    sql_o += """ AND (
                        (o_year ILIKE %s) OR (pub_title ILIKE %s) OR ((To_char(o_date, 'Month DD, YYYY')) ILIKE %s)
                        OR (others_users.o_add_info ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (tag_short_title ILIKE %s)
                        )"""
                    values_o += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                        f"%{searchterm}%",]
                    if datefilter_u:
                        sql_o += """AND (cast (o_year as int) <= %s)"""
                        values_o += [datefilter_u]
                else:
                    sql_o += """"""
                    values_o += [] 
                    
            elif datefilter_u: 
                sql_o += """AND (cast (o_year as int) <= %s)"""
                values_o += [datefilter_u]
                if datefilter: 
                    sql_o += """AND (cast (o_year as int) >= %s)"""
                    values_o += [datefilter]
                    if searchterm:
                        sql_o += """ AND (
                            (o_year ILIKE %s) OR (pub_title ILIKE %s) OR ((To_char(o_date, 'Month DD, YYYY')) ILIKE %s)
                            OR (others_users.o_add_info ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (tag_short_title ILIKE %s)
                            )"""
                        values_o += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                            f"%{searchterm}%",]
                if searchterm:
                    sql_o += """ AND (
                        (o_year ILIKE %s) OR (pub_title ILIKE %s) OR ((To_char(o_date, 'Month DD, YYYY')) ILIKE %s)
                        OR (others_users.o_add_info ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (tag_short_title ILIKE %s)
                        )"""
                    values_o += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                        f"%{searchterm}%",]
                    if datefilter: 
                        sql_o += """AND (cast (o_year as int) >= %s)"""
                        values_o += [datefilter]
                else:
                    sql_o += """"""
                    values_o += [] 
                    
            elif searchterm:
                sql_o += """ AND (
                        (o_year ILIKE %s) OR (pub_title ILIKE %s) OR ((To_char(o_date, 'Month DD, YYYY')) ILIKE %s)
                        OR (others_users.o_add_info ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (tag_short_title ILIKE %s)
                        )"""
                values_o += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                        f"%{searchterm}%",]
                if datefilter:
                    sql_o += """AND (cast (o_year as int) >= %s)"""
                    values_o += [datefilter]
                    if datefilter_u:
                        sql_o += """AND (cast (o_year as int) <= %s)"""
                        values_o += [datefilter_u]
                if datefilter_u:
                    sql_o += """AND (cast (o_year as int) <= %s)"""
                    values_o += [datefilter_u]
                    if datefilter:
                        sql_o += """AND (cast (o_year as int) >= %s)"""
                        values_o += [datefilter]
                    
                else:
                    sql_o += """"""
                    values_o += []    
            else:
                sql_o += """"""
                values_o += [] 

            sql_o += """GROUP BY o_year, publications.pub_id,  tags.tag_short_title, pub_title, to_char(o_date, 'Month YYYY')
            ORDER BY others.o_year DESC"""
            pub_o = db.querydatafromdatabase(sql_o, values_o, cols_o)
            
            modals_o = []
            if pub_o.shape[0]:
                buttons_o=[]
                

                #modal button generation
                for id in pub_o['id']: 
                    buttons_o += [
                        html.Div(
                            dbc.Button('View', id = f"modal_button_fac_{id}", size='sm', color='danger' ), 
                            style={'text-align': 'center'} 
                        ) 
                    ]
                pub_o['More Details'] = buttons_o
                
                #modal content
                for i in range(len(pub_o)): 
                    ids = pub_o['id'][i]
                    pub_title = pub_o['Title'][i]
                    other_fac = pub_o['Faculty Involved'][i]
                    other_cat = pub_o['Criteria'][i]
                    other_date = pub_o['Date'][i]
                    
                    modals_o += [
                        html.Div(
                            dbc.Modal(
                                [
                                    dbc.ModalHeader(dbc.ModalTitle("Record Details"), style=mod_style), 
                                    dbc.ModalBody([
                                        html.Div([
                                            html.Strong("Title: "),
                                            html.Span(f"{pub_title}"),], id = f"modal_title_{ids}"), 
                                        html.Div([
                                            html.Strong("Faculty Involved: "), 
                                            html.Span(f"{other_fac}"),], id = f"modal_other_fac{ids}" ),
                                        html.Div([
                                            html.Strong("Category: "), 
                                            html.Span(f"{other_cat}"),], id = f"modal_other_cat{ids}" ),
                                        html.Div([
                                            html.Strong("Date: "), 
                                            html.Span(f"{other_date}"),], id = f"modal_other_date{ids}" ),
                                        # html.Div([
                                        #     html.Strong("Additional Information: "), 
                                        #     html.Span(f"{other_other}"),], id = f"modal_other_other{ids}" ),
                                    ],), 
                                    # dbc.ModalFooter(
                                    #     dbc.Button("Close", id= f'modal_close_{ids}', n_clicks = 0)
                                    # )
                                ], 
                                id = f"modal_a_fac_{ids}", size ='lg',
                                centered=True, is_open = False
                            ),  id= f'div_modal_fac_{ids}', style={'display': 'none'}
                        )
                    ]
                    
            for j in range(len(pub_o['together'])):
                string = pub_o['together'][j]
                listed = string.split(', ')
                if facdetid not in listed: 
                    pub_o = pub_o.drop(j)
                else: 
                    pass
                
            pub_o.drop(['together'],axis=1,inplace=True)
            pub_o.drop(['id'],axis=1,inplace=True)
            pub_o.drop(['Date'],axis=1,inplace=True)
            
            if pub_o.shape[0]:
                table_o = dbc.Table.from_dataframe(pub_o, striped=True, bordered=True, hover=True, size='sm', style={"whiteSpace": "pre-line"}) 
            else:
                table_o = "No records to display"
            return [table_o, modals_o]
    else: 
        raise PreventUpdate       

#call all undeleted publications only
# sql_aa = """SELECT
#         publications.pub_id
        
#     FROM publications
#     WHERE
#         pub_delete_ind = false
    
#     """
# values_aa = []
# cols_aa = ['id'] 

# pub_aa = db.querydatafromdatabase(sql_aa, values_aa, cols_aa)

# for ids in pub_aa['id']: 
#     modal_a = f"modal_a_fac_{ids}"
#     modal_button = f"modal_button_fac_{ids}"
#     # modal_close = f'modal_close_{ids}'
#     div_modal = f'div_modal_fac_{ids}'
#     @app.callback(
        
#         Output(modal_a, 'is_open'), 
        
#         [
#             Input(modal_button, 'n_clicks'), 
#             # Input(modal_close, 'n_clicks')
#         ], 
#         [
#             State(modal_button, 'is_open')
#         ]
#     )
    
#     def ihopethisworks(n_clicks, open): 
#         if n_clicks: 
#             return True
#         else: 
#             return False


@app.callback (
    [
        Output('previous2', 'data'), 
        Output('firsttime2', 'data')
        
    ], 
    [
        Input('url', 'pathname'), 
    ], 
    [
        State('previous2', 'data'), 
        State('firsttime2', 'data')
    ]
)
def modalloadwhen(pathname, previous, firsttime): 
    if pathname == '/faculty_details': 
        
        sql_aa = """SELECT
                publications.pub_id
                
                FROM publications
                WHERE
                    pub_delete_ind = false
                    
                
                """
        values_aa = []
        cols_aa = ['id'] 

        pub_aa = db.querydatafromdatabase(sql_aa, values_aa, cols_aa)
        pub_aa_list = pub_aa['id'].tolist()
        
        if firsttime == 1: 
            pub_aa_list = pub_aa['id'].tolist()
            previous = pub_aa_list
            subtracted  = pub_aa_list
            
        else: 
            subtracted  = list(set(pub_aa_list)^ set(previous))
            previous = pub_aa_list + subtracted
        
        
        firsttime += 1
        
        for ids in subtracted: 
            
            modal_a = f"modal_a_fac_{ids}"
            modal_button = f"modal_button_fac_{ids}"
            div_modal = f'div_modal_fac{ids}'
            @app.callback(
                
                Output( f"modal_a_fac_{ids}", 'is_open'), 
                
                [
                    Input(f"modal_button_fac_{ids}", 'n_clicks'), 
                    # Input(modal_close, 'n_clicks')
                ], 
                [
                    State(f"modal_button_fac_{ids}", 'is_open')
                ]
            )
            
            def ihopethisworks(n_clicks, open): 
                if n_clicks: 
                    return True
                else: 
                    return False
        
    return[previous, firsttime]