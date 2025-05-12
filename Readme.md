#Project structure 

art-culture-insights-app/
│
├── .gitignore
├── README.md
├── requirements.txt
├── streamlit_app.py
│
├── data/
│   └── raw/              
│   └── processed/        
│
├── snowflake/
│   └── schema.sql        
│   └── views.sql         
│   └── connection.py     
│
├── utils/
│   └── data_loader.py   
│   └── preprocess.py     
│
└── pages/              
    └── home.py
    └── trends.py
    └── map.py
