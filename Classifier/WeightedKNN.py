# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 15:12:41 2017

@author: BOUEHNNI
"""
import math
import operator
import numpy as np
from AbstractClassifier import AbstractClassifier

class WeightedKNN(AbstractClassifier):
    classifier =None
    learningDataAccess=None

    @classmethod
    def getInstance(self):
        if(self.classifier is None):
            self.classifier=WeightedKNN()
        return self.classifier
            
            
    # appliquer kNN sur un vecteur caractéristique
    def classify (self, vectC, disease_name,crop_production_id):
        neighbors = []
        riskRate=0
        neighbors = self.getNeighbors(vectC,disease_name,True)
        print "voisins", neighbors
        result, riskRate = self.getResponse(neighbors,riskRate)   
        vectC.append(result);
        vectC.append(riskRate);
        self.learningDataAccess.addPrediction(vectC,crop_production_id)

        return vectC
    
    # trouver la classe dominante parmi la liste des voisins en entrée
    def getResponse(self, neighbors,riskRate):
        classVotes = {}
        sum_ = 0
        
        for x in range(len(neighbors)):
            response = neighbors[x][-2]          
            if response in classVotes:
                classVotes[response] += neighbors[x][-3]
                
            else:
                classVotes[response] = neighbors[x][-3] 
            sum_ += neighbors[x][-3]
        sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True) 
        
        # calculer la somme pour eviter le cas ou il ya pas un risque ( taux = 0.0)
        if (sortedVotes[0][1]==sum_ and sortedVotes[0][0] == "non"):
            riskRate = 0
        else :
            
            if(sortedVotes[0][0] == "oui"):
                riskRate=sortedVotes[0][1]/(sum_)
            else:
                riskRate=sortedVotes[1][1]/(sum_)
        
        return sortedVotes[0][0], riskRate
    
    # trouver les voisins d'une instance en entrée ( un vecteur caractéristique)
    def getNeighbors(self,vecteurC,disease_name, is_k):
        self.learningDataAccess=self.createLearningDataAccess(disease_name)
        
        trainingSet=self.learningDataAccess.getTrainingSet()
        if(is_k):
        	param = self.learningDataAccess.getParameter(disease_name,"k")
        else:
        	param = self.learningDataAccess.getParameter(disease_name,"l")

        
        distances = []
        
        for x in range(len(trainingSet)):
            dist = self.euclideanDistance(vecteurC, trainingSet[x])
            distances.append((trainingSet[x], dist))
        distances.sort(key=operator.itemgetter(1))
        
        neighbors = []
        for x in range(param):
            neighbors.append(distances[x][0])
            
        return neighbors
    
    # calculer la distance euclidienne entre deux vecteurs caracteristiques
    def euclideanDistance(self,instance1, instance2):
        distance = 0  
        length = len(instance1)
        for x in range(length):
            distance += pow((instance1[x] - instance2[x]), 2)
        return math.sqrt(distance)
    
    # prétraitement des données 
    # normalisation de l'ensemble d'apprentissage
    # normalisation d'un vecteur caractéristique
    
    # normaliser un vecteur caractéristique
    def normalizeVect(self,vectC):
       npArr = np.array(self.trainingSet)
       for j in range(len(vectC)):
           minimum = np.amin(npArr[:,j].astype(np.float))
           maximum = np.amax(npArr[:,j].astype(np.float))
           vectC[j] = self.scale(vectC[j],minimum,maximum)
       return vectC

    # normaliser l'ensemble d'apprentissage
    def normalizeTrainingSet(self,array):
        npArr = np.array(array)
        
        for j in range(np.shape(npArr)[1]-3):
            npArr[:,j] = self.normalize(npArr[:,j].astype(np.float))  
        for i in range(np.shape(npArr)[0]):
            array[i] = list(array[i])
            for k in range(np.shape(npArr)[1]-3):
                array[i][k]= float(npArr[i][k])
        return array
    
    # normaliser les elements d'une liste entre 0 et 1
    def normalize(self,array):
        scaledArray = np.zeros(len(array))
        minimum = np.amin(array)
        maximum = np.amax(array)
        for i in range(len(array)):
            scaledArray[i] = self.scale(array[i],minimum,maximum)
        return scaledArray
    
    # formule de normalisation d'une valeur entre 0 et 1
    def scale (self,x, minimum, maximum ):
        scaledx = (x - minimum) / (maximum - minimum)
        return scaledx