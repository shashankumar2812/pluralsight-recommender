# pluralsight-recommender

The project is a Take Home Coding Challenge to build Recommendation Engine for Pluralsight using the User and Course data. The problem statement is to find simiar users using Machine Learning. Part of the challenge is to build a REST API interface which takes in `user_handle` and responds with a set of similar users.

# Recommender Technical Architecture

The Recommender Architecture will be based on Microservices Architecture and will consist of following 2 individual components.

## 1. Recommendation Generator

The Recommendation Generator will be responsible for generating similar user recommendations given the input data and will save it into the DynamoDB(noSQL) Database.

## 2. Recommendation Server

The Recommendation Server will accept a `user_handle` using a `POST` request and revert with a list of similar users.

