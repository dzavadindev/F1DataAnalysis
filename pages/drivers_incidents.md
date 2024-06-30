# Explanation

This pages aims to answer the question: "**How often has each driver been involved in an incident in the past racing year according to race control?**". We will use drivers information and the race control logs to determine the number of crashes a driver was involved throughout the 2023 racing season. 

``` sql all_incidents
  select * from reports.incidents
```
Select the year you want to see the info for:
<Dropdown
    name=filter_year
    data={all_incidents}
    value=year
/>

``` sql selected_year_incidents
  select * from reports.incidents where year = '${inputs.filter_year.value}'
```

# Visualization

Firstly, the number of incidents to driver will be presented as a bar chart, showcasing how every one driver compares to another.

<BarChart 
    data={selected_year_incidents}
    x=full_name
    y=total_incidents
    swapXY=true
    title="Difference in incident rate for drivers (2023)"
/>

For a more clear view of the statistics, refer to this data table

<DataTable data={selected_year_incidents}> 
  <Column id=full_name title="Driver"/> 
  <Column id=team title="Team"/> 
	<Column id=total_incidents title="Number of Incidents"/> 
</DataTable>

Referring to the data presented, its possible to determine who from the F1 roster has been involved in the most incidents, and how they compare to other drivers   