def toMap(result):
        new_data = {
            "marketIntent":{
                "marketType":result['marketIntent'].marketType,
                "description": result["marketIntent"].description,
                "product": result["marketIntent"].product,
                "inhancedUserMessage": result["marketIntent"].inhancedUserMessage
            },
            'competitorCompanies':[company.name for company in result['competitorCompanies'].competitorCompanies],
            "companiesDetails":[{
                
                    "overall_advantages":company.overall_advantages,
                    "overal_weaknesses":company.overal_weaknesses,
                    "products":[
                        {
                        "name":product.name,
                        "advantages":product.advantages,
                        "weaknesses":product.weaknesses
                        } for product in company.products]
                
                } for company in result['companiesDetails']
                ],
            "finalAnswer":{
                    "gapInMarket":result['finalAnswer'].gapInMarket,
                    "recommendations":result['finalAnswer'].recommendations
            }
        }
        return new_data
