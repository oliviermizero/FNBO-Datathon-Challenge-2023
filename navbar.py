from dash import html
import dash_bootstrap_components as dbc


def create_navbar():
    icon_image = html.Img(src="/assets/icon.png")  # Define the icon_image here

    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(
                dbc.NavLink(
                    [
                        html.I(className="fa-brands fa-github"),  # Font Awesome Icon
                        " "  # Text beside icon
                    ],
                    href="[YOUR GITHUB PROFILE URL]",  # Link the icon should go to
                    target="_blank"  # To make the link open in a new tab
                )
            ),
            dbc.NavItem(
                dbc.NavLink(
                    [
                        html.I(className="fa-brands fa-medium"),  # Font Awesome Icon
                        " "  # Text beside icon
                    ],
                    href="[YOUR MEDIUM PROFILE URL]",
                    target="_blank"
                )
            ),
            dbc.NavItem(
                dbc.NavLink(
                    [
                        html.I(className="fa-brands fa-linkedin"),  # Font Awesome Icon
                        " "  # Text beside icon
                    ],
                    href="[YOUR LINKEDIN PROFILE URL]",
                    target="_blank"
                )
            ),
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="Menu",
                align_end=True,
                children=[  # Add as many menu items as you need
                    dbc.DropdownMenuItem("Analysis", href='/'),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Prediction", href='/page2'),
                    
                ],
            ),
        ],
        brand=icon_image,
        brand_href="/",
        # sticky="top",  # Uncomment if you want the navbar to always appear at the top on scroll.
        color="secondary",  # Change this to change the color of the navbar e.g. "primary", "secondary" etc.
        dark=True,  # Change this to change the color of text within the navbar (False for dark text)
    )

    return navbar
