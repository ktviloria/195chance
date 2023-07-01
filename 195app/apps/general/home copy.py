from dash import dcc
from dash import html
from dash import dash_table
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd
from datetime import date
import plotly.express as px
 
from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        html.Div( 
            [ 
                dcc.Store(id='home_toload', storage_type='memory', data=0), 
            ] 
        ), 
        html.H2("About the Industrial Engineering and Operations Research Department's Publications"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                    html.H5("Publications Tally"), 
                    #html.Br()
                    ],
                    style={"margin-bottom": "15px",  'display': 'flex', 'align-items': 'flex-end', 'min-height': '5vh'}
                ), 
                dbc.Col(
                    html.Div(
                        dcc.Dropdown(
                        id='home_date_filter', clearable=True, searchable=True, placeholder="LOWER YYYY"
                        ),
                        className="dash-bootstrap" 
                    ),
                    #width='20px',
                    style={'max-width': '10%', 'padding-left': '0.5rem', 'padding-right': '0.5rem'}
                    #'flex-grow': '0','flex-basis': '10%'
                ),
                dbc.Col(
                    html.Div(
                        dcc.Dropdown(
                        id='home_date_filter_upper', clearable=True, searchable=True, placeholder="UPPER YYYY"
                        ),
                        className="dash-bootstrap" 
                    ),
                    style={'max-width': '10%', 'padding-left': '0.5rem', 'padding-right': '0.5rem'}
                ),
                
            ]
        ),
        html.Div(id='tallylist'),
        html.Hr(),
        html.H5("Publications Activity This Year"),
        html.Div(id='home_pub_act'),
        html.Hr(),
        html.H5("Summary of Publications Categorized by Publication Type"),
        dbc.Row(
                [
                    # tabs
                    dbc.Col(
                        [
                            dbc.Tabs(
                                [
                                    dbc.Tab(label="Authorships", tab_id="tab_a", label_style={"color": "#800000"}, active_tab_style={'font-weight': 'bold'}),
                                        dbc.Tab(label="Presentations", tab_id="tab_p", label_style={"color": "#800000"}, active_tab_style={'font-weight': 'bold'}),
                                        dbc.Tab(label="Projects", tab_id="tab_r", label_style={"color": "#800000"}, active_tab_style={'font-weight': 'bold'}),
                                        dbc.Tab(label="Others", tab_id="tab_o", label_style={"color": "#800000"}, active_tab_style={'font-weight': 'bold'})
                                ],
                                id='tabs',
                                active_tab='tab_a'
                            ),
                        ],
                        width=8
                    ),
                    # #date filter
                    # dbc.Col(
                    #     html.Div(
                    #         dcc.Dropdown(
                    #         id='home_date_filter', clearable=True, searchable=True, placeholder="YYYY"
                    #         ),
                    #         className="dash-bootstrap" 
                    #     ),
                    #     width=1,
                    # ),
                ],
            ),
        dcc.Graph(id='graph_home')
    ]
)

#date filter callback
@app.callback(
    [
        Output('home_date_filter', 'options'),
        Output('home_date_filter_upper', 'options')
    ],
    [
        Input('url', 'pathname'),
        Input('home_date_filter', 'value')
    ]
) 

def dash_loaddate(pathname, initial_date):
    if pathname == '/home':
        sql_date_filter = """SELECT DISTINCT label, value
            FROM (
                SELECT (a_year) AS label, (a_year) AS value FROM authorships
					inner join publications on publications.pub_id = authorships.pub_id
					where not pub_delete_ind
                UNION
                SELECT (p_year) AS label, (p_year) AS value FROM presentations 
					inner join publications on publications.pub_id = presentations.pub_id
					where not pub_delete_ind
                UNION
                SELECT (r_year) AS label, (r_year) AS value FROM projects
					inner join publications on publications.pub_id = projects.pub_id
					where not pub_delete_ind
                UNION
                SELECT (o_year) AS label, (o_year) AS value FROM others 
					inner join publications on publications.pub_id = others.pub_id
					where not pub_delete_ind
            ) AS subquery
            ORDER BY value DESC
            """
        values_date_filter = []
        cols_date_filter = ['label', 'value']
        date_filter_included = db.querydatafromdatabase(sql_date_filter, values_date_filter, cols_date_filter)
        date_filter_options = date_filter_included.to_dict('records')
        
        if initial_date: 
            sql_date_filter_upper = """SELECT DISTINCT label, value
            FROM (
                SELECT (a_year) AS label, (a_year) AS value FROM authorships
					inner join publications on publications.pub_id = authorships.pub_id
					where not pub_delete_ind
                UNION
                SELECT (p_year) AS label, (p_year) AS value FROM presentations 
					inner join publications on publications.pub_id = presentations.pub_id
					where not pub_delete_ind
                UNION
                SELECT (r_year) AS label, (r_year) AS value FROM projects
					inner join publications on publications.pub_id = projects.pub_id
					where not pub_delete_ind
                UNION
                SELECT (o_year) AS label, (o_year) AS value FROM others 
					inner join publications on publications.pub_id = others.pub_id
					where not pub_delete_ind
            ) AS subquery
            WHERE cast(value as int) >=  %s 
            ORDER BY value DESC
            """
            values_date_filter_upper = [initial_date]
            cols_date_filter_upper = ['label', 'value']
            date_filter_included = db.querydatafromdatabase(sql_date_filter_upper, values_date_filter_upper, cols_date_filter_upper)
            date_filter_upper_options = date_filter_included.to_dict('records')
        else: 
            date_filter_upper_options = date_filter_options
            
    
    else:
        raise PreventUpdate
    
    return [date_filter_options,date_filter_upper_options ]   


#reports generation callback
@app.callback( 
    [
        Output('home_pub_act', 'children'),
        Output('graph_home', 'figure'),
    ], 
    [ 
        Input('url', 'pathname'),
        Input('tabs', 'active_tab'),
        # Input('dash_date_filter', 'value'),
    ]
) 

def home_loadreports(pathname, tab): 
    if pathname == '/home': 
        #publications activity this year query
        sql1 = """ SELECT * from 
            (select
                case
                    when tag_id <=7 then 'authorship'
                end as "pub_type",
                CONCAT(faculty_fn, ' ', faculty_ln) AS full_name,
                a_year as year,
                pub_title
            from publications
            LEFT OUTER JOIN users ON publications.user_id = users.user_id
            LEFT OUTER JOIN faculty ON publications.user_id = faculty.user_id
            left outer join authorships on publications.pub_id = authorships.pub_id where (a_year = '2023' AND pub_delete_ind = false)
			
            
            union all
            
            select
                case
                    when tag_id <=10 then 'presentation'
                end as "pub_type",
                CONCAT(faculty_fn, ' ', faculty_ln) AS full_name,
                p_year,
                pub_title
            from publications
            LEFT OUTER JOIN users ON publications.user_id = users.user_id
            LEFT OUTER JOIN faculty ON publications.user_id = faculty.user_id
            left outer join presentations on publications.pub_id = presentations.pub_id where (p_year = '2023' AND pub_delete_ind = false)
            
            union all
            
            select
                case
                    when tag_id =11 then 'project'
                end as "pub_type",
                CONCAT(faculty_fn, ' ', faculty_ln) AS full_name,
                r_year,
                pub_title
            from publications
            LEFT OUTER JOIN users ON publications.user_id = users.user_id
            LEFT OUTER JOIN faculty ON publications.user_id = faculty.user_id
            left outer join projects on publications.pub_id = projects.pub_id where (r_year = '2023' AND pub_delete_ind = false)
            
            union all
            
            select
                case
                    when tag_id <=13 then 'other'
                end as "pub_type",
                CONCAT(faculty_fn, ' ', faculty_ln) AS full_name,
                o_year,
                pub_title
            from publications
            LEFT OUTER JOIN users ON publications.user_id = users.user_id
            LEFT OUTER JOIN faculty ON publications.user_id = faculty.user_id
            left outer join others on publications.pub_id = others.pub_id  where (o_year = '2023' AND pub_delete_ind = false))
        as pub_act
		""" 
        values1 = [] 
        cols1 = ['Type', 'Faculty Involved', 'Year', 'Title'] 
        pub = db.querydatafromdatabase(sql1, values1, cols1) 
  
        if pub.shape[0]: 
            pub_act = dbc.Table.from_dataframe(pub, striped=True, bordered=True, hover=True, size='sm') 
        else: 
            pub_act = "No publications uploaded this year yet."

        #publication summary graphs
        if tab == 'tab_a':
            sql2= """SELECT distinct (tag) as tag, year, count (pub_id) as publications from
                (select
                    authorships.pub_id AS pub_id,
                    tag_short_title as tag,
				 	a_year as year,
                    publications.tag_id,
                    pub_delete_ind
                from authorships
                LEFT OUTER JOIN publications ON authorships.pub_id = publications.pub_id
                left outer join tags on publications.tag_id = tags.tag_id
                where pub_delete_ind = false
                )
            as tag_summ
            group by tag, tag_id, year
            order by year
            """ 
            values2 = [] 
            cols2 = ['Tag', 'Year', 'Publications'] 

            pub2 = db.querydatafromdatabase(sql2, values2, cols2)
            pub_graph = px.line(pub2, x='Year', y='Publications', color='Tag', title='Authorships')
        
        elif tab == 'tab_p':
            sql2= """SELECT distinct (tag) as tag, year, count (pub_id) as publications from
                (select
                    presentations.pub_id AS pub_id,
                    tag_short_title as tag,
                    p_year as year,
                    publications.tag_id,
                    pub_delete_ind
                from presentations
                LEFT OUTER JOIN publications ON presentations.pub_id = publications.pub_id
                left outer join tags on publications.tag_id = tags.tag_id
                where pub_delete_ind = false
                )
            as tag_summ
            group by tag, tag_id, year
            order by year
            """ 
            values2 = [] 
            cols2 = ['Tag', 'Year', 'Publications'] 

            pub2 = db.querydatafromdatabase(sql2, values2, cols2)
            pub_graph = px.line(pub2, x='Year', y='Publications', color='Tag', title='Presentations')
        
        if tab == 'tab_r':
            sql2= """SELECT distinct (tag) as tag, year, count (pub_id) as publications from
                (select
                    projects.pub_id AS pub_id,
                    tag_short_title as tag,
                    r_year as year,
                    publications.tag_id,
                    pub_delete_ind
                from projects
                LEFT OUTER JOIN publications ON projects.pub_id = publications.pub_id
                left outer join tags on publications.tag_id = tags.tag_id
                where pub_delete_ind = false
                )
            as tag_summ
            group by tag, tag_id, year
            order by year
            """ 
            values2 = [] 
            cols2 = ['Tag', 'Year', 'Publications'] 

            pub2 = db.querydatafromdatabase(sql2, values2, cols2)
            pub_graph = px.line(pub2, x='Year', y='Publications', color='Tag', title='Projects')

                      
        if tab == 'tab_o':
            sql2= """SELECT distinct (tag) as tag, year, count (pub_id) as publications from
                (select
                    others.pub_id AS pub_id,
                    tag_short_title as tag,
                    o_year as year,
                    publications.tag_id,
                    pub_delete_ind
                from others
                LEFT OUTER JOIN publications ON others.pub_id = publications.pub_id
                left outer join tags on publications.tag_id = tags.tag_id
                where pub_delete_ind = false
                )
            as tag_summ
            group by tag, tag_id, year
            order by year
            """ 
            values2 = [] 
            cols2 = ['Tag', 'Year', 'Publications'] 

            pub2 = db.querydatafromdatabase(sql2, values2, cols2)
            pub_graph = px.line(pub2, x='Year', y='Publications', color='Tag', title='Others')

        return [pub_act, pub_graph]
    else:
        raise PreventUpdate
    

#Load Tally
@app.callback (
    [
        Output('tallylist', 'children'), 
        
    ], 
    [
        Input('url', 'pathname'), 
        Input('home_date_filter', 'value'), 
        Input('home_date_filter_upper', 'value')
    ]
)

def loadtallylist (pathname, datefilter, datefilter_u): 
    if pathname == '/home': 
        if datefilter: 
            sqltally = """SELECT 
                faculty_fn || ' ' || faculty_ln AS full_name,
                rank_title,
                COUNT(authorships.pub_id) AS authorships,
                COUNT(presentations.pub_id) AS presentations,
                COUNT(projects.pub_id) AS projects,
                COUNT(others.pub_id) AS others,
                count (publications.pub_id) as publication_count
                
                from faculty
                inner join ranks on ranks.rank_id = faculty.rank_id
                inner join publications on publications.user_id = faculty.user_id
                left outer join authorships on publications.pub_id = authorships.pub_id
                left outer join presentations on publications.pub_id = presentations.pub_id
                left outer join projects on publications.pub_id = projects.pub_id
                left outer join others on publications.pub_id = others.pub_id

            WHERE pub_delete_ind = false AND CAST(COALESCE(a_year, p_year, r_year, o_year)as int) >= %s AND CAST(COALESCE(a_year, p_year, r_year, o_year)as int) <= %s
            group by full_name, rank_title, faculty.user_id
            order by publication_count DESC
            
            """
            values_tally = []
            if datefilter_u: 
                values_tally = [datefilter, datefilter_u]
            else: 
                values_tally = [datefilter, datefilter]
            cols_tally = ['Faculty', 'Rank', 'Authorships', 'Presentations', 'Projects', 'Other Academic Merits', 'Total']
            # sqltally += """HAVING (CAST(COALESCE(a_year, p_year, r_year, o_year) AS varchar) ILIKE %s)
            # order by publication_count DESC"""
            # values_tally += [f"%{datefilter}%"]
            
            
            pubtally = db.querydatafromdatabase(sqltally,values_tally, cols_tally )
        else: 
            sqltally = """SELECT 
                faculty_fn || ' ' || faculty_ln AS full_name,
                rank_title,
                COUNT(authorships.pub_id) AS authorships,
                COUNT(presentations.pub_id) AS presentations,
                COUNT(projects.pub_id) AS projects,
                COUNT(others.pub_id) AS others,
                count (publications.pub_id) as publication_count 
                
                from faculty
                inner join ranks on ranks.rank_id = faculty.rank_id
                inner join publications on publications.user_id = faculty.user_id
                left outer join authorships on publications.pub_id = authorships.pub_id
                left outer join presentations on publications.pub_id = presentations.pub_id
                left outer join projects on publications.pub_id = projects.pub_id
                left outer join others on publications.pub_id = others.pub_id

            WHERE pub_delete_ind = false
            group by full_name, rank_title, faculty.user_id
            order by publication_count DESC
            """
            
            values_tally = []
            cols_tally = ['Faculty', 'Rank', 'Authorships', 'Presentations', 'Projects', 'Other Academic Merits', 'Total']
            pubtally = db.querydatafromdatabase(sqltally,values_tally, cols_tally )
            
        if pubtally.shape[0]: 
            table_tally = dbc.Table.from_dataframe(pubtally, striped=True, bordered=True, hover=True, size='sm', style={"whiteSpace": "pre-line"}) 
        else: 
            table_tally = "No tally to display."
    else: 
        raise PreventUpdate
    return[table_tally]