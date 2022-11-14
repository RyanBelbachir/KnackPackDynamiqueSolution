
from asyncore import write
from tokenize import String
from typing import List
import pandas as pd
import streamlit as st
import os


def sacAdos(capacite, elements):
    #Initialiser le tableau 
    tableau = [[0 for x in range(capacite+1)] for x in range(len(elements)+1)]

    #Remplissage du tableau
    for i in range(1, len(elements)+1):
        for w in range(1, capacite+1):
            if elements[i-1][1] <= w :
                tableau[i][w] = max(elements[i-1][2]+tableau[i-1][w-elements[i-1][1]], tableau[i-1][w])
            else:
                tableau[i][w] = tableau[i-1][w]
    
    w = capacite
    n = len(elements)
    elementsChoisis = []

    #Construction de la liste des éléments composant la solution optimale
    while w >= 0 and n >= 0:
        e = elements[n-1]
        if tableau[n][w] == tableau[n-1][w-e[1]] + e[2]:
            elementsChoisis.append(e)
            w = w - e[1]
        n = n-1
    
    return tableau[-1][-1], elementsChoisis, tableau


#Programme principale

#(nom,poids,valeur)
ele = [("montre",2,6),("portrait",4,12),("trousse",3,10)]

#Principe : Quand l'utilisateur insère les objets un par un jusqu'à être satisfait
#           Après, il pourra cliquer sur ==> Ajouter éléments à chaque insersion
#           L'utilisateur pourra aussi indiquer le poids max du sac à dos, par defaut = 0
#           Dès que l'utilisateur a finit d'insérer il pourra cliquer sur ==> Go
#           Ce bouton va donner comme résultat :
#                           * Un tableau des objets qui ont été inséré
#                           * La matrice de calcul lors de la programmation dynamique (facultatif)
#                           * Un tableau final concernant les objets qui ont été sélectionnés
#                           * Le Gain optimal

def main() :
    st.header("Problème du Sac à Dos :")
    data = pd.DataFrame()
    listt = []
    col1,col2,col3,col4 = st.columns(4)
    obj = col1.text_input("Object :")
    weight = col2.number_input("Weight :", step=1, key=0)
    gain = col3.number_input("Gain", step=1,key=1)
    knackpackWeight = col4.number_input("Poids Max du Sac à dos", step=1,key=2)
    if(st.button("Ajouter Objet",key=100)) :
        file = open("KnackPack","a")
        file.writelines(obj+" "+str(weight)+" "+str(gain)+"\n")
        file.close()
        file = open("KnackPack","r")
        listObj = []
        listWeight = []
        listGain = []
        listt = file.readlines()
        for line in listt:
            listObj.append(str(line).split(" ")[0])
            listWeight.append(str(line).split(" ")[1])
            listGain.append(str(line).split(" ")[2])
        data['Objet']=listObj
        data['Poids']=listWeight
        data['Gain']=listGain
        st.write("Liste initiale des objets : ")
        st.table(data)
        data.to_csv("dataOfKnackPack.csv",index=False)
    
    #Sauvegarder dans un fichier pour une certaine optimisation
    if(st.button("Go",key=101)) :
        i=0
        listt = []
        data = pd.read_csv("dataOfKnackPack.csv")
        listObj = data["Objet"].to_list()
        listWeight = data["Poids"].to_list()
        listGain = data["Gain"].to_list()
        st.write("Liste initiale des objets : ")
        st.table(data)
        while(i<len(data.index)):
            listt.append((str(listObj[i]),int(listWeight[i]),int(listGain[i])))
            i+=1 
        x,y,z = sacAdos(knackpackWeight,listt)
        st.write("Matrice de calcul de la programmation dynamique : ")
        st.table(z)
        st.write("Les éléments choisis sont : ")
        choisis = pd.DataFrame()
        listObjChoice = []
        listWeightChoice = []
        listGainChoice = []
        j=0
        while(j<len(y)):
            print(list(y[j])[0])
            listObjChoice.append(list(y[j])[0])
            listWeightChoice.append(list(y[j])[1])
            listGainChoice.append(list(y[j])[2])
            j+=1
        choisis["Objet"] = listObjChoice
        choisis["Poids"] = listWeightChoice
        choisis["Gain"] = listGainChoice
        st.table(choisis)
        st.write("Le poids Optimal est : ",x)
    
    # Pour effacer le contenu du tableau
    if(st.button('Reset Data',key=102)):
        open('KnackPack', 'w').close()
        os.remove('dataOfKnackPack.csv')

main()