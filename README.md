# holiday_planner




                                                                                                       
Country "latitude":,	"longitude":     airport 
  Bali        22.6486         88.3411           DPS
  Singapore   1.3521          103.8198          SIN
  Thailand    15.8700         100.9925          BKK
  Vietnam     14.0583         108.2772          SGN
  Philippines  12.8797        121.7740          MNL




  
data = {
    "Country": ["Bali", "Singapore", "Thailand", "Vietnam", "Philippines"],
    "Latitude": [22.6486, 1.3521, 15.8700, 14.0583, 12.8797],
    "Longitude": [88.3411, 103.8198, 100.9925, 108.2772, 121.7740],
    "Airport": ["DPS", "SIN", "BKK", "SGN", "MNL"]
}

df = pd.DataFrame(data)
print(df)
