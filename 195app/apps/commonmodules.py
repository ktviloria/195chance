from dash import dcc 
from dash import html 
import dash_bootstrap_components as dbc 
import dash 
from dash.dependencies import Input, Output, State 
from dash.exceptions import PreventUpdate 
import pandas as pd 

from app import app
from apps import dbconnect as db 

# navbar - dbc/css 
navlink_style = { 
 'color': '#fff', 
 'margin-right': '0em', 
 'margin-left': '1em',
 'fontWeight': 'bold',
 'font-size': '19px'
} 
navlink_style_offcanvas = { 
 'color': '#000', 
 'margin-right': '0em', 
 'margin-left': '1em',
 'fontWeight': 'medium',
 'font-size': '25px',
 'float':'left'
} 
nav_style = { 
 'color': '#0000', 
 'padding-right': '2em', 
 'padding-left': '2em', 
 'display': 'flex', 
} 

navbar = dbc.Navbar( 
    [
        dbc.Row( 
            [ 
                #navbar brand 
                dbc.Col( 
                    html.A( 
                        # Use row and col to control vertical alignment of logo / brand 
                        dbc.NavbarBrand(
                            html.Img(src=app.get_asset_url('delphi_logo_wcbg.png'), height="40px"),
                            className="ml-2", 
                            style={'margin-right': '50em', 'color':'light'} 
                        ), 
                        href="/home", 
                    ), 
                    width=1
                ), 
                #navbar links 
                dbc.Col( 
                    dbc.Row( 
                        [ 
                            dbc.Col( 
                                dbc.NavLink(
                                            [html.Div([
                                                html.Img(src=app.get_asset_url('home_nav.png'), height="30px", width="30px", style={'vertical-align': 'middle'}),
                                                html.Span("Home", style={'vertical-align': 'middle', 'padding-left':'10px'}),
                                            ]),
                                        ],
                                        href="/home", style=navlink_style), 
                                width=4 
                            ), 
                            dbc.Col( 
                                dbc.NavLink(
                                            [html.Div([
                                                html.Img(src=app.get_asset_url('faculty_nav.png'), height="40px", width="40px", style={'vertical-align': 'middle'}),
                                                html.Span("Faculty", style={'vertical-align': 'middle', 'padding-left':'10px'}),
                                            ]),
                                        ],
                                        href="/faculty_home", style=navlink_style), 
                                width=4 
                            ), 
                            dbc.Col( 
                                dbc.NavLink(
                                            [html.Div([
                                                html.Img(src=app.get_asset_url('publications_nav.png'), height="35px", width="35px", style={'vertical-align': 'middle'}),
                                                html.Span("Records", style={'vertical-align': 'middle', 'padding-left':'10px'}),
                                            ]),
                                        ],
                                        href="/publications_home", style=navlink_style), 
                                width=4
                            ), 
                        ], 
                    ), 
                    style={'text-align': 'right'}, 
                    width=8
                ),
                #side menu 
                dbc.Col( 
                    html.Div( 
                        [ 
                            dbc.Button(
                                html.Img(src=app.get_asset_url('side_panel_button.png'), height="30px", width="40px"),
                                style = {   
                                        'text-align': 'center',  
                                        'color': '#fff', 
                                        'padding-top': '5px',
                                        'padding-right': '2px',
                                        'padding-left': '2px' 
                                },
                                id="open-offcanvas", n_clicks=0, color="light"
                            ), 
                            dbc.Offcanvas( 
                                [ 
                                    #all users
                                    html.Div(
                                        [html.Div(
                                            html.Img(src=app.get_asset_url('delphi_logo.png'), height="100px"),
                                            style = {   
                                                    'text-align': 'top',  
                                                    'color': '#fff', 
                                                    'padding-top': '0px', 
                                            },
                                        ),
                                        html.Br(),
                                        # html.Br(),
                                        dbc.NavLink(
                                            [html.Div([
                                                html.Img(src=app.get_asset_url('home.png'), height="25px", width="25px"),
                                                html.Span("Home", style={'vertical-align': 'middle','padding-left':'20px'}),
                                            ]),
                                        ],
                                        href="/home", style=navlink_style_offcanvas), 
                                        html.Br(),
                                        html.Br(),
                                        dbc.NavLink(
                                            [html.Div([
                                                html.Img(src=app.get_asset_url('faculty.png'), height="35px", width="25px"),
                                                html.Span("Faculty Members", style={'vertical-align': 'middle','padding-left':'20px'}),
                                            ]),
                                        ],
                                        href="/faculty_home", style=navlink_style_offcanvas),
                                        html.Br(),
                                        html.Br(),
                                        dbc.NavLink(
                                            [html.Div([
                                                html.Img(src=app.get_asset_url('publications.png'), height="30px", width="25px"),
                                                html.Span("Departmental Records", style={'vertical-align': 'middle','padding-left':'20px'}),
                                            ]),
                                        ],
                                        href="/publications_home", style=navlink_style_offcanvas)
                                        ], id='offcanvas_gen_div'
                                    ),
                                    html.Br(),
                                    #faculty
                                    html.Div(
                                        [
                                            html.Br(),
                                            html.Br(),
                                            dbc.NavLink(
                                            [html.Div([
                                                html.Img(src=app.get_asset_url('my_profile.png'), height="25px", width="25px"),
                                                html.Span("My Profile", style={'vertical-align': 'middle','padding-left':'20px'}),
                                            ]),
                                            ],
                                            href="/my_profile", style=navlink_style_offcanvas),
                                            html.Br(),
                                            html.Br(),
                                            dbc.NavLink(
                                            [html.Div([
                                                html.Img(src=app.get_asset_url('my_publications.png'), height="25px", width="25px"),
                                                html.Span("My Records", style={'vertical-align': 'middle','padding-left':'20px'}),
                                            ]),
                                            ],
                                            href="/my_publications", style=navlink_style_offcanvas) 
                                        ],
                                        id='offcanvas_fac_div'
                                    ),
                                    html.Br(),
                                    #admin
                                    html.Div(
                                        [
                                            html.Br(),
                                            dbc.NavLink(
                                            [html.Div([
                                                html.Img(src=app.get_asset_url('dashboard.png'), height="25px", width="25px"),
                                                html.Span("Dashboard", style={'vertical-align': 'middle','padding-left':'20px'}),
                                            ]),
                                            ],
                                            href="/dashboard", style=navlink_style_offcanvas),
                                            html.Br(),
                                            html.Br(),
                                            dbc.NavLink(
                                            [html.Div([
                                                html.Img(src=app.get_asset_url('authors.png'), height="25px", width="25px"),
                                                html.Span("Authors Management", style={'vertical-align': 'middle','padding-left':'20px'}),
                                            ]),
                                            ],
                                            href="/author_manage", style=navlink_style_offcanvas),
                                            html.Br(),
                                            html.Br(),
                                            dbc.NavLink(
                                            [html.Div([
                                                html.Img(src=app.get_asset_url('faculty_mngmt.png'), height="25px", width="25px"),
                                                html.Span("User Management", style={'vertical-align': 'middle','padding-left':'20px'}),
                                            ]),
                                            ],
                                            href="/faculty_manage", style=navlink_style_offcanvas),
                                            html.Br(),
                                            html.Br(),
                                            dbc.NavLink(
                                            [html.Div([
                                                html.Img(src=app.get_asset_url('pub_mngmt.png'), height="25px", width="25px"),
                                                html.Span("Records Management", style={'vertical-align': 'middle','padding-left':'20px'}),
                                            ]),
                                            ],
                                            href="/publications_manage", style=navlink_style_offcanvas),
                                            html.Br(),
                                            html.Br(),
                                            dbc.NavLink(
                                            [html.Div([
                                                html.Img(src=app.get_asset_url('settings.png'), height="25px", width="25px"),
                                                html.Span("Settings", style={'vertical-align': 'middle','padding-left':'20px'}),
                                            ]),
                                            ],
                                            href="/settings", style=navlink_style_offcanvas),
                                            html.Br(),
                                            html.Br(),
                                            dbc.NavLink(
                                            [html.Div([
                                                html.Img(src=app.get_asset_url('reports.png'), height="25px", width="25px"),
                                                html.Span("Reports", style={'vertical-align': 'middle','padding-left':'20px'}),
                                            ]),
                                            ],
                                            href="/reports", style=navlink_style_offcanvas),
                                        ],
                                        id='offcanvas_admin_div'
                                    ),
                                    #logout
                                    dbc.Button(
                                        "Logout", 
                                        id="logout-offcanvas", 
                                        n_clicks=0,
                                        href="/login",
                                        color = 'danger',
                                        style={
                                            'position': 'absolute',
                                            'bottom': 20,
                                            'right': 20,
                                        }
                                    ), 
                                ], 
                                id="offcanvas", 
                                is_open=False, 
                                placement="end",
                                style ={'text-align': 'center',  
                                        'color': '#fff', 
                                        'padding-top': '10px'
                                },
                                scrollable=True,
                            ),                                 
                        ] 
                    ), 
                    style={'text-align': 'right'}, 
                    width=3
                ) 
            ], 
        ) 
    ], 
    dark=True, 
    color='#919191', 
    style={ 
        'color': '#fff', 
        'padding-right': '2em', 
        'padding-left': '2em', 
        'padding-top': '0.5em',
        'padding-bottom': '0.5em',
        'display': 'flex', 
        'flex': '1' 
    } 
) 

#app callback-off canvas
@app.callback( 
    Output("offcanvas", "is_open"),
    Output('offcanvas_fac_div', 'style'),
    Output('offcanvas_admin_div', 'style'),

    Input("open-offcanvas", "n_clicks"),
    Input("logout-offcanvas", "n_clicks"),
    # Input("offcanvas_admin_div", "n_clicks"),
    Input("offcanvas_gen_div", "n_clicks"),
    Input("offcanvas_admin_div", "n_clicks"),
    Input("offcanvas_fac_div", "n_clicks"),

    State("offcanvas", "is_open"),
    State('currentrole', 'data'),
    State('currentuserid', 'data'),
) 
def toggle_offcanvas(n1, logoutbtn, d1, d2, d3,
                     is_open, currentrole, userid
                     ): 
    if currentrole == "faculty":
        offcanvas_fac_div = {'display':'contents'}
        offcanvas_admin_div = {'display':'none'}
    else:
        offcanvas_fac_div = {'display':'none'}
        offcanvas_admin_div = {'display':'contents'}

    sql = """
        select  
		    user_un    
        from 
            users
        where
            user_ID = %s
        """
    val = [f"{userid}"]
    colnames = ['username']
    name = db.querydatafromdatabase(sql, val, colnames)

    # Close the offcanvas when not hovered
    # ctx = dash.callback_context
    # # if ctx.triggered[0]["prop_id"] == "interval.n_intervals" and is_open:
    # #     return False
    # if ctx.triggered[0]["prop_id"] == "offcanvas_admin_div.n_clicks" and is_open:
    #     return False
    
    if n1 or logoutbtn or d1 or d2 or d3:
        return [not is_open, offcanvas_fac_div, offcanvas_admin_div]
    else:
        return [is_open, offcanvas_fac_div, offcanvas_admin_div]
