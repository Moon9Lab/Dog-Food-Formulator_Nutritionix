# FoodData Central

https://fdc.nal.usda.gov/api-guide.html

## Overview

The FoodData Central API provides [REST](http://en.wikipedia.org/wiki/Representational_state_transfer) access to FoodData Central (FDC). It is intended primarily to assist application developers wishing to incorporate nutrient data into their applications or websites.

To take full advantage of the API, developers should familiarize themselves with the database by reading the database documentation available via links on [Data Type Documentation](https://fdc.nal.usda.gov/data-documentation.html). This documentation provides the detailed definitions and descriptions needed to understand the data elements referenced in the API documentation.

**Note:** The API that was available on the USDA Food Composition Databases Web site is no longer being updated and will be discontinued March 31, 2020. Users are encouraged to begin working with the new FoodData Central API system described on this page. This new API allows users to obtain Standard Reference (SR) Legacy data, provides the most current data from the USDA Global Branded Foods Database, and give users the ability to search for specific foods in Foundation Foods and the Food and Nutrient Database for Dietary Studies (FNDDS) 2019-2020.

## What's Available

The API provides two endpoints: the Food Search endpoint, which returns foods that match desired search criteria, and the Food Details endpoint, which returns details on a particular food.

## Gaining Access

Anyone may access and use the API. However, a data.gov API key must be incorporated into each API request. [Sign up to obtain a key](https://fdc.nal.usda.gov/api-key-signup.html), then follow the [instructions for how to use your key](https://api.data.gov/docs/api-key/).

## Rate Limits

FoodData Central currently limits the number of API requests to a default rate of 1,000 requests per hour per IP address, as this is adequate for most applications. Exceeding this limit will cause the API key to be temporarily blocked for 1 hour. More detailed information on rate limits may be found at https://api.data.gov/docs/rate-limits. [Contact FoodData Central](https://fdc.nal.usda.gov/contact.html) if a higher request rate setting is needed.

## Licensing

USDA food composition data are in the public domain and they are not copyrighted. No permission is needed for their use. USDA would appreciate it if developers would list FoodData Central as the source of the data. And, when possible, USDA would like to see the product that uses the data or be notified of their use. The suggested citation is:

U.S. Department of Agriculture, Agricultural Research Service. FoodData Central, 2019. [fdc.nal.usda.gov](https://fdc.nal.usda.gov/).

Note: Release numbers and years change as new versions are released. For more information, please see [Download Data](https://fdc.nal.usda.gov/download-datasets.html).

## API Endpoints

| URL | Verb | Purpose |
| --- | --- | --- |
| /food/{fdcId} | https://app.swaggerhub.com/apis/fdcnal/food-data_central_api/1.0.1#/FDC/getFood | Fetches details for one food item by FDC ID |
| /foods | https://app.swaggerhub.com/apis/fdcnal/food-data_central_api/1.0.1#/FDC/getFoods | https://app.swaggerhub.com/apis/fdcnal/food-data_central_api/1.0.1#/FDC/postFoods | Fetches details for multiple food items using input FDC IDs |
| /foods/list | https://app.swaggerhub.com/apis/fdcnal/food-data_central_api/1.0.1#/FDC/getFoodsList | https://app.swaggerhub.com/apis/fdcnal/food-data_central_api/1.0.1#/FDC/postFoodsList | Returns a paged list of foods, in the 'abridged' format |
| /foods/search | https://app.swaggerhub.com/apis/fdcnal/food-data_central_api/1.0.1#/FDC/getFoodsSearch | https://app.swaggerhub.com/apis/fdcnal/food-data_central_api/1.0.1#/FDC/postFoodsSearch | Returns a list of foods that matched search (query) keywords |

## Sample Calls

**Note:** These calls use DEMO_KEY for the API key, which can be used for initially exploring the API prior to signing up, but has much lower rate limits. See [here](https://api.data.gov/docs/rate-limits) for more info on uses and limitations of DEMO_KEY.

### GET REQUEST:

`curl https://api.nal.usda.gov/fdc/v1/food/######?api_key=DEMO_KEY`

The number (######) in the above sample must be a valid FoodData Central ID.

`curl https://api.nal.usda.gov/fdc/v1/foods/list?api_key=DEMO_KEY`  `curl https://api.nal.usda.gov/fdc/v1/foods/search?api_key=DEMO_KEY&query=Cheddar%20Cheese`

### POST REQUEST:

`curl -XPOST -H "Content-Type:application/json" -d '{"pageSize":25}' https://api.nal.usda.gov/fdc/v1/foods/list?api_key=DEMO_KEY`  `curl -XPOST -H "Content-Type:application/json" -d '{"query":"Cheddar cheese"}' https://api.nal.usda.gov/fdc/v1/foods/search?api_key=DEMO_KEY`  `curl -XPOST -H "Content-Type:application/json" -d "{\"query\":\"Cheddar cheese\"}" https://api.nal.usda.gov/fdc/v1/foods/search?api_key=DEMO_KEY`

Note: If using curl on Windows, the body of the POST request (-d option) is enclosed in double quotes (as shown in the above sample).

`curl -XPOST -H "Content-Type:application/json" -d '{"query": "Cheddar cheese", "dataType": ["Branded"], "sortBy": "fdcId", "sortOrder": "desc"}'`  `https://api.nal.usda.gov/fdc/v1/foods/search?api_key=DEMO_KEY`

Note: The "dataType" parameter values need to be specified as an array.

## API Spec

The OpenAPI v3 spec for the API provides a complete specification of the API endpoints, including input parameters and output data. It is available in [HTML](https://fdc.nal.usda.gov/api-spec/fdc_api.html), [JSON](https://api.nal.usda.gov/fdc/v1/json-spec?api_key=DEMO_KEY), or [YAML](https://api.nal.usda.gov/fdc/v1/yaml-spec?api_key=DEMO_KEY) formats.

### The spec is also available on SwaggerHub at:

https://app.swaggerhub.com/apis/fdcnal/food-data_central_api/1.0.1

