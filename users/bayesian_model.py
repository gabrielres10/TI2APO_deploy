from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.estimators import ParameterEstimator
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination
import pandas as pd

class BayesianModel: 
        
    model = BayesianNetwork([('MoodChanges', 'MajorDepression'), 
                         ('MoodChanges', 'AnxietyDisorder'),
                         ('MoodChanges', 'BipolarDisorder'),
                         ('MoodChanges', 'PTSD'),
                         ('Anxiety', 'MajorDepression'), 
                         ('Anxiety', 'AnxietyDisorder'),
                         ('Anxiety', 'BipolarDisorder'),
                         ('Anxiety', 'PTSD'),
                         ('SleepProblems', 'MajorDepression'), 
                         ('SleepProblems', 'AnxietyDisorder'),
                         ('SleepProblems', 'BipolarDisorder'),
                         ('SleepProblems', 'PTSD'),
                         ('AppetiteChanges', 'MajorDepression'), 
                         ('AppetiteChanges', 'AnxietyDisorder'),
                         ('AppetiteChanges', 'BipolarDisorder'),
                         ('AppetiteChanges', 'PTSD'),
                         ('CognitiveDifficulties', 'MajorDepression'), 
                         ('CognitiveDifficulties', 'AnxietyDisorder'),
                         ('CognitiveDifficulties', 'BipolarDisorder'),
                         ('CognitiveDifficulties', 'PTSD'),
                         ('BehavioralChanges', 'MajorDepression'), 
                         ('BehavioralChanges', 'AnxietyDisorder'),
                         ('BehavioralChanges', 'BipolarDisorder'),
                         ('BehavioralChanges', 'PTSD')])


    # Major Depression
    cpd_values_major_depression = [
        0.95, 0.85, 0.8, 0.75, 0.65, 0.55, 0.5, 0.4,
        0.85, 0.75, 0.7, 0.65, 0.55, 0.45, 0.4, 0.3,
        0.8, 0.7, 0.65, 0.6, 0.5, 0.4, 0.35, 0.25,
        0.75, 0.65, 0.6, 0.55, 0.45, 0.35, 0.3, 0.2,
        0.65, 0.55, 0.5, 0.45, 0.35, 0.25, 0.2, 0.15,
        0.55, 0.45, 0.4, 0.35, 0.25, 0.15, 0.1, 0.05,
        0.5, 0.4, 0.35, 0.3, 0.2, 0.1, 0.05, 0.03,
        0.4, 0.3, 0.25, 0.2, 0.15, 0.1, 0.03, 0.01
    ]

    # Anxiety Disorder
    cpd_values_anxiety_disorder = [
        0.9, 0.8, 0.75, 0.7, 0.6, 0.55, 0.5, 0.45,
        0.8, 0.75, 0.7, 0.65, 0.55, 0.5, 0.45, 0.4,
        0.75, 0.7, 0.65, 0.6, 0.5, 0.45, 0.4, 0.35,
        0.7, 0.65, 0.6, 0.55, 0.45, 0.4, 0.35, 0.3,
        0.6, 0.55, 0.5, 0.45, 0.4, 0.35, 0.3, 0.25,
        0.55, 0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2,
        0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15,
        0.45, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15, 0.1
    ]

    # PTSD
    cpd_values_ptsd = [
        0.85, 0.75, 0.7, 0.65, 0.6, 0.55, 0.5, 0.45,
        0.75, 0.7, 0.65, 0.6, 0.55, 0.5, 0.45, 0.4,
        0.7, 0.65, 0.6, 0.55, 0.5, 0.45, 0.4, 0.35,
        0.65, 0.6, 0.55, 0.5, 0.45, 0.4, 0.35, 0.3,
        0.6, 0.55, 0.5, 0.45, 0.4, 0.35, 0.3, 0.25,
        0.55, 0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2,
        0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15,
        0.45, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15, 0.1
    ]

    # Bipolar Disorder
    cpd_values_bipolar_disorder = [
        0.7, 0.65, 0.6, 0.55, 0.5, 0.45, 0.4, 0.35,
        0.65, 0.6, 0.55, 0.5, 0.45, 0.4, 0.35, 0.3,
        0.6, 0.55, 0.5, 0.45, 0.4, 0.35, 0.3, 0.25,
        0.55, 0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2,
        0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15,
        0.45, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15, 0.1,
        0.4, 0.35, 0.3, 0.25, 0.2, 0.15, 0.1, 0.05,
        0.35, 0.3, 0.25, 0.2, 0.15, 0.1, 0.05, 0.03
    ]



    complementary_values_ptsd = [1 - value for value in cpd_values_ptsd]
    complementary_values_major_depression = [1 - value for value in cpd_values_major_depression]
    complementary_values_anxiety_disorder = [1 - value for value in cpd_values_anxiety_disorder]
    complementary_values_bipolar_disorder = [1 - value for value in cpd_values_bipolar_disorder]


    # Define conditional probability distributions (CPDs)
    cpd_mood_changes = TabularCPD(variable='MoodChanges', variable_card=2, values=[[0.8], [0.2]])
    cpd_anxiety = TabularCPD(variable='Anxiety', variable_card=2, values=[[0.7], [0.3]])
    cpd_sleep = TabularCPD(variable='SleepProblems', variable_card=2, values=[[0.8], [0.2]])
    cpd_appetite = TabularCPD(variable='AppetiteChanges', variable_card=2, values=[[0.8], [0.2]])
    cpd_cognitive = TabularCPD(variable='CognitiveDifficulties', variable_card=2, values=[[0.8], [0.2]])
    cpd_behavioral = TabularCPD(variable='BehavioralChanges', variable_card=2, values=[[0.8], [0.2]])

    cpd_major_depression = TabularCPD(variable='MajorDepression', variable_card=2, values=[cpd_values_major_depression, complementary_values_major_depression], 
                                    evidence=['MoodChanges', 'Anxiety', 'SleepProblems', 'AppetiteChanges', 'CognitiveDifficulties', 'BehavioralChanges'],
                                    evidence_card=[2, 2, 2, 2, 2, 2])

    cpd_anxiety_disorder = TabularCPD(variable='AnxietyDisorder', variable_card=2, values=[cpd_values_anxiety_disorder, complementary_values_anxiety_disorder], 
                                    evidence=['MoodChanges', 'Anxiety', 'SleepProblems', 'AppetiteChanges', 'CognitiveDifficulties', 'BehavioralChanges'],
                                    evidence_card=[2, 2, 2, 2, 2, 2])

    cpd_bipolar_disorder = TabularCPD(variable='BipolarDisorder', variable_card=2, values=[cpd_values_bipolar_disorder, complementary_values_bipolar_disorder], 
                                    evidence=['MoodChanges', 'Anxiety', 'SleepProblems', 'AppetiteChanges', 'CognitiveDifficulties', 'BehavioralChanges'],
                                    evidence_card=[2, 2, 2, 2, 2, 2])

    cpd_ptsd = TabularCPD(variable='PTSD', variable_card=2, values=[cpd_values_ptsd, complementary_values_ptsd], 
                                    evidence=['MoodChanges', 'Anxiety', 'SleepProblems', 'AppetiteChanges', 'CognitiveDifficulties', 'BehavioralChanges'],
                                evidence_card=[2, 2, 2, 2, 2, 2])    
    # Add CPDs to the model
    model.add_cpds(cpd_mood_changes, cpd_anxiety, cpd_sleep, cpd_appetite, cpd_cognitive, cpd_behavioral, cpd_major_depression, cpd_anxiety_disorder, cpd_bipolar_disorder, cpd_ptsd)

    infer=VariableElimination(model)
    
    def use(self, evidence): 
        
        disordersList=['PTSD', 'MajorDepression', 'AnxietyDisorder', 'BipolarDisorder']
        alreadyKnownDisorders=[]
        for dis in disordersList: 
            for evi in evidence: 
                if dis==evi: 
                    alreadyKnownDisorders.append(dis)

        probs={}
        for i in disordersList: 
            if i not in alreadyKnownDisorders: 
                if evidence=={}:
                    probs[i]=self.infer.query(variables=[i]).values[1]
                else:
                    probs[i]=self.infer.query(variables=[i], evidence=evidence).values[1]
        
        print(probs.values)
        
        result=''
        max_val=0
        for i in probs:
            if probs[i]>max_val:
                max_val=probs[i]
                result=i
    
                
        return max_val, result



