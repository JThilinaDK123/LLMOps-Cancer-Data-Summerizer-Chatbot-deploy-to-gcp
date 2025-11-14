# Deploying a medical chatbot on GCP

## Tech Stack

- LLM Groq  
- Hugging Face Transformers  
- FAISS Index 
- Google Artifact Registry
- Google Kubernetes Cluster  
- Circle CI    

---

## Project Setup

### 1. Build the Virtual Environment

Before writing any code, create a virtual environment.

Steps:

1. Create a new folder in your local machine.  
2. Open the terminal inside the folder and run the following commands:

```bash
python -m venv venv
source venv/bin/activate
```

3. Create a `.env` file inside the root directory and add the following credentials:

```
GROQ_API_KEY=<your_groq_api_key>
HUGGINGFACE_TOKEN=<your_hugging_face_token>
```

4. Create the following folder structure:

```
data/               # Add PDF files here
app/common/             # Create __init__.py inside
app/components/             # Create __init__.py inside
app/config/             # Create __init__.py inside
app/templates/             # Create __init__.py inside
app/application.py  # Flask Application
setup.py            # Project setup and management script
```

5. Run the following command to install the project in editable mode:

```bash
pip install -e .
```

6. Inside the `common` folder, create the following Python scripts:

- `logger.py`
- `custom_exception.py`

7. Inside the `components` folder, create the following Python scripts:

- `data_loader.py` # pipeline that make the vector store
- `embeddings.py` # load the embedding model
- `llm.py` # load the llm model
- `pdf_loader.py` # load the pdf files and chunk them
- `prompt_template.py` # system prompt of the llm model
- `retriever.py` # run the llm model
- `vector_store.py` # create the vector store

8. Inside the `config` folder, create the following Python scripts:

- `config.py` # All the configurations

9. Inside the `templates` folder, create the following html file:

- `index.html`

---

## Dockerization

To containerize the application:

1. Create a `Dockerfile` in the root directory.  
2. Create a `kubernetes.yaml` file for Kubernetes deployment.  

Example structure:

```
Dockerfile
kubernetes.yaml
```

## CI/CD Pipeline

1. Create a `config.yml` inside the .circleci folder.  

---

## GCP Environment Setup

### 1. Create a GKE Cluster

Use the following configuration:

- Cluster Name: llmops-project
- Region: us-central1  
- Access using DNS: Yes  
- Review and Create 

---

### 2. Create a Artifact Registry (Repository)

Use the following configuration:

- Repo Name: llmops-repo
- Format: Docker
- Region: us-central1   
- Review and Create 

---


## Circle CI Setup

Set up a CircleCI account:

- Sign up using your Google account. After creating the account, connect it to GitHub to access the repositories.
- Connect project to CircleCI and set Environment variables. Open CircleCI and go to the projects section.
- Connect CircleCI to the GitHub account
- Authorize CircleCI to access your GitHub repositories and select the project repository (CircleCI will automatically detect the .circleci/config.yml file.)
- Then configure project settings:
- Add Environment Variables under Project Settings → Environment Variables:

```bash
GCLOUD_SERVICE_KEY — your Base64-encoded GCP key
GOOGLE_PROJECT_ID — your GCP project ID
GKE_CLUSTER — your GKE cluster name
GOOGLE_COMPUTE_REGION — your compute region
```

How to obtain the `Base64-encoded GCP key`

- Run below code as a 'git bash' command. Copy whole the output (the encoded key)

```bash
cat gcp-key.json | base64 -w 0
```

Trigger the CI/CD pipeline !!!!!

It will show an error ('llmops-secrets' are not avialble)

### Apply llmops-secrets to the kubernetes cluster

Use the following configuration:

- Navigate to Kubernetes dashboard -> Workloads
- Click the application name -> Kubectl -> get yaml
- Paste the below two codes

```bash
gcloud container clusters get-credentials llmops-project \
--region us-central1 \
--project mlops-thilina
```

```bash
kubectl create secret generic llmops-secrets \
--from-literal=GROQ_API_KEY="your_actual_groq_api_key"
```

---


Trigger the CI/CD pipeline Again !!!!!
