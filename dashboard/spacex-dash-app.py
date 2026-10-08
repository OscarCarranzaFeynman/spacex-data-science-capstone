from pathlib import Path
import pandas as pd
import dash
from dash import html, dcc, Input, Output
import plotly.express as px

spacex_df = pd.read_csv(Path(__file__).resolve().parent / 'spacex_launch_dash.csv')
min_payload = float(spacex_df['Payload Mass (kg)'].min())
max_payload = float(spacex_df['Payload Mass (kg)'].max())
app = dash.Dash(__name__)
app.title = 'SpaceX Launch Records Dashboard'
app.layout = html.Div(style={'maxWidth':'1200px','margin':'auto','padding':'20px'}, children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign':'center','color':'#503D36','fontSize':40}),
    html.Label('Launch Site:'),
    dcc.Dropdown(id='site-dropdown', options=[{'label':'All Sites','value':'ALL'}]+[{'label':s,'value':s} for s in sorted(spacex_df['Launch Site'].unique())], value='ALL', placeholder='Select a Launch Site here', searchable=True, clearable=False),
    html.Br(), dcc.Graph(id='success-pie-chart'), html.Br(),
    html.P('Payload range (kg):'),
    dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
        marks={v:f'{v:,}' for v in range(0,10001,1000)}, value=[max(0,min_payload),min(10000,max_payload)],
        allowCross=False, tooltip={'placement':'bottom','always_visible':True}),
    html.Br(), dcc.Graph(id='success-payload-scatter-chart')
])

@app.callback(Output('success-pie-chart','figure'),Input('site-dropdown','value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        counts = spacex_df.groupby('Launch Site',as_index=False)['class'].sum()
        fig = px.pie(counts,values='class',names='Launch Site',title='Successful Launches by Site')
    else:
        filtered = spacex_df[spacex_df['Launch Site']==entered_site]
        counts = filtered['class'].value_counts().reindex([0,1],fill_value=0)
        outcomes = pd.DataFrame({'Outcome':['Failure','Success'],'Count':counts.to_numpy()})
        fig = px.pie(outcomes,values='Count',names='Outcome',title=f'Launch Outcomes — {entered_site}',color='Outcome',color_discrete_map={'Failure':'#d62728','Success':'#2ca02c'})
    fig.update_traces(textinfo='label+percent',hoverinfo='label+value+percent')
    fig.update_layout(template='plotly_white')
    return fig

@app.callback(Output('success-payload-scatter-chart','figure'),[Input('site-dropdown','value'),Input('payload-slider','value')])
def get_scatter_chart(entered_site,payload_range):
    low,high=payload_range
    filtered=spacex_df[spacex_df['Payload Mass (kg)'].between(low,high)].copy()
    if entered_site!='ALL':
        filtered=filtered[filtered['Launch Site']==entered_site].copy()
    filtered['Booster Version Category']=filtered['Booster Version Category'].astype(str)
    label='All Sites' if entered_site=='ALL' else entered_site
    fig=px.scatter(filtered,x='Payload Mass (kg)',y='class',color='Booster Version Category',hover_data=['Launch Site'],
        title=f'Payload Mass vs. Launch Outcome — {label} ({low:,.0f}–{high:,.0f} kg)',
        labels={'Payload Mass (kg)':'Payload Mass (kg)','class':'Launch Outcome','Booster Version Category':'Booster Version'})
    fig.update_traces(marker={'size':10,'opacity':0.75})
    fig.update_yaxes(tickvals=[0,1],ticktext=['Failure','Success'],range=[-0.15,1.15])
    fig.update_layout(template='plotly_white')
    if filtered.empty:
        fig.add_annotation(text='No launches match the selected site and payload range.',xref='paper',yref='paper',x=0.5,y=0.5,showarrow=False)
    return fig

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8050,debug=False)
