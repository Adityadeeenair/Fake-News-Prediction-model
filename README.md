
# 📰 Fake News Detection with Logistic Regression

This repository contains my **first Machine Learning project** – a Fake News Detection model built using **Logistic Regression** in Python.  
The project walks through the **complete ML pipeline** – from raw text data to preprocessing, feature extraction, model training, evaluation, and finally a **simple Flask web app** for deployment.

---

## 🚀 Project Overview
The goal of this project was to build a model that can classify news as **Real** or **Fake**.  
I used a dataset of news headlines and authors, combined them into a single feature, and applied **Natural Language Processing (NLP)** techniques before training the model.

---

## 🛠 Steps Followed
- **Data Preprocessing** – handled missing values and merged relevant columns into one text field  
- **Text Cleaning & Stemming** – removed special characters, converted text to lowercase, eliminated stopwords, and applied stemming  
- **Feature Extraction** – converted text into numerical features using **TF-IDF Vectorization**  
- **Train-Test Split** – divided the dataset into training and testing sets  
- **Model Training** – trained a **Logistic Regression** classifier  
- **Evaluation** – checked performance on both training and testing data, and tested with new inputs  
- **Deployment** – created a simple **Flask web app** for interactive predictions  

---

## 📊 Results
- **Training Accuracy:** 98.6%  
- **Testing Accuracy:** 97.9%  

---

## 🌐 Predictive System
The model expects a news input in the format **(Author + Headline)**, similar to the dataset.  

