import requests
import json


query ="""query {
    searchByAddress(                
        source: "pricelists",
        address: {city: "Beroun"},
        filters: {type: [FLAT]},
        size: 48,
        currency: CZK
    ) {  
	  count
      percentage
      bbox {topLeft {lat, lon}, bottomRight {lat, lon}}
      avgPrice
      priceRange {min, max, currency}
      priceHist {low, high, currency, count}
      avgPricePerM2
      pricePerM2Range {min, max, currency}
      pricePerM2Hist {low, high, currency, count}
      currency
      typeHist {value, count}
      offerTypeHist {value, count}
      energyClassHist {value, count}
      constructionHist {value, count}
      conditionHist {value, count}
      ownershipHist {value, count}
      floorRange {min, max}
      dispositionHist {value, count}
      roomCountHist {value, count}
      avgArea
      areaRange {min, max}
      floorAreaRange {min, max}
      usableAreaRange {min, max}
      livingAreaRange {min, max}
      totalAreaRange {min, max}
      projectCount
      developerCount
	  projects {name
          developer
          gps {lat, lon}
          count
          availableCount
          price {min, max, currency}
          pricePerM2 {min, max, currency}
          area {min, max}
          floorArea {min, max}
          usableArea {min, max}
          livingArea {min, max}
          totalArea {min, max}
          disposition
          roomCount
          ppc}
      estates {
          source
          id
          ppc
          state
          description
          detailUrl
          imageUrls
          thumbnailUrl
          type
          offerType
          condition
          developer
          project
          number
          ownership
          energyClass
          locality
          disposition
          roomCount
          area
          areaType
          floorArea
          usableArea
          livingArea
          totalArea
          floor
          gps {lat, lon}
          address {address, country, region, district, city, borough, neighborhood, street, houseNumber}
          price
          priceType
          currency
          balconyArea
          loggiaArea
          terraceArea
          gardenArea
          cellar
          parking
        }
    }
}
"""

#file = open("r.csv", "r")
url = 'https://api.flatzone.cz/graphql'
r = requests.post(url, json={'query': query})
#print(r.text)
content = json.loads(r.text)
#print(content["data"]["searchByAddress"]["estates"])
#print(content["data"]["searchByAddress"].keys())


interesting = ["priceHist", "pricePerM2Hist", "dispositionHist", "roomCountHist", "projects", "estates"]


for i in interesting:
    name = i + ".csv"
    file = open(name,"w")
    
    columns = ""
    for j in content["data"]["searchByAddress"][i][0]: # j dict
        columns = columns + j + ","

    columns = columns.rstrip(",")
    columns = columns + "\n"
    file.write(columns)
        
    
    for l in content["data"]["searchByAddress"][i]:
        values = ""
        for m in l:
            bunka = str(l[m])
            bunka = bunka.replace(",","|")
            values = values + bunka + ","

        values = values.rstrip(",")
        values = values + "\n"

        file.write(values)
    
    file.close()
