# Machine Learning on GBT Data

Mentors: Pragaash Ponnusamy, pragaashp@berkeley.edu, and Steve Croft, scroft@berkeley.edu

## Research Question

Can signals of interest for SETI (those that are rare and located only in one place, or a few places, on the sky, or are unique in their statistical properties, shape, etc.) be distinguished from various classes of RFI?

## Description

Many of the algorithms that are currently run on Green Bank Telescope data search for simple tones, pulses, or drifting narrow-band signals. But these signals can be difficult to distinguish from human-generated radio frequency interference (RFI), and in addition the pipeline may miss more complex signals that could be of interest. Your task will be to explore and develop unsupervised/semi-supervised machine learning algorithms at scale to identify, extract, and classify signals of interest into various populations, and analyze how these signals cluster under varying feature sets.

For a general overview of what was done, read the SETI Final Report pdf.
Note that due to the amount of data, many of the intermediate files and dataframes mentioned (used for calculations; .npy and .pkl format) have not been pushed to this Github repository. Additionally, all code is currently in a private repository – email jmxia@berkeley.edu if you’d like to have a look at it! 

## Jupyter Notebooks

### Loading in Data

This notebook is where I process and featurize all the data. Read within to find a summary of all the .npy and .pkl files (their contents, how they were created).

### Probabilities CSV

This notebook runs through the files on my computers, pulls out all files containing labelled data, and records these labels. 

### Single GUI Guide

This notebook contains guidelines on how to label data using the fits_single_GUI.

### PCA and t-SNE

This notebook attempts to cluster unlabelled data based on HOG and correaltion values.

### Positive Naive Bayes Classifier_GPS

This notebook attempts to use a bayes classifier to categorize instances of ON/OFF pairs in which the ON file shows a strong GPS signal, but the OFF file shows a very weak/no signal.

### SVM

This notebook attempts to use support vector machines (SVM), logistic regression, linear discriminant analysis (LDA), quadratic discriminant analysis (QDA), in a one vs. rest method, multiclass, and in single class chaining.
