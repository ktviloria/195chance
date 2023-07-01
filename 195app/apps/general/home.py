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
        html.Div( 
            [ 
                dcc.Store(id='home_toload', storage_type='memory', data=0), 
            ] 
        ), 
        html.H2("", id ='welcomemessage'),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                    html.H4("IEORD Research and Activity Tally"), 
                    #html.Br()
                    ],
                    style={'display': 'flex', 'align-items': 'center', 'max-height': '10vh'}
                ), 
                dbc.Col(
                    html.Div(
                        [
                        dbc.FormText("Lower Year", style = {"font-style": "italic"}), 
                        dcc.Dropdown(
                        id='home_date_filter', clearable=True, searchable=True, placeholder="YYYY"
                        ),
                         
                    ]),
                    className="dash-bootstrap",
                    style={'max-width': '10%', 'padding-left': '0.5rem', 'padding-right': '0.5rem'}
                ),
                dbc.Col(
                    html.Div([
                        dbc.FormText("Upper Year",style = {"font-style": "italic"}),
                        dcc.Dropdown(
                        id='home_date_filter_upper', clearable=True, searchable=True, placeholder="YYYY"
                        ),                       
                    ]), className="dash-bootstrap",
                    style={'max-width': '10%', 'padding-left': '0.5rem', 'padding-right': '0.5rem'}
                ),
                
            ]
        ),
        html.Hr(),
        html.Div(id='tallylist'),
        html.Hr(),
        html.H5("Academic Research and Faculty Activity for the Year"),
        html.Div(id='home_pub_act'),
        html.Hr(),
        html.H5("Summary of Academic Research and Activity Categorized by Type"),
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

@app.callback (
    Output('welcomemessage', 'children'), 
    [
        Input('url', 'pathname')
    ], 
    [
        State('currentuserid', 'data')
    ]
)

def welcome_message (pathname, currentuserid ): 
    if pathname == '/home': 
        if currentuserid > 3: 
            message_sql = """SELECT
            faculty_fn 
            FROM faculty 
            where faculty.user_id = %s
            """
            val = [currentuserid]
            col = ['name']
            name_db = db.querydatafromdatabase(message_sql,val,col)
            
            name = name_db['name'][0]
            message = html.Div([
                html.Span('Hi, '), 
                html.Em(f"{name}"), 
                html.Em('!')
            ]   
            )
        else: 
            message = html.Div([
                html.Span('Hi, '), 
                html.Em("admin!")
            ]   
            )
        return[message]
    else: 
        raise PreventUpdate
            
              




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
    ], 
    [
        State('currentuserid', 'data')
    ]
) 

def home_loadreports(pathname, tab, currentuserid): 
    if pathname == '/home': 
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
            
            union 
            
            
            
            select
                case
                    when tag_id =11 then 'Projects'
                end as "pub_type",
                string_agg(faculty_fn || ' ' ||faculty_ln, ' , ') AS full_name,
                r_year,
                pub_title
            from projects_users
            LEFT OUTER JOIN publications ON projects_users.pub_id = publications.pub_id
            LEFT OUTER JOIN users ON projects_users.user_id = users.user_id
            LEFT OUTER JOIN faculty ON projects_users.user_id = faculty.user_id
            left outer join projects on publications.pub_id = projects.pub_id where (pub_delete_ind = false)
            GROUP BY  publications.tag_id,  r_year, pub_title, projects_users.pub_id

            union all
            
            select
                case
                    when tag_id <=13 then 'Other Academic Merits'
                end as "pub_type",
                string_agg(faculty_fn || ' ' ||faculty_ln, ' , ') AS full_name,
                o_year,
                pub_title
            from others_users
            LEFT OUTER JOIN publications ON others_users.pub_id = publications.pub_id
            LEFT OUTER JOIN users ON others_users.user_id = users.user_id
            LEFT OUTER JOIN faculty ON others_users.user_id = faculty.user_id
            left outer join others on publications.pub_id = others.pub_id  where (pub_delete_ind = false)
            GROUP BY  publications.tag_id,  o_year, pub_title, others_users.pub_id
            
            )as pub_act
            
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
        if tab == 'tab_a':
            sql2= """SELECT distinct (tag) as tag, year, count (pub_id) as publications from
                (select
     			    DISTINCT( authorships_users.pub_id)AS pub_id,
                    tag_short_title as tag,
				 	a_year as year,
                    publications.tag_id,
                    pub_delete_ind
                from authorships_users
				LEFT OUTER JOIN authorships ON authorships_users.pub_id = authorships.pub_id
                LEFT OUTER JOIN publications ON authorships_users.pub_id = publications.pub_id
                left outer join tags on publications.tag_id = tags.tag_id
                where pub_delete_ind = false
                )
            as tag_summ
            group by tag, tag_id, year
            order by year
            """ 
            values2 = [] 
            cols2 = ['Criteria', 'Year', 'No. of Publications'] 
            

            pub2 = db.querydatafromdatabase(sql2, values2, cols2)
            pub_graph = px.line(pub2, x='Year', y='No. of Publications', color='Criteria', title='Academic Publications per Year')
        
        elif tab == 'tab_p':
            sql2 = """SELECT distinct (tag) as tag, year, count (pub_id) as publications from
                (select
                    DISTINCT(presentations_users.pub_id) AS pub_id,
                    tag_short_title as tag,
                    p_year as year,
                    publications.tag_id,
                    pub_delete_ind
                from presentations_users
				LEFT OUTER JOIN presentations ON presentations_users.pub_id = presentations.pub_id
                LEFT OUTER JOIN publications ON presentations_users.pub_id = publications.pub_id
                left outer join tags on publications.tag_id = tags.tag_id
                where pub_delete_ind = false
                )
            as tag_summ
            group by tag, tag_id, year
            order by year
            """
            
    
            values2 = [] 
            
            cols2 = ['Criteria', 'Year', 'No. of Presentations'] 

            pub2 = db.querydatafromdatabase(sql2, values2, cols2)
            pub_graph = px.line(pub2, x='Year', y='No. of Presentations', color='Criteria', title='Academic Presentations per Year')
        
        if tab == 'tab_r':
            sql2= """SELECT distinct (tag) as tag, year, count (pub_id) as publications from
                (select
                    DISTINCT( projects_users.pub_id) AS pub_id,
                    tag_short_title as tag,
                    r_year as year,
                    publications.tag_id,
                    pub_delete_ind
                from projects_users
                LEFT OUTER JOIN projects ON projects_users.pub_id = projects.pub_id
                LEFT OUTER JOIN publications ON projects.pub_id = publications.pub_id
                left outer join tags on publications.tag_id = tags.tag_id
                where pub_delete_ind = false
                )
            as tag_summ
            group by tag, tag_id, year
            order by year
            """ 
            values2 = [] 
            cols2 = ['Criteria', 'Year', 'No. of Projects'] 
            

            pub2 = db.querydatafromdatabase(sql2, values2, cols2)
            pub_graph = px.line(pub2, x='Year', y='No. of Projects', color='Criteria', title='Projects per Year')

                      
        if tab == 'tab_o':
            sql2= """SELECT distinct (tag) as tag, year, count (pub_id) as publications from
                (select
                    DISTINCT(others_users.pub_id) as pub_id,
                    tag_short_title as tag,
                    o_year as year,
                    publications.tag_id,
                    pub_delete_ind
                from others_users
                LEFT OUTER JOIN others on others_users.pub_id = others.pub_id
                LEFT OUTER JOIN publications ON others.pub_id = publications.pub_id
                left outer join tags on publications.tag_id = tags.tag_id
                where pub_delete_ind = false
                )
            as tag_summ
            group by tag, tag_id, year
            order by year
            
            """ 
            values2 = [] 
            cols2 = ['Criteria', 'Year', 'No. of Other Academic Merits'] 

            pub2 = db.querydatafromdatabase(sql2, values2, cols2)
            pub_graph = px.line(pub2, x='Year', y='No. of Other Academic Merits', color='Criteria', title='Other Academic Merits per Year')

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
    ], 
    [
        State('currentuserid', 'data')
    ]
)

def loadtallylist (pathname, datefilter, datefilter_u, currentuserid): 
    if pathname == '/home': 
        if datefilter: 
            sqltally = """SELECT COALESCE(authors.full_name, pres.full_name, proj.full_name, other.full_name), 
                COALESCE(authors.fac_rank, pres.fac_rank, proj.fac_rank, other.fac_rank), 
                authors.Publications, pres.PRESENTATIONS, proj.projects, other.other

                FROM 
                    (SELECT 
                        faculty.user_id as authors_fac, 
                        faculty_fn || ' ' || faculty_ln AS full_name ,
                        rank_title as fac_rank, 

                        COUNT(distinct(authorships_users.user_id ,  authorships_users.pub_id)) 
                        as Publications

                        from authorships_users
                        INNER JOIN faculty on authorships_users.user_id = faculty.user_id 
                        INNER JOIN ranks on ranks.rank_id = faculty.rank_id
                        INNER join publications on publications.pub_id = authorships_users.pub_id
                        INNER JOIN authorships on authorships.pub_id = publications.pub_id 
                        
                    WHERE pub_delete_ind = false AND CAST(a_year as int) >= %s AND CAST(a_year as int) <= %s
                    group by faculty_fn || ' ' || faculty_ln, rank_title, faculty.user_id) authors

                FULL JOIN 

                    (SELECT 
                        faculty.user_id as pres_fac, 
                        faculty_fn || ' ' || faculty_ln AS full_name ,
                        rank_title  as fac_rank, 
                        
                        COUNT(distinct(presentations_users.user_id, presentations_users.pub_id)) 
                        as PRESENTATIONS
                        
                        from presentations_users 
                        INNER JOIN faculty on presentations_users.user_id = faculty.user_id 
                        INNER JOIN ranks on ranks.rank_id = faculty.rank_id
                        INNER join publications on publications.pub_id = presentations_users.pub_id
                        INNER JOIN presentations on presentations.pub_id = publications.pub_id 
                        
                        WHERE pub_delete_ind = false AND CAST(p_year as int) >= %s AND CAST(p_year as int) <= %s
                        group by faculty_fn || ' ' || faculty_ln, rank_title, faculty.user_id) pres
                on (pres.pres_fac = authors.authors_fac )


                FULL JOIN 

                (SELECT 
                    faculty.user_id as proj_fac, 
                    faculty_fn || ' ' || faculty_ln AS full_name ,
                    rank_title  as fac_rank, 
                    COUNT(projects.pub_id) as projects
                    
                    from projects
                    INNER JOIN publications on projects.pub_id = publications.pub_id
                    INNER JOIN faculty on publications.user_id = faculty.user_id 
                    INNER JOIN ranks on ranks.rank_id = faculty.rank_id
                    WHERE pub_delete_ind = false AND CAST(r_year as int) >= %s AND CAST(r_year as int) <= %s
                    group by faculty_fn || ' ' || faculty_ln, rank_title, faculty.user_id
                    ) proj
                on (pres.pres_fac = proj.proj_fac )

                FULL JOIN 
                (SELECT 
                    faculty.user_id as others_fac,
                    faculty_fn || ' ' || faculty_ln AS full_name ,
                    rank_title  as fac_rank, 
                    COUNT(others.pub_id) as other
                    
                    from others
                    INNER JOIN publications on others.pub_id = publications.pub_id
                    INNER JOIN faculty on publications.user_id = faculty.user_id 
                    INNER JOIN ranks on ranks.rank_id = faculty.rank_id
                    WHERE pub_delete_ind = false AND CAST(o_year as int) >= %s AND CAST(o_year as int) <= %s
                    group by faculty_fn || ' ' || faculty_ln, rank_title, faculty.user_id
                    ) other
                on (other.others_fac = proj.proj_fac )
            
            """

            values_tally = []
            if datefilter_u: 
                values_tally = [datefilter, datefilter_u, datefilter, datefilter_u, datefilter, datefilter_u,datefilter, datefilter_u]
            else: 
                values_tally = [datefilter, datefilter, datefilter, datefilter, datefilter, datefilter,datefilter, datefilter]
            cols_tally = ['Faculty', 'Rank', 'Publications', 'Presentations', 'Projects', 'Other Academic Merits']
            
            if currentuserid > 3: 
                sqltally += """ WHERE authors.authors_fac = %s 
                """
                values_tally += [currentuserid]
            
            pubtally = db.querydatafromdatabase(sqltally,values_tally, cols_tally )
            
            pubtally['Publications'].fillna(0, inplace= True) 
            pubtally['Presentations'].fillna(0, inplace= True)
            pubtally['Projects'].fillna(0, inplace= True) 
            pubtally['Other Academic Merits'].fillna(0, inplace= True) 
            
            pubtally['Total'] = " " 
            for i in range(len(pubtally)): 
                pubtally['Total'][i] = pubtally['Publications'][i] + pubtally['Presentations'][i] +  pubtally['Projects'][i] + pubtally['Other Academic Merits'][i]
            
     
        else: 
            sqltally = """SELECT COALESCE(authors.full_name, pres.full_name, proj.full_name, other.full_name), 
                COALESCE(authors.fac_rank, pres.fac_rank, proj.fac_rank, other.fac_rank), 
                authors.Publications, pres.PRESENTATIONS, proj.projects, other.other

                FROM 
                    (SELECT 
                        faculty.user_id as authors_fac, 
                        faculty_fn || ' ' || faculty_ln AS full_name ,
                        rank_title as fac_rank, 

                        COUNT(distinct(authorships_users.user_id ,  authorships_users.pub_id)) 
                        as Publications

                        from authorships_users
                        INNER JOIN faculty on authorships_users.user_id = faculty.user_id 
                        INNER JOIN ranks on ranks.rank_id = faculty.rank_id
                        INNER join publications on publications.pub_id = authorships_users.pub_id
                        INNER JOIN authorships on authorships.pub_id = publications.pub_id 
                        
                    WHERE pub_delete_ind = false 
                    group by faculty_fn || ' ' || faculty_ln, rank_title, faculty.user_id) authors

                FULL JOIN 

                    (SELECT 
                        faculty.user_id as pres_fac, 
                        faculty_fn || ' ' || faculty_ln AS full_name ,
                        rank_title  as fac_rank, 
                        COUNT(distinct(presentations_users.user_id, presentations_users.pub_id)) as PRESENTATIONS
                        
                        from presentations_users 
                        INNER JOIN faculty on presentations_users.user_id = faculty.user_id 
                        INNER JOIN ranks on ranks.rank_id = faculty.rank_id
                        INNER join publications on publications.pub_id = presentations_users.pub_id
                        INNER JOIN presentations on presentations.pub_id = publications.pub_id 
                        
                        WHERE pub_delete_ind = false
                        group by faculty_fn || ' ' || faculty_ln, rank_title, faculty.user_id) pres
                on (pres.pres_fac = authors.authors_fac )


                FULL JOIN 

                (SELECT 
                    faculty.user_id as proj_fac, 
                    faculty_fn || ' ' || faculty_ln AS full_name ,
                    rank_title  as fac_rank, 
                    COUNT(projects.pub_id) as projects
                    
                    from projects
                    INNER JOIN publications on projects.pub_id = publications.pub_id
                    INNER JOIN faculty on publications.user_id = faculty.user_id 
                    INNER JOIN ranks on ranks.rank_id = faculty.rank_id
                    WHERE pub_delete_ind = false 
                    group by faculty_fn || ' ' || faculty_ln, rank_title, faculty.user_id
                    ) proj
                on (pres.pres_fac = proj.proj_fac )

                FULL JOIN 
                (SELECT 
                    faculty.user_id as others_fac,
                    faculty_fn || ' ' || faculty_ln AS full_name ,
                    rank_title  as fac_rank, 
                    COUNT(others.pub_id) as other
                    
                    from others
                    INNER JOIN publications on others.pub_id = publications.pub_id
                    INNER JOIN faculty on publications.user_id = faculty.user_id 
                    INNER JOIN ranks on ranks.rank_id = faculty.rank_id
                    WHERE pub_delete_ind = false
                    group by faculty_fn || ' ' || faculty_ln, rank_title, faculty.user_id
                    ) other
                on (other.others_fac = proj.proj_fac )
            """
            
            print(currentuserid)
            
            values_tally = []
            if currentuserid > 3: 
                sqltally += """ WHERE authors.authors_fac = %s 
                """
                values_tally = [currentuserid]
            
            
            
            cols_tally = ['Faculty', 'Rank', 'Publications', 'Presentations', 'Projects', 'Other Academic Merits']
            pubtally = db.querydatafromdatabase(sqltally,values_tally, cols_tally )
            pubtally['Publications'].fillna(0, inplace= True) 
            pubtally['Presentations'].fillna(0, inplace= True)
            pubtally['Projects'].fillna(0, inplace= True) 
            pubtally['Other Academic Merits'].fillna(0, inplace= True) 
            
            pubtally['Total'] = " " 
            
            if currentuserid > 3: 
                pubtally['Total'][0] =  pubtally['Publications'][0] + pubtally['Presentations'][0] +  pubtally['Projects'][0] + pubtally['Other Academic Merits'][0]
            else: 
                for i in range(len(pubtally)): 
                    pubtally['Total'][i] = pubtally['Publications'][i] + pubtally['Presentations'][i] +  pubtally['Projects'][i] + pubtally['Other Academic Merits'][i]
                
        pubtally = pubtally.sort_values(by = ['Total'], ascending=False)            
        if pubtally.shape[0]: 
            table_tally = dbc.Table.from_dataframe(pubtally, striped=True, bordered=True, hover=True, size='sm', style={"whiteSpace": "pre-line"}) 
        else: 
            table_tally = "No tally to display."
    else: 
        raise PreventUpdate
    return[table_tally]