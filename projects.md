
*Click to expand each section

   <details>
     <summary><strong><a href="https://github.com/takline/ResumeGPT">github.com/takline/ResumeGPT</a>:</strong> ResumeGPT is an open-source python library that allows you to simply provide your resume and a job posting link, and it will produce a formatted ATS friendly PDF resume that is optimized and personalize your resume to align with the specific requirements and keywords of the job.</summary>
<h1 align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="images/ResumeGPT-light.png"/>
    <source media="(prefers-color-scheme: light)" srcset="images/ResumeGPT.png"/>
    <img width="400" src="images/ResumeGPT.png"/>
 <br />
</h1>

<div align="center">

<p align="center">
  <a href="#features">
    <b>Features</b>
  </a>
     · 
  <a href="#installation">
    <b>Install</b>
  </a>
     · 
  <a href="#usage">
    <b>Usage</b>
  </a>
      · 
  <a href="#discussions">
    <b>Discussions</b>
  </a>
     · 
  <a href="#contributors">
    <b>Contributors</b>
  </a>

</p>

<br>


</div>

<br>

<h3 align="center">Tailor your resume to match any job posting effortlessly with ResumeGPT.
</h3>

<br/>
ResumeGPT allows you to simply provide your resume and a job posting link, and it will produce a formatted ATS friendly PDF resume that is optimized and personalize your resume to align with the specific requirements and keywords of the job. 

## Features
- Extracts relevant skills, qualifications, and keywords from a job posting.
- Tailors your curent resume to match job requirements.
- Generates professional ATS friendly PDF resumes.
- Allows for user verification and customization before finalizing the resume.

## Installation
To install ResumeGPT, clone the repository and install the required dependencies:

```bash
git clone https://github.com/takline/ResumeGPT.git
cd ResumeGPT
pip install -r requirements.txt
```

## Usage

 - Add your resume to `ResumeGPT/data/sample_resume.yaml` (make sure `ResumeGPT.config.YOUR_RESUME_NAME` is set to your resume filename in the `.data/` folder)
 - Update `ResumeGPT/config/config.ini` with your name and info that will be included in your resume
 - Provide ResumeGPT with the link to a job posting and it will tailot your resume to the job:

### Single job posting usage
```python
url = "https://[link to your job posting]"
resume_improver = ResumeGPT.services.ResumeImprover(url)
resume_improver.create_draft_tailored_resume()
```

ResumeGPT then creates a new resume YAML file in a new folder named after the job posting (`ResumeGPT/data/[Company_Name_Job_Title]/resume.yaml`) with a YAML key/value: `editing: true`. ResumeGPT will wait for you to update this key to verify the resume updates and allow them to make their own updates until users set `editing=false`. Then ResumeGPT will create a PDF version of their resume.


### Custom resume location usage
Initialize `ResumeImprover` via a `.yaml` filepath.:

```python
resume_improver = ResumeGPT.services.ResumeImprover(url=url, resume_location="custom/path/to/resume.yaml")
resume_improver.create_draft_tailored_resume()
```

### Post-initialization usage
```python
resume_improver.update_resume("./new_resume.yaml")
resume_improver.url = "https://[new link to your job posting]"
resume_improver.download_and_parse_job_post()
resume_improver.create_draft_tailored_resume()
```

### Background usage
You can run multiple ResumeGPT.services.ResumeImprover's concurrently via ResumeGPT's BackgroundRunner class (as it takes a couple of minutes for ResumeImprover to complete a single run):
```python
background_configs = [
    {
        "url": "https://[link to your job posting 1]",
        "auto_open": True,
        "manual_review": True,
        "resume_location": "/path/to/resume1.yaml",
    },
    {
        "url": "https://[link to your job posting 2]",
        "auto_open": False,
        "manual_review": False,
        "resume_location": "/path/to/resume2.yaml",
    },
    {
        "url": "https://[link to your job posting 3]",
        "auto_open": True,
        "manual_review": True,
        "resume_location": "/path/to/resume3.yaml",
    },
]
background_runner = ResumeGPT.services.ResumeImprover.create_draft_tailored_resumes_in_background(background_configs=background_configs)
#Check the status of background tasks (saves the output to `ResumeGPT/data/background_tasks/tasks.log`)
background_runner["background_runner"].check_status()
#Stop all running tasks
background_runner["background_runner"].stop_all_tasks()
#Extract a ResumeImprover
first_resume_improver = background_runner["ResumeImprovers"][0]
```

You will follow the same workflow when using ResumeGPT's BackgroundRunner (ex: verify the resume updates via `editing=false` in each `ResumeGPT/data/[Company_Name_Job_Title]/resume.yaml` file). You can also find logs for the BackgroundRunner in `ResumeGPT/data/background_tasks/tasks.log`.


### ResumeGPT PDF Output
Here is an example ATS friendly resume created by ResumeGPT:

<p align="center">
  <img src="./assets/images/example_resume_output.png" alt="Resume Example" width="400"/>
</p>
   </details>
<br>
<hr>
<br>
   <details>
     <summary><strong><a href="https://github.com/takline/Home/tree/main/AI">AI</a>:</strong> This section features projects using platforms like OpenAI, Claude, and Vertex AI. You'll find examples of machine learning model implementation, natural language processing tasks, and AI deployments. The focus is on practical use-cases such as predictive modeling, text analysis, and integrating AI within existing systems.</summary>
             <details>
     <summary><strong><a href="https://github.com/takline/Home/tree/main/AI/OpenAI%20-%20Embeddings%20with%20Notion">OpenAI Embeddings in Notion</strong></summary>

This repo will help guide you through the creation of a Notion chatbot utilizing a blend of LangChain, OpenAI, FAISS, and Streamlit!


## The Concept Behind a Notion Chatbot

Imagine a chatbot seamlessly integrated into Notion.

### The Challenge
In my previous engagement, a client had their entire organizational database on Notion. Given the extensive documentation, swiftly locating specific information was a challenge. To counter this, I devised a Notion chatbot, leveraging cutting-edge AI tools to simplify information retrieval.

###  The Approach
Our strategy begins with LangChain to parse and segment Notion's content, transforming it into vector representations via OpenAI embeddings, and housing them in FAISS, a vector database. We craft a Conversational Retrieval Chain using LangChain to bridge our vector database and OpenAI GPT, aiming to respond to queries with the most pertinent information derived from our Notion database. Enhancements include customizing the system prompt and integrating memory capabilities. The final touch involves crafting a user-friendly chat interface via Streamlit, embedding it directly within Notion.

## Project Roadmap

1. Initial Setup and Framework
We explore the project's framework and set up necessary dependencies. This stage also involves securing an OpenAI API key and replicating a public Notion page to form the foundation of our project.

2. Processing Documents
This phase focuses on transforming Notion's content into numerical vectors. Given the limitations of LLMs like GPT in processing lengthy texts, we employ LangChain to fragment the content into manageable segments. These segments are then vectorized using OpenAI’s embedding model and stored in a vector database.

3. Formulating Queries
User queries are vectorized using the same embedding model and compared against our pre-established vector database. The corresponding content, alongside the user query, is fed into OpenAI GPT to generate responses.

To enhance the chatbot's functionality, we maintain a record of previous interactions, allowing the chatbot to access this conversational history during interactions.

4. Building the Chatbot Interface
We utilize Streamlit to design an intuitive chat interface, which is then hosted online and integrated within the Notion platform.

This guide takes inspiration from Harrison Chase (Founder of LangChain) on interacting with Notion content through LangChain. Our enhancements include:

- Specific markdown characters for optimal content segmentation
- Memory feature for the chatbot
- Using Streamlit for a sophisticated chat interface, incorporating its new chat functionalities
- Embedding the Streamlit chat application into a Notion page

## Tutorial Overview

1. Project Structure and Initiation

    1.1 Framework of the Project

### Project Framework
The notion-chatbot project is structured as follows:

- .streamlit/secrets.toml: For storing the OpenAI API key
- faiss_index: The FAISS index, our vector database
- notion_content: Directory for Notion content in markdown format
- .gitignore: To exclude tracking of the OpenAI API key and Notion content
- app.py: The Streamlit chat application script
- ingest.py: Script for vectorizing Notion content and indexing
- utils.py: Script for creating the Conversation Retrieval Chain
- requirements.txt: Necessary packages for Streamlit Community Cloud deployment

We'll construct these components step-by-step throughout this tutorial.

1.2 Initializing the Project

- Create a project directory named notion-chatbot
- Establish a new environment and install required dependencies
- Generate a .gitignore file to outline untracked files
- Retrieve your OpenAI API key from OpenAI’s portal
- Set up a .streamlit folder and within it, create secrets.toml for storing the OpenAI API key
- Utilize Blendle Employee Handbook as the knowledge base for this tutorial
- If you don’t have a Notion account, register for free on their site
- Duplicate the Blendle Employee Handbook to your Notion for project use

2. Ingesting Documents
2.1 Exporting Notion Content

- Navigate to the Blendle Employee Handbook main page on Notion
- Opt for Export in Markdown and CSV formats, including subpages
- Save the exported file as notion_content.zip, unzip it, and place it in the notion-chatbot folder

For simplicity, we're manually exporting Notion content for this tutorial.

2.2 Vectorizing Notion Content

To utilize the Notion page content as our chatbot's knowledge base, we convert it into vectors and store them using LangChain, OpenAI embedding model, and FAISS.

Open the project

 in your preferred IDE and create ingest.py:

# ingest.py

[Code block detailing the process of loading the OpenAI API key, loading and splitting Notion content, initializing the OpenAI embedding model, and converting text chunks into vectors stored in a FAISS index]

3. Managing Queries
3.1 Query Process

- Establish a chat history to serve as the chatbot's memory, storing user queries and chatbot responses
- User poses a question, which is logged in the chat history
- Blend the question with the chat history to form a standalone query
- Vectorize the standalone query and search for similar vectors in the database
- GPT generates an answer using the most relevant content from Notion
- The chatbot conveys GPT's answer to the user, adding it to the chat history
- Repeat the process for ongoing interactions

3.2 Handling Queries

We develop a LangChain Conversational Retrieval Chain as the core of our application, creating utils.py to house the load_chain() function.

# utils.py

[Code segment outlining the creation of the Conversational Retrieval Chain, including the initialization of the OpenAI embedding model, the chat model, the local FAISS index, and the memory feature, along with the setup of the system prompt]

4. Chatbot Interface Development
4.1 Streamlit Application

With our chatbot's "brain" ready, we proceed to build the Streamlit application:

# app.py

[Code snippet explaining the importation of the chain from utils.py, configuration of the Streamlit page, initialization of the LLM chain and chat history, chat message display mechanism, and the chat logic processing user queries and generating responses]

4.2 Deploying on Streamlit Cloud

Ready to go live? Here's how to deploy on Streamlit Cloud:

- Prepare a requirements.txt file listing all dependencies
- Follow the deployment process, specifying Python version and OpenAI API key

4.3 Integrating Streamlit App in Notion

- After successful deployment, copy your app's URL
- In Notion, choose Embed in the block options and paste the app URL

And there you have it, your interactive Notion chatbot is ready for action!



   </details>
   <details>
   <summary><strong><a href="https://github.com/takline/Home/tree/main/AI/Google%20Gemini%20Vision%20-%20Notion%20Automation">Google Gemini Vision - Notion Automation</a>:</strong></summary>
     ### Video --> Notion --> Google Gemini Summary --> Notion

#### **Overview**

This repository contains a Python application designed to create automated summaries of videos saved to the iOS Notion app. The application integrates Notion, Google Cloud Platform (GCP), and Google's Gemini multimodal Large Language Model (LLM) to fetch videos from Notion, optionally compress them, and then generate summaries using advanced AI techniques. The summarized content is formatted in HTML for easy integration back into Notion or other platforms.

---

#### **Components**

1. **Notion Integration:** Interacts with a Notion database to retrieve videos.

2. **Video Processing:** Compresses videos if they exceed a specified size limit.

3. **Google Cloud Storage:** Uploads the processed videos to Google Cloud for further processing.

4. **Google's Gemini Model:** Utilizes this cutting-edge AI model to generate summaries of the videos.

5. **Pipedream Workflow:** Orchestrates the entire process, triggered when a new note with a video is created in Notion.

---

#### **Setup and Configuration**

1. **Prerequisites:**
   - Python 3.8 or later.
   - Access to Google Cloud Platform and a configured GCP bucket.
   - A Notion account with API access.
   - Pipedream account for workflow automation.

2. **Environment Setup:**
   - Install required Python packages: `ffmpeg-python`, `moviepy`, `google-cloud-aiplatform`.
   - Set environment variables for Google Cloud credentials and Notion API access.

3. **Google Cloud Credentials:**
   - Follow Google Cloud documentation to obtain service account credentials.
   - Update the credentials in the script or set them as environment variables.

4. **Notion Setup:**
   - Create a Notion database with video attachments.
   - Obtain API access and integrate it with the script.

5. **Pipedream Workflow:**
   - Set up a Pipedream workflow that triggers the script when a new video note is created in Notion.

---

#### **Usage**

- **Running the Script:**
  The script can be executed as part of the Pipedream workflow. On triggering, it performs the following steps:
  1. Downloads the video from Notion.
  2. Checks and compresses the video if it's larger than the specified limit.
  3. Uploads the video to Google Cloud Storage.
  4. Sends the video to Google's Gemini model for summarization.
  5. The summary is then parsed and can be used to update the Notion note or for other purposes.

- **Customization:**
  You can customize the script to change the compression settings, summary format, or integrate with different platforms.

---

#### **Gemini Model Overview**

Google's Gemini model is a state-of-the-art multimodal Large Language Model capable of understanding and generating content from both text and media inputs like videos. In this application, Gemini analyzes the video content and generates a comprehensive summary, demonstrating its ability to handle complex AI tasks.

---

#### **Contributing**

Contributions to this project are welcome. Please follow the standard GitHub pull request process to submit your changes.

---

#### **License**

This project is released under MIT License, allowing for both personal and commercial use with proper attribution.

---

#### **Contact**

For any queries or collaboration requests, please reach out to tylerkline@gmail.com.

---

### **Note:**

This README provides a high-level overview of the application, its components, and usage. It's designed to cater to both technical and non-technical audiences, ensuring clarity in understanding the project's functionality and scope.
   </details>    

   </details>
<br>
<hr>
<br>

   <details>
     <summary><strong><a href="https://github.com/takline/Home/tree/main/Data%20Engineering%20%26%20Pipelines">Data Engineering & Pipelines</a>:</strong> My bread and butter - data engineering. Here you will see my experience with building data pipelines (ETL, data warehousing, streaming, etc...). Tools and technologies like Apache Kafka, Spark, and SQL databases are commonly used here. The projects demonstrate effective data management from ingestion to processing and storage.</summary>
<details>
     <summary><strong><a href="https://github.com/takline/Home/tree/main/Data%20Engineering%20%26%20Pipelines/luigi-ml-pipeline">Luigi ML Pipeline</summary>
     # Luigi ML Pipeline

This repository showcases an easy-to-follow method for automating data transformations, modeling, and a [Luigi](https://github.com/spotify/luigi) data pipeline.


#### Key Components

- Python version 3.7 or higher
- Streamlit for interactive applications
- Scikit-learn for machine learning tasks
- Pandas for data handling
- Luigi for workflow automation


## Concept

The entire workflow is encapsulated in an interactive application found in the `pipeline.py` script. Refer to the instructions in the "How to Run the Scripts" section for details on setting up and launching the application.

## Configuration

1. Set up a dedicated virtual environment (using `conda` is suggested):
   ```bash
   conda create --name data_workflow python=3.7
   ```
2. Activate your new virtual environment:
   ```bash
   conda activate data_workflow
   ```
3. Install the necessary packages:
   ```bash
   pip install -r requirements.txt
   ```


## Running the Scripts

#### Interactive Application

To launch the interactive app, use the Streamlit command within your activated virtual environment:
```bash
(data_workflow) streamlit run pipeline.py
```

This will start a local server accessible at: [`http://localhost:8501`](http://localhost:8501).

#### Data Workflow

To run a specific task, for instance `TaskX` located in the `workflow.py` script, use the following command:

```bash
PYTHONPATH=. luigi --module workflow TaskX --local-scheduler
```

Feel free to expand upon the code by adding your own custom tasks!


   </details>
   </details>
<br>
<hr>
<br>
   <details>
     <summary><strong><a href="https://github.com/takline/Home/tree/main/Cloud%20Computing">Cloud Computing</a>:</strong> Work involving AWS, Google Cloud, Azure, and other tech (ex: Snowflake).</summary>
        <details>
     <summary><strong><a href="https://github.com/takline/Home/tree/main/Cloud/LambdaVideoSummary">Lambda Video Summary</summary>
# Lambda & Google Gemini Integration

## Overview
This AWS Lambda function is designed to automatically trigger upon the upload of new files to Dropbox or S3. Upon activation, it processes the uploaded video file and generates a comprehensive summary. This summary includes key points, a deeper analysis, and categorization tags.

This was a fun excuse to try out Google's new multimodal AI model - Gemini. This integration allows the function to not just process video uploads, but to deeply understand and interpret the content.

## Workflow Summary

The AWS Lambda function orchestrates a sophisticated workflow to automate the process of video summarization. Here's a step-by-step overview:

1. **Trigger Event**: The workflow begins when a new video file is uploaded to either Dropbox or an Amazon S3 bucket. This event automatically triggers the AWS Lambda function.

2. **File Processing and Validation**: Upon activation, the function first validates the video file format and size. It ensures compatibility and prepares the file for further processing.

3. **Video Compression**: To optimize for processing speed and efficiency, the video file is compressed. This step adjusts the video to a suitable size and format without significant loss of quality, ensuring it meets the requirements of Google Cloud Storage.

4. **Upload to Google Cloud Storage**: The compressed video file is then securely uploaded to Google Cloud Storage. This step is crucial as it provides a stable and accessible location for the video, ready for analysis by the AI model.

5. **AI Analysis with Gemini Multimodal Model**: With the video in place, Google's Gemini multimodal AI model takes over. This advanced AI system analyzes the video, interpreting both visual and auditory elements. It leverages deep learning to understand context, themes, and key messages within the video.

6. **Generating the Summary**: The AI model processes the content and generates a comprehensive summary. This summary includes the most critical points, insights, and a coherent narrative that encapsulates the essence of the video.

7. **Storing Summary in Notion**: Once the summary is created, it is automatically formatted and stored in a Notion database. This integration provides an organized and easily accessible way to retrieve and review the summaries.

8. **Notification and Logging**: After the summary is successfully stored, the function sends a notification to the user (or a designated recipient) to inform them of the completion of the process. Simultaneously, detailed logs of the operation are maintained for monitoring and troubleshooting purposes.

9. **Cleanup and Maintenance**: The function also includes a cleanup routine to remove temporary files or data used during the process, ensuring efficient use of storage and resources.

10. **Security and Compliance**: Throughout the workflow, security and compliance are prioritized. Sensitive information like API keys and credentials are securely managed using AWS Secrets Manager, ensuring that the entire process is not only efficient but also secure.


## Prerequisites
- AWS account with Lambda and S3 access
- Dropbox account (if using Dropbox triggers)
- Google Cloud Storage account (for video processing and storage)
- Notion account (for storing and managing summaries)

## Configuration
Before deployment, ensure all necessary libraries and dependencies are installed, and configure the following:
- `config.py`: Contains all the configuration settings for AWS, Dropbox, Google Cloud Storage, and Notion.
- `google_auth.json`: A JSON file with your Google Cloud service account credentials.
- `SECRETS`: A dictionary obtained from AWS Secrets Manager, storing sensitive information like API keys and tokens.

## Deployment
1. Clone the repository from `git@github.com:takline/automation.git`.
2. Set up your AWS Lambda environment with the necessary permissions and environment variables.
3. Upload the code to your AWS Lambda function.

## Functionality
The Lambda function comprises several key components:
- Dropbox and S3 triggers: Initiate the function upon file upload.
- Video processing: Compresses and uploads the video to Google Cloud Storage.
- Video summary generation: Utilizes Vertex AI to generate a video summary.
- Notion integration: Creates a new page in Notion with the video summary.

## Usage
1. Upload a video file to your configured Dropbox folder or S3 bucket.
2. The Lambda function triggers automatically, processes the video, and generates a summary.
3. Check the corresponding Notion database for the new summary page.

## Logging
- Logging is handled by `lambda_logs.py`, which records function activity and errors.
- Logs are stored in S3 and can be monitored for troubleshooting and analysis.

## Security
- Use AWS Secrets Manager to securely store and access sensitive information.
- Ensure your AWS Lambda function has the minimum required permissions.

## Limitations
- Video file size is limited by Google Cloud Storage's maximum file size.
   </details>
   </details>
<br>
<hr>
<br>
   <details>
     <summary><strong><a href="https://github.com/takline/Home/tree/main/Analytics%2C%20Reporting%20%26%20Visualization">Analytics, Reporting & Visualization</a>:</strong> Some of my more fun work creating data visualizations for clients. Using tools like Tableau, Python libraries (e.g., Matplotlib, Seaborn), I've focused on effectively translating data into understandable formats, making it easy for decision-makers to grasp key insights.</summary>
             <details>
     <summary><strong><a href="https://github.com/takline/Home/tree/main/AI/OpenAI%20-%20Embeddings%20with%20Notion">Data Visualization Project using Power BI
</summary>
# Data Visualization Project using Power BI

![image](./assets/images/powerBI.png)

Welcome to the GitHub repository for my Data Visualization project using Power BI! In this project, I have utilized Power BI to create compelling visualizations from raw datasets, enabling data-driven insights and informed decision-making. This repository contains the resources and documentation related to the project.

## Project Overview

The primary goal of this project was to transform and visualize complex datasets to provide meaningful insights for better understanding and analysis. I employed various techniques and features offered by Power BI to achieve this, including Power Query for data cleaning and transformation, establishing relationships for data modeling, and utilizing DAX (Data Analysis Expressions) to create explicit measures for enhanced control and reusability.

## Tasks Accomplished
1. Data Cleaning and Transformation using Power Query:
I employed Power Query to clean and transform the raw datasets. This process involved handling missing values, standardizing data formats, and performing necessary data wrangling steps to ensure data accuracy and consistency.

2. Relationships for Data Modeling:
To establish a robust and dynamic data model, I utilized Power BI's relationship feature. By connecting relevant tables through appropriate keys, I created a foundation for generating coherent visualizations that draw insights from multiple data sources.

3. DAX Measures for Enhanced Control and Reusability:
I harnessed the power of DAX to create explicit measures. These measures enable me to perform advanced calculations and aggregations while offering better control, reusability, and efficiency in connecting different components within the report.

4. Creating Diverse Visualizations:
This project encompasses a range of visualization techniques including cards, tables, and graphs. These visualizations have been carefully chosen to represent the data in a comprehensive and intuitive manner, facilitating easier interpretation and analysis.

5. Online Report and Dashboard Creation:
After preparing the data and designing visualizations, I uploaded the Power BI report online. This allowed me to create an interactive dashboard that provides a seamless and user-friendly experience for exploring insights and trends within the data.


Feel free to reach out if you have any questions, suggestions, or feedback regarding this project. I hope these visualizations provide a clear understanding of the data and its implications.

   </details>
        <details>
     <summary><strong><a href="https://github.com/takline/Home/tree/main/Analytics%2C%20Reporting%20%26%20Visualization/Flight_DataViz">Flight Data Visualization Project
</summary>
# Flight Data Visualization Project

## Overview

This project was developed for a hackathon competition (I got second place 😐). It's designed to provide an insightful visualization of flight data using D3.js for interactive graphics and Python for data processing. The focus was on creating an engaging experience that is both informative for engineers and accessible to non-technical users.

To see the project in action, visit [this page](https://takline.github.io/Demos/Analytics,%20Reporting%20&%20Visualization/Flight_DataViz/).

## Features

- **Interactive Flight Data Visualizations**: Utilizes D3.js to present data in an engaging and interactive manner.
- **Data Processing with Python**: Employs Python for efficient and accurate data manipulation and preparation.
- **Comprehensive Analysis**: Offers insights into flight delays, cancellations, and overall travel experiences.

## How It Works

The project is divided into two main components:

1. **Data Processing (Python)**
   - The Python script processes flight data, calculating various metrics like flight counts, travel times, and experience scores.
   - Outputs processed data into a CSV file for use in visualizations.

2. **Visualization (HTML, JavaScript)**
   - HTML and JavaScript with D3.js render the data into interactive charts and graphs.
   - Users can explore different aspects of the data through interactive elements.

## Installation and Setup

1. **Python Environment Setup**
   - Ensure Python >=2.7 is installed.
   - Install required packages: `pandas`.
   - Run the Python script to generate the CSV file.

2. **Web Server Setup**
   - Host the HTML files on a web server.
   - Ensure the CSV file generated by the Python script is accessible to the HTML/JavaScript code.

## Usage

- **For Technical Users**: Run the Python script to process the latest data. Host the HTML files on a server and open them in a web browser.
- **For Non-Technical Users**: Simply navigate to the hosted web page and interact with the visualizations. Hover over elements for detailed info.

## File Structure

- `flights.py`: Python script for processing flight data.
- `index.html`: Main HTML file for the visualization.
- `iframe.html`: Embedded HTML for specific visual components.
- `js/`: JavaScript files, including D3.js for rendering visualizations.
- `css/`: Style sheets for the web interface.

## Contributing

Contributions to enhance this project are welcome. Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature.
3. Commit your changes with clear, descriptive messages.
4. Create a pull request.

## Acknowledgements

I'm grateful for the support of my peers and mentors during the hackathon. Their insights and feedback were invaluable and the competion was a blast.

## Contact

For more information, queries, or suggestions, please reach out to me at [tylerkline@gmail.com].


   </details>
   </details>
<br>
<hr>
<br>
   <details>
     <summary><strong><a href="https://github.com/takline/Home/tree/main/Web%20Scraping%20%26%20Automation">Web Scraping & Automation/</a>:</strong></summary>

   <details>
     <summary><strong><a href="https://github.com/takline/Home/tree/main/Web%20Scraping%20%26%20Automation/web-scraping-with-AI">Web Scraping with AI/</a>:</strong></summary>
     # Web Magic: Unraveling Data from Websites with OpenAI Wizardry

## What's Brewing Here?

Embark on a digital treasure hunt with this code ensemble! It's your magic wand to sift through the web's labyrinth and gracefully extract nuggets of knowledge. We weave together the spells of [OpenAI Functions](https://openai.com/blog/function-calling-and-other-api-updates) and [LangChain](https://python.langchain.com/docs/get_started/introduction) to make this happen. Just sketch out your data map in `schemas.py`, pick your web destination, and let `scrape_with_playwright()` in `main.py` be your guide.

Pro Tip: Web pages are a tapestry of `<p>`, `<span>`, and `<h>` tags. Find the combination that whispers the secrets of your chosen site.

### Example Adventure

1. Craft your digital map in `provide_schema.py`. Whether it's a Pydantic class or a simple dictionary, your wish is our command:

   ```python
   class NewsPortalSchema(BaseModel):
       headline: str
       brief_summary: str
   ```

2. Set sail in `run.py` like this:

   ```python
   asyncio.run(playwright_scrape_and_analyze(
           url="https://www.bbc.com",
           tags=["span"],
           schema_pydantic=NewsPortalSchema
       ))
   ```

## Setting Up Your Magic Kit

### 1. Conjure a Python virtual environment

`python -m venv virtual-env` or `python3 -m venv virtual-env` (Mac)

`py -m venv virtual-env` (Windows 11)

### 2. Awaken your virtual environment

`.\virtual-env\Scripts\activate` (Windows)

`source virtual-env/bin/activate` (Mac)

### 3. Summon dependencies with Poetry's charm

Cast `poetry install --sync` or simply `poetry install`

### 4. Enlist Playwright in your quest

```bash
playwright install
```

### 5. Secretly store your OpenAI API key in a `.env` scroll

```text
OPENAI_API_KEY=XXXXXX
```

## How to Unleash the Magic

### Run it in your own mystical realm

```bash
python run.py
```

## Scrolls of Extra Wisdom

- Transform this into a FastAPI crystal ball to peer into your data through an API gateway.

- Tread the web with the caution of a wise wizard. Only venture where the digital ethics compass allows.

- A little bird told me this wizardry is now part of LangChain's spellbook [in this PR](https://github.com/langchain-ai/langchain/pull/8732). Peek into [the grand library here](https://python.langchain.com/docs/use_cases/web_scraping#quickstart) for more enchantments.

In this enhanced documentation, the instructions are reimagined to be more engaging and less technical, while still providing all the necessary steps to use the code effectively.
   </details>

   <details>
     <summary><strong><a href="https://github.com/takline/Home/tree/main/Web%20Scraping%20%26%20Automation/scrape_sec_13fs">Web Scraping SEC 13Fs/</a>:</strong></summary>
     # Treasury Tales: An Adventure in SEC Data Exploration
Welcome to the magical world of "Treasury Tales"! This enchanting repository houses our Python Web Scraper, a delightful tool for unraveling the mysteries of 13F filings (those intriguing declarations of mutual fund holdings) from the SEC's enchanted forest, known as [EDGAR](https://www.sec.gov/edgar/searchedgar/companysearch.html). Our scraper not only seeks out these filings but also artfully crafts a .tsv file from the gleaned data, like an alchemist turning lead into gold.

## Spellbook Requirements

#### Embarking on Your Journey
- Cast the spell `pip install -r requirements.txt` (or, if you're a wizard of the `pipenv` school, use `pipenv install`) to gather all the magical ingredients.
- Summon the scraper by invoking `python scraper.py` (or, in the lands of `pipenv`, chant `pipenv run python scraper.py`).
- When the oracle speaks, respond with the 10-digit CIK number of the mutual fund you seek to unravel.

#### Potent Potions and Charms

- [Requests](https://2.python-requests.org/en/master/), a mystical Python scroll for conjuring HTTP requests.
- [lxml](https://lxml.de/), a powerful Python tome for parsing the cryptic languages of XML and HTML.
- [Beautiful Soup](https://pypi.org/project/beautifulsoup4/), a sorcerer's Python guide for extracting secrets from the depths of Web pages.
- [re](https://docs.python.org/3/library/re.html), a Python spell for weaving and interpreting the complex tapestry of regular expressions.
- [csv](https://docs.python.org/3/library/csv.html), a Python scroll for decoding and inscribing CSV and TSV scripts.

## Keeper of the Codex
- [Tyler Kline](https://github.com/takline)

## Scrolls of Wisdom
- [SEC: Oracle's Guide to Form 13F](https://www.sec.gov/divisions/investment/13ffaq.htm), a compendium of frequently asked questions and answers, shedding light on the mysteries of Form 13F.

Embark on your journey with "Treasury Tales" and uncover the hidden treasures within the SEC's vast vaults of data. Happy exploring! 🌟📜🔍
   </details>
   </details>
<br>
<hr>
<br>
   <details>
     <summary><strong><a href="https://github.com/takline/Home/tree/main/Blender%20%26%203D%20Python%20Modeling">Blender & 3D Python Modeling</a>:</strong> Showcases some of my pet projects on 3D modelling with Blender's python module.</summary>
   </details>

---
<br>
<br>
