#----- Last update: 06/01/2020 -----

# Program written by Antoine Wegrowski, PhD in ME at University of Washington

# This program is designed to take as an input the S-parameters generated by a
# simulation through the software CST Microwave, and extract the permittivity,
# permeability, impedance, refractive index, transmission and reflection
# parameters of the simulated material, outputting a set of plots of these
# parameters over a specified range of frequency.
# The algorithm is based on the following paper:
# Hsieh, Feng-Ju, and Wei-Chih Wang. “Full extraction methods to retrieve
# effective refractive index and parameters of a bianisotropic metamaterial
# based on material dispersion models.” Journal of Applied Physics 112.6
# (2012): 064907.
# At times, the following paper has also been used:
# Chen, Xudong, et al. “Robust method to retrieve the constitutive effective
# parameters of metamaterials.” Physical Review E 70.1 (2004): 016608.

# NOTA BENE: this program only takes one data set.

# Various packages necessary for execution
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Creating the path variable
# and checking that no destination folder already exist
# in which case the program will abort to avoid overwriting precious data
PATH = os.path.abspath(os.getcwd())
if os.path.exists(PATH+"\\Saved effective parameters"):
    print("A directory named \"Saved effective parameters\" already exists."
        + " Please rename/delete it before running this program.")
    exit()
        

# Defining all valuable variables 
frequnit = 1000000000000
lengthunit = 0.000001

# To change depending on the dimensions of the sample
print("REMINDER: have you updated the slab thickness information for this \
specific sample?")
SlabThick = 9.9*lengthunit #Slab thickness
L10 = 10.1 * lengthunit #Air thickness before sample
L20 = 10.1 * lengthunit #Air thickness after sample
EffBoundThick = SlabThick + L10 + L20 #Effective boundary thickness

# Section II part B of Hsieh
# Assuming L1s = L2s = 0, to change accordingly
L1a = L10
L2a = L20
# Defining the wavenumber
def kzero(x):
    return 2*np.pi*x/299792458

# Importing the data set
S11ad1 = pd.read_table(PATH+'\S11a.txt', skiprows=2,
                       names=['Frequency','Value'], delim_whitespace=True)
S11pd1 = pd.read_table(PATH+'\S11p.txt', skiprows=2,
                       names=['Frequency','Value'], delim_whitespace=True)
S21ad1 = pd.read_table(PATH+'\S21a.txt', skiprows=2,
                       names=['Frequency','Value'], delim_whitespace=True)
S21pd1 = pd.read_table(PATH+'\S21p.txt', skiprows=2,
                       names=['Frequency','Value'], delim_whitespace=True)

# Correcting the frequency order of magnitude in the data files
S11ad1['Frequency'] = S11ad1['Frequency'].map(lambda x: x*frequnit)
S11pd1['Frequency'] = S11ad1['Frequency']
S21ad1['Frequency'] = S11ad1['Frequency']
S21pd1['Frequency'] = S11ad1['Frequency']

# Function reconstructing the complex data from the pair of files
# Note how this returns a dictionary with both frequency and value,
# to be called in need
def complexS(amplitude,phase):
    return {
        "Value":amplitude.Value*np.exp(-1j*phase.Value*np.pi/180),
        "Frequency":amplitude.Frequency}

# Function computing the complex impedance
# Taking in complex S dictionary, returning complex Z
def complexImpedance(S11,S21):
    intermediaryValue = np.sqrt(
        (np.power(1+S11['Value'],2)-np.power(S21['Value'],2))
        /(np.power(1-S11['Value'],2)-np.power(S21['Value'],2)))
    return intermediaryValue*np.sign(intermediaryValue)

# Function computing the exp(jknd)
# Taking in complex S dictionary, returning complex expression of exp(jknd)
def expjknd(S11,S21):
    return S21['Value']/(1-S11['Value']
        *(complexImpedance(S11,S21)-1)/(complexImpedance(S11,S21)+1))

# Function computing the imaginary part of the refractive index
# Taking in complex S dictionary, returning a real value corresponding to the
# imaginary part of the refractive index
def imaginaryN(S11,S21):
    return -np.real(np.log(expjknd(S11,S21))) \
     /(kzero(S11['Frequency'])*EffBoundThick)

# Function computing the real part of the refractive index
# Taking in complex S dictionary, returning a real value corresponding to the
# real part of the refractive index
def realN(S11,S21):
    return np.imag(np.log(expjknd(S11,S21))) \
     /(kzero(S11['Frequency'])*EffBoundThick)
# The below line was used in the final form of the Mathematica program,
# but for now we'll stick with the above
#    return (
#        -S21['Value']*np.pi/180-np.angle(
#            (1-S11['Value']*(complexImpedance(S11,S21)-1)
#            /(complexImpedance(S11,S21)+1))))
#        /(kzero(S11['Frequency'])*EffBoundThick)

# Creating all the effective parameters dataframes
realNdf = pd.DataFrame(columns=['Frequency','Value'])
imaginaryNdf = pd.DataFrame(columns=['Frequency','Value'])
NormEffImpedance = pd.DataFrame(columns=['Frequency','Value'])
mu = pd.DataFrame(columns=['Frequency','Value'])
epsilon = pd.DataFrame(columns=['Frequency','Value'])
fom = pd.DataFrame(columns=['Frequency','Value'])

for x in range(len(S11ad1)):
    realNdf.loc[x] = [
        S11ad1.at[x,'Frequency'],
        realN(
            complexS(S11ad1.loc[x],S11pd1.loc[x]),
            complexS(S21ad1.loc[x],S21pd1.loc[x]))]
    imaginaryNdf.loc[x] = [
        S11ad1.at[x,'Frequency'],
        imaginaryN(
            complexS(S11ad1.loc[x],S11pd1.loc[x]),
            complexS(S21ad1.loc[x],S21pd1.loc[x]))]
    NormEffImpedance.loc[x] = [
        S11ad1.at[x,'Frequency'],
        complexImpedance(
            complexS(S11ad1.loc[x],S11pd1.loc[x]),
            complexS(S21ad1.loc[x],S21pd1.loc[x]))]
    mu.loc[x] = [
        S11ad1.at[x,'Frequency'],
        NormEffImpedance.at[x,'Value']
            *(realNdf.at[x,'Value']+1j*imaginaryNdf.at[x,'Value'])]
    epsilon.loc[x] = [
        S11ad1.at[x,'Frequency'],
        (realNdf.at[x,'Value']+1j*imaginaryNdf.at[x,'Value'])
            /NormEffImpedance.at[x,'Value']]
    fom.loc[x] = [
        S11ad1.at[x,'Frequency'],
        -realNdf.at[x,'Value']/imaginaryNdf.at[x,'Value']]


#Plotting and saving the effective parameters spectra in a folder

os.mkdir(PATH+"\\Saved effective parameters")
   
plt.figure()
plt.plot(
    realNdf.Frequency.map(lambda x: np.real(x)),
    realNdf.Value.map(lambda x: np.real(x)),color='b')
plt.plot(
    imaginaryNdf.Frequency.map(lambda x: np.real(x)),
    imaginaryNdf.Value.map(lambda x: np.real(x)),color='r')
plt.xlabel('Frequency')
plt.ylabel('n')
plt.title('Refractive index VS frequency')
plt.legend(
    ['Real','Imaginary'],
    loc='center left',bbox_to_anchor=(1, 0.5))
plt.savefig(PATH+"\\Saved effective parameters\\Refractive index.png")

plt.figure()
plt.plot(
    NormEffImpedance.Frequency.map(lambda x: np.real(x)),
    NormEffImpedance.Value.map(lambda x: np.real(x)),color='b')
plt.plot(
    NormEffImpedance.Frequency.map(lambda x: np.real(x)),
    NormEffImpedance.Value.map(lambda x: np.imag(x)),color='r')
plt.xlabel('Frequency')
plt.ylabel('Z')
plt.title('Impedance VS frequency')
plt.legend(
    ['Real','Imaginary'],
    loc='center left',bbox_to_anchor=(1, 0.5))
plt.savefig(PATH+"\\Saved effective parameters\\Impedance.png")

plt.figure()
plt.plot(
    epsilon.Frequency.map(lambda x: np.real(x)),
    epsilon.Value.map(lambda x: np.real(x)),color='b')
plt.plot(
    epsilon.Frequency.map(lambda x: np.real(x)),
    epsilon.Value.map(lambda x: np.imag(x)),color='r')
plt.xlabel('Frequency')
plt.ylabel('epsilon')
plt.title('Permittivity VS frequency')
plt.legend(
    ['Real','Imaginary'],
    loc='center left',bbox_to_anchor=(1, 0.5))
plt.savefig(PATH+"\\Saved effective parameters\\Permittivity.png")

plt.figure()
plt.plot(
    mu.Frequency.map(lambda x: np.real(x)),
    mu.Value.map(lambda x: np.real(x)),color='b')
plt.plot(
    mu.Frequency.map(lambda x: np.real(x)),
    mu.Value.map(lambda x: np.imag(x)),color='r')
plt.xlabel('Frequency')
plt.ylabel('mu')
plt.title('Permeability VS frequency')
plt.legend(
    ['Real','Imaginary'],
    loc='center left',bbox_to_anchor=(1, 0.5))
plt.savefig(PATH+"\\Saved effective parameters\\Permeability.png") 

plt.figure()
plt.plot(
    fom.Frequency.map(lambda x: np.real(x)),
    fom.Value.map(lambda x: np.real(x)),color='black')
plt.xlabel('Frequency')
plt.ylabel('-Re(n)/Im(n)')
plt.title('Figure of merit')
plt.savefig(PATH+"\\Saved effective parameters\\Figure of merit.png") 

plt.figure()
plt.plot(S11ad1.Frequency,S11ad1.Value,color='black')
plt.xlabel('Frequency')
plt.ylabel('|S11|')
plt.title('Reflection VS frequency')
plt.savefig(PATH+"\\Saved effective parameters\\Reflection.png")

plt.figure()
plt.plot(S21ad1.Frequency,S21ad1.Value,color='black')
plt.xlabel('Frequency')
plt.ylabel('|S21|')
plt.title('Transmission VS frequency')
plt.savefig(PATH+"\\Saved effective parameters\\Transmission.png") 

plt.figure()
plt.plot(S11ad1.Frequency,S11pd1.Value,color='black')
plt.xlabel('Frequency')
plt.ylabel('S11 phase')
plt.title('Reflection phase VS frequency')
plt.savefig(PATH+"\\Saved effective parameters\\Reflection.png")

plt.figure()
plt.plot(S21ad1.Frequency,S21pd1.Value,color='black')
plt.xlabel('Frequency')
plt.ylabel('S21 phase')
plt.title('Transmission phase VS frequency')
plt.savefig(PATH+"\\Saved effective parameters\\Transmission.png")