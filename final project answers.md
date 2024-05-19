 ------------key objectives--------------
 1. Read in data from multiple csv files
 2. Explore the data(millions of rows!)
 3. join multiple Dataframes
 4. create new columns to aid in analysis
 5. Filter, sort and aggregate the data to pinpoint and summarize important information
 6. Work with datetime fields to analyze the time series
 7. Build ploys to communicate key insights
 8. Optimize the import workflow
 9. Write out summary tables for stakeholders

- Task 1
	- read in the transactions data
	- read in the only columns ``household key``,``basket_id``,``day``,``product_id``,``quantity``,and``sales_value``.
	- convert ``day``,``quantity`` and ``product_id`` to the smallest appropriate integer types

- Task 2(TIME BASED ANALYSIS)
	- plot the sum of sales by month, are sales growing over time?
	- next, plot the same series after filtering down to the dates April 2016 and October 2017
	- then, plot the sum of monthly sales in 2016 vs the monthly sales 2017,
	- finally, plot total sales by the day of the week

- Task 3(DEMOGRAPHICS)
	- Read in the ``hh_demographic.csv`` file, but only the columns ``age_desc``,``income_desc``,``household_key``,and ``ee_comp_desc``.Convert the appropriate columns to the category dtype.
	- then group the transactions table by ``household_id`` and calculate the sum of ``sales_value`` by household
	- once you've done that, join the demographics dataframe to the aggregated transactions table. Since we're interested in analyzing the demographic data we have, make sure not to include rows for transactions that don't match.
	- plot the sum of sales by ``age_desc`` and ``income_desc``(in separate charts).
	- then, create the pivot table of the mean households sales by ``age_desc`` and ``ee_comp_desc``. Which of our demographics have the highest average sales? 

- Task 3(PRODUCT DEMOGRAPHICS)
	- read in the ``product.csv file``
	- only read in ``product_id`` and department from product(consider converting columns)
	- Join the product dataframe  to transactions and demographics tables, performing an inner join when joining both tables.
	- finally, pivot the fully joined dataframe by ``age_desc`` and ``department``,calculating the sum of sales. Which category does our youngest demographic perform well in.
	- export to excel file or csv file