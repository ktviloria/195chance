#for viewing my publications with buttons leading to editing and adding
#only faculty users have access to this page
#only publication details of current faculty user is shown

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

layout= html.Div( 
    [ 
        dbc.Card(
            [
                dbc.CardHeader(html.H2("My Records")),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                    dbc.DropdownMenu(
                                    children=[
                                        dbc.DropdownMenuItem("Publications", href="form_authorships?mode=add"),
                                        dbc.DropdownMenuItem("Presentations", href="form_presentations?mode=add"),
                                        dbc.DropdownMenuItem("Projects", href="form_projects?mode=add"),
                                        dbc.DropdownMenuItem("Other Academic Merits", href="form_others?mode=add"),
                                    ],
                                    label='Add Research/Activity', color='danger'),
                                    ]
                                ),
                                dbc.Col(
                                    html.Div(
                                        [
                                            dbc.Button("Download CSV", id="btn_csv_mypub", color="dark", className="me-1"),
                                            dcc.Download(id="download-dataframe-csv-mypub")
                                        ], className="d-grid d-md-flex justify-content-md-end"
                                    )
                                )
                            ]
                        ),
                        html.Hr(),
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
                                        dbc.FormText("Lower Year",style = {"font-style": "italic"}), 
                                        dcc.Dropdown(id='mypub_date_filter', clearable=True, searchable=True, placeholder="YYYY"),
                                        ]
                                    ), className="dash-bootstrap", 
                                    style={'min-width': '8%', 'padding-left': '0.5rem', 'padding-right': '0.5rem'}
                                ),
                                dbc.Col(
                                    html.Div(
                                        [
                                        dbc.FormText("Upper Year",style = {"font-style": "italic"}), 
                                        dcc.Dropdown(id='mypub_date_filter_upper', clearable=True, searchable=True, placeholder="YYYY"),
                                        ]
                                    ), className="dash-bootstrap", 
                                    style={'min-width': '8%', 'padding-left': '0.5rem', 'padding-right': '0.5rem'}
                                ),
                                #search filter
                                dbc.Col(
                                    [
                                    dbc.FormText("Search criteria, title, or any keyword on the table", style = {"font-style": "italic", "font-size":"13px"}),
                                    dbc.Input(type="text", id="mypub_filter", placeholder="Enter Keyword"),
                                    ], style={'min-width': '22%', 'padding-left': '0.5rem', 'padding-right': '0.5rem'}
                                ),    
                            ],
                            className="mb-3",
                        ),
                        html.Div(id='mypublist')
                    ]
                ),
            ]
        )
    ]
)

@app.callback(
    [
        Output('mypub_date_filter', 'options'),
        Output('mypub_date_filter_upper', 'options'),
    ],
    [
        Input('url', 'pathname'),
        Input('tabs', 'active_tab'),
        Input('mypub_date_filter', 'value'),
    ],
    [
        State('currentuserid', 'data')
    ]
)
def mypub_loaddropdown (pathname, tab, initial_date, currentuserid):
    if pathname == '/my_publications':
        if tab == 'tab_a':
            mypub_sql_date_filter = """SELECT DISTINCT (a_year) as label, (a_year) as value
                                from authorships
                                    INNER JOIN publications on authorships.pub_id = publications.pub_id
                                    INNER JOIN faculty on publications.user_id = faculty.user_id
                                WHERE
                                    pub_delete_ind = false AND
                                    faculty.user_id = %s 
                                    ORDER BY value DESC
                                """
        elif tab == 'tab_p':
            mypub_sql_date_filter = """SELECT DISTINCT (p_year) as label, (p_year) as value
                                from presentations
                                    INNER JOIN publications on presentations.pub_id = publications.pub_id
                                    INNER JOIN faculty on publications.user_id = faculty.user_id
                                WHERE
                                    pub_delete_ind = false AND
                                    faculty.user_id = %s
                                    ORDER BY value DESC
                                """
        elif tab == 'tab_r':
            mypub_sql_date_filter = """SELECT DISTINCT (r_year) as label, (r_year) as value
                                from projects
                                    INNER JOIN publications on projects.pub_id = publications.pub_id
                                    INNER JOIN faculty on publications.user_id = faculty.user_id
                                WHERE
                                    pub_delete_ind = false AND
                                    faculty.user_id = %s
                                    ORDER BY value DESC
                                """
        elif tab == 'tab_o':
            mypub_sql_date_filter = """SELECT DISTINCT (o_year) as label, (o_year) as value
                                from others
                                    INNER JOIN publications on others.pub_id = publications.pub_id
                                    INNER JOIN faculty on publications.user_id = faculty.user_id
                                WHERE
                                    pub_delete_ind = false AND
                                    faculty.user_id = %s
                                    ORDER BY value DESC
                                """
        else:
            raise PreventUpdate
        
        mypub_values_date_filter = [f"{currentuserid}"]
        mypub_cols_date_filter = ['label', 'value']
        mypub_date_filter_included = db.querydatafromdatabase(mypub_sql_date_filter, mypub_values_date_filter, mypub_cols_date_filter)
        mypub_date_filter_options = mypub_date_filter_included.to_dict('records')
        
        if initial_date: 
            
            if tab == 'tab_a':
                mypub_sql_date_filter_upper = """SELECT DISTINCT (a_year) as label, (a_year) as value
                                from authorships
                                    INNER JOIN publications on authorships.pub_id = publications.pub_id
                                    INNER JOIN faculty on publications.user_id = faculty.user_id
                                WHERE
                                    pub_delete_ind = false AND
                                    faculty.user_id = %s AND cast(a_year as int) >=  %s 
                                    ORDER BY value DESC
                                """
            elif tab == 'tab_p':
                mypub_sql_date_filter_upper = """SELECT DISTINCT (p_year) as label, (p_year) as value
                                    from presentations
                                        INNER JOIN publications on presentations.pub_id = publications.pub_id
                                        INNER JOIN faculty on publications.user_id = faculty.user_id
                                    WHERE
                                        pub_delete_ind = false AND
                                        faculty.user_id = %s AND cast(p_year as int) >=  %s 
                                        ORDER BY value DESC
                                    """
            elif tab == 'tab_r':
                mypub_sql_date_filter_upper = """SELECT DISTINCT (r_year) as label, (r_year) as value
                                    from projects
                                        INNER JOIN publications on projects.pub_id = publications.pub_id
                                        INNER JOIN faculty on publications.user_id = faculty.user_id
                                    WHERE
                                        pub_delete_ind = false AND
                                        faculty.user_id = %s AND cast(r_year as int) >=  %s 
                                        ORDER BY value DESC
                                    """
            elif tab == 'tab_o':
                mypub_sql_date_filter_upper = """SELECT DISTINCT (o_year) as label, (o_year) as value
                                    from others
                                        INNER JOIN publications on others.pub_id = publications.pub_id
                                        INNER JOIN faculty on publications.user_id = faculty.user_id
                                    WHERE
                                        pub_delete_ind = false AND
                                        faculty.user_id = %s AND cast(o_year as int) >=  %s
                                        ORDER BY value DESC
                                    """
            mypub_values_date_filter_upper = [f"{currentuserid}", initial_date]
            mypub_cols_date_filter_upper = ['label', 'value']
            mypub_date_filter_included_upper = db.querydatafromdatabase(mypub_sql_date_filter_upper, mypub_values_date_filter_upper, mypub_cols_date_filter_upper)
            mypub_date_filter_options_upper = mypub_date_filter_included_upper.to_dict('records')
        else:
            mypub_date_filter_options_upper = mypub_date_filter_options
        
        
            
            
            
    else:
        raise PreventUpdate
    
    return [mypub_date_filter_options, mypub_date_filter_options_upper]    

@app.callback(
    [
        Output('mypublist', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('tabs', 'active_tab'),
        Input('mypub_filter', 'value'),
        Input('mypub_date_filter', 'value'), 
        Input('mypub_date_filter_upper', 'value')
    ],
        State('currentuserid', 'data')
)

#publist
def mypub_loadpublist(pathname, tab, searchterm, datefilter, datefilter_u,  currentuserid):
    if pathname == '/my_publications':      
        if tab == 'tab_a':
            sql_a = """SELECT  publications.pub_id,
                a_year,
				lead_authors_agg.lead_author_names,
				lead_authors_agg.lead_up_affiliations,
				publications.pub_title,
                tags.tag_short_title,
				contributing_authors_agg.contributing_author_names,
				contributing_authors_agg.contributing_up_affiliations,
                To_char(a_date, 'Month YYYY'),
                a_pub_name, 
                a_publisher, 
                a_doi, 
                a_isxn, 
                a_scopus, 
                to_char(publications.pub_last_upd::timestamp, 'Month DD YYYY HH24:MI:SS') as timestampz,
                publications.modified_by

                FROM publications
                INNER JOIN authorships on publications.pub_id = authorships.pub_id
				INNER JOIN authors on publications.user_id = authors.author_user_id
                LEFT OUTER JOIN (
					SELECT
						pub_id,
						string_agg(lead_author_name, ', ') AS lead_author_names,
						string_agg(author_up_constituent, ', ') AS lead_up_affiliations
					FROM pub_lead_authors
					INNER JOIN authors ON pub_lead_authors.a_lead_id = authors.author_id
					GROUP BY pub_id
				) AS lead_authors_agg ON publications.pub_id = lead_authors_agg.pub_id
				LEFT OUTER JOIN (
					SELECT
						pub_id,
						string_agg(contributing_author_name, ', ') AS contributing_author_names,
						string_agg(author_up_constituent, ', ') AS contributing_up_affiliations
					FROM pub_contributing_authors
					INNER JOIN authors ON pub_contributing_authors.a_contributing_id = authors.author_id
					GROUP BY pub_id
				) AS contributing_authors_agg ON publications.pub_id = contributing_authors_agg.pub_id
                LEFT OUTER JOIN tags on publications.tag_id = tags.tag_id
                WHERE publications.pub_delete_ind = false and authors.author_user_id = %s
				

                """
            values_a = [f"{currentuserid}"]
            cols_a = ['id', 'Year', 'Lead Author(s)', 'Lead Authors Affiliation', 'Title', 'Criteria', 'Other Contributing Author(s)', 'Contributing Authors Affiliation', 'Date', 'Publication', 'Publisher', 'DOI','ISXN', 'Scopus',  'Last Updated', 'Last Modified By']
            
            #fix additivity of searchterms and filters
            if datefilter:
                sql_a += """AND (cast (a_year as int) >= %s)"""
                values_a += [datefilter]
                if datefilter_u:
                    sql_a += """AND (cast (a_year as int) <= %s)"""
                    values_a += [datefilter_u]
                    if searchterm:
                        sql_a += """ AND (
                            (lead_author_names ILIKE %s) OR (contributing_author_names ILIKE %s) OR
                            (pub_title ILIKE %s) OR (tag_short_title ILIKE %s) OR (a_year ILIKE %s) OR ((To_char(a_date, 'Month YYYY')) ILIKE %s)
                            OR (a_pub_name ILIKE %s) OR (a_publisher ILIKE %s) OR (a_doi ILIKE %s) OR (a_isxn ILIKE %s) OR (a_scopus ILIKE %s)
                        ) """
                        values_a += [f"%{searchterm}%", f"%{searchterm}%",
                                     f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                     f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
                if searchterm:
                    sql_a += """ AND (
                    (lead_author_names ILIKE %s) OR (contributing_author_names ILIKE %s) OR
                    (pub_title ILIKE %s) OR (tag_short_title ILIKE %s) OR (a_year ILIKE %s) OR ((To_char(a_date, 'Month YYYY')) ILIKE %s)
                    OR (a_pub_name ILIKE %s) OR (a_publisher ILIKE %s) OR (a_doi ILIKE %s) OR (a_isxn ILIKE %s) OR (a_scopus ILIKE %s)
                ) """
                    values_a += [f"%{searchterm}%", f"%{searchterm}%",
                                     f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                     f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
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
                    (lead_author_names ILIKE %s) OR (contributing_author_names ILIKE %s) OR
                    (pub_title ILIKE %s) OR (tag_short_title ILIKE %s) OR (a_year ILIKE %s) OR ((To_char(a_date, 'Month YYYY')) ILIKE %s)
                    OR (a_pub_name ILIKE %s) OR (a_publisher ILIKE %s) OR (a_doi ILIKE %s) OR (a_isxn ILIKE %s) OR (a_scopus ILIKE %s)
                ) """
                        values_a += [f"%{searchterm}%", f"%{searchterm}%",
                                     f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                     f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
                if searchterm:
                    sql_a += """ AND (
                    (lead_author_names ILIKE %s) OR (contributing_author_names ILIKE %s) OR
                    (pub_title ILIKE %s) OR (tag_short_title ILIKE %s) OR (a_year ILIKE %s) OR ((To_char(a_date, 'Month YYYY')) ILIKE %s)
                    OR (a_pub_name ILIKE %s) OR (a_publisher ILIKE %s) OR (a_doi ILIKE %s) OR (a_isxn ILIKE %s) OR (a_scopus ILIKE %s)
                ) """
                    values_a += [f"%{searchterm}%", f"%{searchterm}%",
                                     f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                     f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
                    if datefilter:
                        sql_a += """AND (cast (a_year as int) >= %s)"""
                        values_a += [datefilter]
                else:
                    sql_a += """"""
                    values_a += [] 
            
            elif searchterm:
                sql_a += """ AND (
                    (lead_author_names ILIKE %s) OR (contributing_author_names ILIKE %s) OR
                    (pub_title ILIKE %s) OR (tag_short_title ILIKE %s) OR (a_year ILIKE %s) OR ((To_char(a_date, 'Month YYYY')) ILIKE %s)
                    OR (a_pub_name ILIKE %s) OR (a_publisher ILIKE %s) OR (a_doi ILIKE %s) OR (a_isxn ILIKE %s) OR (a_scopus ILIKE %s)
                ) """
                values_a += [f"%{searchterm}%", f"%{searchterm}%",
                                     f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                     f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
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

            sql_a += """GROUP BY publications.pub_id, a_year,
				lead_authors_agg.lead_author_names, lead_authors_agg.lead_up_affiliations,
				contributing_authors_agg.contributing_author_names, contributing_authors_agg.contributing_up_affiliations,
				tags.tag_short_title, To_char(a_date, 'Month YYYY'),a_pub_name, a_publisher, 
                a_doi, a_isxn, a_scopus, publications.modified_by, to_char(publications.pub_last_upd::timestamp, 'Month DD YYYY HH24:MI:SS')
				ORDER BY authorships.a_year DESC"""
            pub_a = db.querydatafromdatabase(sql_a, values_a, cols_a) 
            
            if pub_a.shape[0]: 
                buttons_a = []
                pub_details = []
                other_info = []
                 
                for id in pub_a['id']: 
                    buttons_a += [ 
                        html.Div( 
                            dbc.Button('Edit/Delete', href=f"/form_authorships?mode=edit&id={id}", size='sm', color='secondary', ), 
                            style={'text-align': 'center'} 
                        ) 
                    ] 

                for i in range(len(pub_a)): 
                    inputs_1 = [pub_a['Date'][i], pub_a['Publication'][i], pub_a['Publisher'][i]]
                    if not all (inputs_1) :  
                        pub_details += " "
                    else: 
                        pub_details += [("Published in/on: %s in %s by %s" % (pub_a['Date'][i], pub_a['Publication'][i], pub_a['Publisher'][i]))] 
                    other_info += [("DOI: %s \n Issue Number: %s \n Scopus: %s"  % (pub_a['DOI'][i], pub_a['ISXN'][i], pub_a['Scopus'][i]) or " " )]

                pub_a['Publication Details'] = pub_details
                pub_a['Other Information'] = other_info
                

                last_update_holder = pub_a['Last Updated']
                pub_a.drop(['Last Updated'],axis=1,inplace=True)
                pub_a['Last Updated'] = last_update_holder 

                last_modifiedby_holder = pub_a['Last Modified By']
                pub_a.drop(['Last Modified By'],axis=1,inplace=True)
                pub_a['Last Modified By'] = last_modifiedby_holder 

                pub_a['Action'] = buttons_a
                
            pub_a.drop(['id'],axis=1,inplace=True)
            pub_a.drop(['Lead Authors Affiliation'],axis=1,inplace=True)
            pub_a.drop(['Contributing Authors Affiliation'],axis=1,inplace=True)
            pub_a.drop(['Date'],axis=1,inplace=True)
            pub_a.drop(['Publication'],axis=1,inplace=True)
            pub_a.drop(['Publisher'],axis=1,inplace=True)
            pub_a.drop(['DOI'],axis=1,inplace=True)
            pub_a.drop(['ISXN'],axis=1,inplace=True)
            pub_a.drop(['Scopus'],axis=1,inplace=True)
            
            if pub_a.shape[0]:
                table_a = dbc.Table.from_dataframe(pub_a, striped=True, bordered=True, hover=True, size='sm', style={"whiteSpace": "pre-line"}) 
            else:
                table_a = "No records to display."
            return [table_a]
            
        elif tab == 'tab_p':
            sql_p = """SELECT publications.pub_id,
                p_year,
				pres_authors_agg.pres_author_names,
                pres_authors_agg.pres_up_affiliations,
                publications.pub_title,
                tags.tag_short_title,
                to_char(p_start_date, 'Month DD, YYYY'), 
                to_char(p_end_date, 'Month  DD, YYYY'), 
                p_conf, 
                p_loc, 
                p_add_info, 
                to_char(publications.pub_last_upd::timestamp, 'Month DD YYYY HH24:MI:SS'),
                publications.modified_by
            FROM presentations
                LEFT OUTER JOIN faculty on presentations.p_author_id = faculty.user_id
                INNER JOIN publications on presentations.pub_id = publications.pub_id
                LEFT OUTER JOIN (
					SELECT
						pub_id,
						string_agg(author_name, ', ') AS pres_author_names,
						string_agg(author_up_constituent, ', ') AS pres_up_affiliations
					FROM pres_authors
					INNER JOIN authors ON pres_authors.p_author_id = authors.author_id
					GROUP BY pub_id
				) AS pres_authors_agg ON publications.pub_id = pres_authors_agg.pub_id
                LEFT OUTER JOIN tags on publications.tag_id = tags.tag_id
            WHERE
				publications.pub_delete_ind = false AND
                faculty.user_id = %s
                """
            values_p = [f"{currentuserid}"]
            cols_p = ['id', 'Year', 'Presenter(s)', 'Presenters Affiliation', 'Title', 'Criteria', 'Start Date', 'End Date',
                      'Conference', 'Location', 'Other Info', 'Last Updated', 'Last Modified By']
            
            if datefilter:
                sql_p += """AND (cast (p_year as int) >= %s)"""
                values_p += [datefilter]
                if datefilter_u:
                    sql_p += """AND (cast (p_year as int) <= %s)"""
                    values_p += [datefilter_u]
                    if searchterm:
                        sql_p += """ AND (
                            (pres_author_names ILIKE %s) OR (pub_title ILIKE %s) 
                            OR (p_conf ILIKE %s) OR (p_loc ILIKE %s) OR (p_add_info ILIKE %s) OR (tag_short_title ILIKE %s)
                            OR (p_year ILIKE %s) OR (to_char(p_start_date, 'Month DD, YYYY') ILIKE %s) OR (to_char(p_end_date, 'Month DD, YYYY')ILIKE %s)
                            )
                            """
                        values_p += [f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%",f"%{searchterm}%"]
                if searchterm:
                    sql_p += """ AND (
                            (pres_author_names ILIKE %s) OR (pub_title ILIKE %s) 
                            OR (p_conf ILIKE %s) OR (p_loc ILIKE %s) OR (p_add_info ILIKE %s) OR (tag_short_title ILIKE %s)
                            OR (p_year ILIKE %s) OR (to_char(p_start_date, 'Month DD, YYYY') ILIKE %s) OR (to_char(p_end_date, 'Month DD, YYYY')ILIKE %s)
                            )
                            """
                    values_p += [f"%{searchterm}%", f"%{searchterm}%",
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
                            (pres_author_names ILIKE %s) OR (pub_title ILIKE %s) 
                            OR (p_conf ILIKE %s) OR (p_loc ILIKE %s) OR (p_add_info ILIKE %s) OR (tag_short_title ILIKE %s)
                            OR (p_year ILIKE %s) OR (to_char(p_start_date, 'Month DD, YYYY') ILIKE %s) OR (to_char(p_end_date, 'Month DD, YYYY')ILIKE %s)
                            )
                            """
                        values_p += [f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%",f"%{searchterm}%"]
                if searchterm:
                    sql_p += """ AND (
                            (pres_author_names ILIKE %s) OR (pub_title ILIKE %s) 
                            OR (p_conf ILIKE %s) OR (p_loc ILIKE %s) OR (p_add_info ILIKE %s) OR (tag_short_title ILIKE %s)
                            OR (p_year ILIKE %s) OR (to_char(p_start_date, 'Month DD, YYYY') ILIKE %s) OR (to_char(p_end_date, 'Month DD, YYYY')ILIKE %s)
                            )
                            """
                    values_p += [f"%{searchterm}%", f"%{searchterm}%",
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
                            (pres_author_names ILIKE %s) OR (pub_title ILIKE %s) 
                            OR (p_conf ILIKE %s) OR (p_loc ILIKE %s) OR (p_add_info ILIKE %s) OR (tag_short_title ILIKE %s)
                            OR (p_year ILIKE %s) OR (to_char(p_start_date, 'Month DD, YYYY') ILIKE %s) OR (to_char(p_end_date, 'Month DD, YYYY')ILIKE %s)
                            )
                            """
                values_p += [f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%",f"%{searchterm}%"]
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

            sql_p += """GROUP BY publications.pub_id, p_year, pres_authors_agg.pres_author_names, pres_authors_agg.pres_up_affiliations, tags.tag_short_title, pub_title,
                    to_char(p_start_date, 'Month DD, YYYY'), to_char(p_end_date, 'Month  DD, YYYY'), p_conf, p_loc, p_add_info
            ORDER BY p_year DESC"""
            pub_p = db.querydatafromdatabase(sql_p, values_p, cols_p)
            
            if pub_p.shape[0]: 
                pres_details = []
                other_details = []
                for i in range(len(pub_p)): 
                    pres_details += [("Presented from: %s to %s \n Presented at: %s (%s)" % (pub_p['Start Date'][i], pub_p['End Date'][i], pub_p['Conference'][i], pub_p['Location'][i]) or "No Details Provided")]
                    other_details += [pub_p['Other Info'][i]]
            
                pub_p['Presentation Details'] = pres_details
                pub_p['Additional Info'] = other_details
                
                buttons_p = [] 
                for id in pub_p['id']: 
                    buttons_p += [ 
                        html.Div( 
                            dbc.Button('Edit/Delete', href=f"/form_presentations?mode=edit&id={id}", size='sm', color='secondary', ), 
                            style={'text-align': 'center'} 
                        ) 
                    ] 
                
                last_update_holder_p = pub_p['Last Updated']
                pub_p.drop(['Last Updated'],axis=1,inplace=True)
                pub_p['Last Updated'] = last_update_holder_p

                last_modifiedby_holder_p = pub_p['Last Modified By']
                pub_p.drop(['Last Modified By'], axis=1, inplace=True)
                pub_p['Last Modified By'] = last_modifiedby_holder_p
                
                pub_p['More Details'] = buttons_p
            
            pub_p.drop(['id'],axis=1,inplace=True)
            pub_p.drop(['Presenters Affiliation'],axis=1,inplace=True)
            pub_p.drop(['Start Date'],axis=1,inplace=True)
            pub_p.drop(['End Date'],axis=1,inplace=True)
            pub_p.drop(['Conference'],axis=1,inplace=True)
            pub_p.drop(['Location'],axis=1,inplace=True)
            pub_p.drop(['Other Info'],axis=1,inplace=True)
            
            if pub_p.shape[0]:
                table_p = dbc.Table.from_dataframe(pub_p, striped=True, bordered=True, hover=True, size='sm', style={"whiteSpace": "pre-line"}) 
            else:
                table_p = "No records to display."
            return [table_p]
            
            # table_p = dbc.Table.from_dataframe(pub_p, striped=True, bordered=True, hover=True, size='sm', style={"whiteSpace": "pre-line"}) 
            # return [table_p] 

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
                projects_users.r_roles, 
                r_timeframe, 
                to_char(r_start_date, 'Month DD, YYYY'),
                to_char(r_end_date, 'Month DD, YYYY'), 
                r_fund_org,
                to_char(publications.pub_last_upd::timestamp, 'Month DD, YYYY HH24:MI:SS'),
                publications.modified_by
            FROM projects_users
				INNER JOIN projects on projects_users.pub_id = projects.pub_id
                LEFT OUTER JOIN faculty on projects_users.user_id = faculty.user_id
				INNER JOIN publications on projects_users.pub_id = publications.pub_id
                INNER JOIN tags on publications.tag_id = tags.tag_id               
            WHERE
                pub_delete_ind = false AND
                faculty.user_id = %s
                """
            values_r = [f"{currentuserid}"]
            cols_r = ['Year', 'id', 'Faculty Involved', 'Criteria', 'Title', 'Role', 'Timeframe', 'Start Date', 'End Date', 'Funding Organization',
                      'Last Updated', 'Last Modified By']  
            
            if datefilter:
                sql_r += """AND (cast (r_year as int) >= %s)"""
                values_r += [datefilter]
                if datefilter_u:
                    sql_r += """AND (cast (r_year as int) <= %s)"""
                    values_r += [datefilter_u]
                    if searchterm:
                        sql_r += """ AND (
                            (r_year ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                            OR (r_timeframe ILIKE %s) OR (r_fund_org ILIKE %s) OR (tag_short_title ILIKE %s)
                            OR ((To_char(r_start_date, 'Month DD, YYYY')) ILIKE %s) OR ((To_char(r_end_date, 'Month DD, YYYY')) ILIKE %s)
                            OR (projects_users.r_roles ILIKE %s))"""
                        values_r += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                            f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"
                            ]  
                if searchterm:
                    sql_r += """ AND (
                        (r_year ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                        OR (r_timeframe ILIKE %s) OR (r_fund_org ILIKE %s) OR (tag_short_title ILIKE %s)
                        OR ((To_char(r_start_date, 'Month DD, YYYY')) ILIKE %s) OR ((To_char(r_end_date, 'Month DD, YYYY')) ILIKE %s)
                        OR (projects_users.r_roles ILIKE %s))"""
                    values_r += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                        f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"
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
                            OR (r_timeframe ILIKE %s) OR (r_fund_org ILIKE %s) OR (tag_short_title ILIKE %s)
                            OR ((To_char(r_start_date, 'Month DD, YYYY')) ILIKE %s) OR ((To_char(r_end_date, 'Month DD, YYYY')) ILIKE %s)
                            OR (projects_users.r_roles ILIKE %s))"""
                        values_r += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
                if searchterm:
                    sql_r += """ AND (
                        (r_year ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                        OR (r_timeframe ILIKE %s) OR (r_fund_org ILIKE %s) OR (tag_short_title ILIKE %s)
                        OR ((To_char(r_start_date, 'Month DD, YYYY')) ILIKE %s) OR ((To_char(r_end_date, 'Month DD, YYYY')) ILIKE %s)
                        OR (projects_users.r_roles ILIKE %s))"""
                    values_r += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                            f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
                    if datefilter:
                        sql_r += """AND (cast (r_year as int) >= %s)"""
                        values_r += [datefilter]

                else:
                    sql_r += """"""
                    values_r += [] 
                    
            elif searchterm:
                sql_r += """ AND (
                        (r_year ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                        OR (r_timeframe ILIKE %s) OR (r_fund_org ILIKE %s) OR (tag_short_title ILIKE %s)
                        OR ((To_char(r_start_date, 'Month DD, YYYY')) ILIKE %s) OR ((To_char(r_end_date, 'Month DD, YYYY')) ILIKE %s)
                        OR (projects_users.r_roles ILIKE %s))"""
                values_r += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                        f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"
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
            to_char(r_end_date, 'Month  DD, YYYY'), r_fund_org, r_end_date, projects_users.r_roles
            ORDER BY projects.r_year DESC"""
            pub_r = db.querydatafromdatabase(sql_r, values_r, cols_r)

            # if searchterm:
            #     #OR (tag_short_title %s)
            # #OR (r_start_date ILIKE %s)
            # #OR (r_end_date ILIKE %s)
            #     sql_r += """ AND (r_year ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
            #         OR (r_roles ILIKE %s) OR (r_timeframe ILIKE %s) OR (r_fund_org ILIKE %s)"""
            #     values_r += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
            #             f"%{searchterm}%", f"%{searchterm}%",
            #             ]

            # sql_r += """ORDER BY projects.r_year DESC"""
            # pub_r = db.querydatafromdatabase(sql_r, values_r, cols_r)

            # if pub_r.shape[0]: 
            #     buttons_r = [] 
            #     for currentuserid in pub_r['userID']: 
            #         buttons_r += [ 
            #             html.Div( 
            #                 dbc.Button('Edit/Delete', href=f"/form_projects?mode=edit&id={currentuserid}", size='sm', color='secondary', ), 
            #                 style={'text-align': 'center'} 
            #             ) 
            #         ] 
            #     pub_r['Action'] = buttons_r
            # pub_r.drop(['userID'],axis=1,inplace=True)
            # table_r = dbc.Table.from_dataframe(pub_r, striped=True, bordered=True, hover=True, size='sm') 
            # return [table_r]
            
            if pub_r.shape[0]: 
                proj_details1 = []
                proj_details2 = [] 
                proj_details = []
                for i in range(len(pub_r)):
                    
                    
                    if pub_r['Timeframe'][i] == None:
                        proj_details2 += [" "] 
                    else: 
                        proj_details2 += [("Executed project in %s from %s to %s" % (pub_r['Timeframe'][i],pub_r['Start Date'][i], pub_r['End Date'][i])) or " "]
                    
                    proj_details += [proj_details2[i]]

                
                buttons_r = [] 
                for id in pub_r['id']: 
                    buttons_r += [ 
                        html.Div( 
                            dbc.Button('Edit/Delete', href=f"/form_projects?mode=edit&id={id}&key={currentuserid}", size='sm', color='secondary', ), 
                            style={'text-align': 'center'} 
                        ) 
                    ] 
                    
                pub_r['Project Details'] = proj_details

                last_update_holder_r = pub_r['Last Updated']
                pub_r.drop(['Last Updated'],axis=1,inplace=True)
                pub_r['Last Updated'] = last_update_holder_r

                last_modifiedby_holder_r = pub_r['Last Modified By']
                pub_r.drop(['Last Modified By'],axis=1,inplace=True)
                pub_r['Last Modified By'] = last_modifiedby_holder_r

                pub_r['More Details'] = buttons_r
            
            pub_r.drop(['Faculty Involved'],axis=1,inplace=True)
            pub_r.drop(['id'],axis=1,inplace=True)  
            pub_r.drop(['Start Date'],axis=1,inplace=True)
            pub_r.drop(['End Date'],axis=1,inplace=True)
            pub_r.drop(['Timeframe'],axis=1,inplace=True)
            
            if pub_r.shape[0]:
                table_r = dbc.Table.from_dataframe(pub_r, striped=True, bordered=True, hover=True, size='sm', style={"whiteSpace": "pre-line"}) 
            else:
                table_r = "No records to display."
            return [table_r] 

            # table_r = dbc.Table.from_dataframe(pub_r, striped=True, bordered=True, hover=True, size='sm', style={"whiteSpace": "pre-line"}) 
            # return [table_r]

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
                    others_users.o_add_info, 
                    to_char(o_date, 'Month YYYY'),
                    to_char(publications.pub_last_upd::timestamp, 'Month DD, YYYY HH24:MI:SS'),
                    publications.modified_by
                FROM others_users
                    INNER JOIN others on others_users.pub_id = others.pub_id
                    LEFT OUTER JOIN faculty on others_users.user_id = faculty.user_id
                    INNER JOIN publications on others_users.pub_id = publications.pub_id
                    INNER JOIN tags on publications.tag_id = tags.tag_id  
                WHERE
                    pub_delete_ind = false AND
                    faculty.user_id = %s
                """
            values_o = [f"{currentuserid}"]
            cols_o = ['Year', 'id', 'Faculty Involved', 'Criteria', 'Title', 'Other Details', 'Date',  "Last Updated", "Last Modified By"] 
            
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
            
            sql_o += """GROUP BY o_year, publications.pub_id, faculty.user_id, tags.tag_short_title, pub_title, to_char(o_date, 'Month YYYY'), others_users.o_add_info
            ORDER BY others.o_year DESC"""
            pub_o = db.querydatafromdatabase(sql_o, values_o, cols_o)

            # if searchterm:
            # #OR (tag_short_title %s)
            #     sql_o += """ AND (pub_title ILIKE %s) OR (o_year ILIKE %s) OR ((To_char(a_date, 'Month YYYY')) ILIKE %s)
            #         OR (o_add_info ILIKE %s)"""
            #     values_o += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"  
            #         ]

            # sql_o += """ORDER BY others.o_year DESC"""
            
            # pub_o = db.querydatafromdatabase(sql_o, values_o, cols_o)
            # if pub_o.shape[0]: 
            #     buttons_o = [] 
            #     for currentuserid in pub_o['userID']: 
            #         buttons_o += [ 
            #             html.Div( 
            #                 dbc.Button('Edit/Delete', href=f"/my_publications_profile?mode=edit&id={currentuserid}", size='sm', color='secondary', ), 
            #                 style={'text-align': 'center'} 
            #             ) 
            #         ] 
            #     pub_o['Action'] = buttons_o
            # pub_o.drop(['userID'],axis=1,inplace=True)
            # table_o = dbc.Table.from_dataframe(pub_o, striped=True, bordered=True, hover=True, size='sm') 
            # return [table_o]
            
            if pub_o.shape[0]: 
                buttons_o = [] 
                for id in pub_o['id']: 
                    buttons_o += [ 
                        html.Div( 
                            dbc.Button('Edit/Delete', href=f"/form_others?mode=edit&id={id}&key={currentuserid}", size='sm', color='secondary', ), 
                            style={'text-align': 'center'} 
                        ) 
                    ] 
                pub_o['More Details'] = buttons_o

            pub_o.drop(['id'],axis=1,inplace=True)   
            pub_o.drop(['Faculty Involved'],axis=1,inplace=True)   
            
            if pub_o.shape[0]:
                table_o = dbc.Table.from_dataframe(pub_o, striped=True, bordered=True, hover=True, size='sm', style={"whiteSpace": "pre-line"}) 
            else:
                table_o = "No records to display."
            return [table_o] 
            
            # table_o = dbc.Table.from_dataframe(pub_o, striped=True, bordered=True, hover=True, size='sm',style={"whiteSpace": "pre-line"}) 
            # return [table_o]
    else: 
        return ["No records to display."]      

@app.callback(
    [
        Output("download-dataframe-csv-mypub", "data"), ##
        Output("btn_csv_mypub", "n_clicks")
    ],
    [
        Input('tabs', 'active_tab'),
        Input("btn_csv_mypub", "n_clicks"),
        Input('mypub_filter', 'value'),
        Input('mypub_date_filter', 'value'),
        Input('mypub_date_filter_upper', 'value'),
    ],  ##
    [
        State('currentuserid', 'data')
    ], prevent_initial_call=True ##
)

def download_mypub(tab, n_clicks,searchterm, datefilter, datefilter_u,  currentuserid):
    download_table_a = []
    #print(not n_clicks)
    if n_clicks== None:
        raise PreventUpdate

    if n_clicks==1:
        #print(not n_clicks)
        n_clicks = None
        #print(n_clicks)
        #print(not n_clicks)
    
        if tab == 'tab_a':
            sql_a_down = """SELECT 
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
                to_char(publications.pub_last_upd::timestamp, 'Month DD YYYY HH24:MI:SS') as timestampz,
                publications.modified_by

                FROM authorships_users
                INNER JOIN authorships on authorships_users.pub_id = authorships.pub_id
                LEFT OUTER JOIN faculty on authorships_users.user_id = faculty.user_id
                INNER JOIN publications on authorships_users.pub_id = publications.pub_id
                LEFT OUTER JOIN authorship_role on authorships_users.authorship_role = authorship_role.a_label_id
                LEFT OUTER JOIN tags on publications.tag_id = tags.tag_id
                WHERE publications.pub_delete_ind = false and faculty.user_id = %s

                """
            values_a_down = [f"{currentuserid}"]
            cols_a_down = ['Year','id', 'Faculty Involved', 'Criteria', 'Title', 'All Authors',  'Date', 'Publication', 'Publisher', 'DOI','ISXN', 'Scopus', 'Last Updated', 'Last Modified By']            
            #fix additivity of searchterms and filters
            if datefilter:
                sql_a_down += """AND (cast (a_year as int) >= %s)"""
                values_a_down += [datefilter]
                if datefilter_u:
                    sql_a_down += """AND (cast (a_year as int) <= %s)"""
                    values_a_down += [datefilter_u]
                    if searchterm:
                        sql_a_down += """ AND (
                            ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) OR (a_year ILIKE %s)
                            OR (a_authors ILIKE %s) OR (a_pub_name ILIKE %s) OR ((To_char(a_date, 'Month YYYY')) ILIKE %s)
                            OR (a_publisher ILIKE %s) OR (a_doi ILIKE %s) OR (a_isxn ILIKE %s) OR (a_scopus ILIKE %s) OR (tag_short_title ILIKE %s)
                            OR (authorship_role.a_label ILIKE %s))"""
                        values_a_down += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
                if searchterm:
                    sql_a_down += """ AND (
                        ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) OR (a_year ILIKE %s)
                        OR (a_authors ILIKE %s) OR (a_pub_name ILIKE %s) OR ((To_char(a_date, 'Month YYYY')) ILIKE %s)
                        OR (a_publisher ILIKE %s) OR (a_doi ILIKE %s) OR (a_isxn ILIKE %s) OR (a_scopus ILIKE %s) OR (tag_short_title ILIKE %s)
                        OR (authorship_role.a_label ILIKE %s))"""
                    values_a_down += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                            f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                            f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
                    if datefilter_u:
                        sql_a_down += """AND (cast (a_year as int) <= %s)"""
                        values_a_down += [datefilter_u]
                else:
                    sql_a_down += """"""
                    values_a_down += [] 
                    
            elif datefilter_u: 
                sql_a_down += """AND (cast (a_year as int) <= %s)"""
                values_a_down += [datefilter_u]
                if datefilter:
                    sql_a_down += """AND (cast (a_year as int) >= %s)"""
                    values_a_down += [datefilter]
                    if searchterm:
                        sql_a_down += """ AND (
                            ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) OR (a_year ILIKE %s)
                            OR (a_authors ILIKE %s) OR (a_pub_name ILIKE %s) OR ((To_char(a_date, 'Month YYYY')) ILIKE %s)
                            OR (a_publisher ILIKE %s) OR (a_doi ILIKE %s) OR (a_isxn ILIKE %s) OR (a_scopus ILIKE %s) OR (tag_short_title ILIKE %s)
                            OR (authorship_role.a_label ILIKE %s))"""
                        values_a_down += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
                if searchterm:
                    sql_a_down += """ AND (
                        ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) OR (a_year ILIKE %s)
                        OR (a_authors ILIKE %s) OR (a_pub_name ILIKE %s) OR ((To_char(a_date, 'Month YYYY')) ILIKE %s)
                        OR (a_publisher ILIKE %s) OR (a_doi ILIKE %s) OR (a_isxn ILIKE %s) OR (a_scopus ILIKE %s) OR (tag_short_title ILIKE %s)
                        OR (authorship_role.a_label ILIKE %s))"""
                    values_a_down += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                            f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                            f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
                    if datefilter:
                        sql_a_down += """AND (cast (a_year as int) >= %s)"""
                        values_a_down += [datefilter]
                else:
                    sql_a_down += """"""
                    values_a_down += [] 
            
            elif searchterm:
                sql_a_down += """ AND (
                    ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) OR (a_year ILIKE %s)
                    OR (a_authors ILIKE %s) OR (a_pub_name ILIKE %s) OR ((To_char(a_date, 'Month YYYY')) ILIKE %s)
                    OR (a_publisher ILIKE %s) OR (a_doi ILIKE %s) OR (a_isxn ILIKE %s) OR (a_scopus ILIKE %s) OR (tag_short_title ILIKE %s)
                    OR (authorship_role.a_label ILIKE %s))"""
                values_a_down += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                        f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                        f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
                if datefilter:
                    sql_a_down += """AND (cast (a_year as int) >= %s)"""
                    values_a_down += [datefilter]
                    if datefilter_u:
                        sql_a_down += """AND (cast (a_year as int) <= %s)"""
                        values_a_down += [datefilter_u]
                elif datefilter_u:
                    sql_a_down += """AND (cast (a_year as int) <= %s)"""
                    values_a_down += [datefilter_u]
                    if datefilter:
                        sql_a_down += """AND (cast (a_year as int) >= %s)"""
                        values_a_down += [datefilter]
                else:
                    sql_a_down += """"""
                    values_a_down += []     
            else:
                sql_a_down += """"""
                values_a_down += []

            sql_a_down += """GROUP BY publications.pub_id, authorships.a_year, tags.tag_short_title,
	        a_authors, To_char(a_date, 'Month YYYY'),a_pub_name, a_publisher, 
	        a_doi, a_isxn, a_scopus, to_char(publications.pub_last_upd::timestamp, 'Month DD YYYY HH24:MI:SS'),publications.modified_by
            ORDER BY authorships.a_year DESC"""   
            pub_a_down = db.querydatafromdatabase(sql_a_down, values_a_down, cols_a_down)
            
            download_table_a = dcc.send_data_frame(pub_a_down.to_csv, "mypublications_download.csv")

            return [download_table_a, n_clicks] ##
        
        elif tab =='tab_p':
            sql_p_down = """SELECT
                p_year,
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
                to_char(publications.pub_last_upd::timestamp, 'Month DD YYYY HH24:MI:SS'),
                publications.modified_by
            FROM presentations_users
				INNER JOIN presentations on presentations_users.pub_id = presentations.pub_id
                LEFT OUTER JOIN faculty on presentations_users.user_id = faculty.user_id
				INNER JOIN publications on presentations_users.pub_id = publications.pub_id
                INNER JOIN tags on publications.tag_id = tags.tag_id
            WHERE
                pub_delete_ind = false AND
                faculty.user_id = %s
                """
            values_p_down = [f"{currentuserid}"]
            cols_p_down = ['Year', 'id', 'Faculty Involved', 'Criteria', 'Title', 'All Authors', 'Start Date', 'End Date', 'Conference',
                      'Location', 'Other Info', 'Last Updated', 'Last Modified By']
            
            if datefilter:
                sql_p_down += """AND (cast (p_year as int) >= %s)"""
                values_p_down += [datefilter]
                if datefilter_u:
                    sql_p_down += """AND (cast (p_year as int) <= %s)"""
                    values_p_down += [datefilter_u]
                    if searchterm:
                        sql_p_down += """ AND (
                            ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                            OR (p_authors ILIKE %s) OR (p_year ILIKE %s) OR (p_conf ILIKE %s)
                            OR (p_loc ILIKE %s) OR (p_add_info ILIKE %s) OR (tag_short_title ILIKE %s)
                            OR (to_char(p_start_date, 'Month DD, YYYY') ILIKE %s) OR (to_char(p_end_date, 'Month DD, YYYY')ILIKE %s)
                            )"""
                        values_p_down += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                                f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%",]
                if searchterm:
                    sql_p_down += """ AND (
                        ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                        OR (p_authors ILIKE %s) OR (p_year ILIKE %s) OR (p_conf ILIKE %s)
                        OR (p_loc ILIKE %s) OR (p_add_info ILIKE %s) OR (tag_short_title ILIKE %s)
                        OR (to_char(p_start_date, 'Month DD, YYYY') ILIKE %s) OR (to_char(p_end_date, 'Month DD, YYYY')ILIKE %s)
                        )"""
                    values_p_down += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                            f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                            f"%{searchterm}%", f"%{searchterm}%",]
                    if datefilter_u:
                        sql_p_down += """AND (cast (p_year as int) <= %s)"""
                        values_p_down += [datefilter_u]
                else:
                    sql_p_down += """"""
                    values_p_down += [] 
            
            elif datefilter_u: 
                sql_p_down += """AND (cast (p_year as int) <= %s)"""
                values_p_down += [datefilter_u]
                if datefilter:
                    sql_p_down += """AND (cast (p_year as int) >= %s)"""
                    values_p_down += [datefilter]
                    if searchterm:
                        sql_p_down += """ AND (
                            ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                            OR (p_authors ILIKE %s) OR (p_year ILIKE %s) OR (p_conf ILIKE %s)
                            OR (p_loc ILIKE %s) OR (p_add_info ILIKE %s) OR (tag_short_title ILIKE %s)
                            OR (to_char(p_start_date, 'Month DD, YYYY') ILIKE %s) OR (to_char(p_end_date, 'Month DD, YYYY')ILIKE %s)
                            )"""
                        values_p_down += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                                f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%",]
                if searchterm:
                    sql_p_down += """ AND (
                        ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                        OR (p_authors ILIKE %s) OR (p_year ILIKE %s) OR (p_conf ILIKE %s)
                        OR (p_loc ILIKE %s) OR (p_add_info ILIKE %s) OR (tag_short_title ILIKE %s)
                        OR (to_char(p_start_date, 'Month DD, YYYY') ILIKE %s) OR (to_char(p_end_date, 'Month DD, YYYY')ILIKE %s)
                        )"""
                    values_p_down += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                            f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                            f"%{searchterm}%", f"%{searchterm}%",]
                    if datefilter:
                        sql_p_down += """AND (cast (p_year as int) >= %s)"""
                        values_p_down += [datefilter]
                        
                else:
                    sql_p_down += """"""
                    values_p_down += [] 
            
            elif searchterm:
                sql_p_down += """ AND (
                    ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                    OR (p_authors ILIKE %s) OR (p_year ILIKE %s) OR (p_conf ILIKE %s)
                    OR (p_loc ILIKE %s) OR (p_add_info ILIKE %s) OR (tag_short_title ILIKE %s)
                    OR (to_char(p_start_date, 'Month DD, YYYY') ILIKE %s) OR (to_char(p_end_date, 'Month DD, YYYY')ILIKE %s)
                    )"""
                values_p_down += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                        f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                        f"%{searchterm}%", f"%{searchterm}%",]
                if datefilter:
                    sql_p_down += """AND (cast (p_year as int) >= %s)"""
                    values_p_down += [datefilter]
                    if datefilter_u:
                        sql_p_down += """AND (cast (p_year as int) <= %s)"""
                        values_p_down += [datefilter_u]
                if datefilter_u:
                        sql_p_down += """AND (cast (p_year as int) <= %s)"""
                        values_p_down += [datefilter_u]
                        if datefilter:
                            sql_p_down += """AND (cast (p_year as int) >= %s)"""
                            values_p_down += [datefilter]
                else:
                    sql_p_down += """"""
                    values_p_down += []     
            else:
                sql_p_down += """"""
                values_p_down += []
                
            sql_p_down += """GROUP BY p_year, publications.pub_id, tags.tag_short_title, pub_title, p_authors, to_char(p_start_date, 'Month DD, YYYY'), 
            to_char(p_end_date, 'Month  DD, YYYY'), p_conf, p_loc, p_add_info
            ORDER BY presentations.p_year DESC"""
            pub_p_down = db.querydatafromdatabase(sql_p_down, values_p_down, cols_p_down)

            download_table_p = dcc.send_data_frame(pub_p_down.to_csv, "mypresentations_download.csv")

            return [download_table_p, n_clicks] ##
        
        elif tab == 'tab_r':
            sql_r_down = """SELECT
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
                to_char(r_start_date, 'Month DD, YYYY'),
                to_char(r_end_date, 'Month DD, YYYY'), 
                r_fund_org,
                to_char(publications.pub_last_upd::timestamp, 'Month DD, YYYY HH24:MI:SS'),
                publications.modified_by
            FROM projects_users
				INNER JOIN projects on projects_users.pub_id = projects.pub_id
                LEFT OUTER JOIN faculty on projects_users.user_id = faculty.user_id
				INNER JOIN publications on projects_users.pub_id = publications.pub_id
                INNER JOIN tags on publications.tag_id = tags.tag_id               
            WHERE
                pub_delete_ind = false AND
                faculty.user_id = %s
                """
            values_r_down = [f"{currentuserid}"]
            cols_r_down = ['Year', 'id', 'Faculty Involved', 'Criteria', 'Title', 'Timeframe', 'Start Date', 'End Date', 'Funding Organization',
                      'Last Updated', 'Last Modified By'] 

            if datefilter:
                sql_r_down += """AND (cast (r_year as int) >= %s)"""
                values_r_down += [datefilter]
                if datefilter_u:
                    sql_r_down += """AND (cast (r_year as int) <= %s)"""
                    values_r_down += [datefilter_u]
                    if searchterm:
                        sql_r_down += """ AND (
                            (r_year ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                            OR (r_timeframe ILIKE %s) OR (r_fund_org ILIKE %s) OR (tag_short_title ILIKE %s)
                            OR ((To_char(r_start_date, 'Month DD, YYYY')) ILIKE %s) OR ((To_char(r_end_date, 'Month DD, YYYY')) ILIKE %s)
                            )"""
                        values_r_down += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                            f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                            ]  
                if searchterm:
                    sql_r_down += """ AND (
                        (r_year ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                        OR (r_timeframe ILIKE %s) OR (r_fund_org ILIKE %s) OR (tag_short_title ILIKE %s)
                        OR ((To_char(r_start_date, 'Month DD, YYYY')) ILIKE %s) OR ((To_char(r_end_date, 'Month DD, YYYY')) ILIKE %s)
                        )"""
                    values_r_down += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                        f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                    ]  
                    if datefilter_u:
                        sql_r_down += """AND (cast (r_year as int) <= %s)"""
                        values_r_down += [datefilter_u]
                else:
                    sql_r_down += """"""
                    values_r_down += [] 
                    
            elif datefilter_u: 
                sql_r_down += """AND (cast (r_year as int) <= %s)"""
                values_r_down += [datefilter_u]
                if datefilter:
                    sql_r_down += """AND (cast (r_year as int) >= %s)"""
                    values_r_down += [datefilter]
                    if searchterm:
                        sql_r_down += """ AND (
                            (r_year ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                            OR (r_timeframe ILIKE %s) OR (r_fund_org ILIKE %s) OR (tag_short_title ILIKE %s)
                            OR ((To_char(r_start_date, 'Month DD, YYYY')) ILIKE %s) OR ((To_char(r_end_date, 'Month DD, YYYY')) ILIKE %s)
                            )"""
                        values_r_down += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
                if searchterm:
                    sql_r_down += """ AND (
                        (r_year ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                        OR (r_timeframe ILIKE %s) OR (r_fund_org ILIKE %s) OR (tag_short_title ILIKE %s)
                        OR ((To_char(r_start_date, 'Month DD, YYYY')) ILIKE %s) OR ((To_char(r_end_date, 'Month DD, YYYY')) ILIKE %s)
                        )"""
                    values_r_down += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                            f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
                    if datefilter:
                        sql_r_down += """AND (cast (r_year as int) >= %s)"""
                        values_r_down += [datefilter]

                else:
                    sql_r_down += """"""
                    values_r_down += [] 
                    
            elif searchterm:
                sql_r_down += """ AND (
                        (r_year ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                        OR (r_timeframe ILIKE %s) OR (r_fund_org ILIKE %s) OR (tag_short_title ILIKE %s)
                        OR ((To_char(r_start_date, 'Month DD, YYYY')) ILIKE %s) OR ((To_char(r_end_date, 'Month DD, YYYY')) ILIKE %s)
                        )"""
                values_r_down += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                        f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                        ]  
                if datefilter:
                    sql_r_down += """AND (cast (r_year as int) >= %s)"""
                    values_r_down += [datefilter]
                    if datefilter_u:
                        sql_r_down += """AND (cast (r_year as int) <= %s)"""
                        values_r_down += [datefilter_u]
                if datefilter_u:
                    sql_r_down += """AND (cast (r_year as int) <= %s)"""
                    values_r_down += [datefilter_u]
                    if datefilter:
                        sql_r_down += """AND (cast (r_year as int) >= %s)"""
                        values_r_down += [datefilter]
                    
                else:
                    sql_r_down += """"""
                    values_r_down += []     
            else:
                sql_r_down += """"""
                values_r_down += []    
            
            sql_r_down += """GROUP BY r_year, publications.pub_id, tags.tag_short_title, pub_title, r_timeframe, to_char(r_start_date, 'Month DD, YYYY'), 
            to_char(r_end_date, 'Month  DD, YYYY'), r_fund_org, r_end_date
            ORDER BY projects.r_year DESC"""
            pub_r_down = db.querydatafromdatabase(sql_r_down, values_r_down, cols_r_down)

            download_table_r = dcc.send_data_frame(pub_r_down.to_csv, "myprojects_download.csv")

            return [download_table_r, n_clicks] ##
        
        elif tab == 'tab_o':
            sql_o_down = """SELECT
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
                    to_char(publications.pub_last_upd::timestamp, 'Month DD, YYYY HH24:MI:SS'),
                    publications.modified_by
                FROM others_users
                    INNER JOIN others on others_users.pub_id = others.pub_id
                    LEFT OUTER JOIN faculty on others_users.user_id = faculty.user_id
                    INNER JOIN publications on others_users.pub_id = publications.pub_id
                    INNER JOIN tags on publications.tag_id = tags.tag_id  
                WHERE
                    pub_delete_ind = false AND
                    faculty.user_id = %s
                """
            values_o_down = [f"{currentuserid}"]
            cols_o_down = ['Year', 'id', 'Faculty Involved [Other Details]', 'Criteria', 'Title', 'Date',  "Last Updated", "Last Modified By"]
                        
            if datefilter:
                sql_o_down += """AND (cast (o_year as int) >= %s)"""
                values_o_down += [datefilter]
                if datefilter_u:
                    sql_o_down += """AND (cast (o_year as int) <= %s)"""
                    values_o_down += [datefilter_u]
                    if searchterm:
                        sql_o_down += """ AND (
                            (o_year ILIKE %s) OR (pub_title ILIKE %s) OR ((To_char(o_date, 'Month DD, YYYY')) ILIKE %s)
                            OR (o_add_info ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (tag_short_title ILIKE %s)
                            )"""
                        values_o_down += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                            f"%{searchterm}%",]
                if searchterm:
                    sql_o_down += """ AND (
                        (o_year ILIKE %s) OR (pub_title ILIKE %s) OR ((To_char(o_date, 'Month DD, YYYY')) ILIKE %s)
                        OR (o_add_info ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (tag_short_title ILIKE %s)
                        )"""
                    values_o_down += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                        f"%{searchterm}%",]
                    if datefilter_u:
                        sql_o_down += """AND (cast (o_year as int) <= %s)"""
                        values_o_down += [datefilter_u]
                else:
                    sql_o_down += """"""
                    values_o_down += [] 
                    
            elif datefilter_u: 
                sql_o_down += """AND (cast (o_year as int) <= %s)"""
                values_o_down += [datefilter_u]
                if datefilter: 
                    sql_o_down += """AND (cast (o_year as int) >= %s)"""
                    values_o_down += [datefilter]
                    if searchterm:
                        sql_o_down += """ AND (
                            (o_year ILIKE %s) OR (pub_title ILIKE %s) OR ((To_char(o_date, 'Month DD, YYYY')) ILIKE %s)
                            OR (o_add_info ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (tag_short_title ILIKE %s)
                            )"""
                        values_o_down += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                            f"%{searchterm}%",]
                if searchterm:
                    sql_o_down += """ AND (
                        (o_year ILIKE %s) OR (pub_title ILIKE %s) OR ((To_char(o_date, 'Month DD, YYYY')) ILIKE %s)
                        OR (o_add_info ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (tag_short_title ILIKE %s)
                        )"""
                    values_o_down += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                        f"%{searchterm}%",]
                    if datefilter: 
                        sql_o_down += """AND (cast (o_year as int) >= %s)"""
                        values_o_down += [datefilter]
                else:
                    sql_o_down += """"""
                    values_o_down += [] 
                    
            elif searchterm:
                sql_o_down += """ AND (
                        (o_year ILIKE %s) OR (pub_title ILIKE %s) OR ((To_char(o_date, 'Month DD, YYYY')) ILIKE %s)
                        OR (o_add_info ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (tag_short_title ILIKE %s)
                        )"""
                values_o_down += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                        f"%{searchterm}%",]
                if datefilter:
                    sql_o_down += """AND (cast (o_year as int) >= %s)"""
                    values_o_down += [datefilter]
                    if datefilter_u:
                        sql_o_down += """AND (cast (o_year as int) <= %s)"""
                        values_o_down += [datefilter_u]
                if datefilter_u:
                    sql_o_down += """AND (cast (o_year as int) <= %s)"""
                    values_o_down += [datefilter_u]
                    if datefilter:
                        sql_o_down += """AND (cast (o_year as int) >= %s)"""
                        values_o_down += [datefilter]
                    
                else:
                    sql_o_down += """"""
                    values_o_down += []    
            else:
                sql_o_down += """"""
                values_o_down += [] 
            
            sql_o_down += """GROUP BY o_year, publications.pub_id, faculty.user_id, tags.tag_short_title, pub_title, to_char(o_date, 'Month YYYY')
            ORDER BY others.o_year DESC"""
            pub_o_down = db.querydatafromdatabase(sql_o_down, values_o_down, cols_o_down)

            download_table_o = dcc.send_data_frame(pub_o_down.to_csv, "my_othermerits_download.csv")

            return [download_table_o, n_clicks]
        else: 
            PreventUpdate

            

            

  
