import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path

def nefesh_btl(nefesh):
    """
    Parameters
    ----------
    nefesh : int
        The number of persons the household has.

    Returns
    -------
    Float
        The standardised number of persons in the household, 
        according to National Security Institue and the Central Bureau of Statistics definition.
    
    Required libraries
    ------------------
    None.

    """
    l = [1.25, 2, 2.65, 3.2, 3.75, 4.25, 4.75, 5.2]
    if nefesh <= len(l) - 1:
        return l[int(nefesh - 1)]
    else:
        return 5.6 + (nefesh - 9) * 0.4


def find_nearest(array, value):
    """

    Parameters
    ----------
    array : numpy array
        The array to be searched.
    value : flaot or int
        A number which get searched in the array.

    Returns
    -------
    int or float
        Returns the closest value in the array to the value searched, from bottom.
    
    Required libraries
    ------------------
    numpy

    """
    array = np.asarray(array)
    if value < array[0]:
        return array[0][0]
    elif value >= array[-1]:
        return array[-1][0]
    array = array[array > value]
    idx = (np.abs(array - value)).argmin()
    return array[idx]

@st.cache_data
def load_data(file, p, i=None):
    """
    A function to load the data.
    Mainly for streamlit.cache_data.

    Parameters
    ----------
    file : str
        The file name to of the file load
    p : Path object
        The path to the file.
    i : str, optional
        The column to read as an index of the dataframe. The default is None.

    Returns
    -------
    DataFrame
        The loaded dataframe.
    
    Required libraries
    ------------------
    pandas

    """
    return pd.read_csv(p / (file + ".csv"), index_col=i)

path = Path(".")
data = load_data('deciles_limits', path, i='p')
data_percent = load_data('percentiles_limits', path, i='p')
migzar_option_dict = {'non_haredim': 'יהודים לא-חרדים',
                      'haredim': 'יהודים חרדים',
                      'arabs': 'ערבים'}

st.markdown("""<style> 
                div.row-widget.stRadio > div {
                 direction:rtl; 
                 text-align:right !important;
                 } 
                </style>""", unsafe_allow_html=True)
                
st.markdown("<h1 style='text-align: center;'>?באיזה עשירון ואחוזון אתם</h1>", unsafe_allow_html=True)

st.markdown("<div style='text-align: center;'>:הכניסו את ההכנסות החודשיות נטו של משק הבית שלכם מכלל המקורות</div>", unsafe_allow_html=True)
st.markdown("""<style> 
                input {
                 direction:rtl; 
                 text-align:center !important;
                 } 
                </style>""", unsafe_allow_html=True)

col1, = st.columns(1)
with col1:
    income = st.number_input(":הכניסו את ההכנסות החודשיות נטו של משק הבית מכלל המקורות", 
                             min_value=1000, 
                             max_value=1000000000,
                             step=100,
                             label_visibility='collapsed')
    
    st.markdown("<div style='text-align: center;'>:הכניסו את מספר הנפשות במשק הבית (כולל ילדים)</div>", unsafe_allow_html=True)
    persons = st.number_input("הכנס את מספר הנפשות במשק הבית (כולל ילדים)", 
                              step=1, 
                              min_value=1, 
                              max_value=20,
                              label_visibility='collapsed')

    st.markdown("<div style='text-align: center;'>?מאיזה מגזר אתם</div>", unsafe_allow_html=True)
    migzar = st.radio(label='מגזר',
                      options=migzar_option_dict.keys(),
                      key='decile_radio',
                      label_visibility='collapsed',
                      format_func=lambda x: '{}'.format(migzar_option_dict.get(x)))
    
# Caculating income per standard person by dividing the income recived from the user by the number of persons (standardized).
income_per_s_person = income/nefesh_btl(persons)
decile = data.index[data['all'] == find_nearest(data['all'], income_per_s_person)][0]
percentile = data_percent.index[data_percent['all'] == find_nearest(data_percent['all'], income_per_s_person)][0]

decile_m = data.index[data[migzar] == find_nearest(data[migzar], income_per_s_person)][0]
percentile_m = data_percent.index[data_percent[migzar] == find_nearest(data_percent[migzar], income_per_s_person)][0]


st.markdown("<h2 style='text-align: center;'>:משק הבית שלך בעשירון הכללי</h2>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>{}</h1>".format(decile), unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>:ובאחוזון הכללי</h2>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>{}</h1>".format(percentile), unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>:משק הבית שלך בעשירון של המגזר שלך</h2>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>{}</h1>".format(decile_m), unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>:ובאחוזון של המגזר שלך</h2>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>{}</h1>".format(percentile_m), unsafe_allow_html=True)

st.markdown("<div style='text-align: center;'>לפי סקר הוצאות משק הבית 2021 של הלשכה המרכזית לסטטיסטיקה</div>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center;'>עשירון תחתון = 1, עשירון עליון = 10</div>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center;'>אחוזון תחתון = 1, אחוזון עליון = 100</div>", unsafe_allow_html=True)
st.markdown("""<a style='display: block; text-align: center;' href="https://twitter.com/tom_sadeh">@tom_sadeh</a>""", unsafe_allow_html=True)

