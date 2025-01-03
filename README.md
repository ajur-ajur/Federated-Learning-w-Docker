# Federated Learning w Docker

Compiled by Aldira F. Lazuardi

This repository is a proof of concept of **Federated Learning** by utilizing **Docker** containers. This project is nowhere perfect, as it's a simulation of what Federated Learning can be, a machine learning process trained in different nodes (in this case containers). This repository will try to guide the reader in creating a federated model using the **CIC-IDS-2017** dataset that has been preprocessed and sampled to only 10% of its size (this is done to ensure workability in different PC specifications) and trained using **Logistic Regression** algorithm. Furthermore this repository is free to be recompiled for any kinds of usage, however the author does not support anything that can do harm to anyone.

## Getting the Files

The files on this repository can be easily cloned by using git command:

    gh repo clone ajur-ajur/Federated-Learning-w-Docker

Cloning with an IDE like Visual Studio Code by using url:

    https://github.com/ajur-ajur/Federated-Learning-w-Docker.git

Or, you can always download the zip files by clicking the 'Download ZIP' button under the green '<> Code' button.

## Project Setup

Before we run this project, make sure everything has been setup accordingly:

 1. Make sure Docker is installed in your system, please refer to the official [Docker Website](https://www.docker.com/) and follow their installation instructions.
 2. Make sure Python is install in your system, again, please refer to the official [Python Website](https://www.python.org/) and follow their installation instructions. For additional reference, this project utilizes Python 3.11 (currently, the author of this project has no plan to upgrade or downgrade the python version).
 3. Make sure both Docker and Python are setup inside your workstation, for additional reference, the author uses Visual Studio Code and the documentation can be found [here](https://code.visualstudio.com/docs/containers/overview), and [here](https://code.visualstudio.com/docs/languages/python).

## File Composition

At the end of the process, your directory should look something like this:

    .
    ├── aggregator
    │   ├── aggregated_model.pkl
    │   └── aggregator.py
    ├── venv
    └── worker
        ├── cic-ids-2017(10).csv
        └── worker.py
    ├── .gitignore
    ├── docker-compose.yml
    ├── Dockerfile.aggregator
    ├── Dockerfile.worker
    ├── model_matrix.ipynb
    ├── README.md
    └── requirements.txt

Keep in mind that the `venv` directory can be named however you like when installing your virtual environment (which I recommend) you can find the official python's guide in making virtual environment [here](https://docs.python.org/3/library/venv.html). Whether you created a virtual environment or not, make sure to install the requirements listed in `requirements.txt`, you can easily install all requirements by using pip:

`pip install -r requirements.txt`

this requirements file will be used both inside the host system and the containers.

One more thing, the dataset for the preprocessed and sampled `CIC-IDS-2017` can also be found [here](https://drive.google.com/file/d/1aWMHeQZ5n8VYCin0wB0i2XZIvbFk8OGR/view?usp=sharing), the file is processed on this [google colab notebook](https://colab.research.google.com/drive/1mbiVFCnERUcDAU3nNhoZfdK2a6byXAp0?usp=sharing) (its in Indonesian), refer to section 4.7. just before section 5, there exist a cell to save a model which are already preprocessed and sampled, the sampled percentage can be adjusted in section 3.8. under the `sample_size` variable.

## Running the Project

After you finished setting everything up, the project can be run easily as typing:

    docker-compose build
    docker-compose up
that's it. Or, by any other means to build and up containers using Docker.

The training and aggregation method is automatic, once everything is done you should find a file named `aggregated_model.pkl` under `aggregator` directory you can refer to the first section of this document to find how the directories are setup.

## Breakdown

The author have written comments inside every file in this project, but this section will try to breakdown how everything connects to each other. First we will take a look at the containers, following that the machine learning process.

### Containers

The project uses **4 distinct containers** (you can adjust this according to your need). A single container is used as a central aggregator, while the rest are tasked as workers. The aggregator is responsible for combining weights from all workers into one complete model, this can be done by doing a simple average aggregation, in the current project context, the aggregator will average the slope coefficient and intercept given to it by the workers since this project uses **Logistic Regression**. 
The workers, work. Work in this context, is to fit a machine learning model. The model acquired from each node (worker) are different, in true **Federated Learning** application, each nodes are given different types of data corresponding to their environment, but in this project we will have to rely on the randomness of model fitting to do our work.

### Machine Learning

Like previously said, **Logistic Regression** is used to create the IDS model. The reason this method is selected, because its fast and accurate for binary classification. Fast in term of training and lightweight for small containers, remembering that we do not have all the resource available for heavier models like using Keras or TensorFlow. The workers uses HTTP post request to send a simple object (weights as in coefficient and intercept) to the aggregator. The aggregator uses flask to create a local server accepting only http requests from worker nodes.

## Further Improvements

As of now, the aggregator container will always listens for model weights even after the weights already been aggregated and exported to the host machine. Further improvements needed to automate and shutdown the aggregator after it finishes its given tasks.
