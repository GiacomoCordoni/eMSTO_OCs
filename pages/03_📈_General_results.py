
'''
Created on 4 Feb
@author: Giacomo Cordoni
Main page for Dashboard information -> general information about work and data included in the dashboard
'''

import streamlit as st
	# basic
import os, numpy
import pandas as pd
from scipy import stats
from copy import copy
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff


def median_trend(X, Y, nbins=10):
    bins = numpy.linspace(numpy.nanquantile(X, 0.005),numpy.nanquantile(X, 0.995), nbins)
    delta = bins[1]-bins[0]
    idx  = numpy.digitize(X, bins, right=False)
    med = numpy.array([numpy.nanquantile(Y[idx==k], 0.5) for k in range(1, nbins)])
    q16 = numpy.array([numpy.nanquantile(Y[idx==k], 0.16) for k in range(1, nbins)])
    q84 = numpy.array([numpy.nanquantile(Y[idx==k], 0.84) for k in range(1, nbins)])
    N   = numpy.array([len(Y[idx==k]) for k in range(1, nbins)])
    return numpy.array(bins[1:] - delta/2), med, q16, q84, N


st.set_page_config(page_title='General Results',layout='wide', page_icon='📈')

st.title('General Results')

dfresults   = pd.read_csv('./data/TableResults_v2.csv', sep=',', index_col='name', comment='#')
dfpar_dias  = pd.read_csv('./data/ClustersPars.csv', sep=',', index_col='name')
dfall       = pd.read_csv('./data/AllData.csv', sep=',', index_col=None)
dftoff      = dfall.loc[dfall['in_toff'] & dfall['vbok']].copy()


dfresults['name'] = dfresults.index
dfresults['loga'] = numpy.log10(dfresults['age']*1e9) 
# Interface: Select clusters name
list_clusters = dfresults.loc[dfresults['flag_vbroad']].index
# start plotting part

###### first panel on the left
fig1_1 = px.density_heatmap(dftoff, x='dcn', y='vbroad', 
                          nbinsx=35, nbinsy=22, color_continuous_scale='greys')

xmed, ymed, q16, q84, N = median_trend(dftoff['dcn'], dftoff['vbroad'], nbins=8)
xmed = numpy.array(xmed)
ymed = numpy.array(ymed)
fig1_2 = px.scatter(x=xmed, y=ymed, 
        error_y=(q84-ymed), error_y_minus=(ymed-q16))
fig1_2.update_traces(marker=dict(size=12, color='#0096ff', opacity=0.8,
                    line=dict(width=0.8,color='#000000')),
                    error_y=dict(color='#000000', width=0.1)
                )
fig1_3 = px.line(x=xmed, y=ymed)
fig1_3.update_traces(line=dict(width=1.8,color='#0096ff'))
fig_dcvb = go.Figure(data = fig1_1.data + fig1_2.data + fig1_3.data).update_layout(
        coloraxis=fig1_1.layout.coloraxis
    )
fig_dcvb.update_layout(xaxis_title='ΔColor',
                  yaxis_title='v<sub>broad</sub>',
                  coloraxis_colorbar=dict(title='Counts'))

####### second panel on the left

fig2_1 = px.scatter(dfresults, x='age', y='vbmax',
            hover_data='name', 
            opacity=0.99
        )
fig2_1.update_traces(marker=dict(size=12, opacity=0.8,
            line=dict(width=0.8,color='#000000'))
        )
fig_corrage = go.Figure(data = fig2_1.data)

fig_corrage.update_layout(xaxis_title='Age',
                  yaxis_title='v<sub>broad</sub><sup>max</sup>',
                  xaxis_range=[0,1.5], yaxis_range=[150, 390])


fig2 = px.scatter(dfresults, x='loga', y='stdcol_fid', 
                    hover_data='name', 
                    opacity=0.99)
fig2.update_traces(marker=dict(size=12, opacity=0.8,
                    line=dict(width=0.8,color='#000000'))
                )
fig_dcage = go.Figure(data = fig2.data)

fig_dcage.update_layout(xaxis_title='Age',
                  yaxis_title='ΔColor',
                  )

container1 = st.container(border=True)
col1, col2, col3 = st.columns([1.5, 1, 1.0]) #col2, col3

with container1: 
    with col1:
        st.subheader('$\Delta\mathrm{Color}$ vs. $v_\mathrm{broad}$')
        st.plotly_chart(fig_dcvb, use_container_width=True)

    with col2:
        st.subheader('Correlation vs. Age')
        st.plotly_chart(fig_corrage, use_container_width=True)       
    
    with col3:
        st.subheader('$\Delta\mathrm{Color}$ vs. Age')
        st.plotly_chart(fig_dcage, use_container_width=True)


