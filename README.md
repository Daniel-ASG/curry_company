# 1. Business problem
The Cury Company is a technology company that created an application that connects restaurants, delivery people, and people.
Through this application, it is possible to order a meal, in any registered restaurant, and have it delivered at the comfort of your home by a delivery person also registered in the Cury Company application.

The company conducts business between restaurants, delivery drivers, and people, and generates a lot of data about deliveries, types of orders, weather conditions, delivery drivers' ratings, etc. Although the delivery is growing, in terms of deliveries, the CEO does not have complete visibility into the company's growth KPIs.

You have been hired as a Data Scientist to create data solutions for delivery, but before you train algorithms, the company's need is to have the key strategic KPIs organized in a single tool, so that the CEO can consult and make simple but important decisions.

The Cury Company has a business model called Marketplace, which intermediates the business between three main customers: Restaurants, deliverers, and buyers. To track the growth of this business, the CEO would like to see the following growth metrics:

### On the company side:
  1. Amount of orders per day.
  2. Amount of orders per week.
  3. Distribution of orders by traffic type.
  4. Comparison of order volume by city and traffic type.
  4. The number of orders per deliverer per week.
  5. The central location of each city by traffic type.
### On the deliveryman side:
  1. The lowest and highest age of the deliverers.
  2. The worst and best condition of vehicles.
  3. The average rating per delivery man.
  4. The average rating and standard deviation by traffic type.
  5. The average rating and standard deviation by weather conditions.
  6. The 10 fastest delivery drivers by city.
  7. The 10 slowest deliverers by city.
### On the restaurant side:
  1. The number of unique deliverers.
  2. The average distance from restaurants and delivery locations.
  3. The average delivery time and standard deviation by city.
  4. The average delivery time and standard deviation by city and order type.
  5. The average delivery time and standard deviation by city and traffic type.
  6. The average delivery time during festivals.

The goal of this project is to create a set of charts and/or tables that display these metrics in the best possible way for the CEO.

# 2. Assumptions made for the analysis
  1. The analysis was performed with data between 11/02/2022 and 06/04/2022.
  2. Marketplace was the business model assumed.
  3. The 3 main business views were: Order transaction view, restaurant view and delivery man view.

# 3. Solution Strategy
The strategy dashboard was developed using the metrics that reflect the 3 main business model views of the company:
  1. Company growth view
  2. View of restaurant growth
  3. Delivery drivers' view of growth

Each vision is represented by the following set of metrics.

1. **Vision of company growth**
    1. Orders per day
    2. Percentage of orders by traffic conditions
    3. Number of requests by type and by city.
    4. Orders by week
    5. Number of orders by delivery type
    6. Order quantity by traffic conditions and city type
2. **View of restaurant growth**
    1. Amount of unique orders.
    2. Average distance traveled.
    3. Average delivery time during festival and normal days.
    4. Standard deviation of delivery time during festival and normal days.
    5. Average delivery time by city.
    6. Distribution of average delivery time by city.
    7. Average delivery time by order type.
3. **Delivery growth view**
    1. Age of the oldest and youngest delivery person.
    2. Assessment of the best and worst vehicle.
    3. Average rating per delivery person.
    4. Average evaluation by traffic conditions.
    5. Average rating by weather conditions.
    6. Average time of the fastest delivery person.
    7. Average time of the fastest delivery person by city.

# 4. Top 3 Data Insights
1. The seasonality of the number of orders is daily. There is approximately a 10% variation in the number of orders on sequential days.
2. Semi-Urban type cities do not have low traffic conditions.
3. The biggest variations in delivery time, happen during sunny weather.

# 5. the final product of the project
Online dashboard, hosted in a Cloud and available for access from any internet connected device.
To access the final result, please go to the [Streamlit dashboard link](https://daniel-asg-curry-company.streamlit.app/).

# 6. Conclusion
The goal of this project was to create a set of charts and/or tables that display these metrics in the best possible way for the CEO.
From the Company's view, we can conclude that the number of orders grew between week 06 and week 13 of the year 2022.

# 7. next steps
1. Reduce the number of metrics.
2. Create new filters.
3. Add new business views.
4. Develop Machine Learning Models that can help the company improve its performance.
