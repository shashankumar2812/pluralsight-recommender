# Pluralsight Recommender

The project is a Take Home Coding Challenge to build Recommendation Engine for Pluralsight using the User and Course data. The problem statement is to find simiar users using Machine Learning. Part of the challenge is to build a REST API interface which takes in `user_handle` and responds with a set of similar users. 

# 1. Recommendation Approach 
From infrastructure point of view, Recommendations are generated in Batch format and are written to database. These recommendations are then exposed via a RESTful API interface. 
Considering Machine Learning part of the problem, there are many ways to find similar users out of which I have implemented three different models using following two similarity approaches:

1.	Similarity based on interests
2.	Similarity based on user interaction with the platform (Assessment Scores and Course view time)

## 1.1. Similarity based on interests 
In this approach, my hypothesis is users who have similar interest tags are similar. After data preprocessing and cleaning, I represented documented in TF-IDF vector form (Bag Of Words model) and then found users who are closer in the vector space using cosine similarity. As the recommendation domain problems are generally dealing with sparse data, my choice of similarity metric is cosine similarity. This is the default model for generating similar users. It means if `model_handle` is not explicitly mentioned as a query parameter, the recommendation api returns response of this model. 

## 1.2. Similarity based on user interaction with the platform
This is a Collaborative Filtering (Assessment Scores and Course view time) based approach and the hypothesis is users who have watched similar courses are similar. Following two models have been built using Collaborative Filtering approach:
### 1.2.1. K Nearest Neighbor based on Course View Time
A user-item interaction matrix have been built where each cell represents the interaction information(course view time) between user and the course. The next step is to assume each user can be represented as n-dimensional feature vector where each one of the n-dimensions is a course. The final step is to find similarity(cosine similarity in this case) between these vectors.
### 1.2.2. Deep Neural Network based on Course Level View
The problem formulation goes as follows: Similar users watch courses with similar difficulty level. For instance, if a user X1 watched a course Y1 with difficulty level beginner, so she/he will be similar to User X2 who watched the same course Y1. So, if we can create such a Neural Network which can figure out a target level for a particular user based on User-Course viewing interaction with User Embedding layer, we can represent the users in Embedding space. The same Embedding representation is utilized to find similar users in the Embedding space using cosine similarity.


# 2. Prerequisites

1. Python 3.7
2. awscli installed and configured for access. Please use [this link](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) to configure it
3. Run DynamoDB local. Please use [this link](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html) to configure and run local DynamoDB

# 3. Running Locally
1. Clone the repo locally
2. Copy `example.env` to `.env` in the main folder structure
3. Create virtual environment using:
`python3 -m venv venv`

4. Activate virtual environment using: 
`source venv/bin/activate`

5. Install requirements using following:
`pip3 install -r requirements.txt`

6. Make sure DynamoDB local is running
7. Run Recommendation Generator by running: 
`python3 run_generator.py`

8. Run Recommendation Server by running: 
`python3 run_server.py`

# 4. Recommender Technical Architecture

The Recommender Architecture is based on Microservices Architecture and consists of following 2 individual components. For simplicity, the codebase is kept same for this excercise but ideally we should split Recommendation Generator and Server in separate code bases with a (thin) shared library.

## 4.1. Recommendation Generator

The Recommendation Generator is responsible for generating similar user recommendations given the input data and will save it into the DynamoDB(noSQL) Database.

## 4.2. Recommendation Server

The Recommendation Server will accept a `user_handle` using a `POST` request and revert with a list of similar users. 

Endpoint: `http://127.0.0.1:5000/similar-users/`
## 4.2.1. Request 1: 
Sample request format for user with `user_handle` `999` will return default `model_handle` `tfidf_user_interest`: 
```
{
	"user_handle": 999
}
```

Sample Response format:

```
[
    "request_data": 999,
    "data": {
        "model_handle": "tfidf_user_interest",
        "similar_users": [
            67,
            319,
            353,
            376,
            381,
            391,
            393,
            450,
            464,
            516
        ]
    }
]
```
## 4.2.2. Request 2: 
Sample request format for user:
```
{
	"user_handle": 999,
    "model_handle": "dnn_collab_filtering_user_course_level"
}
```

Sample Response format:

```
[
    {
        "model_handle": "dnn_collab_filtering_user_course_level",
        "similar_users": [
            901,
            6871,
            686,
            2429,
            3212,
            4889,
            8467,
            4651,
            8989,
            2471
        ]
    }
]
```

## 4.2.3. Request 3: 
Sample request format for user:
```
{
	"user_handle": 999,
    "model_handle": "knn_collab_filtering_user_course_view"
}
```

Sample Response format:

```
[
    {
        "model_handle": "knn_collab_filtering_user_course_view",
        "similar_users": [
            901,
            6871,
            686,
            2429,
            3212,
            4889,
            8467,
            4651,
            8989,
            2471
        ]
    }
]
```


Here is an example requesting similar users using Postman:
![Alt text](/images/collaborative_filtering_api_response.png?raw=true "Postman")

### 4.3. Local Recommender Architecture
![Alt text](/images/recommendation_microservice_architecture_local.png?raw=true "Local")

## 5. Future work
### 5.1. Real World Recommender Architecture (AWS Stack)
With very minimal effort the same project can be migrated to a fully managed (AWS stack) real-world production level Recommendation Engine. Below is an overview.
![Alt text](/images/recommendation_microservice_architecture.png?raw=true "Real-World")

### 5.2. Machine Learning
1.	We can come up with a way of combining the output of all the above model and use it to find similar users. 
2.	Create an AB testing setup to evaluate above models against each other in outside world.
3.	It would be fun to experiment with Algorithms like Matrix Factorization, Factorization Machines and Neural Networks (may be Auto-encoders). One way would be to feed more data to a Neural Network having User Embedding layer which can be utilized for finding similar users.
4.	I believe Sagemaker’s built-in algorithm Factorization Machine can be a strong contender for solving this problem. Because it would have costed me money, I chose not to try it.

### 5.3. Backend
1.	Develop a separate Microservice for Data Ingestion.
2.	Configure Recommendation Generator algorithms on Sagemaker platform on a specified schedule. The approach is to use Sagemaker as an abstraction layer for managing model training and deployment infrastructure for ML pipeline.
3.	Deploy Flask in Kubernetes cluster.
4.	Implement AB testing layer in Flask or use Sagemaker’s AB Testing capability.
5.	Add Security to the REST API and add healthcheck endpoint.
6.	Integrate the application with Datadog or Sentry for monitoring.

## 6. References
1.	[Recommender Systems handbook by Francesco Ricci](https://www.springer.com/gp/book/9780387858203)
2.	[Deep Learning with Python from Francoise Chollet](https://www.amazon.com/Deep-Learning-Python-Francois-Chollet/dp/1617294438)
3. [Recommender Systems Specialization](https://www.coursera.org/specializations/recommender-systems)
4.	[Deep Learning based Recommender System](https://arxiv.org/pdf/1707.07435.pdf)
5.	[Factorization Machines](https://www.csie.ntu.edu.tw/~b97053/paper/Rendle2010FM.pdf)
6.	[Recommender Systems and Deep Learning in Python](https://www.udemy.com/course/recommender-systems/)
7.	[Building Recommender Systems with Machine Learning and AI](https://www.udemy.com/course/building-recommender-systems-with-machine-learning-and-ai/)