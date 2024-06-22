"""
Created on 4 Feb
@author: Giacomo Cordoni
Main page for Dashboard information -> general information about work and data included in the dashboard
"""
import streamlit as st

st.set_page_config(page_title="Home",layout="centered", page_icon="💡")

st.sidebar.image("img/logoanu.png", use_column_width=True)

st.title("Survey of extended Main Sequence Turn-offs in Galactic Open Clusters: Stellar rotations from Gaia RVS spectra")

st.subheader("Giacomo Cordoni et al. ")
container1 = st.container()
col1, col2, col3, col4 = st.columns(4) 

with container1: 
    with col1:
        st.link_button(":blue[Go to article] 📄 ", "https://giacomocordoni.github.io/publication/", type="secondary", use_container_width=True)
    with col2:
        st.link_button(":blue[Go to website] 🌏", "https://giacomocordoni.github.io/", type="secondary", use_container_width=True)

# st.write("Australian National University, Research School of Astronomy and Astrophysics")

st.write("""
The origin of extended main-sequence turn-offs (eMSTO) in star clusters younger than 2 Gyr still challenges our current understanding of stellar evolution. Exploiting data from Gaia Data Release 3 (DR3), we investigate eMSTOs in a large sample of 32 Galactic open clusters younger than 2.4 Gyr. We first validate Gaia rotational velocities from Radial Velocity Spectrometer (RVS) spectra by comparing them with literature values and assessing their correlation with magnetic activity measurements from LAMOST spectra. 
    """)

st.image("./img/img_rhk.png", width=600, caption="Correlation between Gaia DR3 projected rotational velocities and magnetic actitivy index from LAMOST DR9")

st.write("""         
We detect a general positive correlation between turn-off color and projected stellar rotation, with slow-rotating stars predominantly found on the bluer side of the turn-off. Comparing our observations with theoretical models, we find that the eMSTO morphology is well-reproduced by a single population formed with a high rotation rate, and observed with rotation axis inclination ranging between 0◦ (pole-on) and 90◦ (edge-on). 
""")

st.image("./img/img2.png", width=600, caption="Comparison between observed maximum Gaia projected rotational velocities and predicted maximum equatorial rotation velocity from PARSEC models")

st.write("""         
This contrasts with observations of Magellanic Clouds clusters, where a population of non-rotating stars appears to be ubiquitous in clusters younger than 700 Myr. However, we note that our interpretation, while successfully explaining the overall eMSTO morphology, cannot fully explain the observed projected rotational velocities. Additionally, two young clusters, NGC 3532 and NGC 2287, exhibit moderate evidence of a split main sequence in color and rotation, suggesting a possible small spread in the initial rotation rate. Finally, we advise caution in determining the ages of young clusters from non-rotating isochrones, as neglecting the effects of stellar rotation can impact the isochrone dating by up to factors of 5-20%.
    """)

        
st.image("./img/img1_1.png", caption="Results for the 17 analyzed clusters")

st.write("""
Please note that the App is still a work in progress. 
         For any questions, information or collaborations, feel free to contact us by mail at giacomo.cordoni@anu.edu.au  
    """)
