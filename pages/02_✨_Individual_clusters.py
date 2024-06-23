
'''
Created on 4 Feb
@author: Giacomo Cordoni
Main page for Dashboard information -> general information about work and data included in the dashboard
'''

import streamlit as st
	# basic
import os, numpy 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff


st.set_page_config(page_title='Individual clusters',layout='wide', page_icon='✨')

st.title('Individual clusters results')

def get_cluster_data(df, cl):
    dfcl = df.loc[df['clname'] == cl].copy().reset_index()
    return(dfcl)


dfto        = pd.read_csv('./data/TableResults_v2.csv', sep=',', index_col='name', comment='#')
dfpar_dias  = pd.read_csv('./data/ClustersPars.csv', sep=',', index_col='name')
dfall       = pd.read_csv('./data/AllData.csv', sep=',', index_col=None)

# Interface: Select clusters name
list_clusters = dfto.loc[dfto['flag_vbroad'], :].index
cluster_name = st.sidebar.selectbox(
    'Select open cluster with vbroad analysis',
    list(list_clusters),
    index=14
    )

df  = get_cluster_data(df=dfall, cl=cluster_name)

ra      = dfpar_dias.loc[cluster_name, 'ra']
dec     = dfpar_dias.loc[cluster_name, 'dec']
age     = 10**(dfpar_dias.loc[cluster_name, 'loga']-9)
dist    = dfpar_dias.loc[cluster_name, 'dist']
av      = dfpar_dias.loc[cluster_name, 'av']

st.sidebar.subheader('Cluster properties (Dias et al. 2021)')
st.sidebar.subheader('$RA = %.2f^\circ$' %(ra))
st.sidebar.subheader('$DEC = %.2f^\circ$' %(dec))
st.sidebar.subheader('$Age = %.2f\, \mathrm{Gyr}$' %(age))
st.sidebar.subheader('$Dist = %g\,\mathrm{kpc}$' %(dist))
st.sidebar.subheader('$Av = %.3f\,\mathrm{mag}$' %(av,))


fig1_1 = px.scatter(df, x='col', y='mag', hover_data='source_id') #, width=400, height=800
fig1_1.update_traces(marker=dict(size=4, color='#000000', opacity=0.1,
                        line=dict(width=0.1,color='#ffffff'))
                    )

fig1_2 = px.scatter(df.loc[df['vbok']], x='col', y='mag', hover_data='source_id', # width=400, height=800,
        color= 'vbroad', color_continuous_scale = 'rdbu_r')
fig1_2.update_traces(marker=dict(size=7,
                        line=dict(width=0.0,color='#000000'))
                    )

fig_cmd = go.Figure(data = fig1_1.data + fig1_2.data).update_layout(coloraxis=fig1_2.layout.coloraxis)
fig_cmd.update_layout(xaxis_title='G<sub>BP</sub> - G<sub>BP</sub>',
                  yaxis_title='G<sub>BP</sub>',
                  coloraxis_colorbar=dict(title='v<sub>broad</sub>[km/s]'),
                  yaxis_range=[17,5])

toff_group_labels = [''] #, 'Group 2', 'Group 3'
colors = ['#000000'] #, '#37AA9C', '#94F3E4'
# Create distplot with curve_type set to 'normal'
fig_todist = px.histogram(df.loc[df['in_toff']], x='dcn', histnorm='probability', nbins=10)
fig_todist.update_layout(
    xaxis_title='ΔColor',
    yaxis_title='Density'
) 

vbtoff_hist_data = [df.loc[df['in_toff'] & df['vbok'], 'vbroad']]
vbtoff_group_labels = ['Turn-off vbroad'] #, 'Group 2', 'Group 3'
colors = ['#000000'] #, '#37AA9C', '#94F3E4'
# Create distplot with curve_type set to 'normal'
fig_vbtodist = px.histogram(df.loc[df['in_toff'] & df['vbok']], x='vbroad', histnorm='probability', nbins=10)
fig_vbtodist.update_layout(
    xaxis_title='v<sub>broad</sub>[km/s]',
    yaxis_title='Density'
)



# fig_todist = ff.create_distplot(toff_hist_data, toff_group_labels, show_hist=False, colors=colors)
# fig_todist.update_layout(
#     xaxis_title='ΔColor',
#     yaxis_title='KDE'
# )
# vbtoff_hist_data = [df.loc[df['in_toff'] & df['vbok'], 'vbroad']]
# vbtoff_group_labels = ['Turn-off vbroad'] #, 'Group 2', 'Group 3'
# colors = ['#000000'] #, '#37AA9C', '#94F3E4'
# # Create distplot with curve_type set to 'normal'
# fig_vbtodist = ff.create_distplot(vbtoff_hist_data, vbtoff_group_labels, show_hist=False, colors=colors)
# fig_vbtodist.update_layout(
#     xaxis_title='v<sub>broad</sub>',
#     yaxis_title='KDE'
# )


fig4 = px.scatter(df.loc[df['in_toff'] & df['vbok']], x='dcn', y='vbroad', hover_data='source_id',
        opacity=0.99, color= 'w_vbroad', color_continuous_scale = 'greens',
        error_y='vbroad_error')

fig4.update_traces(marker=dict(size=12,
                    line=dict(width=0.1,color='#000000')),
                    error_y=dict(color='#000000', width=0.1)
                )

fig_vbdc = go.Figure(data = fig4.data).update_layout(coloraxis=fig4.layout.coloraxis)


fig_vbdc.update_layout(xaxis_title='ΔColor',
                  yaxis_title='v<sub>broad</sub>',
                  coloraxis_colorbar=dict(title='v<sub>broad</sub>/εv<sub>broad</sub>'),
                  ) #yaxis_range=[20,5]


fig5 = px.scatter(df.loc[df['log_rhk'].notna()], x='dcn', y='log_rhk', hover_data='source_id',
        opacity=0.99, color= 'vbroad', color_continuous_scale = 'rdbu_r', 
        error_y='log_rhk_err')

fig5.update_traces(marker=dict(size=12,
                        line=dict(width=0.1,color='#000000')), 
                        error_y=dict(color='#000000', width=0.1)
                    )
fig_dcrhk = go.Figure(data = fig5.data).update_layout(coloraxis=fig5.layout.coloraxis)
fig_dcrhk.update_layout(yaxis_title='v<sub>broad</sub> [km/s]',
                  xaxis_title='log R<sub>HK</sub>',
                  coloraxis_colorbar=dict(title='G<sub>RP</sub>'),
                  ) #yaxis_range=[20,5]


container1 = st.container()
col1, col2, col3 = st.columns(3) 

with container1: 
    with col1:
        st.subheader('Colour Magnitude Diagram')
        st.plotly_chart(fig_cmd, use_container_width=True)
    with col2:
        st.subheader('Turn-off $\Delta\mathrm{Color}$ dist.')
        st.plotly_chart(fig_todist, use_container_width=True)     
    with col3:
        st.subheader('Turn-off $v_\mathrm{broad}$ dist. ')
        st.plotly_chart(fig_vbtodist, use_container_width=True)


container2 = st.container()
col4, col5  = st.columns(2)
with container2:   
    with col4:
        st.header('$\Delta\mathrm{Color}$ - $v_\mathrm{broad}$  relation')
        st.info('$R_\mathcal{S} = %.3f \pm %.3f$' %(dfto.loc[cluster_name, 'corr'], dfto.loc[cluster_name,'ecorr']))
        st.plotly_chart(fig_vbdc, use_container_width=True)
        


