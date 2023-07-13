#for viewing all publications of the department
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
                dcc.Store(id='pubdet_toload', storage_type='memory', data=0), 
                dcc.Store(id = 'previous', storage_type='session', data =[]), 
                dcc.Store(id = 'firsttime', storage_type='session', data = 1)
            ],
            # [
            #     html.Button("Download CSV", id="btn_csv"),
            #     dcc.Download(id="download-dataframe-csv"),
            # ] 
        ),
        html.Div('', id = 'modals_holder',  style={'display': 'none'}), 
        dbc.Card(
            [
                dbc.CardHeader(html.H2("Departmental Records")),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                # tabs
                                dbc.Col(
                                    [
                                        dbc.Tabs(
                                            children=[
                                                dbc.Tab(label="Publications", tab_id="tab_a", label_style={"color": "#800000"}, active_tab_style={'font-weight': 'bold'}),
                                                dbc.Tab(label="Presentations", tab_id="tab_p", label_style={"color": "#800000"}, active_tab_style={'font-weight': 'bold'}),
                                                dbc.Tab(label="Projects", tab_id="tab_r", label_style={"color": "#800000"}, active_tab_style={'font-weight': 'bold'}),
                                                dbc.Tab(label="Other Academic Merits", tab_id="tab_o", label_style={"color": "#800000"}, active_tab_style={'font-weight': 'bold'})
                                            ],
                                            id='tabs',
                                            active_tab='tab_a',
                                            #vertical=True
                                        ),
                                    ],
                                    width=7
                                ),
                                #date filter
                                dbc.Col(
                                    html.Div(
                                        [
                                        dbc.FormText("Lower Year", style = {"font-style": "italic"}), 
                                        dcc.Dropdown(id='pubhome_date_filter', clearable=True, searchable=True, placeholder="YYYY"),
                                        ]
                                    ),
                                    className="dash-bootstrap", style={'min-width': '8%', 'padding-left': '0.5rem', 'padding-right': '0.5rem'},
                                ),
                                dbc.Col(
                                    html.Div(
                                        [
                                        dbc.FormText("Upper Year",style = {"font-style": "italic"}), 
                                        dcc.Dropdown(id='pubhome_date_filter_upper', clearable=True, searchable=True, placeholder="YYYY"),  
                                        ]
                                    ),
                                    className="dash-bootstrap", style={'min-width': '8%', 'padding-left': '0.5rem', 'padding-right': '0.5rem'}
                                ),
                                
                                #search filter
                                dbc.Col(
                                    [
                                        dbc.FormText("Search faculty, criteria, title, or any keyword on the table/modal", style = {"font-style": "italic", "font-size":"11px"}), 
                                        dbc.Input(
                                            type="text", id="pub_filter", placeholder="Enter Keyword"
                                        ),
                                    ],
                                    style={'min-width': '22%', 'padding-left': '0.5rem', 'padding-right': '0.5rem'}
                                ),
                            ],
                            className="mb-3",
                        ),
                        #publist
                        html.Div(id='publist')
                    ]
                )
            ]
        )
    ]
)

# df = pd.DataFrame({"a": [1, 2, 3, 4], "b": [2, 1, 5, 6], "c": ["x", "x", "y", "y"]})
# @app.callback(
#     Output("download-dataframe-csv", "data"),
#     Input("btn_csv", "n_clicks"),
#     prevent_initial_call=True,
# )

# def func(n_clicks):
#     return dcc.send_data_frame(df.to_csv, "mydf.csv")

@app.callback(
    [
        Output('pubhome_date_filter', 'options'),
        Output('pubhome_date_filter_upper', 'options')
    ],
    [
        Input('url', 'pathname'),
        Input('tabs', 'active_tab'),
        Input('pubhome_date_filter', 'value'),
    ]
) 

def pubhome_loaddropdown(pathname, tab, initial_date):
    if pathname == '/publications_home':
        if tab == 'tab_a':
            pubhome_sql_date_filter = """SELECT DISTINCT (a_year) as label, (a_year) as value
                                from authorships
                                ORDER BY value DESC"""
        elif tab == 'tab_p':
            pubhome_sql_date_filter = """SELECT DISTINCT (p_year) as label, (p_year) as value
                                from presentations
                                ORDER BY value DESC"""
        elif tab == 'tab_r':
            pubhome_sql_date_filter = """SELECT DISTINCT (r_year) as label, (r_year) as value
                                from projects
                                ORDER BY value DESC"""
        elif tab == 'tab_o':
            pubhome_sql_date_filter = """SELECT DISTINCT (o_year) as label, (o_year) as value
                                from others
                                ORDER BY value DESC"""
        else:
            raise PreventUpdate
        
        pubhome_values_date_filter = []
        pubhome_cols_date_filter = ['label', 'value']
        pubhome_date_filter_included = db.querydatafromdatabase(pubhome_sql_date_filter, pubhome_values_date_filter, pubhome_cols_date_filter)
        pubhome_date_filter_options = pubhome_date_filter_included.to_dict('records')

        if initial_date: 
            if tab == 'tab_a':
                pubhome_sql_date_filter_upper = """SELECT DISTINCT (a_year) as label, (a_year) as value
                                from authorships
                                WHERE cast(a_year as int) >=  %s 
                                ORDER BY value DESC"""
            elif tab == 'tab_p':
                pubhome_sql_date_filter_upper = """SELECT DISTINCT (p_year) as label, (p_year) as value
                                    from presentations
                                    WHERE cast(p_year as int) >=  %s 
                                    ORDER BY value DESC"""
            elif tab == 'tab_r':
                pubhome_sql_date_filter_upper = """SELECT DISTINCT (r_year) as label, (r_year) as value
                                    from projects
                                    WHERE cast(r_year as int) >=  %s 
                                    ORDER BY value DESC"""
            elif tab == 'tab_o':
                pubhome_sql_date_filter_upper = """SELECT DISTINCT (o_year) as label, (o_year) as value
                                    from others
                                    WHERE cast(o_year as int) >=  %s 
                                    ORDER BY value DESC"""
            
            pubhome_values_filter_upper = [initial_date]
            pubhome_cols_date_filter_upper = ['label', 'value']
            
            pubhome_date_filter_included_upper = db.querydatafromdatabase(pubhome_sql_date_filter_upper, pubhome_values_filter_upper, pubhome_cols_date_filter_upper)
            pubome_date_filter_options_upper = pubhome_date_filter_included_upper.to_dict('records')
        else: 
            pubome_date_filter_options_upper = pubhome_date_filter_options
    
    
    
    else:
        raise PreventUpdate
    
    return [pubhome_date_filter_options, pubome_date_filter_options_upper]    


@app.callback(
    [
        Output('publist', 'children'), 
        Output('modals_holder', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('tabs', 'active_tab'),
        Input('pub_filter', 'value'),
        Input('pubhome_date_filter', 'value'), 
        Input('pubhome_date_filter_upper', 'value')
    ]
)

def pubhome_loadpublist(pathname, tab, searchterm, datefilter, datefilter_u):
    if pathname == '/publications_home':
        
        if tab == 'tab_a':
            sql_a = """SELECT  publications.pub_id,
                a_year,
				(select string_agg(lead_author_name, ', ')
				 from pub_lead_authors
				 where pub_lead_authors.pub_id = publications.pub_id
				) as lead_authors,
                publications.pub_title,
                tags.tag_short_title,
				(select string_agg(contributing_author_name, ', ')
				 from pub_contributing_authors
				 where pub_contributing_authors.pub_id = publications.pub_id
				) as contributing_authors,
                To_char(a_date, 'Month YYYY'),
                a_pub_name, 
                a_publisher, 
                a_doi, 
                a_isxn, 
                a_scopus

                FROM authorships
                INNER JOIN publications on authorships.pub_id = publications.pub_id
                LEFT OUTER JOIN pub_lead_authors on authorships.a_lead_id = pub_lead_authors.a_lead_id
				LEFT OUTER JOIN pub_contributing_authors on authorships.a_contributing_id = pub_contributing_authors.a_contributing_id
                LEFT OUTER JOIN tags on publications.tag_id = tags.tag_id
                WHERE publications.pub_delete_ind = false     
                """
    
            values_a = []
            cols_a = ['id', 'Year', 'Lead Author(s)', 'Title', 'Criteria', 'Other Contributing Author(s)', 'Date', 'Publication', 'Publisher', 'DOI','ISXN', 'Scopus'] 
            
            sql_a2 = sql_a
            sql_a2 += """GROUP BY publications.pub_id, a_year, tags.tag_short_title, To_char(a_date, 'Month YYYY'),a_pub_name, a_publisher, 
                a_doi, a_isxn, a_scopus, publications.modified_by, to_char(publications.pub_last_upd::timestamp, 'Month DD YYYY HH24:MI:SS')
            ORDER BY authorships.a_year DESC"""
            
            pub_a2 = db.querydatafromdatabase(sql_a2, values_a, cols_a)
             
            
            #fix additivity of searchterms and filters
            if datefilter:
                sql_a += """AND (cast (a_year as int) >= %s)"""
                values_a += [datefilter]
                if datefilter_u:
                    sql_a += """AND (cast (a_year as int) <= %s)"""
                    values_a += [datefilter_u]
                    if searchterm:
                        sql_a += """ AND (
                    (pub_lead_authors.lead_author_name ILIKE %s) OR (pub_contributing_authors.contributing_author_name ILIKE %s) OR
                    (pub_title ILIKE %s) OR (tag_short_title ILIKE %s) OR (a_year ILIKE %s) OR ((To_char(a_date, 'Month YYYY')) ILIKE %s)
                    OR (a_pub_name ILIKE %s) OR (a_publisher ILIKE %s) OR (a_doi ILIKE %s) OR (a_isxn ILIKE %s) OR (a_scopus ILIKE %s)
                ) """
                        values_a += [f"%{searchterm}%", f"%{searchterm}%",
                                     f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                     f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
                if searchterm:
                    sql_a += """ AND (
                    (pub_lead_authors.lead_author_name ILIKE %s) OR (pub_contributing_authors.contributing_author_name ILIKE %s) OR
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
                    (pub_lead_authors.lead_author_name ILIKE %s) OR (pub_contributing_authors.contributing_author_name ILIKE %s) OR
                    (pub_title ILIKE %s) OR (tag_short_title ILIKE %s) OR (a_year ILIKE %s) OR ((To_char(a_date, 'Month YYYY')) ILIKE %s)
                    OR (a_pub_name ILIKE %s) OR (a_publisher ILIKE %s) OR (a_doi ILIKE %s) OR (a_isxn ILIKE %s) OR (a_scopus ILIKE %s)
                ) """
                        values_a += [f"%{searchterm}%", f"%{searchterm}%",
                                     f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                     f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
                if searchterm:
                    sql_a += """ AND (
                    (pub_lead_authors.lead_author_name ILIKE %s) OR (pub_contributing_authors.contributing_author_name ILIKE %s) OR
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
                    (pub_lead_authors.lead_author_name ILIKE %s) OR (pub_contributing_authors.contributing_author_name ILIKE %s) OR
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
                
            sql_a += """GROUP BY publications.pub_id, a_year, tags.tag_short_title, To_char(a_date, 'Month YYYY'),a_pub_name, a_publisher, 
                a_doi, a_isxn, a_scopus, publications.modified_by, to_char(publications.pub_last_upd::timestamp, 'Month DD YYYY HH24:MI:SS')
            ORDER BY authorships.a_year DESC"""
            pub_a = db.querydatafromdatabase(sql_a, values_a, cols_a)        
            
            modals_a = []
            if pub_a.shape[0]: 
                buttons_a = [] 
                for ids in pub_a['id']: 
                    buttons_a += [
                        html.Div(
                            dbc.Button('View', id = f"modal_button_{ids}", size='sm', color='danger', ), 
                            style={'text-align': 'center'} 
                        ) 
                    ]
                pub_a['More Details'] = buttons_a 
                
            if pub_a2.shape[0]:    
                for i in range(len(pub_a2)): 
                    ids = pub_a2['id'][i]
                    pub_title = pub_a2['Title'][i]
                    pub_lead = pub_a2['Lead Author(s)'][i]
                    pub_category = pub_a2['Criteria'][i]
                    pub_contributing = pub_a2['Other Contributing Author(s)'][i]
                    pub_date = pub_a2['Date'][i]
                    pub_publication = pub_a2['Publication'][i]
                    pub_publisher = pub_a2['Publisher'][i]
                    pub_DOI = pub_a2['DOI'][i]
                    pub_ISXN = pub_a2['ISXN'][i]
                    pub_Scopus = pub_a2['Scopus'][i]
                    
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
                                            html.Strong("Lead Author(s): "),
                                            html.Span(f"{pub_lead}"),], id = f"modal_lead_authors_{ids}"),
                                        html.Div([
                                            html.Strong("Other Contributing Author(s): "),
                                            html.Span(f"{pub_contributing}"),], id = f"modal_contributing_authors_{ids}"),
                                        html.Div([
                                            html.Strong("Publication Category: "), 
                                            html.Span(f"{pub_category}"),], id = f"modal_pub_category_{ids}"
                                        ), 
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

                                ], 
                                id = f"modal_a_{ids}", size ='lg',
                                centered=True, is_open = False
                            ),  id= f'div_modal_{ids}', style={'display': 'none'}
                        )
                    ]
           
            pub_a.drop(['id'],axis=1,inplace=True)
            pub_a.drop(['Date'],axis=1,inplace=True)
            pub_a.drop(['Publication'],axis=1,inplace=True)
            pub_a.drop(['Publisher'],axis=1,inplace=True)
            pub_a.drop(['DOI'],axis=1,inplace=True)
            pub_a.drop(['ISXN'],axis=1,inplace=True)
            pub_a.drop(['Scopus'],axis=1,inplace=True)
            
            if pub_a.shape[0]:
                table_a = dbc.Table.from_dataframe(pub_a, striped=True, bordered=True, hover=True, size='sm', style={"whiteSpace": "pre-line"}) 
            else:
                table_a = "No records to display"
            return [table_a, modals_a]
        
        elif tab == 'tab_p':
            sql_p = """SELECT publications.pub_id,
                p_year,
				(select string_agg(author_name, ', ')
				 from pres_authors
				 where pres_authors.pub_id = publications.pub_id
				) as p_authors,
                publications.pub_title,
                tags.tag_short_title,
                to_char(p_start_date, 'Month DD, YYYY'), 
                to_char(p_end_date, 'Month  DD, YYYY'), 
                p_conf, 
                p_loc, 
                p_add_info
            FROM presentations
                INNER JOIN publications on presentations.pub_id = publications.pub_id
                LEFT OUTER JOIN pres_authors on presentations.p_author_id = pres_authors.p_author_id
                LEFT OUTER JOIN tags on publications.tag_id = tags.tag_id
            WHERE
				publications.pub_delete_ind = false 
            """
            
            values_p = []
            cols_p = ['id', 'Year', 'Presenter(s)', 'Title', 'Criteria', 'Start Date', 'End Date',
                      'Conference', 'Location', 'Other Info']
            
            sql_p2 = sql_p 
            sql_p2 += """GROUP BY publications.pub_id, p_year, pres_authors.author_name, tags.tag_short_title, pub_title,
                    to_char(p_start_date, 'Month DD, YYYY'), to_char(p_end_date, 'Month  DD, YYYY'), p_conf, p_loc, p_add_info
            ORDER BY p_year DESC"""
            
            pub_p2 = db.querydatafromdatabase(sql_p2, values_p, cols_p)

            if datefilter:
                sql_p += """AND (cast (p_year as int) >= %s)"""
                values_p += [datefilter]
                if datefilter_u:
                    sql_p += """AND (cast (p_year as int) <= %s)"""
                    values_p += [datefilter_u]
                    if searchterm:
                        sql_p += """ AND (
                            (pres_authors.author_name ILIKE %s) OR
                            (pub_title ILIKE %s) OR (tag_short_title ILIKE %s) OR (p_year ILIKE %s) OR (to_char(p_start_date, 'Month DD, YYYY') ILIKE %s) OR (to_char(p_end_date, 'Month DD, YYYY')ILIKE %s)
                            OR (p_conf ILIKE %s) OR (p_loc ILIKE %s) OR (p_add_info ILIKE %s) 
                            )
                            """
                        values_p += [f"%{searchterm}%",
                                     f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%",f"%{searchterm}%"]
                if searchterm:
                    sql_p += """ AND (
                            (pres_authors.author_name ILIKE %s) OR
                            (pub_title ILIKE %s) OR (tag_short_title ILIKE %s) OR (p_year ILIKE %s) OR (to_char(p_start_date, 'Month DD, YYYY') ILIKE %s) OR (to_char(p_end_date, 'Month DD, YYYY')ILIKE %s)
                            OR (p_conf ILIKE %s) OR (p_loc ILIKE %s) OR (p_add_info ILIKE %s) 
                            )
                            """
                    values_p += [f"%{searchterm}%",
                                     f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
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
                            (pres_authors.author_name ILIKE %s) OR
                            (pub_title ILIKE %s) OR (tag_short_title ILIKE %s) OR (p_year ILIKE %s) OR (to_char(p_start_date, 'Month DD, YYYY') ILIKE %s) OR (to_char(p_end_date, 'Month DD, YYYY')ILIKE %s)
                            OR (p_conf ILIKE %s) OR (p_loc ILIKE %s) OR (p_add_info ILIKE %s) 
                            )
                            """
                        values_p += [f"%{searchterm}%",
                                     f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%",f"%{searchterm}%"]
                if searchterm:
                    sql_p += """ AND (
                            (pres_authors.author_name ILIKE %s) OR
                            (pub_title ILIKE %s) OR (tag_short_title ILIKE %s) OR (p_year ILIKE %s) OR (to_char(p_start_date, 'Month DD, YYYY') ILIKE %s) OR (to_char(p_end_date, 'Month DD, YYYY')ILIKE %s)
                            OR (p_conf ILIKE %s) OR (p_loc ILIKE %s) OR (p_add_info ILIKE %s) 
                            )
                            """
                    values_p += [f"%{searchterm}%",
                                     f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%",f"%{searchterm}%"]
                    if datefilter:
                        sql_p += """AND (cast (p_year as int) >= %s)"""
                        values_p += [datefilter]
                        
                else:
                    sql_p += """"""
                    values_p += [] 
            
            elif searchterm:
                sql_p += """ AND (
                    (pres_authors.author_name ILIKE %s) OR
                    (pub_title ILIKE %s) OR (tag_short_title ILIKE %s) OR (p_year ILIKE %s)
                ) """
                values_p += [
                    # f"%{searchterm}%", f"%{searchterm}%",
                    f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                    # f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"
                    ]
                if datefilter:
                    sql_p += """AND (cast (p_year as int) >= %s)"""
                    values_p += [datefilter]
                    if datefilter_u:
                        sql_p += """AND (cast (p_year as int) <= %s)"""
                        values_p += [datefilter_u]
                elif datefilter_u:
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
                
            sql_p += """GROUP BY publications.pub_id, p_year, pres_authors.author_name, tags.tag_short_title, pub_title,
                    to_char(p_start_date, 'Month DD, YYYY'), to_char(p_end_date, 'Month  DD, YYYY'), p_conf, p_loc, p_add_info
            ORDER BY p_year DESC"""
            pub_p = db.querydatafromdatabase(sql_p, values_p, cols_p)

            modals_p = []
            if pub_p.shape[0]:
                buttons_p = [] 
                for id in pub_p['id']: 
                    buttons_p += [
                        html.Div(
                            dbc.Button('View', id = f"modal_button_{id}", size='sm', color='danger', ), 
                            style={'text-align': 'center'} 
                        ) 
                    ]
                pub_p['More Details'] = buttons_p
            
            if pub_p2.shape[0]:
                for i in range(len(pub_p2)): 
                    ids = pub_p2['id'][i]
                    pub_title = pub_p2['Title'][i]
                    pres_presenters = pub_p['Presenter(s)'][i]
                    pres_category = pub_p2['Criteria'][i]
                    pres_conf = pub_p2['Conference'][i]
                    pres_start = pub_p2['Start Date'][i]
                    pres_end = pub_p2['End Date'][i]
                    pres_loc = pub_p2['Location'][i]
                    pres_other = pub_p2['Other Info'][i]
                    
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
                                            html.Strong("Presenters: "), 
                                            html.Span(f"{pres_presenters}"),], id = f"modal_pres_presenters_{ids}"),
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
                                id = f"modal_a_{ids}", size ='lg',
                                centered=True, is_open = False
                            ),  id= f'div_modal_{ids}', style={'display': 'none'}
                        )
                    ]

                # for i in range(len(pub_p)): 
                #     pres_details += [("Presented from: %s to %s \n Presented at: %s (%s)" % (pub_p['Start Date'][i], pub_p['End Date'][i], pub_p['Conference'][i], pub_p['Location'][i]) or "No Details Provided")]
                #     other_details += [pub_p['Other Info'][i]] 
            
                # pub_p['Presentation Details'] = pres_details
                # pub_p['Additional Info'] = other_details
                
                
            pub_p.drop(['id'],axis=1,inplace=True)
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
                        ) AS combined_values
                    FROM projects_users
                        INNER JOIN projects on projects_users.pub_id = projects.pub_id
                        LEFT OUTER JOIN faculty on projects_users.user_id = faculty.user_id
                        INNER JOIN publications on projects_users.pub_id = publications.pub_id
                        INNER JOIN tags on publications.tag_id = tags.tag_id
                    WHERE
                        pub_delete_ind = false

                """
            values_r = []
            cols_r = ['Year', 'id', 'Faculty Involved', 'Criteria', 'Title', 'Timeframe', 'Start Date', 'End Date', 'Funding Organization', 'Contract'] 
            
            sql_r2 = sql_r
            sql_r2 +=  """GROUP BY r_year, publications.pub_id, tags.tag_short_title, pub_title, r_timeframe, to_char(r_start_date, 'Month DD, YYYY'), 
            to_char(r_end_date, 'Month  DD, YYYY'), r_fund_org, r_end_date, r_start_date
            ORDER BY projects.r_year DESC"""
            pub_r2 = db.querydatafromdatabase(sql_r2, values_r, cols_r)    
            
            
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
                        values_r += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                            f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"
                            ]  
                if searchterm:
                    sql_r += """ AND (
                        (r_year ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                        OR (r_timeframe ILIKE %s) OR (r_fund_org ILIKE %s) OR (tag_short_title ILIKE %s)
                        OR ((To_char(r_start_date, 'Month DD, YYYY')) ILIKE %s) OR ((To_char(r_end_date, 'Month DD, YYYY')) ILIKE %s)
                        OR (projects_users.r_roles ILIKE %s))"""
                    values_r += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                        f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"
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
                        values_r += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
                                f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%" , f"%{searchterm}%"]
                if searchterm:
                    sql_r += """ AND (
                        (r_year ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
                        OR (r_timeframe ILIKE %s) OR (r_fund_org ILIKE %s) OR (tag_short_title ILIKE %s)
                        OR ((To_char(r_start_date, 'Month DD, YYYY')) ILIKE %s) OR ((To_char(r_end_date, 'Month DD, YYYY')) ILIKE %s)
                        OR (projects_users.r_roles ILIKE %s))"""
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
                        OR (r_timeframe ILIKE %s) OR (r_fund_org ILIKE %s) OR (tag_short_title ILIKE %s)
                        OR ((To_char(r_start_date, 'Month DD, YYYY')) ILIKE %s) OR ((To_char(r_end_date, 'Month DD, YYYY')) ILIKE %s)
                        OR (projects_users.r_roles ILIKE %s))"""
                values_r += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
                        f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"
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
                

                for id in pub_r['id']: 
                    buttons_r += [
                        html.Div(
                            dbc.Button('View', id = f"modal_button_{id}", size='sm', color='danger', ), 
                            style={'text-align': 'center'} 
                        ) 
                    ]
                pub_r['More Details'] = buttons_r
            
            if pub_r2.shape[0]:
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
                                id = f"modal_a_{ids}", size ='lg',
                                centered=True, is_open = False
                            ),  id= f'div_modal_{ids}', style={'display': 'none'}
                        )
                    ]

                

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
                        to_char(o_date, 'Month YYYY')
                    FROM others_users
                        INNER JOIN others on others_users.pub_id = others.pub_id
                        LEFT OUTER JOIN faculty on others_users.user_id = faculty.user_id
                        INNER JOIN publications on others_users.pub_id = publications.pub_id
                        INNER JOIN tags on publications.tag_id = tags.tag_id  
                    WHERE
                        pub_delete_ind = false
                """
            values_o = []
            cols_o = ['Year', 'id', 'Faculty Involved', 'Criteria', 'Title', 'Date'] 
            
            sql_o2 = sql_o
            sql_o2 += """GROUP BY o_year, publications.pub_id,  tags.tag_short_title, pub_title, to_char(o_date, 'Month YYYY')
            ORDER BY others.o_year DESC"""
            
            pub_o2 = db.querydatafromdatabase(sql_o2, values_o, cols_o)
            
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
                

                for id in pub_o['id']: 
                    buttons_o += [
                        html.Div(
                            dbc.Button('View', id = f"modal_button_{id}", size='sm', color='danger' ), 
                            style={'text-align': 'center'} 
                        ) 
                    ]
                pub_o['More Details'] = buttons_o
                
            if pub_o2.shape[0]:
                
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
                                id = f"modal_a_{ids}", size ='lg',
                                centered=True, is_open = False
                            ),  id= f'div_modal_{ids}', style={'display': 'none'}
                        )
                    ]
                

            pub_o.drop(['id'],axis=1,inplace=True)
            pub_o.drop(['Date'],axis=1,inplace=True)

            if pub_o.shape[0]:
                table_o = dbc.Table.from_dataframe(pub_o, striped=True, bordered=True, hover=True, size='sm', style={"whiteSpace": "pre-line"}) 
                
            else:
                table_o = "No records to display."
            return [table_o, modals_o]    
             
    else: 
        raise PreventUpdate      

sql_aa = """SELECT
        publications.pub_id
    FROM publications
    WHERE
        pub_delete_ind = false
    
    """
values_aa = []
cols_aa = ['id'] 

pub_aa = db.querydatafromdatabase(sql_aa, values_aa, cols_aa)


for ids in pub_aa['id']: 
    modal_a = f"modal_a_{ids}"
    modal_button = f"modal_button_{ids}"
    modal_close = f'modal_close_{ids}'
    div_modal = f'div_modal_{ids}'
    @app.callback(
        
        Output(modal_a, 'is_open'), 
        
        [
            Input(modal_button, 'n_clicks'), 
        ], 
        [
            State(modal_button, 'is_open')
        ]
    )
    
    def ihopethisworks(n_clicks, open): 
        if n_clicks: 
            return True
        else: 
            return False

# @app.callback (
#     [
#         Output('previous', 'data'), 
#         Output('firsttime', 'data')
        
#     ], 
#     [
#         Input('url', 'pathname'), 
#     ], 
#     [
#         State('previous', 'data'), 
#         State('firsttime', 'data')
#     ]
# )
# def modalloadwhen(pathname, previous, firsttime): 
#     if pathname == '/publications_home': 
    
#         sql_aa = """SELECT
#                 publications.pub_id
                
#                 FROM publications
#                 WHERE
#                     pub_delete_ind = false
                
#                 """
#         values_aa = []
#         cols_aa = ['id'] 

#         pub_aa = db.querydatafromdatabase(sql_aa, values_aa, cols_aa)
#         pub_aa_list = pub_aa['id'].tolist()
        
#         if firsttime == 1: 
#             pub_aa_list = pub_aa['id'].tolist()
#             previous = pub_aa_list
#             subtracted  = pub_aa_list
            
#         else: 
#             subtracted  = list(set(pub_aa_list)^ set(previous))
#             previous = pub_aa_list + subtracted
        
        
#         firsttime += 1
        
#         for ids in subtracted: 
            
#             modal_a = f"modal_a_{ids}"
#             modal_button = f"modal_button_{ids}"
#             div_modal = f'div_modal_{ids}'
#             @app.callback(
                
#                 Output( f"modal_a_{ids}", 'is_open'), 
                
#                 [
#                     Input(f"modal_button_{ids}", 'n_clicks'), 
#                     # Input(modal_close, 'n_clicks')
#                 ], 
#                 [
#                     State(f"modal_button_{ids}", 'is_open')
#                 ]
#             )
            
#             def ihopethisworks(n_clicks, open): 
#                 if n_clicks: 
#                     return True
#                 else: 
#                     return False
        
#     return[previous, firsttime]
    