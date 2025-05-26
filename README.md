# DSI321_2025_BT_Materials: Real-Time News Analysis on Sustainable Construction Materials
This project focuses on real-time news analysis of sustainable construction materials by continuously scraping the latest news articles from Google News RSS.
## Project Overview ##
This project is designed to collect and visualize real-time news related to sustainable or alternative construction materials. It combines data engineering tools and interactive visualization to create a complete pipeline — from data ingestion to analysis. The goal is to provide insights into trending topics and frequently mentioned terms in the sustainable construction industry.

## Project Evaluation Overview ##
This project has been developed in alignment with the key assessment criteria outlined for DSI321, with optional components supporting DSI324 objectives. The following aspects demonstrate compliance with the required standards:

-   Repository Setup: The repository was initialized within the first week of the project timeline and named precisely as required: dsi321.

-   Commit Activity: Version control has been maintained with over 15 meaningful commits made across at least three consecutive weeks, reflecting continuous development and refinement.

-   Data Collection Workflow: A news scraping pipeline is implemented using Prefect 2.0 to automatically fetch news headlines and metadata related to alternative construction materials. The job is scheduled to run every 15 minutes, ensuring real-time updates.

-   Dataset Volume & Coverage: Over 1,000 news records are collected, spanning a complete 24-hour period, thus satisfying both quantity and temporal coverage requirements.

-   Data Schema & Integrity: 
    - The schema is consistently structured, with clearly defined fields such as title, summary, published_date, source, and url.
        
    - All data types are appropriate—no use of generic object types.

    - The dataset contains no duplicate records, and schema validation confirms over 90% data completeness.

-   Documentation Quality:

    - The README.md file is thorough and exceeds 1,000 characters.

    - It includes a project summary, instructions for use, architectural components, tools employed (e.g., Prefect, lakeFS, Streamlit), and potential applications.

-   Interactive Visualization:

    - A Streamlit dashboard is integrated to visualize collected data.

    - It includes a dynamic Word Cloud that showcases the most commonly occurring keywords, providing insight into trending topics in sustainable construction.

-   (Optional – DSI324): For extended analysis, the project can incorporate a basic machine learning model (e.g., Linear Regression) to explore patterns or frequency shifts over time, aligning with core learning outcomes of DSI324.
    
## Benefits of This Project ##
This project offers practical and educational value across several dimensions, supporting both real-world applications and academic objectives:

-   Hands-On Experience with Data Pipelines: By implementing an automated news scraping pipeline using Prefect 2.0, the project provides direct experience with workflow orchestration, task scheduling, and pipeline monitoring.

-   Real-Time Data Collection & Processing: The system captures live data from Google News RSS feeds, allowing students and researchers to work with continuously updating, real-world datasets related to sustainable construction.

-   Structured and Versioned Data Storage: Leveraging lakeFS for Parquet file storage enables data versioning, reproducibility, and traceability—key principles in modern data engineering and data lake design.

-   Visual Insight Through Interactive Dashboard: The integration with Streamlit enhances accessibility to insights by visualizing frequent topics through Word Clouds, helping users quickly grasp emerging trends in green building materials.

-   Scalable Foundation for Further Analysis: The clean and validated dataset, along with the modular architecture, makes it easy to expand the project by adding advanced analytics, NLP techniques, or predictive models.

-   Supports Interdisciplinary Learning: The project bridges multiple skill areas, including web scraping, data cleaning, cloud storage, data visualization, and machine learning—making it ideal for students in both DSI321 and DSI324.

-   Environmental Relevance: By focusing on sustainable construction materials, this project contributes to awareness and analysis of environmentally friendly innovations, aligning with broader goals in sustainability and green technology.

## Automation & Efficiency

**Automated Scheduling**: The data pipeline is configured to run automatically every 15 minutes using **Prefect 2.0**, ensuring consistent and up-to-date data collection without manual intervention.

**Efficient Storage & Version Control**: All collected data is stored in **lakeFS** as partitioned Parquet files. This enables:
- Easy retrieval of historical data
- Full version control over datasets
- Reproducibility of results and experiments

This automation ensures high reliability and minimizes the risk of data loss while improving productivity and consistency in the workflow.

## Technologies & Components Overview
This project leverages a set of modern technologies and components to build an end-to-end, automated, and interactive data pipeline:

-   Web Scraping: Utilizes feedparser to collect news directly from Google News RSS feeds — a lightweight and efficient approach that eliminates the need for login credentials or browser automation tools like Selenium.

-   Data Processing: Employs pandas to clean, transform, and structure the scraped data into a consistent format ready for storage and analysis.

-   Data Storage: Stores processed data as Parquet files in lakeFS, a version-controlled, S3-compatible object storage system. Data is partitioned by year, month, and day to support efficient querying and data lineage tracking.

-   Workflow Orchestration: Uses Prefect 2.0 to manage and schedule scraping tasks. The pipeline is set to execute automatically every 15 minutes, supporting near real-time data updates.

-   Visualization: A Streamlit web app is used to visualize results. Combined with matplotlib and the WordCloud library, it presents the most frequently discussed keywords from the collected news.

-   Text Cleaning: Integrates Python’s built-in re and string modules, along with nltk.stopwords, to clean and normalize news headlines before visualization and analysis.

-   Environment Management: The project environment is containerized with Docker Compose, enabling seamless coordination of multiple services including Prefect Server, lakeFS, PostgreSQL, CLI tools, and scraping workers.

-   Version Control & Deployment: All code and pipeline configurations are maintained in Git and hosted on GitHub. Users can manually deploy or use CLI commands to register and manage flows.

## Prepare & Run 

1. **Create and activate a virtual environment**

    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate 
2. **Start Docker Services (Prefect + lakeFS + Database)**

    ```bash
    docker compose --profile server up -d     # Start Prefect server & database
    docker compose --profile worker up -d     # Start Prefect worker
    docker compose --profile cli run cli      # (Optional) Get a shell in CLI container
3. **Deploy or run the scraping flow**: To deploy the Prefect flow that runs every 15 minutes:
    ```bash
    python main_2.py
4. **Launch the Streamlit dashboard**
    ```bash
    streamlit run dashboard.py
5. **View Prefect UI**: Open your browser and go to **http://localhost:4200** (or just localhost) to monitor scheduled runs and logs.
## Conclusion ##
This project showcases a full-stack data pipeline and dashboard application, using cutting-edge tools for real-time data collection, storage, and analysis. It offers an efficient way to monitor sustainability trends in the construction industry, and demonstrates the practical integration of Prefect, lakeFS, and Streamlit in a modern data workflow.
## Author
"Patcharada Chuachai 6524651293"

