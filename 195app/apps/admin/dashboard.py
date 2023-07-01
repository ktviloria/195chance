from dash import dcc
from dash import html
from dash import dash_table
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd
from datetime import date
import datetime
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
                        html.H5("Academic Research and Faculty Activity for the Year"),
                        html.Div(id='dash_pub_act'),
                        html.Hr(),
                        html.H5("Departmental Reports to Date"),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                                [
                                                    html.H4("Total Academic Research and Faculty Activity", className="card-title"),
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
                                                    html.H4("Total Publications", className="card-title"),
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
                                                    html.H4("Total Other Academic Merits", className="card-title"),
                                                    html.H5(id='tot_o'),
                                                ]
                                            ),
                                    ),
                                ),
                            ]
                        ),
                        html.Hr(),
                        html.H5("See Academic Research and Faculty Activity Summary based on:"),
                        dbc.Row(
                            [
                                #tabs
                                dbc.Col(
                                    [
                                        dbc.Tabs(
                                            [
                                                dbc.Tab(label="Type", tab_id="tab_pubtype", label_style={"color": "#800000"},active_tab_style={'font-weight':'bold'}),
                                                dbc.Tab(label="Faculty Members", tab_id="tab_fac", label_style={"color": "#800000"}, active_tab_style={'font-weight':'bold'}),
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
                                        [
                                        dbc.FormText("Academic Year",  style = {"font-style": "italic"}),
                                        dcc.Dropdown(id='dash_date_filter', clearable=True, searchable=True, placeholder="YYYY"),
                                        ]
                                    ), className="dash-bootstrap", width=1,
                                ),
                                #faculty filter
                                dbc.Col(
                                    html.Div(
                                        [
                                        dbc.FormText("Faculty Member",  style = {"font-style": "italic"}),
                                        dcc.Dropdown(id='dash_fac_filter', clearable=True, searchable=True, placeholder="Select"),
                                        
                                        ], id='dash_fac_filter_div', className="dash-bootstrap" 
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
            (
            select
                case
                    when tag_id <=7 then 'Publications'
                end as "pub_type",
                string_agg(faculty_fn || ' ' ||faculty_ln, ' , ') AS full_name,
                a_year as year,
                pub_title
            from authorships_users 
            LEFT OUTER JOIN users ON authorships_users.user_id = users.user_id
            LEFT OUTER JOIN publications ON authorships_users.pub_id = publications.pub_id
			LEFT OUTER JOIN faculty ON authorships_users.user_id = faculty.user_id
            left outer join authorships on publications.pub_id = authorships.pub_id where (pub_delete_ind = false)
			GROUP BY  publications.tag_id,  a_year, pub_title, authorships_users.pub_id
			
            
            union all
            
            select
                case
                    when tag_id <=10 then 'Presentations'
                end as "pub_type",
                string_agg(faculty_fn || ' ' ||faculty_ln, ' , ') AS full_name,
                p_year as year ,
                pub_title
            from presentations_users
			LEFT OUTER JOIN users ON presentations_users.user_id = users.user_id
            LEFT OUTER JOIN publications ON presentations_users.pub_id = publications.pub_id
            LEFT OUTER JOIN faculty ON presentations_users.user_id = faculty.user_id
            left outer join presentations on publications.pub_id = presentations.pub_id where (pub_delete_ind = false)
			GROUP BY  publications.tag_id,  p_year, pub_title, presentations_users.pub_id
            
            
            union all
            
            select
                case
                    when tag_id =11 then 'Projects'
                end as "pub_type",
                string_agg(faculty_fn || ' ' || faculty_ln, ' , ') AS full_name,
                r_year as year ,
                pub_title
            from projects_users
            LEFT OUTER JOIN users ON projects_users.user_id = users.user_id
            LEFT OUTER JOIN publications ON projects_users.pub_id = publications.pub_id
            LEFT OUTER JOIN faculty ON projects_users.user_id = faculty.user_id
            LEFT OUTER JOIN projects ON publications.pub_id = projects.pub_id where (pub_delete_ind = false)
            GROUP BY publications.tag_id, r_year, pub_title, projects_users.pub_id
                    
            union all
            
            select
                case
                    when tag_id <=13 then 'Other Academic Merits'
                end as "pub_type",
                string_agg(faculty_fn || ' ' ||faculty_ln, ' , ') AS full_name,
                o_year as year,
                pub_title
            from others_users
            LEFT OUTER JOIN users ON others_users.user_id = users.user_id
            LEFT OUTER JOIN publications ON others_users.pub_id = publications.pub_id
            LEFT OUTER JOIN faculty ON others_users.user_id = faculty.user_id
            left outer join others on others_users.pub_id = others.pub_id  where (pub_delete_ind = false)
            GROUP BY publications.tag_id, o_year, pub_title, others_users.pub_id) 
            
        as pub_act
		""" 
        values1 = [] 
        cols1 = ['Type', 'Faculty Involved', 'Year', 'Title'] 
        pub = db.querydatafromdatabase(sql1, values1, cols1) 
        
        pub['Year'] = pd.to_numeric(pub['Year'])
        pub['Year'] = pub['Year'].round(decimals = 0)
        
        today = datetime.date.today()
        today_year = today.year
        maxyear = max((pub['Year']))
        
        for i in range(len(pub)): 
            if pub['Year'][i] != today_year:
                
                pub = pub.drop(i)
        
        
        
  
        if pub.shape[0]: 
            pub_act = dbc.Table.from_dataframe(pub, striped=True, bordered=True, hover=True, size='sm') 
        else: 
            pub_act = "No academic research and activity uploaded this year yet."

        #publication summary graphs
        if tab == 'tab_pubtype':
            sql2= """SELECT distinct (pub_type) as label, year, count (pub_id) as value from 
                (
                    select DISTINCT (authorships_users.pub_id)as pub_id, authorships.a_year as year,
						case
							when tag_id <=7 then 'Publication'
						end as "pub_type"
					from authorships_users
					LEFT OUTER JOIN publications on authorships_users.pub_id = publications.pub_id
					LEFT OUTER JOIN faculty ON authorships_users.user_id = faculty.user_id
					left outer join authorships on publications.pub_id = authorships.pub_id 
					where pub_delete_ind = false
                    
                    union all
                    
                    select DISTINCT (presentations_users.pub_id) as pub_id, presentations.p_year as year,
                        case
                            when tag_id <=10 then 'presentation'
                        end as "pub_type"
                    from presentations_users
					LEFT OUTER JOIN publications on presentations_users.pub_id = publications.pub_id
                    LEFT OUTER JOIN users ON presentations_users.user_id = users.user_id
                    LEFT OUTER JOIN faculty ON presentations_users.user_id = faculty.user_id
                    left outer join presentations on publications.pub_id = presentations.pub_id where pub_delete_ind = false
                    
                    union all
                    
                    select DISTINCT (projects_users.pub_id) as pub_id, projects.r_year as year,  
                        case
                            when tag_id =11 then 'project'
                        end as "pub_type"
                    from projects_users
                    LEFT OUTER JOIN publications on projects_users.pub_id = publications.pub_id
                    LEFT OUTER JOIN users ON projects_users.user_id = users.user_id
                    LEFT OUTER JOIN faculty ON projects_users.user_id = faculty.user_id
                    left outer join projects on publications.pub_id = projects.pub_id where pub_delete_ind = false
                    
                    union all
                    
                    select DISTINCT (others_users.pub_id) as pub_id, others.o_year as year,
                        case
                            when tag_id <=13 then 'other academic merits'
                        end as "pub_type"
                    from others_users
                    LEFT OUTER JOIN publications on others_users.pub_id = publications.pub_id
                    LEFT OUTER JOIN users ON others_users.user_id = users.user_id
                    LEFT OUTER JOIN faculty ON others_users.user_id = faculty.user_id
                    left outer join others on publications.pub_id = others.pub_id  where pub_delete_ind = false
                )
                as pub_type_summ
                group by pub_type, year
            """ 
            values2 = [] 
            cols2 = ['Type', 'Year', 'No. of Academic Research and Faculty Activity'] 

            if datefilter:
                sql2 += """ HAVING (CAST(year AS varchar) ILIKE %s)"""
                values2 += [f"%{datefilter}%"]
                pub2 = db.querydatafromdatabase(sql2, values2, cols2)
                pub_graph = px.bar(pub2, x='Type', y='No. of Academic Research and Faculty Activity', title='Academic Research and Faculty Activity per Type for Selected Year')
            else:
                sql2 += """order by year"""
                values2 += [] 
                pub2 = db.querydatafromdatabase(sql2, values2, cols2)
                pub_graph = px.line(pub2, x='Year', y='No. of Academic Research and Faculty Activity', color='Type', title='Academic Research and Faculty Activity Through the Years')
        
        elif tab == 'tab_fac':
            sql3 = """ SELECT
                distinct (full_name) as faculty, (pub_type) as label, year, count (pub_id) as value
				from 
                (
                    select
							authorships_users.pub_id as pub_id,
                            authorships_users.user_id,
                            authorships.a_year as year,
                            CONCAT(faculty_fn, ' ', faculty_ln) AS full_name,
							case
                            	when tag_id <=7 then 'Publication'
                        	end as "pub_type"
                        from authorships_users
						LEFT OUTER JOIN publications ON authorships_users.pub_id = publications.pub_id 
                        LEFT OUTER JOIN faculty ON authorships_users.user_id = faculty.user_id
                        left outer join authorships on authorships_users.pub_id = authorships.pub_id where pub_delete_ind = false

                    union all
                    
                    select presentations_users.pub_id as pub_id,
                        presentations_users.user_id,
                        presentations.p_year as year,
						CONCAT(faculty_fn, ' ', faculty_ln) AS full_name,
                        case
                            when tag_id <=10 then 'Presentation'
                        end as "pub_type"
                    from presentations_users
					LEFT OUTER JOIN publications on presentations_users.pub_id = publications.pub_id
                    LEFT OUTER JOIN faculty ON presentations_users.user_id = faculty.user_id
                    left outer join presentations on presentations_users.pub_id = presentations.pub_id where pub_delete_ind = false
                    
                    union all
                    
                    select projects_users.pub_id as pub_id,
                        projects_users.user_id,
                        projects.r_year as year,
						CONCAT(faculty_fn, ' ', faculty_ln) AS full_name,
                        case
                            when tag_id =11 then 'Project'
                        end as "pub_type"
                    from projects_users
                    LEFT OUTER JOIN publications on projects_users.pub_id = publications.pub_id
                    LEFT OUTER JOIN faculty ON projects_users.user_id = faculty.user_id
                    left outer join projects on projects_users.pub_id = projects.pub_id where pub_delete_ind = false

                    union all
                    
                    select others_users.pub_id as pub_id,
                        others_users.user_id,
                        others.o_year as year,
						CONCAT(faculty_fn, ' ', faculty_ln) AS full_name,
                        case
                            when tag_id <=13 then 'Other Academic Merits'
                        end as "pub_type"
                    from others_users
                    LEFT OUTER JOIN publications ON others_users.pub_id = publications.pub_id
                    LEFT OUTER JOIN faculty ON others_users.user_id = faculty.user_id
                    left outer join others on others_users.pub_id = others.pub_id  where pub_delete_ind = false
                )
                as pub_type_summ
				group by full_name, pub_type, user_id, year
            """
            values3 = [] 
            cols3 = ['Faculty', 'Type', 'Year', 'No. of Academic Research and Faculty Activity' ] 

            #filters
            if datefilter:
                sql3 += """HAVING (CAST(year AS varchar) ILIKE %s)"""
                values3 += [f"%{datefilter}%"]
                pub3 = db.querydatafromdatabase(sql3, values3, cols3)
                if facfilter:
                    sql3 += """ AND (CAST(user_id AS varchar) ILIKE %s)"""
                    values3 += [f"%{facfilter}%"]
                    pub3 = db.querydatafromdatabase(sql3, values3, cols3)
                    pub_graph = px.bar(pub3, x='Type', y='No. of Academic Research and Faculty Activity', title = 'Academic Research and Faculty Activity per Type for Selected Year and Faculty')
                    pub_graph.update_xaxes(categoryorder='category ascending')
                else:
                    sql3 += """"""
                    values3 += [] 
                    pub3 = db.querydatafromdatabase(sql3, values3, cols3)
                    pub_graph = px.bar(pub3, x='Type', y='No. of Academic Research and Faculty Activity', color='Faculty', title = 'Academic Research and Faculty Activity per Type for for Selected Year')
                    pub_graph.update_xaxes(categoryorder='category ascending')
                            
            elif facfilter:
                sql3 += """ HAVING (CAST(user_id AS varchar) ILIKE %s)"""
                values3 += [f"%{facfilter}%"]
                pub3 = db.querydatafromdatabase(sql3, values3, cols3)                
                if datefilter:
                    sql3 += """AND (CAST(year AS varchar) ILIKE %s)"""
                    values3 += [f"%{datefilter}%"]
                    pub3 = db.querydatafromdatabase(sql3, values3, cols3)
                    pub_graph = px.bar(pub3, x='Type', y='No. of Academic Research and Faculty Activity', title = 'Academic Research and Faculty Activity per Type for Selected Faculty and Year')
                    pub_graph.update_xaxes(categoryorder='category ascending')
                else:
                    sql3 += """"""
                    values3 += [] 
                    pub3 = db.querydatafromdatabase(sql3, values3, cols3)
                    pub_graph = px.bar(pub3, x='Year', y='No. of Academic Research and Faculty Activity', color='Type', title = 'Academic Research and Faculty Activity per Type for Selected Faculty')
                    pub_graph.update_xaxes(categoryorder='category ascending')
                 
            else:
                sql3 += """order by year"""
                values3 += []
                pub3 = db.querydatafromdatabase(sql3, values3, cols3)
                pub3 = pub3.sort_values(by='Year')
                pub_graph = px.bar(pub3, x='Year', y='No. of Academic Research and Faculty Activity', color='Faculty', title = 'Academic Research and Faculty Activity Through the Years')
       
        #total publications CARDS
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