CREATE DATABASE IF NOT EXISTS facerecognition_att;

USE facerecognition_att;

CREATE TABLE IF NOT EXISTS student (
    Dep VARCHAR(50) NOT NULL,
    roll_no INT NOT NULL,
    email VARCHAR(100),
    year VARCHAR(20),
    semester VARCHAR(20),
    subject VARCHAR(100),
    photo VARCHAR(20),
    PRIMARY KEY (roll_no)
);