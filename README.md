# Pluralsight Recommender

The project is a Take Home Coding Challenge to build Recommendation Engine for Pluralsight using the User and Course data. The problem statement is to find simiar users using Machine Learning. Part of the challenge is to build a REST API interface which takes in `user_handle` and responds with a set of similar users. 

# 1. Recommendation Approach
There are many ways to find similar users. Broadly speaking following 2 ways:

1.	Similarity based on interests
2.	Similarity based on user interaction with the platform (Assessment Scores and Course view time)

# 1.1. Similarity based on interests 
In this approach, my hypothesis is users who have similar interest tags are similar. After data preprocessing and cleaning, I represented documented in TF-IDF vector form (Bag Of Words model) and then found users who are closer in the vector space using cosine similarity. As the recommendation domain problems are generally dealing with sparse data, my choice of similarity metric is cosine similarity. 

# 1.2. Similarity based on user interaction with the platform (Assessment Scores and Course view time)
This is a Collaborative Filtering based approach and the hypothesis is users who have watched similar courses are similar. Here, I have build a user-item interaction matrix where each cell represents the interaction information(course view time/assessment score) between user and the course. The next step is to assume these users as a representation of n-dimensional feature vector where each one of the n-dimensions is a course. The final step is to find similarity(cosine similarity in this case) between these vectors.


# 2. Prerequisites

1. Python 3.7
2. awscli installed and configured for access
3. DynamoDB local
4. Flask local

## 3. Running Locally
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
One sample request format for user with `user_handle` `999`: 
```{
	"user_handle": 999
}```

Sample Response format:
```{
    "request_data": 999,
    "data": {
        "model_handle": "collaborative_filtering_course_view",
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
}```

Here is an example:
![Alt text](/images/collaborative_filtering_api_response.png?raw=true "Postman")

### 4.3. Local Recommendater Architecture
![Alt text](/images/recommendation_microservice_architecture_local.png?raw=true "Local")

With very minimal effort the same project can be migrated to a fully managed (AWS stack) real-world production level Recommendation Engine. Below is an overview.

### 4.4. Real World Recommendater Architecture
![Alt text](/images/recommendation_microservice_architecture.png?raw=true "Real-World")