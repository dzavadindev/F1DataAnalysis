# Explanation

This pages aims to answer the question: "**Which constructors can still win the world championship at the moment in the last racing season for which we have data?**".  

I have noticed that within the dataset, there is contradictory data, like for example a constructors team being to score 66 points for one race. I think this is because there are things like fastest lap (for drivers) which gives you bonus points. But, for the sake of simplicity I purely assumed that maximum points in a race is what you can get for scoring first place every time. 

``` sql all_predictions
  select * from reports.predictions
```

Select the year you want to see the info for:
<Dropdown
    name=filter_year
    data={all_predictions}
    value=year
/>

``` sql selected_year_predictions
  select * from reports.predictions where year = '${input.filter_year.value}'
```

# Visualization

## Potential of constructors

To start up, we have made a general analysis of the possibilities, it being "if from this point on the team gets the first place in every race, what score would they have?". This shows what is possible to score throughout the entirety of the Championship, top 3 contenders being the teams that are likely to still win the Championship according to the latest data we have available.

<DataTable data={selected_year_predictions}> 
  <Column id=team title="Teams"/> 
	<Column id=potential_points title="Potential points"/> 
</DataTable>

## Predicted points for 2023

Then, to try predict the final scoreboard of 2023 season, we have taken the average of points every team scored so far, and stretched that through the remaining races. This gives a relative placement on the scoreboard, where 575 is the prediction for highest placement (as 575 is the absolute maximum amount of points possible to score, as 23 races * by 25 points for first place as for 2023)

<BarChart 
    data={selected_year_predictions}
    x=team
    y=predicted_points
    title="Estimated scores by the end of the season"
/>

Referring to the data presented, its possible to determine the constructor teams that are still have the possibility to win and even see predictions for possible final scores (given the predictions will get better the further the championship progresses) 