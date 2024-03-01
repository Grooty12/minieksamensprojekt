import numpy as np
import csv
import streamlit as st
array_plot = []
data_plot = []

uploadedFile = st.file_uploader("Upload datafil", type='csv')
for n, row in enumerate(uploadedFile):
    if n != 0:
        str_list = row.decode().strip().split(',')
        arr = np.array(str_list, dtype=float)
        data_plot.append([a for a in arr])


def distance(a, b):
    length_data = [(c - b[d]) ** 2 for d, c in enumerate(a) if d != len(a) - 1]
    return np.sqrt(np.sum(length_data))


def one_nn(p, closest=None):
    if closest is None:
        closest = [2093812093810293, "ok"]
    for a in data_plot:
        length = distance(a, p)
        if length < closest[0]:
            closest = [length, a[-1]]
    return closest[1]


def check_common_number(arr):
    longest = [len(arr[0]), len(arr[1])]
    return 1 if longest[0]/longest[1] > 306/694 else 0


def sort_similar_numbers(arr, numbers=None, index=None):
    if index is None:
        index = []
    if numbers is None:
        numbers = []
    for j, i in enumerate(arr):
        if j == 0:
            numbers.append([i[1]])
            index.append(i[1])
        else:
            in_index = [False, 0]
            for h, g in enumerate(index):
                if i[1] != g:
                    in_index = [False, h]
                else:
                    in_index = [True, h]
                    break
            if in_index[0] is True:
                numbers[in_index[1]].append(i[1])
            else:
                numbers.append([i[1]])
                index.append(i[1])
    return check_common_number(numbers)


def k_nn(knn_array, p, m, lengths=None):
    if lengths is None:
        lengths = []
    if m % 2 == 0:
        m = m + 1
    if len(knn_array) == 1:
        return one_nn(p)
    else:
        for a in knn_array:
            lengths.append([distance(a, p), a[-1]])
        lengths.sort()
        lengths = lengths[:m]
        number = sort_similar_numbers(lengths)
        p.append(number)
        return p

st.title("Har du diabetis?? Indtast værdier")
children = st.slider("Mængde af børn", 0, 10, 1)
glucose = st.slider("Glukoseniveau", 0, 250, 100)
blodtryk = st.slider("Blodtryk", 0, 200, 100)
hudtykkelse = st.slider("Hudtykkelse", 0, 50, 25)
insulin = st.slider("Insulingniveau", 0, 200, 100)
BMI = st.slider("BMI", 15, 35, 20)
diabetesmulighed = st.slider("Diabetismulighed", 0.00, 1.00, 0.50, 0.01)
alder = st.slider("Alder", 0, 150, 40)

point = k_nn(data_plot, [children, glucose, blodtryk, hudtykkelse, insulin, BMI, diabetesmulighed, alder], 50)

tekst = "Vi gætter du har diabetis" if point[-1] == 1 else "Vi gætter du ikke har diabetis"
st.markdown(tekst)
