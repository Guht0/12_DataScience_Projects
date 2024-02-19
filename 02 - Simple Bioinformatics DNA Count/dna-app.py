# import libraries
import pandas as pd
import streamlit as st
import altair as alt #  for interactive visualizations
from PIL import Image

# Page title
#image = Image.open('dna-logo.jpg')
#st.image(image, use_column_width=True) # Displaying the image

st.write("""
    # DNA Nucleotide Count Web App
         
    This app counts the nucleotide composition of query DNA!
         
    ***
""") # *** = Horizontal line

# Imput Text Box
st.header('Enter your DNA sequence:')

sequence_input = ">DNA Query\nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"

sequence = st.text_area("Sequence input", sequence_input, height=150)
#sequence
sequence = sequence.splitlines() # Creating a list with each individual line from text box
#sequence
sequence = sequence[1:] # Skips the sequence name (first line)
#sequence
sequence = ''.join(sequence) # Joins all lines into one string | Concatenates list to string
#sequence

st.write("""
    ***
""")

# Print the input DNA sequence
st.header('INPUT (DNA Query)')
sequence

# DNA nucleotide count
st.header('OUTPUT (DNA Nucleotide Count)')

### 1. Print dictionary
st.subheader('1. Print dictionary')
def DNA_nucleotide_count(seq):
    d = dict([
              ('A', seq.count('A')), # Count how many times A repeat in the DNA sequence
              ('T', seq.count('T')),
              ('G', seq.count('G')),
              ('C', seq.count('C')),
            ])
    return d

X = DNA_nucleotide_count(sequence)

X

### 2. Print text
st.subheader('2. Print text')
st.write('There are ' + str(X['A']) + ' adenine (A)')
st.write('There are ' + str(X['T']) + ' thymine (T)')
st.write('There are ' + str(X['G']) + ' guanine (G)')
st.write('There are ' + str(X['C']) + ' cytosine (C)')

### 3. Display DataFrame
st.subheader('3. Display DataFrame')
df = pd.DataFrame.from_dict(X, orient='index') # Creating a dataframa based on the dictionary X
#df
df = df.rename({0: 'Count'}, axis='columns') # Renaming tem first column
#df
df.reset_index(inplace=True) # Resetting index to default. By doing that the nucleotides that were previously indexed will be displayed as the first columns
#df
df = df.rename(columns = {'index':'Nucleotide'}) #  Rename the fisrt column called 'index' to 'Nucleotide'
st.write(df) # can awlso use 'st.dataframe()' or simply 'df' instead of st.write() in order to exibe the table. Using the st.write or st.dataframe makes the df a streamlit object

### 4. Display Bar Chart using Altair
st.subheader('4. Display Bar chart')
p = alt.Chart(df).mark_bar().encode(
    x = 'Nucleotide',
    y = 'Count'
)
#p
p = p.properties(
    width = alt.Step(80)
)
st.write(p)