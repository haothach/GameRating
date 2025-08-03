#  Predictive Modeling and Data Analysis for Game Ratings
This project builds a complete pipeline for collecting, cleaning, transforming, and visualizing video game data using the **RAWG API**.

**The end goal of the project is to:**
Build a machine learning model capable of predicting user ratings for video games using data from RAWG.

**The data pipeline utilizes:**
- **RAWG** as the data source  
- **Google Cloud Storage (GCS)** as the data lake  
- **Google BigQuery (GBQ)** as the data warehouse

![Data Pipeline Overview](https://res.cloudinary.com/dnoubiojc/image/upload/v1754229819/Untitled_Diagram.drawio_1_yzyro9.png)

## How to run
**Option 1: Run immediately using preprocessed data**
- Extract `Data.rar` to the root directory  
- Run notebooks in order: `Game_Cleaning.ipynb → Data_Transform.ipynb → Visualize.ipynb`

**Option 2: Crawl and process data from scratch**

**Requirements**:
- A valid **RAWG API key**
- A **Google Cloud service account JSON key file** with access to GCS and BigQuery

**Steps**:

- Run `Crawl_Data` to collect data from RAWG  
- Then run:  
  `clone_raw_data.ipynb → Game_Cleaning.ipynb → clone_processed_data.ipynb → Data_Transform.ipynb → Visualize.ipynb`

## Run the Interactive Dashboard (Streamlit)

![Dashboard Overview](https://res.cloudinary.com/dnoubiojc/image/upload/v1754236310/Screenshot_2025-08-03_225056_yfp44t.png)

To launch the interactive Streamlit dashboard:

1. Open the `gamedashboard/` directory
2. Install required packages:
```
pip install -r requirements.txt
```
3. Run the app:
```
streamlit run app.py
```

##   Contact

If you have any questions or need support, feel free to contact:

**Email:** [haonhut.thach@gmail.com](mailto:haonhut.thach@gmail.com)
