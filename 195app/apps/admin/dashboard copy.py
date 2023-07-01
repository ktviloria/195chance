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
        dbc.Card(
            [
                dbc.CardHeader(html.H2("Department Insights")), 
                dbc.CardBody(
                    [
                        html.H5("Publications activity this year"),
                        html.Div(id='dash_pub_act'),
                        html.Hr(),
                        html.H5("Departmental Reports to date"),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                                [
                                                    html.H4("Total Publications", className="card-title"),
                                                    html.H5(id='tot_pub'),
                                                ]
                                            ),
                                    ),
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                                [
                                                    html.H4("Active Faculty Members", className="card-title"),
                                                    html.H5(id='tot_fac'),
                                                ]
                                            ),
                                    ),
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                                [
                                                    html.H4("Total Authorships", className="card-title"),
                                                    html.H5(id='tot_a'),
                                                ]
                                            ),
                                    ),
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                                [
                                                    html.H4("Total Presentations", className="card-title"),
                                                    html.H5(id='tot_p'),
                                                ]
                                            ),
                                    ),
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                                [
                                                    html.H4("Total Projects", className="card-title"),
                                                    html.H5(id='tot_r'),
                                                ]
                                            ),
                                    ),
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                                [
                                                    html.H4("Total Other Publications", className="card-title"),
                                                    html.H5(id='tot_o'),
                                                ]
                                            ),
                                    ),
                                ),
                            ]
                        ),
                        html.Hr(),
                        html.H5("See publication summary based on:"),
                        dbc.Row(
                            [
                                #tabs
                                dbc.Col(
                                    [
                                        dbc.Tabs(
                                            [
                                                dbc.Tab(label="Publication Type", tab_id="tab_pubtype", label_style={"color": "#800000"},active_tab_style={'font-weight':'bold'}),
                                                dbc.Tab(label="Faculty Member", tab_id="tab_fac", label_style={"color": "#800000"}, active_tab_style={'font-weight':'bold'}),
                                            ],
                                            id='tabs',
                                            active_tab='tab_pubtype'
                                        ),
                                    ],
                                    width=8
                                ),
                                #date filter
                                dbc.Col(
                                    html.Div(
                                        dcc.Dropdown(
                                        id='dash_date_filter', clearable=True, searchable=True, placeholder="YYYY"
                                        ),
                                        className="dash-bootstrap" 
                                    ),
                                    width=1,
                                ),
                                #faculty filter
                                dbc.Col(
                                    html.Div(
                                        dcc.Dropdown(
                                        id='dash_fac_filter', clearable=True, searchable=True, placeholder="Select Faculty Member"
                                        ),
                                        id='dash_fac_filter_div',
                                        className="dash-bootstrap" 
                                    ),
                                    width=3,   
                                ),
                            ]
                        ),
                        dcc.Graph(id='graph_dash'),
                        html.Hr(),
                    ]
                )
            ]
        )
    ]
) 

#date filter callback
@app.callback(
    [
        Output('dash_date_filter', 'options'),
        Output('dash_fac_filter_div', 'style')
    ],
    [
        Input('url', 'pathname'),
        Input('tabs', 'active_tab'),
    ]
) 
def dash_loaddate(pathname, tab):
    if pathname == '/dashboard':
        sql_date_filter ="""SELECT DISTINCT label, value
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
    
        fac_filter_div = None if tab == 'tab_fac' else {'display':'none'}
    
    else:
        raise PreventUpdate
    
    return [date_filter_options, fac_filter_div]   


#faculty filter callback
@app.callback(
    [
        Output('dash_fac_filter', 'options'),
    ],
    [
        Input('url', 'pathname'),
    ]
) 
def dash_loadfac(pathname):
    if pathname == '/dashboard':
        sql_fac_filter = """SELECT DISTINCT (faculty_fn || ' ' || faculty_ln) as label, (user_id) as value
            FROM faculty
            ORDER BY value ASC"""
        values_fac_filter = []
        cols_fac_filter = ['label', 'value']
        fac_filter_included = db.querydatafromdatabase(sql_fac_filter, values_fac_filter, cols_fac_filter)
        fac_filter_options = fac_filter_included.to_dict('records')
    else:
        raise PreventUpdate
    return [fac_filter_options] 


#department insights callback
@app.callback( 
    [
        Output('dash_pub_act', 'children'),
        Output('graph_dash', 'figure'),
        Output('tot_pub', 'children'),
        Output('tot_fac', 'children'),
        Output('tot_a', 'children'),
        Output('tot_p', 'children'),
        Output('tot_r', 'children'),
        Output('tot_o', 'children'),
    ], 
    [ 
        Input('url', 'pathname'),
        Input('tabs', 'active_tab'),
        Input('dash_date_filter', 'value'),
        Input('dash_fac_filter', 'value'),
    ]
) 

def dash_loadreports(pathname, tab, datefilter, facfilter): 
    if pathname == '/dashboard': 
        #publications activity this year query
        sql1 = """SELECT * from 
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
        if tab == 'tab_pubtype':
            sql2= """SELECT distinct (pub_type) as label, year, count (pub_id) as value from 
                (
                    select authorships.pub_id as pub_id, authorships.a_year as year,
                        case
                            when tag_id <=7 then 'authorship'
                        end as "pub_type"
                    from publications
                    LEFT OUTER JOIN users ON publications.user_id = users.user_id
                    LEFT OUTER JOIN faculty ON publications.user_id = faculty.user_id
                    left outer join authorships on publications.pub_id = authorships.pub_id where pub_delete_ind = false
                    
                    union all
                    
                    select presentations.pub_id as pub_id, presentations.p_year as year,
                        case
                            when tag_id <=10 then 'presentation'
                        end as "pub_type"
                    from publications
                    LEFT OUTER JOIN users ON publications.user_id = users.user_id
                    LEFT OUTER JOIN faculty ON publications.user_id = faculty.user_id
                    left outer join presentations on publications.pub_id = presentations.pub_id where pub_delete_ind = false
                    
                    union all
                    
                    select projects.pub_id as pub_id, projects.r_year as year,  
                        case
                            when tag_id =11 then 'project'
                        end as "pub_type"
                    from publications
                    LEFT OUTER JOIN users ON publications.user_id = users.user_id
                    LEFT OUTER JOIN faculty ON publications.user_id = faculty.user_id
                    left outer join projects on publications.pub_id = projects.pub_id where pub_delete_ind = false
                    
                    union all
                    
                    select others.pub_id as pub_id, others.o_year as year,
                        case
                            when tag_id <=13 then 'other'
                        end as "pub_type"
                    from publications
                    LEFT OUTER JOIN users ON publications.user_id = users.user_id
                    LEFT OUTER JOIN faculty ON publications.user_id = faculty.user_id
                    left outer join others on publications.pub_id = others.pub_id  where pub_delete_ind = false
                )
                as pub_type_summ
                group by pub_type, year
            """ 
            values2 = [] 
            cols2 = ['Type', 'Year', 'Publications'] 

            if datefilter:
                sql2 += """ HAVING (CAST(year AS varchar) ILIKE %s)"""
                values2 += [f"%{datefilter}%"]
                pub2 = db.querydatafromdatabase(sql2, values2, cols2)
                pub_graph = px.bar(pub2, x='Type', y='Publications')
            else:
                sql2 += """order by year"""
                values2 += [] 
                pub2 = db.querydatafromdatabase(sql2, values2, cols2)
                pub_graph = px.line(pub2, x='Year', y='Publications', color='Type')
        
        elif tab == 'tab_fac':
            sql3 = """ SELECT
                distinct (full_name) as faculty, (pub_type) as label, year, count (pub_id) as value
				from 
                (
                    select
                            authorships.pub_id as pub_id,
                            publications.user_id,
                            authorships.a_year as year,
                            CONCAT(faculty_fn, ' ', faculty_ln) AS full_name,
							case
                            	when tag_id <=7 then 'authorship'
                        	end as "pub_type"
                        from publications
                        LEFT OUTER JOIN users ON publications.user_id = users.user_id
                        LEFT OUTER JOIN faculty ON publications.user_id = faculty.user_id
                        left outer join authorships on publications.pub_id = authorships.pub_id where pub_delete_ind = false

                    union all
                    
                    select presentations.pub_id as pub_id,
                        publications.user_id,
                        presentations.p_year as year,
						CONCAT(faculty_fn, ' ', faculty_ln) AS full_name,
                        case
                            when tag_id <=10 then 'presentation'
                        end as "pub_type"
                    from publications
                    LEFT OUTER JOIN users ON publications.user_id = users.user_id
                    LEFT OUTER JOIN faculty ON publications.user_id = faculty.user_id
                    left outer join presentations on publications.pub_id = presentations.pub_id where pub_delete_ind = false
                    
                    union all
                    
                    select projects.pub_id as pub_id,
                        publications.user_id,
                        projects.r_year as year,
						CONCAT(faculty_fn, ' ', faculty_ln) AS full_name,
                        case
                            when tag_id =11 then 'project'
                        end as "pub_type"
                    from publications
                    LEFT OUTER JOIN users ON publications.user_id = users.user_id
                    LEFT OUTER JOIN faculty ON publications.user_id = faculty.user_id
                    left outer join projects on publications.pub_id = projects.pub_id where pub_delete_ind = false
                    
                    union all
                    
                    select others.pub_id as pub_id,
                        publications.user_id,
                        others.o_year as year,
						CONCAT(faculty_fn, ' ', faculty_ln) AS full_name,
                        case
                            when tag_id <=13 then 'other'
                        end as "pub_type"
                    from publications
                    LEFT OUTER JOIN users ON publications.user_id = users.user_id
                    LEFT OUTER JOIN faculty ON publications.user_id = faculty.user_id
                    left outer join others on publications.pub_id = others.pub_id  where pub_delete_ind = false
                )
                as pub_type_summ
				group by full_name, pub_type, user_id, year
            """
            values3 = [] 
            cols3 = ['Faculty', 'Publication Type', 'Year', 'Publication Count' ] 

            #filters
            if datefilter:
                sql3 += """HAVING (CAST(year AS varchar) ILIKE %s)"""
                values3 += [f"%{datefilter}%"]
                pub3 = db.querydatafromdatabase(sql3, values3, cols3)
                if facfilter:
                    sql3 += """ AND (CAST(user_id AS varchar) ILIKE %s)"""
                    values3 += [f"%{facfilter}%"]
                    pub3 = db.querydatafromdatabase(sql3, values3, cols3)
                    pub_graph = px.bar(pub3, x='Publication Type', y='Publication Count')
                    pub_graph.update_xaxes(categoryorder='category ascending')
                else:
                    sql3 += """"""
                    values3 += [] 
                    pub3 = db.querydatafromdatabase(sql3, values3, cols3)
                    pub_graph = px.bar(pub3, x='Publication Type', y='Publication Count', color='Faculty')
                    pub_graph.update_xaxes(categoryorder='category ascending')
                            
            elif facfilter:
                sql3 += """ HAVING (CAST(user_id AS varchar) ILIKE %s)"""
                values3 += [f"%{facfilter}%"]
                pub3 = db.querydatafromdatabase(sql3, values3, cols3)                
                if datefilter:
                    sql3 += """AND (CAST(year AS varchar) ILIKE %s)"""
                    values3 += [f"%{datefilter}%"]
                    pub3 = db.querydatafromdatabase(sql3, values3, cols3)
                    pub_graph = px.bar(pub3, x='Publication Type', y='Publication Count')
                    pub_graph.update_xaxes(categoryorder='category ascending')
                else:
                    sql3 += """"""
                    values3 += [] 
                    pub3 = db.querydatafromdatabase(sql3, values3, cols3)
                    pub_graph = px.bar(pub3, x='Year', y='Publication Count', color='Publication Type')
                    pub_graph.update_xaxes(categoryorder='category ascending')
                 
            else:
                sql3 += """order by year"""
                values3 += []
                pub3 = db.querydatafromdatabase(sql3, values3, cols3)
                pub3 = pub3.sort_values(by='Year')
                pub_graph = px.bar(pub3, x='Year', y='Publication Count', color='Faculty')
       
        #total publications
        sql4 = """ SELECT
				COUNT(pub_id)
            FROM
                publications
			WHERE
				pub_delete_ind = FALSE
        """ 
        values4 = [] 
        cols4 = ['Publications'] 
        pub4 = db.querydatafromdatabase(sql4, values4, cols4) 
        tot_pub = pub4.iat[0,0]

        #total faculty
        sql5 = """ SELECT
				COUNT(user_id)
            FROM
                faculty
			WHERE
				faculty_active_ind = TRUE AND
                faculty_delete_ind = FALSE
        """ 
        values5 = [] 
        cols5 = ['Faculty'] 
        faculty = db.querydatafromdatabase(sql5, values5, cols5) 
        tot_fac = faculty.iat[0,0]

        #total authorships
        sql6 = """ SELECT
				COUNT(authorships.pub_id) AS authorships
            FROM
                publications
                left outer join authorships on publications.pub_id = authorships.pub_id
			WHERE
				pub_delete_ind = FALSE
        """ 
        values6 = [] 
        cols6 = ['Authorships'] 
        authorships = db.querydatafromdatabase(sql6, values6, cols6) 
        tot_a = authorships.iat[0,0]

        #total presentations
        sql7 = """ SELECT
				COUNT(presentations.pub_id) AS others
            FROM
                publications
                left outer join presentations on publications.pub_id = presentations.pub_id
			WHERE
				pub_delete_ind = FALSE
        """ 
        values7 = [] 
        cols7 = ['Presentations'] 
        presentations = db.querydatafromdatabase(sql7, values7, cols7) 
        tot_p = presentations.iat[0,0]

        #total projects
        sql8 = """ SELECT
				COUNT(projects.pub_id) AS projects
            FROM
                publications
                left outer join projects on publications.pub_id = projects.pub_id
			WHERE
				pub_delete_ind = FALSE
        """ 
        values8 = [] 
        cols8 = ['Projects'] 
        projects = db.querydatafromdatabase(sql8, values8, cols8) 
        tot_r = projects.iat[0,0]

        #total others
        sql9 = """ SELECT
				COUNT(others.pub_id) AS others
            FROM
                publications
                left outer join others on publications.pub_id = others.pub_id
			WHERE
				pub_delete_ind = FALSE
        """ 
        values9 = [] 
        cols9 = ['Others'] 
        others = db.querydatafromdatabase(sql9, values9, cols9) 
        tot_o = others.iat[0,0]

        return [pub_act, pub_graph, tot_pub, tot_fac, tot_a, tot_p, tot_r, tot_o]
    else:
        raise PreventUpdate
