import pandas as pd
import numpy as np
import streamlit as st
import matplotlib as mpl
import matplotlib.pyplot as plt
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
    array = np.asarray(array)
    if value < array[0]:
        return array[0][0]
    elif value > array[-1]:
        return array[-1][0]
    array = array[array > value]
    idx = (np.abs(array - value)).argmin()
    return array[idx]

@st.cache_data
def load_data(file, p, i=None):
    return pd.read_csv(p / (file + ".csv"), index_col=i)

path = Path(".")
data = load_data('limits', path, i='decile')

st.markdown("<h1 style='text-align: center;'>מחשבון עשירונים</h1>", unsafe_allow_html=True)

st.markdown("<div style='text-align: center;'>:הכניסו את ההכנסות נטו של משק הבית שלכם מכלל המקורות</div>", unsafe_allow_html=True)
income = st.number_input(":הכניסו את ההכנסות נטו של משק הבית מכלל המקורות", 
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

income_per_s_person = income/nefesh_btl(persons)
decile = data.index[data['limit'] == find_nearest(data, income_per_s_person)][0]

st.markdown("<h2 style='text-align: center;'>:משק הבית שלך בעשירון</h2>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>{}</h1>".format(decile), unsafe_allow_html=True)
st.markdown("<div style='text-align: center;'>לפי סקר הוצאות משק הבית 2021 של הלשכה המרכזית לסטטיסטיקה</div>", unsafe_allow_html=True)
st.markdown("""<a style='display: block; text-align: center;' href="https://twitter.com/tom_sadeh">@tom_sadeh</a>""", unsafe_allow_html=True)
