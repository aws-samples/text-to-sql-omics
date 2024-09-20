# Amplify App

This folder contains the frontend and backend code needed to initiate an Amplify App.

## Pre-requisites

Node.js v20.11.0

```
npm install -g @aws-amplify/cli
npm install -g vite
npm install
```

## Create the Amplify App

Initialize the Amplify project with default configurations using your AWS Profile.

```
amplify init
amplify add auth
//Default configuration
//Email
```

```
amplify add api
//GraphQL
//Authorization Mode: Amazon Cognito User Pool
//Blank Schema
//answer YES to edit the schema now.
```

The CLI will open a `schema.graphql` file to edit:

- Open the provided `prototype_schema.graphql`
- Copy the contents of `prototype_schema.graphql`
- Paste it into the `schema.graphql` file and save

```
amplify push
```

The result will be an Amplify app that authenticates through Cognito, and uses an AppSync GraphQL API, connected to DynamoDB tables.

## Skip to the `python-cdk` project deployment

Before continuing with the deployment steps in this file, it is the moment to
deploy the backend infrastructure. Go to the [python-cdk](./python_cdk/README.md) instructions
and execute the deployment. You will need the Cognito User Pool ID created by the above Amplify steps. 
More details on the instructions of that file.

## Environment Variables

After the deployment of the CDK code, you can now copy the URL of the created API Gateway API.
Save a file named `.env.local` to the project root folder to establish the environment variables. Values can be retrieved from API Gateway in the AWS Console.

```
VITE_API_QUERY=https://abcxyz.us-east-1.amazonaws.com/prod/sqlToTextBase
```

In API Gateway, navigate to Stages. Locate the `Invoke URL`.

- The value for VITE_API_QUERY is `Invoke URL` + "sqlToTextBase".


## Preview

Previewing the app will create a localhost endpoint that you can view in a browser. From there, create the user account, and log in.

```
vite
```

## Build & Run

```
vite build
vite preview
```
