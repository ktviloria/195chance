import hashlib 

import dash_bootstrap_components as dbc 
from dash import dcc, html, callback_context 
from dash.dependencies import Input, Output, State 
from dash.exceptions import PreventUpdate 

from app import app 
from apps import dbconnect as db 

layout =html.Div(
    dbc.Col(
        [
            #logo
            dbc.Row(
                [
                    dbc.Col(
                        html.Img(src=app.get_asset_url('delphi_logo.png'), height="180px"),
                        width = {"size": 6, "offset": 3},
                    )
                ],
                className="mb-3",
                # align="center",
                # justify="center",
                style = {   
                        'text-align': 'center',  
                        'color': '#fff', 
                        'padding-top': '25px', 
                },
            ),
            #App Name
            dbc.Row(
                html.H1("DelPHI"),
                style={'font-weight':'bold','text-align': 'center', 'font-family': "Times New Roman"},
                align="center",
                justify="center",
            ),
            dbc.Row(
                html.H4("Departmental Publications Hearth for IEORD"),
                style={'font-weight': 'normal','text-align': 'center'},
                align="center",
                justify="center",
            ),
            html.Hr(),
            #alert
            dbc.Alert('Username or password is incorrect.', color='danger', id='login_alert', is_open=False),
            #Enter username or email
            dbc.Row( 
                [
                    dbc.Label("Username", width=2, size='lg', style={"font-weight": "normal"}), 
                    dbc.Col( 
                        dbc.Input( 
                            type="text", id="user_un", placeholder="Enter username", size = 'lg' 
                        ), 
                        width=6, 
                    ), 
                ],
                className="mb-3",
                align="center",
                justify="center",
            ),
            #Enter password
            dbc.Row( 
                [
                    dbc.Label("Password", width=2, size='lg', style={"font-weight": "normal"}), 
                    dbc.Col( 
                        dbc.Input( 
                            type="password", id="user_pass", placeholder="Enter password", size='lg' 
                            ), 
                        width=6, 
                    ),
                ],
                className="mb-3",
                align="center",
                justify="center",
            ),
            #login button
            dbc.Row(
                dbc.Button('Login', id='login_loginbtn', size='lg', color='danger', class_name='me-1', style={'width':'150px'}),
                className="mb-3",
                align="center",
                justify="center",
            ),
            html.Br(),
            #UPD-IEORD
            html.Div(
                html.Img(src=app.get_asset_url('UPD-IEORD.png')),
                style = { 
                        'position': 'bottom', 
                        'bottom': '0',
                        'left': '0px', 
                        'bottom': '30px',   
                        'right': '0px',    
                        'text-align': 'center',  
                        'color': '#fff', 
                        'padding-top': '10px', 
                },          
            )
        ],
        width={"size": 6, "offset": 3},
    ), 
)


#login process - allows user to use the app if correct login details, pulls up alert if incorrect details, changes userid and role to default when user logs out
@app.callback( 
    [ 
        Output('login_alert', 'is_open'),
        Output('url', 'pathname'), 
        Output('currentuserid', 'data'), 
        Output('currentrole', 'data')
    ], 
    [ 
        Input('login_loginbtn', 'n_clicks'), 
    ], 
    [ 
        # State('user_mail', 'value'),
        State('user_un', 'value'), 
        State('user_pass', 'value'),    
        State('sessionlogout', 'data'), 
        State('currentuserid', 'data'), 
        State('currentrole', 'data')  
    ] 
) 
def loginprocess(loginbtn, username, password, 
                 sessionlogout, currentuserid, currentrole): 
    openalert=False
    #pull up database information
    if loginbtn and username and password: 
        sql = """SELECT 
                user_id, 
                user_type 
            FROM users 
            WHERE  
                user_un = %s AND
                user_pass = %s""" 
        encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest()  

        values = [username, encrypt_string(password)] 
        cols = ['userid', 'usertype'] 
        df = db.querydatafromdatabase(sql, values, cols) 
            
        if df.shape[0]: # if query returns rows 
                currentuserid = df['userid'][0]
                currentrole = df['usertype'][0]
                url = '/home'
        else: 
            openalert = True
            url = '/'
            currentuserid = ''
            currentrole = ''
            # print('incorrect login details') 
    else:
        url = '/'
        currentuserid = -1
        currentrole = -1
        # print('login: this changes currentuser and currentrole to -1')
    return [openalert, url, currentuserid, currentrole]
