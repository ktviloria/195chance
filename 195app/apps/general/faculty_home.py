#for viewing all faculty members of the department with button leading to more details of each faculty member
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
import numpy 
 
from app import app
from apps import dbconnect as db
 
from urllib.parse import urlparse, parse_qs

layout= html.Div( 
    [ 
        dbc.Card(
            [
                dbc.CardHeader(html.H2("Faculty Members")),
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                html.H4("Find Faculty Member", style={'fontWeight': 'bold'}),
                                dbc.Row(
                                    [
                                        dbc.Label(
                                            html.Div([
                                                html.Img(src=app.get_asset_url('search.png'), height="20px", width="18px", style={'position':'left','vertical-align':'middle'}),
                                                html.Span("Search", style={'vertical-align': 'right', 'padding-left':'5px', 'font-size':'20px'}),
                                            ]),
                                            width=1
                                        ),
                                        dbc.Col(
                                            dbc.Input(
                                                type="text", id="fac_filter", placeholder="Enter faculty first name or last name", style={'display': 'flex', 'align-items': 'center', 'height': '5vh'}
                                            ),
                                            width=4,
                                        ),
                                        dbc.Col(
                                            [
                                            dcc.Dropdown(
                                               options=[
                                                        {'label': 'Professor', 'value': 'Professor'},
                                                        {'label': 'Associate Professor', 'value': 'Associate Professor'},
                                                        {'label': 'Assistant Professor', 'value': 'Assistant Professor'},
                                                        {'label': 'Instructor', 'value': 'Instructor'},
                                                        {'label': 'University Professor', 'value': 'University Professor'},
                                                        {'label': 'Teaching Fellow', 'value': 'Teaching Fellow'},
                                                        {'label': 'Teaching Associate', 'value': 'Teaching Associate'},
                                                    ],
                                                id = 'rank_dropdown', multi = True, placeholder="Filter faculty by rank"
                                            ),
                                            ],width=6,
                                        )
                                    ],
                                    className="mb-3",
                                ),
                                dbc.Row(       
                                    [
                                        dbc.Col( id='faclist1', style={"justify-content": "center"}), 
                                        dbc.Col( id='faclist2', style={"justify-content": "center"}),
                                        dbc.Col( id='faclist3', style={"justify-content": "center"}),  
                                    ], justify=  "center",                        
                                   
                                ), 
                                # html.Div(
                                #     [
                                #         dbc.Modal(
                                #             [
                                #                 dbc.ModalHeader(dbc.ModalTitle("Faculty Details"), close_button=True),
                                #                 dbc.ModalBody(id='modal_body')
                                #             ],
                                #             id="modal-centered",
                                #             centered=True,
                                #             is_open=False,
                                #         ),
                                #     ]
                                # )
                            ]
                        )
                    ]
                )
            ]
        ),
    ]
)



#faculty list with name, rank and button that opens faculty_details
@app.callback(
    [
        Output('faclist1', 'children'),
        Output('faclist2', 'children'),
        Output('faclist3', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('fac_filter', 'value'),
        Input('rank_dropdown', 'value')
    ]
)

def facultyhome_loadfacultylist(pathname, searchterm, rankfilter):
    if pathname == '/faculty_home':
        sql = """SELECT
                faculty.user_id,
                faculty_ln || ', ' || faculty_fn AS faculty_full_name,
                rank_title
            FROM faculty
                INNER JOIN ranks ON faculty.rank_id = ranks.rank_id
                INNER JOIN users on faculty.user_id = users.user_id
                
                
            """
        val = []
        colnames = ['userID', 'Full Name', 'Rank'] 
        
        
        
        
        
        if rankfilter != None and searchterm != None: 
            for i in range(len(rankfilter)):
                if i == 0:
                    sql += """WHERE rank_title ILIKE %s """
                    val +=  [f"{rankfilter[i]}%"]
                else:
                    sql += """OR rank_title ILIKE %s"""
                    val +=  [f"{rankfilter[i]}%"]
                    
                sql += """ AND (faculty_delete_ind = false AND
                faculty_active_ind = true) AND (
                ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (rank_title ILIKE %s))
                """
                val += [f"%{searchterm}%", f"%{searchterm}%"]
            sql += """AND (faculty_delete_ind = false AND
            faculty_active_ind = true)
            """
        if rankfilter != None and searchterm == None: 
            for i in range(len(rankfilter)):
                if i == 0:
                    sql += """WHERE rank_title ILIKE %s """
                    val +=  [f"{rankfilter[i]}%"]
                else:
                    sql += """OR rank_title ILIKE %s"""
                    val +=  [f"{rankfilter[i]}%"]
            sql += """AND (faculty_delete_ind = false AND
            faculty_active_ind = true)
            """
        if rankfilter == None and searchterm != None: 
            sql += """WHERE (faculty_delete_ind = false AND
            faculty_active_ind = true)
            """
            sql += """ AND (((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (rank_title ILIKE %s))
            """
            val += [f"%{searchterm}%", f"%{searchterm}%"]
            
        if rankfilter == None and searchterm == None: 
            sql += """WHERE (faculty_delete_ind = false AND
            faculty_active_ind = true)
            """
            

        # if searchterm:
        #     # We use the operator ILIKE for pattern-matching
        #     # The % before and after the term means that
        #     # there can be text before and after
        #     # the search term
        #     sql += """ AND ((faculty_fn || ' ' || faculty_ln) ILIKE %s) OR (rank_title ILIKE %s)
        #     """
        #     val += [f"%{searchterm}%", f"%{searchterm}%",]
            

        # if rankfilter:
        #     for i in range(len(rankfilter)):
        #         if i == 0:
        #             sql += """AND rank_title ILIKE %s """
        #             val +=  [f"{rankfilter[i]}%"]
        #         else:
        #             sql += """OR rank_title ILIKE %s"""
        #             val +=  [f"{rankfilter[i]}%"]
        
        
            


        sql += """ORDER BY faculty.faculty_ln ASC"""
        fac = db.querydatafromdatabase(sql, val, colnames)

        # if fac.shape[0]: 
        #     buttons = [] 
        #     for userid in fac['userID']: 
        #         buttons += [ 
        #             html.Div( 
        #                 dbc.Button('View',
        #                 href=f'/faculty_details?mode=view&id={userid}',
        #                 # id='viewbtn',
        #                 size='sm', color='info') 
        #             ) 
        #         ] 
        #     fac['More Details'] = buttons 
        # table = dbc.Table.from_dataframe(fac, striped=True, bordered=True, hover=True, size='sm') 
        # return [table] 
        cards1 =[]
        cards2 =[]
        cards3 =[]    
            
        if fac.shape[0]: 
            cards = []
            for i in range(len(fac)): 
                name_of_fac = fac['Full Name'][i]
                faculty_rank = fac['Rank'][i]
                userid = fac['userID'][i]
                fac_pic = app.get_asset_url(f"{userid}.png")
                # cards += [
                #         dbc.CardImg(src=fac_pic), 
                #         dbc.CardBody(
                #             [
                #                 html.H4(f'{name_of_fac}'), 
                #                 html.P(f'{faculty_rank}'),
                #                 dbc.Button('More Details', href=f'/faculty_details?mode=view&id={userid}')
                #             ]
                #         )
                #     ]
                cards +=[ dbc.Card(
                    [
                        dbc.CardImg(src=fac_pic), 
                        dbc.CardBody(
                            [
                                html.H5(f'{name_of_fac}'), 
                                html.P(f'{faculty_rank}'),
                                dbc.Button('More Details', color='danger', href=f'/faculty_details?mode=view&id={userid}')
                            ]
                        )
                    ],style={"width": "20rem", "height": "30rem"},
                )]
                
                cards1, cards2, cards3 = [cards[i::3]for i in range(3)]
                # print(cards1)
                # print(cards2)
                # print(cards3)
                # cards1 = cards[0::3]
                # cards2 = cards[1::3]
                # cards3 = cards[2::3]
        return[cards1, cards2, cards3]
    else: 
        return ["No records to display.", " ", " "]
