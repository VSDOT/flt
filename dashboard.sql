
CREATE DATABASE dashboard;

CREATE TABLE dashboard.account (
user_id int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
username text NOT NULL,
email varchar(50) UNIQUE NOT NULL,
password text NOT NULL
);

CREATE TABLE dashboard.azure (
azure_id int NOT NULL,
subscription_id VARCHAR(100) UNIQUE NOT NULL,
tenent_id VARCHAR(100) UNIQUE NOT NULL,
client_id VARCHAR(100) UNIQUE NOT NULL,
client_secret VARCHAR(100) UNIQUE NOT NULL,
FOREIGN KEY (azure_id) REFERENCES account(user_id)
);

CREATE TABLE dashboard.aws (
aws_id int NOT NULL,
accesskey VARCHAR(100) UNIQUE NOT NULL,
secretkey VARCHAR(100) UNIQUE NOT NULL,
FOREIGN KEY (aws_id) REFERENCES account(user_id)
);

CREATE TABLE dashboard.gcp (
gcp_id int NOT NULL,
project_id VARCHAR(100) UNIQUE NOT NULL,
credentials VARCHAR(100) UNIQUE NOT NULL,
FOREIGN KEY (gcp_id) REFERENCES account(user_id)
);
