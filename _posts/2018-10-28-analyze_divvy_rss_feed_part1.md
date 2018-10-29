---
title: How are people riding Divvy bikes in Chicago on a Monday? (Part 1)
author: nacho
layout: post
---
[Divvy](https://www.divvybikes.com/) is Chicago's bike share program which works the same way as NYC's [Citi Bike](https://www.citibikenyc.com/) and Washington DC's [Capital Bikeshare](https://www.capitalbikeshare.com/).  You undock a bike from a station, ride it for 30 minutes until you dock it back into any station, with a fee.

It's a great way to get from point A to B, but I usually ride them during summertime along Lake Michigan, which is absolutely ***GLORIOUS***.  Below is a picture I took when me and my friends went on for a ride.




![jpeg](/images/2018-10-28-analyze_divvy_rss_feed_part1_files/2018-10-28-analyze_divvy_rss_feed_part1_3_0.jpeg){: .center-image height="600px"}



Divvy exposes a [JSON feed](https://feeds.divvybikes.com/stations/stations.json) online, which seems to update every few seconds on how many bikes are available in all the stations in real time.  This seemed like interesting data, so I collected for ~24 hours starting from Monday, October 8th, 2018 and started peaking in for any interesting patterns.

<br/>
## How large are the stations, and where are the largest stations?<br/>

There are **588 stations** that are operational as of October 8th, 2018 and the **median dock count is 15**(station size).  If you're Divvy station has more than 15 docks, now you know that you're at a relatively larger station or not.

Also, histrogram of station dock counts below shows that the majority of the stations are smaller than 20 docks.  Specifically, **~80% (470) of stations have fewer than 20 docks**.


![png](/images/2018-10-28-analyze_divvy_rss_feed_part1_files/2018-10-28-analyze_divvy_rss_feed_part1_8_0.png){: .center-image }


Moving onto the bigger stations, there are exactly 10 stations that has more than 40 docks as below.  The largest stations have 55 docks and there are 3 stations with this many docks available.




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>station name</th>
      <th>total docks</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Columbus Dr &amp; Randolph St</td>
      <td>55.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Shedd Aquarium</td>
      <td>55.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Field Museum</td>
      <td>55.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Canal St &amp; Adams St</td>
      <td>47.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Ravenswood Ave &amp; Lawrence Ave</td>
      <td>47.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Streeter Dr &amp; Grand Ave</td>
      <td>47.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Millennium Park</td>
      <td>47.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Michigan Ave &amp; Washington St</td>
      <td>43.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Larrabee St &amp; Kingsbury St</td>
      <td>43.0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Michigan Ave &amp; 8th St</td>
      <td>42.0</td>
    </tr>
  </tbody>
</table>
</div>



As expected, most of these stations are located in the downtown Chicago area, except for the [Ravenswood Ave & Lawrence](https://www.google.com/maps/place/Divvy+Station:+Ravenswood+Ave+%26+Lawrence+Ave/@41.9690647,-87.6741959,3a,75y,260.11h,90t/data=!3m7!1e1!3m5!1sNJ47KNZ-sIN2KJHE8rpdSw!2e0!6s%2F%2Fgeo3.ggpht.com%2Fcbk%3Fpanoid%3DNJ47KNZ-sIN2KJHE8rpdSw%26output%3Dthumbnail%26cb_client%3Dsearch.TACTILE.gps%26thumb%3D2%26w%3D234%26h%3D106%26yaw%3D260.11026%26pitch%3D0%26thumbfov%3D100!7i13312!8i6656!4m8!1m2!2m1!1sdivvy+Ravenswood+Ave+%26+Lawrence!3m4!1s0x880fd223bd912f4f:0x491bfb46039d36dd!8m2!3d41.9690567!4d-87.674241) Ave and [Larrabee St & Kingsbury St](https://www.google.com/maps/place/N+Kingsbury+St+%26+N+Larrabee+St,+Chicago,+IL+60610/@41.8977745,-87.6429428,3a,75y,187.5h,90t/data=!3m7!1e1!3m5!1syF7jeG18zexd9_SrVc-dLg!2e0!6s%2F%2Fgeo3.ggpht.com%2Fcbk%3Fpanoid%3DyF7jeG18zexd9_SrVc-dLg%26output%3Dthumbnail%26cb_client%3Dsearch.TACTILE.gps%26thumb%3D2%26w%3D86%26h%3D86%26yaw%3D187.4999%26pitch%3D0%26thumbfov%3D100!7i16384!8i8192!4m5!3m4!1s0x880fd3348132faf9:0x8bc5db7cbbbbc56e!8m2!3d41.897778!4d-87.6430376) station.  

The Ravenswood station features a double-sided docking design and the Larrabee station seems to be next by the Groupon HQ based on Google Street View images.  Not sure why there are huge stations there, but these might be locations with high foot-traffic outside of downtown Chicago.  Might be worth checking out once Chicago turns warmer.

<br/>
## Where are the bikes parked throughout Monday?

Below is an animated **heatmap of where bikes are parked in 10 minute intervals**.  This might reveal some interesting travel patterns that show how people are using Divvy bikes.  Each circle is a station, where red indicates more bikes parked and ligher yellow indicates fewer bikes.  Also, larger circles indicate bigger stations with more docking spots.

![gif](/images/2018-10-28-analyze_divvy_rss_feed_part1_files/divvy_heatmap.gif){: .center-image }

There are a few patterns we can observe:

  - The day starts off with a lot of bikes (red) parked in the downtown Chicago area.
  - The heat (red) starts to clear out a little from the eastern side of downtown Chicago since start of day.
  - More heat (red) clears out of downtown Chicago to north and northwest neighborhoods starting from 4:00pm.

All in all, people seem to use Divvy (decrease in red) actively in the eastern part of downtown Chicago staring from earlier in the day, followed by a lot of bikes in downtown Chicago flushing out to north and northwest neighborhoods around commute time.

<br/>
## Trends in total bikes available in Divvy 
Below is a chart that sums up the activity observed in the heatmap above across all stations in the Divvy system.  More specifically, the total number of bikes parked in all stations are shown over time.

The reason for two lines corresponding to min/max is because a station could report different numbers of bikes parked in a 1 second interval (least time measurement unit for Divvy) when there is high activity.  Grey area shows the difference of the min/max lines, which could tell us how actively bikes docked and undocked in single stations (single-station busyness).


![png](/images/2018-10-28-analyze_divvy_rss_feed_part1_files/2018-10-28-analyze_divvy_rss_feed_part1_21_0.png){: .center-image }


Consistent with what we observed from the heatmap, we see the number of bikes available decrease from start of day until  12:00pm (both the min/max lines).  This drawdown might be driven by the heat clearing out from the eastern part of downtown Chicago in the heatmap.

After this comes a drastic dip in bike count from 4:00pm, followed by a spike up until 8:00pm.  I'm pretty sure that this pattern is driven by the heat flushing out of downtown Chicago and spreading to north and northwest neighborhoods in the heatmap.

Single station busyness (grey area) spikes up when the number of bikes dip down to minimum shortly after 5:00pm, meaning that this is an extremely busy time, where people are not only using Divvy bikes a lot, but also docking and undocking very frequently.

We've seen a few charts, and have a few hypothesis for the patterns that we see in them so far:
- **Hypothesis 1: Decrease in bike count from morning until 12:00pm is driven by high usage patterns in eastern downtown Chicago stations.**
- **Hypothesis 2: Dip and spike in bike count starting from 4:00pm are caused by commuters going home from downtown Chicago to north and northwest neighborhoods.**

<br/>
In part 2, I'll start looking into station level patterns that are driving the overall trend in the chart above to verify the hypotheses I established and dig out other interesting patterns.

Hope you enjoyed reading and stay tuned to see if my guesses are correct :)

<br/>
## More

Python script to download json feed from Divvy, click [here](https://github.com/lacolombe-nowifi/etl/blob/dev/scrape_divvy_rss_feed.py).

Jupyter notebook for analysis in this post, click [here](https://github.com/ncho-sqd/ncho-sqd.github.io/blob/master/original_posts/analyze_divvy_rss_feed_part1.ipynb).
