import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

st.title("Umrechnung Stundenlohn in Jahreslohn")
st.header("Festlegung gesetzliche Abgaben")
col1, col2, col3 = st.columns(3)
with col1:
    AHV = st.number_input('AHV [%]', min_value=0.0, value=10.6, max_value=20.0)
    ALV = st.number_input('ALV [%]', min_value=0.0, value=1.1, max_value=2.0)
with col2:
    Unfall = st.number_input('Unfall/NBU [%]', min_value=0.0, value=1.5, max_value=20.0)
    Krankentaggeld = st.number_input('Krankentaggeld [%]', min_value=0.0, value=5.0, max_value=10.0)
with col3:
    BVG = st.number_input('BVG [%]', min_value=0.0, value=15.0, max_value=20.0)
    
Brutto_stundenlohn = st.slider('Brutto Stundenlohn [CHF]', min_value=0, value=80, max_value=250, step=5)
Arbeitstage = st.slider('Arbeitstage [Tage]', min_value=220, value=250, max_value=300, step=1)
Stunden_pro_Tag = st.slider('Stunden pro Tag [Stunden]', min_value=7.0, value=8.5, max_value=10.0, step=0.1)
Administration = st.slider('Administration [%]', min_value=0.0, value=2.0, max_value=5.0, step=0.1)
Total_Abzuege = AHV + ALV + Unfall + Krankentaggeld + BVG + Administration
Nettostundenlohn = (Brutto_stundenlohn * ( 100 - Total_Abzuege) ) / 100


st.header("Berechnung Abzüge")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Abzüge [%]", value=f'{Total_Abzuege:,.1f}%')
with col2:
    st.metric(label="Brutto Stundenlohn [CHF]", value=f'{Brutto_stundenlohn:,.2f}')
with col3:  
    st.metric( label="Netto Stundenlohn [CHF]", value=f'{Nettostundenlohn:,.2f}', delta=f'{Nettostundenlohn-Brutto_stundenlohn:,.2f}')



st.header("Hochrechnung Monats- und Jahreslohn")

Umsatz = Arbeitstage * Stunden_pro_Tag * Brutto_stundenlohn
Geschätzter_Brutto_Jahreslohn = (Umsatz * ( 100 - Total_Abzuege) ) / 100

col21, col22, col23 = st.columns(3)
with col21:
    st.metric(label="Umsatz [CHF]", value=f'{Umsatz:,.2f}')
with col22:  
    st.metric( label="Berechneter Monatslohn [CHF]", value=f'{Geschätzter_Brutto_Jahreslohn/13:,.2f}')
with col23:  
    st.metric( label="Berechneter Jahreslohn [CHF]", value=f'{Geschätzter_Brutto_Jahreslohn:,.2f}')


st.header("Zusammensetzung von CHF 100 Lohn")
source = pd.DataFrame({
    "category": ["AHV", "ALV", "Unfall", "Krankentaggeld","BVG", "Admin", "Lohn"],
    "value": [AHV, ALV, Unfall, Krankentaggeld, BVG, Administration, (100-Total_Abzuege)]
})

chart = alt.Chart(data=source, title="Zusammensetzung").mark_arc(innerRadius=80).encode(
    theta="value",
    color="category:N",
)


base = alt.Chart(source).encode(
    alt.Theta("value:Q").stack(True),
    alt.Color("category:N").legend(None)
)

pie = base.mark_arc(outerRadius=120)
text = base.mark_text(radius=150, size=16).encode(text="category:N")
st.altair_chart(pie + text)

