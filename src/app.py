# pip install dash-ag-grid==2.0.0a2
import dash_ag_grid as dag
import dash
from dash import Dash, html, Input, Output, State, no_update, ctx, dcc
import dash_bootstrap_components as dbc # pip install dash-bootstrap-components
import pandas as pd                     # pip install pandas
import os
from datetime import datetime
from dash import callback_context
from dash.exceptions import PreventUpdate


app = Dash(__name__, 
           external_stylesheets=[dbc.themes.CYBORG],
        #    meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}]
           )
server = app.server


responsible_bd = [
    'beiyi.lim@klook.com',
    'chloe.ang@klook.com',
    'fynn.loh@klook.com',
    'nicholas.kang@klook.com',
    'vivian.tan@klook.com',
    'saiseong.chue@klook.com'
    ]

# df_init = pd.read_csv("TTD - Lose Case Tracker 2024  - SG.csv")
# df_init = pd.read_csv("/Users/varun.srivastava/Desktop/Klook_Projects/BD_Alerts/src/lose_case_tracker_010924.csv")

df_init = pd.read_csv("https://raw.githubusercontent.com/varun-dev-stack/test_lose_case_alert/main/src/lose_case_tracker_010924.csv")

print(f'Checking the columns in df_init {df_init.columns}')
df_init.rename(columns={'date':'Report Date','BML ':'BML'}, inplace=True)
print(df_init.columns)
columns=['Report Date', 'responsible_bd', 'bu_level_1',
       'segment', 'activity_id', 'activity_name', 'package_id', 'package_name', 'sku_id',
       'sku_name', 'selling_currency', 'cost', 'klook_market_price',
       'klook_price', 'klook_auto_price', 'BML',
       'competitor_price', 'competitor_code', 'competitor_package_name',
       'participation_date', 'competitor_url', 'country_name_en', 'price_discrepancy',
       'Var', 'take_rate', 'TR_after_match','Var_auto','destination']

df = df_init[columns]
df['Price_Action'] = ""
df['Report_to_merchant'] = ""
df['BD_options'] = ""
df['Report Date'] = pd.to_datetime(df['Report Date'], errors='coerce')
df = df[~df['Report Date'].isna()]
df['Report Date'] = df['Report Date'].dt.strftime('%Y-%m-%d')
print(f'Check the columns of df {df.columns}')
df['segment'].fillna('Segment N/A',inplace=True)
df['destination'].fillna('Dest. N/A',inplace=True)

# Define the custom order for sorting
custom_order = ['Segment 0', 'Segment 1', 'Segment 2', 'Segment 3', 'Segment N/A']
# Convert the 'Segment' column to a categorical type with the custom order
df['segment'] = pd.Categorical(df['segment'], categories=custom_order, ordered=True)

df = df.sort_values(by=['Report Date','segment'], ascending=[False, True])

segment_options = [{'label': segment, 'value': segment} for segment in df['segment'].unique()]

print(f'segment_options are {segment_options}')

current_date = datetime.now().strftime('%Y-%m-%d')

dropdown_options = [{'label': bd, 'value': bd} for bd in df['responsible_bd'].unique()]
regions = [{'label': destination, 'value': destination} for destination in df['destination'].unique()]
# file_path = 'src/bd_alerts_test/'
file_path = "https://raw.githubusercontent.com/varun-dev-stack/test_lose_case_alert/main/src/bd_alerts_test"
bd_options = [
              "Option 1",
              "Option 2",
              "Option 3",
              "Option 4",
            #   "Can't match - Take rate is low",
            #   "Can't match - Peak season, high demand",
            #   "Can't match - Incorrect price (Submit a ticket to Pricing Team)",
            #   "Can't match - Incorrect mapping (Submit a ticket to Pricing Team)",
            #   "Can't match - Competitor bulk purchased",
            #   "Can't match - Not major competitor, monitoring",
            #   "Can't match - Competitor is runing limited time promotion",
            #   "Can't match - Runing a price test",
            #   "Can't match - Rate Plan",
            #   "Can't match - White lable",
            #   "Can't match - others",
            #   "Can't match - Not feasible"
              ]

init_num=0


print(df.shape)

columnDefs = [
    {
        'headerName':'BD Input Section',
        "marryChildren": True,
        'headerClass': 'cyan-header',
        'children':[
            {
                "headerName":"Reported to Merchant?",
                "field":"Report_to_merchant",
                "pinned":True,
                "cellEditor": "agSelectCellEditor",
                "cellEditorParams": {
                    "values": ['Yes','No']
                    },
            },
            {

                "headerName":"BD Action",
                "field":"BD_options",
                "pinned":True,
                "cellEditor": "agSelectCellEditor",
                "cellEditorParams": {
                    "values": bd_options
                },
            },
            {
                "headerName": "BD Feedback", 
                "pinned":True,
                "field": "Price_Action", "columnGroupShow":"closed"
            }
            ]
    },
    # {
    #     "headerName": "Report Date",
    #     "field": "Report Date",
    # },
    {
        "headerName": "BU_Level_1",
        "suppressStickyLabel": True,
        "field": "bu_level_1",
    },
    {
        'headerName': 'Activity Details',
        "marryChildren": True,
        'headerClass': 'teal-header',
        "suppressStickyLabel": True,
        'children':[
            {
                "headerName": "AID",
                "field": "activity_id","columnGroupShow":"closed"
            },
            {
                "headerName": "Activity",
                "field": "activity_name","columnGroupShow":"open"
            },
            {
                "headerName": "PID",
                "field": "package_id","columnGroupShow":"open"
            },
            {
                "headerName": "SKU ID",
                "field": "sku_id","columnGroupShow":"open"
            },
            # {
            #     "headerName": "Segment",
            #     "field": "segment","columnGroupShow":"open"
            # },
            # {
            #     "headerName": "BD",
            #     "field": "responsible_bd","columnGroupShow":"open"
            # },
            ]
    },
    {
        'headerName':'Package Details',
        "marryChildren": True,
        'headerClass': 'teal-header',
        "suppressStickyLabel": True,
        'children':[
            {
                "headerName": "Package",
                "field": "package_name","columnGroupShow":"closed"
            },
            {
                "headerName": "SKU",
                "field": "sku_name","columnGroupShow":"open"
            },
            {
                "headerName": "Participation Date",
                "field": "participation_date","columnGroupShow":"closed"
            },
    ]
    },
    {
        "headerName": "Competitor",
        "suppressStickyLabel": True,
        "field": "competitor_code",
    },
    {
        "headerName": "Competitor Package",
        "suppressStickyLabel": True,
        "field": "competitor_package_name",
    },
    {
        'headerName':'Price Comparison',
        "marryChildren": True,
        'headerClass': 'teal-header',
        "suppressStickyLabel": True,
        'children':[
            {
                "headerName": "Currency",
                "field": "selling_currency"
            },
            {
                "headerName": "Klook Price",
                "field": "klook_price",
            },
            {
                "headerName": "Comp. Price",
                "field": "competitor_price",
            }
            ]
    },
    {
        'headerName':'TR & Variance',
        "marryChildren": True,
        'headerClass': 'teal-header',
        "suppressStickyLabel": True,
        'children':[
            {
                "headerName": "BML",
                "field": "BML ","columnGroupShow":"closed"
            },
            {
                "headerName": "Price Variance%",
                "field": "Var","columnGroupShow":"closed"
            },
            {
                "headerName": "TR%",
                "field": "take_rate","columnGroupShow":"open"
            },
            {
                "headerName": "TR% (after price match)",
                "field": "TR_after_match","columnGroupShow":"open"
            }
            ]
    }

]

defaultColDef = {
    "filter": True,
    "floatingFilter": True,
    "resizable": True,
    "sortable": True,
    "editable": True,
    "minWidth": 135,
    "wrapHeaderText": True,
    "autoHeaderHeight": True
}


table = dag.AgGrid(
    id="portfolio-table",
    className="ag-theme-alpine-dark",
    columnDefs=columnDefs,
    rowData=df.to_dict("records"),
    columnSize="sizeToFit",
    defaultColDef=defaultColDef,
    rowDragManaged=True,
    dashGridOptions={"rowSelection": "multiple", "suppressRowClickSelection": True, "animateRows": False},
)

table_submitted = dag.AgGrid(
    id="portfolio-table-submitted",
    className="ag-theme-alpine-dark",
    columnDefs=columnDefs,
    rowData=[],
    columnSize="sizeToFit",
    defaultColDef=defaultColDef,
    rowDragManaged=True,
    dashGridOptions={
        "undoRedoCellEditing": True, 
        "selectedRows":"multiple",
        },
)


app.layout = dbc.Container(
    [
        dcc.Store(id='trigger-update'),
        html.Div("Lose Case Tracker App", className="h3 p-2 text-white bg-secondary", id='not-important'),
        dbc.Row(
            [
                dbc.Col(
                        html.Div
                        (
                            [
                                html.P(),
                                html.P('Observation Date', style={'color': 'white'}),
                                dcc.DatePickerSingle(
                                    id='date_filter',
                                    date=max(pd.to_datetime(df['Report Date'])).date(),  # Set default date to the max date in the dataframe
                                    min_date_allowed=min(pd.to_datetime(df['Report Date'])).date(),  # Set minimum allowed date
                                    max_date_allowed=max(pd.to_datetime(df['Report Date'])).date(),  # Set maximum allowed date
                                    initial_visible_month=max(pd.to_datetime(df['Report Date'])).date(),  # Set initial visible month
                                    display_format='DD/MM/YYYY',  # Format for the date display
                                    # className='dcc_control',  # CSS class for styling
                                    style={'width': '100%', 'height': '38px'}  # Ensure full width within the column
                                )
                           ], 
                           style={'padding': '10px','margin-bottom': '0px'}
                        ),
                        width=3,
                        # style={'margin':'auto'}
                ),

                 dbc.Col(
                    html.Div
                    (
                        [
                            html.P(),
                            html.P('Region',  style={'color': 'white'}),
                            dcc.Dropdown
                            (
                                id='region_filter',
                                # options = regions,
                                options=[{'label': destination, 'value': destination} for destination in df['destination'].unique()],
                                # value='Singapore',
                                value=df['destination'].unique()[0],
                                # className='dcc_control',
                                style={'width':'85%', 'height': '38px'},
                                searchable=True,
                            )
                        ], 
                    style={'padding': '10px', 'margin-bottom': '0px'}
                    ),
                    width=3,
                ),

                dbc.Col(
                    html.Div
                    (
                        [
                            html.P(),
                            html.P('Responsible BD',  style={'color': 'white'}),
                            dcc.Dropdown
                            (
                                id='bd_filter',
                                options=[],
                                value='',
                                # value='fynn.loh@klook.com',
                                # className='dcc_control',
                                style={'width':'100%', 'height': '38px'},
                                searchable=True,
                            )
                        ], 
                        style={'padding': '10px', 'margin-bottom': '0px', 'margin-right': '10px'}
                    ),
                    width=3,
                ),

                dbc.Col(
                    html.Div
                    (
                        [
                            html.P(),
                            html.P('Segment',  style={'color': 'white'}),
                            dcc.Dropdown
                            (
                                id='segment_filter',
                                options=segment_options,  # Use filtered options here
                                value=segment_options[0]['value'],
                                style={'width':'100%', 'height': '38px'},
                                searchable=True,
                            )
                        ], 
                    style={'padding': '10px', 'margin-bottom': '0px', 'margin-left': '50px'}
                    ),
                    width=3,
                ),
            ],
            justify='center',  # Align the columns centrally
        ),

        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card([
                                dbc.CardBody(
                                    [
                                        table,
                                        dbc.Row([
                                            dbc.Col([
                                                dbc.Button(
                                                    id="save-btn",
                                                    children="Save Table",
                                                    color="primary",
                                                    size="md",
                                                    className='mt-2'
                                                ),
                                            ], width=3)
                                        ]),
                                    ]
                                ),
                            ],)
                    ],
                    width=12,
                ),
            ],
            className="py-4",
        ),
        dbc.Row(
            dbc.Alert(children=None,
                      color="success",
                      id='alerting',
                      is_open=False,
                      duration=2000,
                      className='ms-4',
                      style={'width':'18rem'}
            ),
        ),
        html.P(),
        html.Br(),
        html.Div("Action Tracker", className="h4 p-2 text-white bg-secondary", id='action_tracker',style={'display': 'none'} ),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        table_submitted
                    ),
                    id='submitted_table_div',
                    style={'display': 'none'}
                )
            )
        ),
    ],

)

@app.callback(
    Output('bd_filter', 'options'),
    Output('bd_filter', 'value'),
    [Input('date_filter', 'date'),
     Input('region_filter', 'value'),
    #  Input('segment_filter', 'value')
     ]
)
def update_responsible_bd_options(selected_date, selected_region):

    # Filter the DataFrame based on the selected values
    filtered_df = df[(df['Report Date'] == selected_date) &
                     (df['destination'] == selected_region)]
    
    # Extract unique "Responsible BD" options from the filtered DataFrame
    bd_options = [{'label': bd, 'value': bd} for bd in filtered_df['responsible_bd'].unique()]
    # print(f'Checking the value of bd_options {bd_options}')

    # If no options are available, return an empty list or a default option
    if not bd_options:
        bd_options = [{'label': 'No BD Available', 'value': 'No BD Available'}]
        value = 'No BD Available'
    else:
        value = bd_options[0]['value']

    return bd_options, value

@app.callback(
    Output('segment_filter', 'options'),
    Output('segment_filter', 'value'),
    [Input('date_filter', 'date'),
     Input('region_filter', 'value'),
     Input('bd_filter', 'value')
     ]
)
def update_segment_options(selected_date, selected_region, selected_bd):

    # Filter the DataFrame based on the selected values
    filtered_df = df[(df['Report Date'] == selected_date) &
                     (df['destination'] == selected_region) &
                     (df['responsible_bd'] == selected_bd)
                     ]
    
    # Extract unique "Responsible BD" options from the filtered DataFrame
    segments = [{'label': segment, 'value': segment} for segment in filtered_df['segment'].unique()]
    # print(f'Checking the value of bd_options {bd_options}')

    # If no options are available, return an empty list or a default option
    if not segments:
        segments = [{'label': 'No Segment Available', 'value': 'No Segment Available'}]
        value = 'Segment not defined'
    else:
        value = segments[0]['value']

    return segments, value

@app.callback(
        Output("portfolio-table","rowData"),
        [Input("date_filter","date"),
        Input("bd_filter","value"),
        Input('region_filter', 'value'),
        Input('segment_filter', 'value')
        ]
)
def update_lose_case_table(date, resp_bd, selected_region, selected_segment):
    df_filtered = df[(df['Report Date'] == date) & 
                     (df['responsible_bd'] == resp_bd) &
                     (df['destination'] == selected_region) &
                     (df['segment'] == selected_segment)]
    
    return df_filtered.to_dict('records')


@app.callback(
    [Output("alerting", "is_open"),
     Output("alerting", "children"),
     Output("alerting", "color"),
     Output('trigger-update', 'data')],
    Input("save-btn", "n_clicks"),
    State("portfolio-table", "rowData"),  # Use updated rowData
    prevent_initial_call=True,
)
def update_dash_table(n,data):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if n is None:
            return False, None, None, None
        else:
            init_table = pd.DataFrame(data)
            # updated_table = init_table[init_table['Price_Action'] != ""]
            updated_table = init_table[init_table['Report_to_merchant'] != ""]

            print(f'Checking the value of updated table {updated_table}')
            resp_bd = updated_table['responsible_bd'].unique()[0]
            file_name = file_path + resp_bd + '_test_data.csv'
            print(f'Checking the value of file_name {file_name}')
            # if len(updated_table['Price_Action'].unique())>0:
            if len(updated_table['Report_to_merchant'].unique())>0:
                if not os.path.exists(file_name):
                    store_data_df = updated_table.copy()
                    store_data_df['timestamp'] = timestamp
                    store_data_df.to_csv(file_name, index=False)
                    # print(f'value of store_data_df while creating is {store_data_df.shape}')
                else:
                    existing_data = pd.read_csv(file_name)
                    # print(f'value of existing_data while creating is {existing_data.shape}')
                    # print(f'Checking the columns of existing data {existing_data.columns}')
                    print("")

                    store_data_df = updated_table.copy()
                    store_data_df['timestamp'] = timestamp
                    # print(f'value of store_data_df while concatenating is {store_data_df.shape}')
                    # print("")

                    updated_data = pd.concat([existing_data, store_data_df], ignore_index=True)
                    # print(f'value of updated_data while concatenating is {updated_data.shape}')
                    # print("")

                    updated_data.to_csv(file_name, index=False)
                    # print(f"Data appended to existing CSV file at {file_path + resp_bd + '_test_data.csv'}")
                    # print("")
                    
                return True, "Data Saved! Well done!", "success", True
            else:
                return False, None, None, None     


@app.callback(
    [Output("portfolio-table-submitted", "rowData"),
     Output("submitted_table_div", "style"),
     Output("action_tracker", "style")],
    [Input("save-btn", "n_clicks"),
     Input("date_filter","date"),
     Input("bd_filter", "value"),
     Input('trigger-update', 'data')],
    prevent_initial_call=True
)
def show_bd_updated_date(n, date, responsible_bd, trigger_update):
    file_name = file_path + responsible_bd + '_test_data.csv'
    # print(f'Show file name here {file_name}')
    print(f'Value of n is {n}')

    # Case 1: Triggered by date_filter or bd_filter changes, or dashboard load/refresh
    ctx = dash.callback_context
    if not ctx.triggered:
        triggered_input = None
    else:
        triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
        # print(f'triggered input is {triggered_input}')

    if triggered_input in ['date_filter', 'bd_filter'] or (n is None and trigger_update is None):
        # print("Triggered by date_filter, bd_filter, or dashboard load/refresh")
        if not os.path.exists(file_name):
            return [], {'display': 'none'}, {'display': 'none'}
        else:
            submitted_df = pd.read_csv(file_name)
            # print(f'Checking the value of submitted data {submitted_df}')
            show_df = submitted_df[(submitted_df['Report Date'] == date)]

            # Identify all columns except the Timestamp and price_action columns
            # columns_except_timestamp_and_price_action = show_df.columns.difference(['timestamp', 'Price_Action'])
            columns_except_timestamp_and_merchant_action = show_df.columns.difference(['timestamp', 'Report_to_merchant', 'Price_Action','BD_options'])


            # Corrected sort_values call
            df_sorted = show_df.sort_values(
                by=['timestamp'] + list(columns_except_timestamp_and_merchant_action),
                ascending=[False] + [True] * len(columns_except_timestamp_and_merchant_action)
            )

            # Drop duplicates based on all columns except Timestamp and price_action, keep the latest entry
            df_unique = df_sorted.drop_duplicates(subset=columns_except_timestamp_and_merchant_action, keep='first')

            return df_unique.to_dict('records'), {'display': 'block'}, {'display': 'block'}

    # Case 2: Triggered by save button click
    elif n is not None or trigger_update:
        print("Triggered by save button click")
        print(f'Value of n is {n}')
        submitted_df = pd.read_csv(file_name)
        # print(f'value of file name is {file_name}')
        # print(f'value of date is {date}')
        show_df = submitted_df[submitted_df['Report Date'] == date]

        # Identify all columns except the Timestamp and price_action columns
        # columns_except_timestamp_and_price_action = show_df.columns.difference(['timestamp', 'Price_Action'])
        columns_except_timestamp_and_merchant_action = show_df.columns.difference(['timestamp', 'Report_to_merchant', 'Price_Action','BD_options'])


        # Corrected sort_values call
        df_sorted = show_df.sort_values(
            by=['timestamp'] + list(columns_except_timestamp_and_merchant_action),
            ascending=[False] + [True] * len(columns_except_timestamp_and_merchant_action)
        )

        # Drop duplicates based on all columns except Timestamp and price_action, keep the latest entry
        df_unique = df_sorted.drop_duplicates(subset=columns_except_timestamp_and_merchant_action, keep='first')
        
        # print(f'Checking the value of submitted data {show_df}')
        return df_unique.to_dict('records'), {'display': 'block'}, {'display': 'block'}

    return [], {'display': 'none'}




if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)