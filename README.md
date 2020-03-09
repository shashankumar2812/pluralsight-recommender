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
### 1.2.2. Deep Neaural Network based on Course Level View
The problem formulation goes as follows: Similar users watch courses with similar difficulty level. For instance, if a user X1 watched a course Y1 with difficulty level beginner, so she/he will be similar to User X2 who watched the same course Y1. So, if we can create such a Neural Network which can figure out a target level for a particular user based on User-Course viewing interaction with User Embedding layer, we can represent the users in Embedding space. The same Embedding representation is utilized to find similar users in the Embedding space using cosine similarity.


# 2. Prerequisites

1. Python 3.7
2. awscli installed and configured for access. Please use [this link](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) to configure it
3. DynamoDB local. Please use [this link](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html) to configure local DynamoDB

# 3. Running Locally
1. Clone the repo locally
2. Copy `example.env` to `.env` in the main folder structure
3. Create virtual environment using:
`python3 -m venv venv`

4. Activate virtual environment using: 
`source venv/bin/activate`

5. Install requirements using following:
`pip3 install -r requirements.txt`

6. Run Recommendation Generator by running: 
`python3 run_generator.py`

6. Run Recommendation Server by running: 
`python3 run_server.py`

# 4. Recommender Technical Architecture

The Recommender Architecture is based on Microservices Architecture and consists of following 2 individual components.

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

### 4.3. Local Recommendater Architecture
![Alt text](/images/recommendation_microservice_architecture_local.png?raw=true "Local")

With very minimal effort the same project can be migrated to a fully managed (AWS stack) real-world production level Recommendation Engine. Below is an overview.

### 4.4. Real World Recommendater Architecture (AWS Stack)
![Alt text](/images/recommendation_microservice_architecture.png?raw=true "Real-World")
