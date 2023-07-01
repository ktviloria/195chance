#for viewing my profile with button leading to editing
#only faculty users have access to this page
#only profile details of current faculty user is shown

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
 
from urllib.parse import urlparse, parse_qs

layout= html.Div( 
    [ 
        html.Div( 
            [ 
                dcc.Store(id='myprof_toload', storage_type='memory', data=0), 
            ] 
        ), 
        html.H2("My Profile"), 
        html.Hr(), 
        html.Div(
            dbc.Row(
                [
                    #picture
                    dbc.Col(
                        html.Img(id='my_pic', height="200px"),
                        width = {"size": 3, "order": 0, "offset": 1}
                    ),
                    #details
                    dbc.Col(
                        html.Div(
                            [
                                #Name
                                dbc.Row(
                                    [
                                        html.Div ("Name: ", id='mydet_name'),
                                        # html.Div(id='mydet_name'),
                                    ]
                                ),
                                #Rank
                                dbc.Row(
                                    [
                                        dbc.Label("Rank: ", id='mydet_rank'),
                                        # html.Div(id='mydet_rank')
                                    ]
                                ),
                                #Birthdate
                                dbc.Row(
                                    [
                                        dbc.Label("Birthdate: ", id='mydet_bday'),    
                                        # html.Div(id='mydet_bday')
                                    ]
                                    ),
                                #Mail
                                dbc.Row(
                                    [
                                        dbc.Label("Email: ", id='mydet_mail'),
                                        # html.Div(id='mydet_mail')
                                    ]
                                ),
                                #Areas of expertise
                                dbc.Row(
                                    [
                                        html.Strong("Areas of Expertise: "),
                                        # html.Div(id='mydet_expert1')
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label("Expertise 1: ", id='mydet_expert1'),
                                        # html.Div(id='mydet_expert1')
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label("Expertise 2: ", id='mydet_expert2'),
                                        # html.Div(id='mydet_expert2')
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label("Expertise 3: ", id='mydet_expert3'),
                                        # html.Div(id='mydet_expert3')
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label("Expertise 4: ", id='mydet_expert4'),
                                        # html.Div(id='mydet_expert4')
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label("Expertise 5: ", 'mydet_expert5'),
                                        # html.Div(id='mydet_expert5')
                                    ]
                                ),
                            ]
                        ),
                        width = 5
                    ),
                    #edit profile button
                    dbc.Col(
                        [
                        dbc.DropdownMenu(
                        children=[
                            dbc.DropdownMenuItem("Edit Profile", href="/edit_my_profile"),
                            dbc.DropdownMenuItem("Edit Username", href="/edit_username"),
                            dbc.DropdownMenuItem("Edit Password", href="/edit_password")
                        ],
                        label='Edit', color='danger'),
                        ]
                    ),
                    
                    # dbc.Col(
                    #     dbc.Button("Edit Profile", color='danger', href='/edit_my_profile'),
                    #     width = {"size": 2,  "offset": 1}
                    # ),
                    # dbc.Col(
                    #     dbc.Button("Edit Username", color='danger', href='/edit_my_profile'),
                    #     width = {"size": 2,  "offset": 1}
                    # ),
                    # dbc.Col(
                    #     dbc.Button("Edit Password", color='danger', href='/edit_password'),
                    #     width = {"size": 2, "order": "last", "offset": 1}
                    # ),
                ]
            ),
            # id='myprof'
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                            dbc.CardHeader ([html.H5("My publication activity summary:", style={'fontWeight':'bold'})]),
                            dbc.CardBody(
                                [
                                    dcc.Graph(id='graph_myprof1', style={'width': '100%', 'height': '100%'}),
                                    html.Div(
                                        [
                                        dcc.Dropdown(id='myprof_date_filter', clearable=True, searchable=True, placeholder="YYYY", style = {'width': '30%'}), 
                                        ], #className="dash-bootstrap"
                                    ),
                                    html.Div(
                                        [
                                        dcc.Graph(id='graph_myprof2',style={'width': '100%', 'height': '100%'})
                                        ]
                                    ),
                                ]
                            )
                            ], style ={'width': '95%', 'margin': 'auto'}
                        )
                    ]
                )
                # dbc.Col(
                #     [
                #         dcc.Graph(id='graph_myprof1'),
                #     ]
                # ),
                # dbc.Col(
                #     [
                #         html.Div(
                #             dcc.Dropdown(
                #                 id='myprof_date_filter', clearable=True, searchable=True, placeholder="YYYY"
                #             ), className="dash-bootstrap"
                #         ),
                #         html.Div(
                #             dcc.Graph(id='graph_myprof2')
                #         ),
                #     ] 
                # ),
            ]
        )      
    ] 
) 

@app.callback(
    [
        Output('myprof_date_filter', 'options'),
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('currentuserid', 'data')
    ]
)
def myprof_loaddropdown (pathname, currentuserid):
    if pathname == '/my_profile':
        sql_date_filter = """SELECT DISTINCT label, value
            FROM (
                SELECT (a_year) AS label, (a_year) AS value FROM authorships
					inner join publications on publications.pub_id = authorships.pub_id
                    INNER JOIN faculty on publications.user_id = faculty.user_id
					where not pub_delete_ind AND faculty.user_id = %s
                UNION
                SELECT (p_year) AS label, (p_year) AS value FROM presentations 
					inner join publications on publications.pub_id = presentations.pub_id
                    INNER JOIN faculty on publications.user_id = faculty.user_id
					where not pub_delete_ind AND faculty.user_id = %s
                UNION
                SELECT (r_year) AS label, (r_year) AS value FROM projects
					inner join publications on publications.pub_id = projects.pub_id
                    INNER JOIN faculty on publications.user_id = faculty.user_id
					where not pub_delete_ind AND faculty.user_id = %s
                UNION
                SELECT (o_year) AS label, (o_year) AS value FROM others 
					inner join publications on publications.pub_id = others.pub_id
                    INNER JOIN faculty on publications.user_id = faculty.user_id
					where not pub_delete_ind AND faculty.user_id = %s
            ) AS subquery
            ORDER BY value DESC
            """
        values_date_filter = [f"{currentuserid}", f"{currentuserid}", f"{currentuserid}", f"{currentuserid}"]
        cols_date_filter = ['label', 'value']
        date_filter_included = db.querydatafromdatabase(sql_date_filter, values_date_filter, cols_date_filter)
        date_filter_options = date_filter_included.to_dict('records')
    
    else:
        raise PreventUpdate
    
    return [date_filter_options]       

@app.callback( 
        [ 
            Output('my_pic', 'src'),
            Output('mydet_name', 'children'),
            Output('mydet_rank', 'children'),
            Output('mydet_bday', 'children'),
            Output('mydet_mail', 'children'),
            Output('mydet_expert1', 'children'),
            Output('mydet_expert2', 'children'),
            Output('mydet_expert3', 'children'),
            Output('mydet_expert4', 'children'),
            Output('mydet_expert5', 'children'),
            Output('graph_myprof1', 'figure'),  
            Output('graph_myprof2', 'figure')
        ], 
        [ 
            Input('url', 'pathname'),
            Input('myprof_date_filter', 'value'), 
        ],
        [ 
            State('url', 'search'), 
            State('currentuserid', 'data'),
        ] 
)

def facdetails_load(pathname, datefilter, search, currentuserid): 
    if pathname == '/my_profile': 
        sql = """SELECT
                faculty.user_id,
                faculty_fn || ' ' || faculty_ln AS faculty_full_name,
                rank_title,
                faculty_bdate,
                faculty_mail,
                faculty_contact,
                faculty_expert1,
                faculty_expert2,  
                faculty_expert3,  
                faculty_expert4, 
                faculty_expert5
            FROM faculty
                INNER JOIN ranks ON faculty.rank_id = ranks.rank_id
                INNER JOIN users on faculty.user_id = users.user_id
            WHERE
                faculty_delete_ind = false            """
        values = [f"{currentuserid}"]
        cols = ['userID', 'Full Name', 'Rank', 'Birthdate', 'Email', 'Contact Number', 'Expertise 1', 'Expertise 2', 'Expertise 3', 'Expertise 4', 'Expertise 5' ] 
        faculty = db.querydatafromdatabase(sql, values, cols)

        counter = 0 
        for i in range(len(faculty)):
            if faculty['userID'][i] != int(currentuserid):
                faculty = faculty.drop(i)
            else: 
                counted = counter 
            counter += 1
        userID = faculty['userID'][counted]
        fullname_h = " %s" % (faculty['Full Name'][counted] or " ")
        fullname = [
            html.Div([
                html.Strong("Name: "),
                html.Span(f"{fullname_h}"), 
                ]
            ),
        ]
        rank_h = " %s" % (faculty['Rank'][counted] or " ")
        rank = [
            html.Div([
                html.Strong("Rank: "),
                html.Span(f"{rank_h}"), 
                ]
            ),
        ]
        birthdate_h = " %s" % (faculty['Birthdate'][counted] or " ")
        birthdate =  [
            html.Div([
                html.Strong("Birthdate: "),
                html.Span(f"{birthdate_h}"), 
                ]
            ),
        ]
        mail_h = " %s" % (faculty['Email'][counted] or " ")
        mail = [
            html.Div([
                html.Strong("Email: "),
                html.Span(f"{mail_h}"), 
                ]
            ),
        ]
        contactnumber = "Contact Number %s" % (faculty['Contact Number'][counted] or " ")
        expertise1= faculty['Expertise 1'][counted]
        expertise2= faculty['Expertise 2'][counted]
        expertise3= faculty['Expertise 3'][counted]
        expertise4= faculty['Expertise 4'][counted]
        expertise5= faculty['Expertise 5'][counted]
        fac_pic = app.get_asset_url(f"{currentuserid}.png")

        sql2="""
            select distinct (pub_type) as label,  year, count (pub_id) as value from 
                (
                    select authorships.pub_id as pub_id, authorships.a_year as year,
                        case
                            when tag_id <=7 then 'authorship'
                        end as "pub_type"
                    from publications
                    LEFT OUTER JOIN users ON publications.user_id = users.user_id
                    LEFT OUTER JOIN faculty ON publications.user_id = faculty.user_id
                    left outer join authorships on publications.pub_id = authorships.pub_id 
                    where pub_delete_ind = false AND faculty.user_id = %s
                    
                    union all
                    
                    select presentations.pub_id as pub_id, presentations.p_year as year, 
                        case
                            when tag_id <=10 then 'presentation'
                        end as "pub_type"
                    from publications
                    LEFT OUTER JOIN users ON publications.user_id = users.user_id
                    LEFT OUTER JOIN faculty ON publications.user_id = faculty.user_id
                    left outer join presentations on publications.pub_id = presentations.pub_id 
                    where pub_delete_ind = false AND faculty.user_id = %s
                    
                    union all
                    
                    select projects.pub_id as pub_id, projects.r_year as year,
                        case
                            when tag_id =11 then 'project'
                        end as "pub_type"
                    from publications
                    LEFT OUTER JOIN users ON publications.user_id = users.user_id
                    LEFT OUTER JOIN faculty ON publications.user_id = faculty.user_id
                    left outer join projects on publications.pub_id = projects.pub_id 
                    where pub_delete_ind = false AND faculty.user_id = %s
                    
                    union all
                    
                    select others.pub_id as pub_id, others.o_year as year,
                        case
                            when tag_id <=13 then 'other'
                        end as "pub_type"
                    from publications
                    LEFT OUTER JOIN users ON publications.user_id = users.user_id
                    LEFT OUTER JOIN faculty ON publications.user_id = faculty.user_id
                    left outer join others on publications.pub_id = others.pub_id  
                    where pub_delete_ind = false AND faculty.user_id = %s
                )
                as pub_summ
                group by pub_type, year
                order by year
            """ 
        values2 = [f"{currentuserid}", f"{currentuserid}",f"{currentuserid}", f"{currentuserid}"] 
        cols2 = ['Type', 'Year', 'Publications']

        #sql2 += """order by year"""
        #values2 += [] 
        pub2 = db.querydatafromdatabase(sql2, values2, cols2)
        pubsumm_graph1 = px.line(pub2, x='Year', y='Publications', color='Type')
    
        sql3="""
            select
            distinct (tag) as tag,
            year,
            count (pub_id) as publications,
            case
                when tag_id <=7 then 'authorship'
                when tag_id <=10 then 'presentation'
                when tag_id =11 then 'project'
                when tag_id <=13 then 'other'
            end as "pub_type"
            from
                (select
                    authorships.pub_id AS pub_id,
                    tag_short_title as tag,
				 	a_year as year,
                    publications.tag_id,
                    pub_delete_ind
                from authorships
                LEFT OUTER JOIN publications ON authorships.pub_id = publications.pub_id
                left outer join tags on publications.tag_id = tags.tag_id
                INNER JOIN faculty on publications.user_id = faculty.user_id
                where pub_delete_ind = false AND faculty.user_id = %s
				 
				union all
				 
				select
                    presentations.pub_id AS pub_id,
                    tag_short_title as tag,
                    p_year as year,
                    publications.tag_id,
                    pub_delete_ind
                from presentations
                LEFT OUTER JOIN publications ON presentations.pub_id = publications.pub_id
                left outer join tags on publications.tag_id = tags.tag_id
                INNER JOIN faculty on publications.user_id = faculty.user_id
                where pub_delete_ind = false AND faculty.user_id = %s
				 
				union all
				 
				select
                    projects.pub_id AS pub_id,
                    tag_short_title as tag,
                    r_year as year,
                    publications.tag_id,
                    pub_delete_ind
                from projects
                LEFT OUTER JOIN publications ON projects.pub_id = publications.pub_id
                left outer join tags on publications.tag_id = tags.tag_id
                INNER JOIN faculty on publications.user_id = faculty.user_id
                where pub_delete_ind = false AND faculty.user_id = %s
				 
				union all
				
				select
                    others.pub_id AS pub_id,
                    tag_short_title as tag,
                    o_year as year,
                    publications.tag_id,
                    pub_delete_ind
                from others
                LEFT OUTER JOIN publications ON others.pub_id = publications.pub_id
                left outer join tags on publications.tag_id = tags.tag_id
                INNER JOIN faculty on publications.user_id = faculty.user_id
                where pub_delete_ind = false AND faculty.user_id = %s
                )
            as tag_summ
            group by pub_type, tag, tag_id, year
            """ 
        values3 = [f"{currentuserid}", f"{currentuserid}", f"{currentuserid}", f"{currentuserid}"] 
        cols3 = ['Tag', 'Year', 'Publications', 'Type']

        if datefilter:
            sql3 += """HAVING (CAST(year AS varchar) ILIKE %s)"""
            values3 += [f"%{datefilter}%"] 
            pub3 = db.querydatafromdatabase(sql3, values3, cols3)
            pubsumm_graph2 = px.bar(pub3, x='Type', y='Publications', color='Tag')
        else:
            sql3 += """order by year"""
            values3 += [] 
            pub3 = db.querydatafromdatabase(sql3, values3, cols3)
            pubsumm_graph2 = px.bar(pub3, x='Year', y='Publications', color='Type', hover_data=['Tag'], barmode='group')
    else:
        raise PreventUpdate
    return [fac_pic, fullname, rank, birthdate, mail, expertise1, expertise2, expertise3, expertise4, expertise5, pubsumm_graph1, pubsumm_graph2]


# #personal publications summary
# @app.callback(
#     [
#         Output('mysumm', 'children')
#     ],
#     [
#         Input('url', 'pathname'),
#         Input('tabs', 'active_tab'),
#         Input('myprof_pub_filter', 'value'),
#         Input('myprof_date_filter', 'value'),
#     ],
#     State('currentuserid', 'data')
# )

# def myprof_loadpublist(pathname, tab, searchterm, datefilter, currentuserid):
#     if pathname == '/my_profile':
#         if tab == 'tab_a':
#             sql_a = """SELECT
#                     a_year,
#                     publications.pub_id,
#                     faculty_fn || ' ' || faculty_ln AS faculty_full_name,
#                     tag_short_title,
#                     pub_title,
#                     a_authors,
#                     authorship_role.a_label,
#                     To_char(a_date, 'Month YYYY'), 
#                     a_pub_name, 
#                     a_publisher, 
#                     a_doi, 
#                     a_isxn, 
#                     a_scopus,
#                     to_char(publications.pub_last_upd::timestamp, 'Month DD YYYY HH24:MI:SS'),
#                     modified_by
#                 FROM authorships
#                     INNER JOIN publications on authorships.pub_id = publications.pub_id
#                     INNER JOIN faculty on publications.user_id = faculty.user_id
#                     INNER JOIN tags on publications.tag_id = tags.tag_id
#                     FULL JOIN authorship_role on authorships.authorship_role = authorship_role.a_label_id
#                 WHERE
#                     pub_delete_ind = false AND
#                     faculty.user_id = %s
#                 """
#             values_a = [f"{currentuserid}"]
#             cols_a = ['Year','id', 'Faculty Involved', 'Publication Tag', 'Title', 'All Authors', 'Involvement', 'Date', 'Publication', 'Publisher', 'DOI','ISXN', 'Scopus', 'Last Updated', 'Last Modified By']
            
#             # if searchterm:
#             # #OR (tag_short_title %s)
#             #     sql_a += """ AND (faculty_fn ILIKE %s) OR (faculty_ln ILIKE %s) OR (pub_title ILIKE %s) 
#             #         OR (a_authors ILIKE %s) OR (a_pub_date ILIKE %s) OR (a_pub_name ILIKE %s)
#             #         OR (a_publisher ILIKE %s) OR (a_doi ILIKE %s) OR (a_isxn ILIKE %s) OR (a_scopus ILIKE %s)"""
#             #     values_a += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
#             #             f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
#             #             f"%{searchterm}%", f"%{searchterm}%"]
            
#             # sql_a += """ORDER BY authorships.a_year DESC"""
#             # pub_a = db.querydatafromdatabase(sql_a, values_a, cols_a)
#             # pub_a.drop(['id'],axis=1,inplace=True)
#             # table_a = dbc.Table.from_dataframe(pub_a, striped=True, bordered=True, hover=True, size='sm') 
#             # return [table_a] 

#              #fix additivity of searchterms and filters
#             if datefilter:
#                 sql_a += """AND (a_year ILIKE %s)"""
#                 values_a += [f"%{datefilter}%"]
#                 if searchterm:
#                     sql_a += """ AND (
#                         ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) OR (a_year ILIKE %s)
#                         OR (a_authors ILIKE %s) OR (a_pub_name ILIKE %s) OR ((To_char(a_date, 'Month YYYY')) ILIKE %s)
#                         OR (a_publisher ILIKE %s) OR (a_doi ILIKE %s) OR (a_isxn ILIKE %s) OR (a_scopus ILIKE %s) OR (tag_short_title ILIKE %s)
#                         )"""
#                     values_a += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
#                             f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
#                             f"%{searchterm}%", f"%{searchterm}%"]
#                 else:
#                     sql_a += """"""
#                     values_a += [] 
#             elif searchterm:
#                 sql_a += """ AND (
#                     ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) OR (a_year ILIKE %s)
#                     OR (a_authors ILIKE %s) OR (a_pub_name ILIKE %s) OR ((To_char(a_date, 'Month YYYY')) ILIKE %s)
#                     OR (a_publisher ILIKE %s) OR (a_doi ILIKE %s) OR (a_isxn ILIKE %s) OR (a_scopus ILIKE %s) OR (tag_short_title ILIKE %s)
#                     )"""
#                 values_a += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
#                         f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
#                         f"%{searchterm}%", f"%{searchterm}%"]
#                 if datefilter:
#                     sql_a += """AND (a_year ILIKE %s)"""
#                     values_a += [f"%{datefilter}%"]
#                 else:
#                     sql_a += """"""
#                     values_a += []     
#             else:
#                 sql_a += """"""
#                 values_a += []
            
#             sql_a += """ORDER BY authorships.a_year DESC"""
#             pub_a = db.querydatafromdatabase(sql_a, values_a, cols_a) 
            
#             if pub_a.shape[0]: 
#                 buttons_a = []
#                 pub_details = []
#                 other_info = []
                 
#                 for id in pub_a['id']: 
#                     buttons_a += [ 
#                         html.Div( 
#                             dbc.Button('Edit/Delete', href=f"/form_authorships?mode=edit&id={id}", size='sm', color='secondary', ), 
#                             style={'text-align': 'center'} 
#                         ) 
#                     ] 
                    
                
#                 for i in range(len(pub_a)): 
#                     inputs_1 = [pub_a['Date'][i], pub_a['Publication'][i], pub_a['Publisher'][i]]
#                     if not all (inputs_1) :  
#                         pub_details += " "
#                     else: 
#                         pub_details += [("Published in/on: %s in %s by %s" % (pub_a['Date'][i], pub_a['Publication'][i], pub_a['Publisher'][i]))] 
#                     # inputs_2 = [pub_a['DOI'][i], pub_a['ISXN'][i], pub_a['Scopus'][i]]
#                     # if not all (inputs_2): 
#                     #     other_info += " "
#                     # else: 
#                     other_info += [("DOI: %s \n Issue Number: %s \n Scopus: %s"  % (pub_a['DOI'][i], pub_a['ISXN'][i], pub_a['Scopus'][i]) or " " )]

#                 pub_a['Publication Details'] = pub_details
#                 pub_a['Other Information'] = other_info

#                 last_update_holder = pub_a['Last Updated']
#                 pub_a.drop(['Last Updated'],axis=1,inplace=True)
#                 pub_a['Last Updated'] = last_update_holder 

#                 last_modifiedby_holder = pub_a['Last Modified By']
#                 pub_a.drop(['Last Modified By'],axis=1,inplace=True)
#                 pub_a['Last Modified By'] = last_modifiedby_holder

#                 pub_a['More Details'] = buttons_a
                 
#             pub_a.drop(['id'],axis=1,inplace=True)
#             pub_a.drop(['Date'],axis=1,inplace=True)
#             pub_a.drop(['Publication'],axis=1,inplace=True)
#             pub_a.drop(['Publisher'],axis=1,inplace=True)
#             pub_a.drop(['DOI'],axis=1,inplace=True)
#             pub_a.drop(['ISXN'],axis=1,inplace=True)
#             pub_a.drop(['Scopus'],axis=1,inplace=True)
            
#             if pub_a.shape[0]:
#                 table_a = dbc.Table.from_dataframe(pub_a, striped=True, bordered=True, hover=True, size='sm', style={"whiteSpace": "pre-line"}) 
#             else:
#                 table_a = "No records to display"
#             return [table_a]
            
#             # table_a = dbc.Table.from_dataframe(pub_a, striped=True, bordered=True, hover=True, size='sm',  style={"whiteSpace": "pre-line"}) 
#             # return [table_a]


#         elif tab == 'tab_p':
#             sql_p = """SELECT
#                 p_year,
#                 publications.pub_id,
#                 faculty_fn || ' ' || faculty_ln AS faculty_full_name,
#                 tag_short_title,
#                 pub_title,
#                 p_authors,
#                 to_char(p_start_date, 'Month DD YYYY'), 
#                 to_char(p_end_date, 'Month DD YYYY'), 
#                 p_conf, 
#                 p_loc, 
#                 p_add_info,
#                 to_char(publications.pub_last_upd::timestamp, 'Month DD YYYY HH24:MI:SS'),
#                 modified_by
#             FROM presentations
#                 INNER JOIN publications on presentations.pub_id = publications.pub_id
#                 INNER JOIN faculty on publications.user_id = faculty.user_id
#                 INNER JOIN tags on publications.tag_id = tags.tag_id
                
#             WHERE
#                 pub_delete_ind = false AND
#                 faculty.user_id = %s
#                 """
#             values_p = [f"{currentuserid}"]
#             cols_p = ['Year', 'id', 'Faculty Involved', 'Publication Tag', 'Title', 'All Authors',  'Start Date', 'End Date', 'Conference',
#                       'Location', 'Other Info', 'Last Updated', 'Last Modified By']
            
#             # if searchterm:
#             # #OR (tag_short_title %s)
#             #     sql_p += """ AND (faculty_fn ILIKE %s) OR (faculty_ln ILIKE %s)
#             #     OR (pub_title ILIKE %s) OR (p_authors ILIKE %s) OR (p_pres_date ILIKE %s)
#             #     OR (p_conf ILIKE %s) OR (p_loc ILIKE %s) OR (p_add_info ILIKE %s)"""
#             #     values_p += [f"%{searchterm}%", f"%{searchterm}%",
#             #                  f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
#             #                  f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%"]
            
#             if datefilter:
#                 sql_p += """AND (p_year ILIKE %s)"""
#                 values_p += [f"%{datefilter}%"]
#                 if searchterm:
#                     sql_p += """ AND (
#                         ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
#                         OR (p_authors ILIKE %s) OR (p_year ILIKE %s) OR (p_conf ILIKE %s)
#                         OR (p_loc ILIKE %s) OR (p_add_info ILIKE %s) OR (tag_short_title ILIKE %s)
#                         OR (to_char(p_start_date, 'Month DD YYYY') ILIKE %s) OR (to_char(p_end_date, 'Month DD YYYY')ILIKE %s)
#                         )"""
#                     values_p += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
#                             f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
#                             f"%{searchterm}%", f"%{searchterm}%",]
#                 else:
#                     sql_p += """"""
#                     values_p += [] 
#             elif searchterm:
#                 sql_p += """ AND (
#                     ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
#                     OR (p_authors ILIKE %s) OR (p_year ILIKE %s) OR (p_conf ILIKE %s)
#                     OR (p_loc ILIKE %s) OR (p_add_info ILIKE %s) OR (tag_short_title ILIKE %s)
#                     OR (to_char(p_start_date, 'Month DD YYYY') ILIKE %s) OR (to_char(p_end_date, 'Month DD YYYY')ILIKE %s)
#                     )"""
#                 values_p += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
#                         f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
#                         f"%{searchterm}%", f"%{searchterm}%",]
#                 if datefilter:
#                     sql_p += """AND (p_year ILIKE %s)"""
#                     values_p += [f"%{datefilter}%"]
#                 else:
#                     sql_p += """"""
#                     values_p += []     
#             else:
#                 sql_p += """"""
#                 values_p += []
#             sql_p += """ORDER BY presentations.p_year DESC"""
#             pub_p = db.querydatafromdatabase(sql_p, values_p, cols_p)
            
            
#             if pub_p.shape[0]: 
#                 pres_details = []
#                 other_details = []
#                 for i in range(len(pub_p)): 
#                     pres_details += [("Presented from: %s to %s \n Presented at: %s (%s)" % (pub_p['Start Date'][i], pub_p['End Date'][i], pub_p['Conference'][i], pub_p['Location'][i]) or "No Details Provided")]
#                     other_details += [pub_p['Other Info'][i]]
            
#                 pub_p['Presentation Details'] = pres_details
#                 pub_p['Additional Info'] = other_details
                
#                 buttons_p = [] 
#                 for id in pub_p['id']: 
#                     buttons_p += [ 
#                         html.Div( 
#                             dbc.Button('Edit/Delete', href=f"/form_presentations?mode=edit&id={id}", size='sm', color='secondary', ), 
#                             style={'text-align': 'center'} 
#                         ) 
#                     ] 

#                 last_update_holder_p = pub_p['Last Updated']
#                 pub_p.drop(['Last Updated'],axis=1,inplace=True)
#                 pub_p['Last Updated'] = last_update_holder_p

#                 last_modifiedby_holder_p = pub_p['Last Modified By']
#                 pub_p.drop(['Last Modified By'], axis=1, inplace=True)
#                 pub_p['Last Modified By'] = last_modifiedby_holder_p

#                 pub_p['More Details'] = buttons_p
                
#             pub_p.drop(['id'],axis=1,inplace=True)
#             pub_p.drop(['Start Date'],axis=1,inplace=True)
#             pub_p.drop(['End Date'],axis=1,inplace=True)
#             pub_p.drop(['Conference'],axis=1,inplace=True)
#             pub_p.drop(['Location'],axis=1,inplace=True)
#             pub_p.drop(['Other Info'],axis=1,inplace=True)
            
#             if pub_p.shape[0]:
#                 table_p = dbc.Table.from_dataframe(pub_p, striped=True, bordered=True, hover=True, size='sm', style={"whiteSpace": "pre-line"}) 
#             else:
#                 table_p = "No records to display"
#             return [table_p]
            
#             # table_p = dbc.Table.from_dataframe(pub_p, striped=True, bordered=True, hover=True, size='sm', style={"whiteSpace": "pre-line"}) 
#             # return [table_p]
#         elif tab == 'tab_r':
#             sql_r = """SELECT
#                 r_year,
#                 publications.pub_id,
#                 faculty_fn || ' ' || faculty_ln AS faculty_full_name,
#                 tag_short_title,
#                 pub_title,
#                 r_roles, 
#                 r_timeframe, 
#                 to_char(r_start_date, 'Month DD YYYY'),
#                 to_char(r_end_date, 'Month DD YYYY'), 
#                 r_fund_org,
#                 to_char(publications.pub_last_upd::timestamp, 'Month DD YYYY HH24:MI:SS'),
#                 modified_by
#             FROM projects
#                 INNER JOIN publications on projects.pub_id = publications.pub_id
#                 INNER JOIN faculty on publications.user_id = faculty.user_id
#                 INNER JOIN tags on publications.tag_id = tags.tag_id
#             WHERE
#                 pub_delete_ind = false AND
#                 faculty.user_id = %s
#                 """
#             values_r = [f"{currentuserid}"]
#             cols_r = ['Year', 'id', 'Faculty Involved', 'Publication Tag', 'Title', 'Role', 'Timeframe', 'Start Date', 'End Date', 'Funding Organization',
#                       'Last Updated', 'Last Modified By']  
            
#             # if searchterm:
#             # #OR (tag_short_title %s)
#             # #OR (r_start_date ILIKE %s)
#             # #OR (r_end_date ILIKE %s)
#             #     sql_r += """ AND (faculty_fn ILIKE %s) OR (faculty_ln ILIKE %s) OR (pub_title ILIKE %s) 
#             #         OR (r_roles ILIKE %s) OR (r_timeframe ILIKE %s) OR (r_fund_org ILIKE %s)"""
#             #     values_r += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
#             #             f"%{searchterm}%", f"%{searchterm}%",
#             #             ]
#             if datefilter:
#                 sql_r += """AND (r_year ILIKE %s)"""
#                 values_r += [f"%{datefilter}%"]
#                 if searchterm:
#                     sql_r += """ AND (
#                         (r_year ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
#                         OR (r_roles ILIKE %s) OR (r_timeframe ILIKE %s) OR (r_fund_org ILIKE %s) OR (tag_short_title ILIKE %s)
#                         OR ((To_char(r_start_date, 'Month DD YYYY')) ILIKE %s) OR ((To_char(r_end_date, 'Month DD YYYY')) ILIKE %s)
#                         )"""
#                     values_r += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
#                         f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
#                         ]  
#                 else:
#                     sql_r += """"""
#                     values_r += [] 
#             elif searchterm:
#                 sql_r += """ AND (
#                         (r_year ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (pub_title ILIKE %s) 
#                         OR (r_roles ILIKE %s) OR (r_timeframe ILIKE %s) OR (r_fund_org ILIKE %s) OR (tag_short_title ILIKE %s)
#                         OR ((To_char(r_start_date, 'Month DD YYYY')) ILIKE %s) OR ((To_char(r_end_date, 'Month DD YYYY')) ILIKE %s)
#                         )"""
#                 values_r += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
#                         f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%",
#                         ]  
#                 if datefilter:
#                     sql_r += """AND (r_year ILIKE %s)"""
#                     values_r += [f"%{datefilter}%"]
#                 else:
#                     sql_r += """"""
#                     values_r += []     
#             else:
#                 sql_r += """"""
#                 values_r += []    
            
#             sql_r += """ORDER BY projects.r_year DESC"""
#             pub_r = db.querydatafromdatabase(sql_r, values_r, cols_r)

#             if pub_r.shape[0]: 
#                 proj_details1 = []
#                 proj_details2 = [] 
#                 proj_details = []
#                 for i in range(len(pub_r)):
#                     if pub_r['Role'][i] == None:
#                         proj_details1 += [" "] 
#                     else:     
#                         proj_details1 += [("Executed project as  %s \n"  % (pub_r['Role'][i])) or " "]
                    
#                     if pub_r['Timeframe'][i] == None:
#                         proj_details2 += [" "] 
#                     else: 
#                         proj_details2 += [("Executed project in %s from %s to %s" % (pub_r['Timeframe'][i],pub_r['Start Date'][i], pub_r['End Date'][i])) or " "]
                    
#                     proj_details += [proj_details1[i] + proj_details2[i]]

                
#                 buttons_r = [] 
#                 for id in pub_r['id']: 
#                     buttons_r += [ 
#                         html.Div( 
#                             dbc.Button('Edit/Delete', href=f"/form_projects?mode=edit&id={id}", size='sm', color='secondary', ), 
#                             style={'text-align': 'center'} 
#                         ) 
#                     ] 
                    
#                 pub_r['Project Details'] = proj_details

#                 last_update_holder_r = pub_r['Last Updated']
#                 pub_r.drop(['Last Updated'],axis=1,inplace=True)
#                 pub_r['Last Updated'] = last_update_holder_r

#                 last_modifiedby_holder_r = pub_r['Last Modified By']
#                 pub_r.drop(['Last Modified By'],axis=1,inplace=True)
#                 pub_r['Last Modified By'] = last_modifiedby_holder_r

#                 pub_r['More Details'] = buttons_r
            
#             pub_r.drop(['id'],axis=1,inplace=True)  
#             pub_r.drop(['Start Date'],axis=1,inplace=True)
#             pub_r.drop(['End Date'],axis=1,inplace=True)
#             pub_r.drop(['Timeframe'],axis=1,inplace=True)
#             pub_r.drop(['Role'],axis=1,inplace=True)
            
#             if pub_r.shape[0]:
#                 table_r = dbc.Table.from_dataframe(pub_r, striped=True, bordered=True, hover=True, size='sm', style={"whiteSpace": "pre-line"}) 
#             else:
#                 table_r = "No records to display"
#             return [table_r] 

#             # table_r = dbc.Table.from_dataframe(pub_r, striped=True, bordered=True, hover=True, size='sm', style={"whiteSpace": "pre-line"}) 
#             # return [table_r] 

#         elif tab == 'tab_o':
#             sql_o = """SELECT
#                     o_year,
#                     publications.pub_id,
#                     faculty.user_id,
#                     faculty_fn || ' ' || faculty_ln AS faculty_full_name,
#                     tag_short_title,
#                     pub_title,
#                     To_char(o_date, 'Month DD YYYY'),
#                     o_add_info,
#                     to_char(publications.pub_last_upd::timestamp, 'Month DD YYYY HH24:MI:SS'),
#                     modified_by
#                 FROM others
#                     INNER JOIN publications on others.pub_id = publications.pub_id
#                     INNER JOIN faculty on publications.user_id = faculty.user_id
#                     INNER JOIN tags on publications.tag_id = tags.tag_id
#                 WHERE
#                     pub_delete_ind = false AND
#                     faculty.user_id = %s
#                 """ 
#             values_o = [f"{currentuserid}"]
#             cols_o = ['Year', 'id', 'userID', 'Faculty Involved', 'Publication Tag', 'Title', 'Date', 'Other Info', 'Last Updated', 'Last Modified By'] 
            
#             # if searchterm:
#             # #OR (tag_short_title %s)
#             #     sql_o += """ AND (faculty_fn ILIKE %s) OR (faculty_ln ILIKE %s) OR (pub_title ILIKE %s) 
#             #         OR (o_date ILIKE %s) OR (o_add_info ILIKE %s)"""
#             #     values_o += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
#             #             f"%{searchterm}%"]
#             if datefilter:
#                 sql_o += """AND (o_year ILIKE %s)"""
#                 values_o += [f"%{datefilter}%"]
#                 if searchterm:
#                     sql_o += """ AND (
#                         (o_year ILIKE %s) OR (pub_title ILIKE %s) OR ((To_char(o_date, 'Month YYYY')) ILIKE %s)
#                         OR (o_add_info ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (tag_short_title ILIKE %s)
#                         )"""
#                     values_o += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
#                         f"%{searchterm}%",]
#                 else:
#                     sql_o += """"""
#                     values_o += [] 
#             elif searchterm:
#                 sql_o += """ AND (
#                         (o_year ILIKE %s) OR (pub_title ILIKE %s) OR ((To_char(o_date, 'Month YYYY')) ILIKE %s)
#                         OR (o_add_info ILIKE %s) OR ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (tag_short_title ILIKE %s)
#                         )"""
#                 values_o += [f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", f"%{searchterm}%", 
#                         f"%{searchterm}%",]
#                 if datefilter:
#                     sql_o += """AND (o_year ILIKE %s)"""
#                     values_o += [f"%{datefilter}%"]
#                 else:
#                     sql_o += """"""
#                     values_o += []    
#             else:
#                 sql_o += """"""
#                 values_o += [] 

#             sql_o += """ORDER BY others.o_year DESC"""
#             pub_o = db.querydatafromdatabase(sql_o, values_o, cols_o) 
            
#             if pub_o.shape[0]: 
#                 buttons_o = [] 
#                 for id in pub_o['id']: 
#                     buttons_o += [ 
#                         html.Div( 
#                             dbc.Button('Edit/Delete', href=f"/form_others?mode=edit&id={id}", size='sm', color='secondary', ), 
#                             style={'text-align': 'center'} 
#                         ) 
#                     ] 
#                 pub_o['More Details'] = buttons_o
            
#             pub_o.drop(['id'],axis=1,inplace=True)  
#             pub_o.drop(['userID'],axis=1,inplace=True) 

#             if pub_o.shape[0]:
#                 table_o = dbc.Table.from_dataframe(pub_o, striped=True, bordered=True, hover=True, size='sm', style={"whiteSpace": "pre-line"}) 
#             else:
#                 table_o = "No records to display"
#             return [table_o] 
#             # table_o = dbc.Table.from_dataframe(pub_o, striped=True, bordered=True, hover=True, size='sm') 
#             # return [table_o] 
#     else: 
#         return PreventUpdate      
