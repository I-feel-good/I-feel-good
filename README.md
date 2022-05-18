# I-feel-good.. L'application du bonheur

# What is it?
This repository contains :
- a **[machine learning model](#the-model)**, trained to predict the emotional category of texts from the diaries of the patients of coach Mr. Zen, our client.
- an **[app](#the-application)** (streamlit) who serves as a graphical interface for the model, and it's an application dedicated to Mr Zen's patients


# The model
>The model we are using is [Keras](https://keras.io/guides/).
Keras is a deep learning API written in Python, running on top of the machine learning platform TensorFlow. It was developed with a focus on enabling fast experimentation. Being able to go from idea to result as fast as possible is key to doing good research.

Keras is:

> - Simple -- but not simplistic. Keras reduces developer cognitive load to free you to focus on the parts of the problem that really matter.
> - Flexible -- Keras adopts the principle of progressive disclosure of complexity: simple workflows should be quick and easy, while arbitrarily advanced workflows should be possible via a clear path that builds upon what you've already learned.
> - Powerful -- Keras provides industry-strength performance and scalability: it is used by organizations and companies including NASA, YouTube, and Waymo.

We are using the vector representation of words of **GloVe** unsupervised pre-trained machine learning model available freely on the internet in .txt file. It allows us to significally increase our prediction performance.

The model architecture is based on LSTM (Long Short Term Memory) layers which is an improvement of classical Reccurent Neural Networks (RNN). It allows us to get rid of the Vanish Gradient problem which occurs in long enough textual data.

We also tried other models that we ended up not using, such as:
- TextHero and FastText
- Scikit-learn

## Features
The model needs texts of patients which must be cleaned and tokenized in order to make predictions. It predicts the emotional main character of texts distributed in 6 categories: happy, sadness, love, anger, fear and surprise.


# The application
The application was made using **streamlit** in order to have a simple but good result while **saving development time**.

The **goal** of this application is **to provide easier predictions** to the user, Mr Zen which predicts whether the writings of Mr Zen's patients fall into the following categories :
- Happy 
- Sadness
- Love 
- Anger
- Fear
- Surprise

### Main skills:

![Python](https://img.shields.io/badge/-Python-0D1117?style=for-the-badge&logo=javascript&labelColor=0D1117&textColor=0D1117)&nbsp;

### Tools:

![Visual Studio Code](https://img.shields.io/badge/-Visual%20Studio%20Code-0D1117?style=for-the-badge&logo=visual-studio-code&logoColor=007ACC&labelColor=0D1117)&nbsp;
![Git](https://img.shields.io/badge/-Git-0D1117?style=for-the-badge&logo=git&labelColor=0D1117)&nbsp;
![GitHub](https://img.shields.io/badge/-GitHub-0D1117?style=for-the-badge&logo=github&labelColor=0D1117)&nbsp;
![Windows](https://img.shields.io/badge/-Windows-0D1117?style=for-the-badge&logo=windows&labelColor=0D1117)&nbsp;
![microsoft-office](https://img.shields.io/badge/-microsoft_office-0D1117?style=for-the-badge&logo=microsoft-office&labelColor=0D1117)&nbsp;
![Linux](https://img.shields.io/badge/-linux-0D1117?style=for-the-badge&logo=linux&labelColor=0D1117)&nbsp;

### Other Knowledge:

![Markdown](https://img.shields.io/badge/-Markdown-0D1117?style=for-the-badge&logo=markdown&labelColor=0D1117)&nbsp;

