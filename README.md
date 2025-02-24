
<div align="center">
<pre>
██╗   ██╗██╗██████╗ ███████╗ ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗
██║   ██║██║██╔══██╗██╔════╝██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝
██║   ██║██║██████╔╝█████╗  ██║     ███████║█████╗  ██║     █████╔╝ 
╚██╗ ██╔╝██║██╔══██╗██╔══╝  ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ 
 ╚████╔╝ ██║██████╔╝███████╗╚██████╗██║  ██║███████╗╚██████╗██║  ██╗
  ╚═══╝  ╚═╝╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝
--------------------------------------------------------------------
web-based sentiment analyzer
</pre>
</div>
<hr></hr>

<div align="center"> <a href="https://vibecheck-app-8e9f5148afc1.herokuapp.com/"> <img src="https://img.shields.io/badge/try%20it%20here-blue?link=https%3A%2F%2Fsantoswaso.pythonanywhere.com%2F" alt="Static Badge"> </a> </div>
<p align="center"> <code>vibecheck</code> is a <strong>sentiment analysis web-app</strong>.</p>
<p align="center"> It classifies text into three sentiment categories: <strong>positive</strong>, <strong>negative</strong>, or <strong>neutral</strong>.

<div align="center">
  <img src="https://github.com/tjrelyts/vibecheck/blob/main/img/demo.gif" alt="Demo gif">
</div>


<h2>Future Improvements</h2>

- <strong>Model Performance:</strong> The model still has room for improvement as the model accuracy is around 80% on average. This can be achieved by experimenting with different preprocessing methods (tokenization, stop word removal), models, and datasets to achieve better accuracy.

<h2>Challenges</h2>

- <strong>Web Integration:</strong> Integrating the machine learning model with Flask to create an interactive web application was a key challenge.
	- <strong>Solution:</strong> Leveraged <strong>Pickle</strong> to serialize the model and vectorizer, ensuring smooth deployment.

<h2>Results</h2>
Currently, <code>vibecheck</code> is successfully deployed as a live web application using <a href="https://www.pythonanywhere.com/"><strong>PythonAnywhere</strong></a>. The app provides real-time sentiment analysis and is accessible to all users with a web browser and an internet connection. Key accomplishments include:

- Building a sentiment analysis model with **scikit-learn** and deploying it with **Flask**.
- Ensuring the web app provides real-time feedback on user inputs.
- Designing an intuitive and user-friendly interface.

<h2>Resources</h2>

- <strong><a href="https://www.kaggle.com/datasets/jp797498e/twitter-entity-sentiment-analysis/">Twitter Sentiment Analysis Dataset</a>:</strong> The dataset used to train the model, available on <strong><a href="https://www.kaggle.com/">Kaggle</a></strong>.
- <strong>Flask:</strong> A lightweight Python framework for web development.
- <strong>scikit-learn:</strong> A powerful machine learning library used for building and training the sentiment classification model.
- <strong>Pickle:</strong> Used to save and load the model and vectorizer objects.

<h2>File Notes</h2>

- <strong>model.pkl:</strong> The trained Naive Bayes model that performs the sentiment classification.
- <strong>vectorizer.pkl:</strong> The vectorizer object used to convert input text into a numerical format that the model can process.



