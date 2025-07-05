#Project structure 

art-culture-insights-app/
│
├── .gitignore
├── README.md
├── requirements.txt
├── streamlit_app.py
│
├── data/
│   └── raw/ (has 4 .csv files 1. fee-from-tourism2019-21.csv, Foreign-exchange-earning2014-20.csv,internation-tourism2001-21.csv, state-wise-finance-artcluture-2019-24.csv)             
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


TABLES FINAL
1. tourism_fee
2. tourism_fee_clean
3. tourism_fee_final (final table)
4. foreign_exchange_earnings_year_wise
5. international_tourism_stats
6. international_tourism_stats_clean
7. tourism_growth_trends
8. india_share_trend
9. state_cultural_funding
10. state_cultural_funding_clean
11. dim_states
12. funding_by_state
13. funding_by_year
14. funding_by_agency
