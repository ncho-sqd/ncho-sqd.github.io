---
title: How are people riding Divvy bikes in Chicago on a Monday? (Part 2)
author: nacho
layout: post
---
In [part 1](https://ncho-sqd.github.io/2018/10/28/analyze_divvy_rss_feed_part1.html), we looked at some basic stats for Divvy stations and how the bike counts change over time on **Monday, October 8th, 2018**.

Most notable pattern was a **huge decrease and a sharp spike** in number of bikes parked during commute time (4:00-9:00pm).  A weaker yet interesting pattern was a **pesistent decrease** in bikes parked from morning time leading up to 12:00pm.


![png](/images/2018-12-11-analyze_divvy_rss_feed_part2_files/2018-12-11-analyze_divvy_rss_feed_part2_6_0.png){: .center-image }


Our (yet unexamined) hypothesis for these patterns were as below:
* **Hypothesis 1: Decrease in bike count from morning until 12:00pm is driven by high usage patterns in eastern downtown Chicago stations.**
* **Hypothesis 2: Dip and spike in bike count starting from 4:00pm are caused by commuters going home from downtown Chicago to north and northwest neighborhoods.**<br/><br/>

Here, we will attempt to prove these claims by diving into the more granular patterns in individual bike stations.

<br/>
## Bike count pattern over time by station

In order to understand patterns on individual station-level, let's start by looking at **bike counts for all of the 588 stations over time**.

Each line shows a single station.  Redder lines indicate larger stations and bluer lines smaller stations.  Orange somewhere in between.


![png](/images/2018-12-11-analyze_divvy_rss_feed_part2_files/2018-12-11-analyze_divvy_rss_feed_part2_9_0.png){: .center-image }


Too much going on here, so let's break down this chart into smaller groups of similar station size (colors).


![png](/images/2018-12-11-analyze_divvy_rss_feed_part2_files/2018-12-11-analyze_divvy_rss_feed_part2_11_0.png){: .center-image }



![png](/images/2018-12-11-analyze_divvy_rss_feed_part2_files/2018-12-11-analyze_divvy_rss_feed_part2_11_1.png){: .center-image }



![png](/images/2018-12-11-analyze_divvy_rss_feed_part2_files/2018-12-11-analyze_divvy_rss_feed_part2_11_2.png){: .center-image }



![png](/images/2018-12-11-analyze_divvy_rss_feed_part2_files/2018-12-11-analyze_divvy_rss_feed_part2_11_3.png){: .center-image }



![png](/images/2018-12-11-analyze_divvy_rss_feed_part2_files/2018-12-11-analyze_divvy_rss_feed_part2_11_4.png){: .center-image }



![png](/images/2018-12-11-analyze_divvy_rss_feed_part2_files/2018-12-11-analyze_divvy_rss_feed_part2_11_5.png){: .center-image }


There is still a lot going on for some charts, but we start to see some patterns here.

* Huge decrease and spike in bike count during commute time is **NOT** driven by the largest stations (red line).
* Rather, you somewhat see a **decreasing** pattern for **stations around 30-40 docks** during commute time (light orange, light blue).
* You can also see a strong **increasing** pattern for **stations around 20 docks** during commute time.
* This may indicate that **bikes are moving from 30-40 dock stations to ~20 dock stations during commute time**.
<br/><br/>

We've seen that **larger stations are mostly located in the downtown Chicago area**, so the fact that bikes are moving from relatively larger to smaller stations during commute time seems to suggest that **people may indeed be using Divvy a lot to go home (surrounding neighborhoods) from their workplace (downtown Chicago area) after work**.

<br/>
## How do we know where people are going?

Ultimately, what we are trying to understand is from where to where people are moving with Divvy. The two hypothesis we laid out are essentially a claim on this **flow of people** at different times of the day.

*  This flow can be **"localized"**, meaning that people are moving from different locations to another different enough locations, which may or may not result in weak localized movement patterns throughout the Divvy system.  This kind of pattern, if any, is more difficult to find due to its sporadic and ephemeral nature.
*  The flow can also be **"global"** in a sense that many people follow **similar travel patterns that a strong movement pattern manifests in our data**.  **Patterns noted in our hypotheses are likely an expression of such "global" flows which we are trying to find evidence of**.
<br/><br/>

Let's start out by looking at **system-wide bike flows in Divvy** first.  Below chart shows "net flow" of bikes throughout Divvy, which is basically the difference in bike counts for each timestamp from the previous one. Negative values mean people docked out more bikes than docked in and vice versa for positive values.


![png](/images/2018-12-11-analyze_divvy_rss_feed_part2_files/2018-12-11-analyze_divvy_rss_feed_part2_14_0.png){: .center-image }


Time intervals relevant to our two hypothesis are shaded grey above. We see an overall negative net flow in the earlier period and a negative net flow followed by a strong positive net flow in the later shaded period.

Now, this is an aggregated overall trend we see in the Divvy system.  What if we can decompose **component patterns**, if any, which results in the overall pattern shown above when aggregated?  If we can identify these **"building blocks"** of the overall flow pattern, wouldn't we be able to explain **"component pattern #1 + #2 = overall grey shaded area pattern"**?  We can then trace back stations driving component pattern #1 and #2 and make observations on how they are contributing to the overall pattern.

**It's much like un-building a completed lego to understand the building blocks so that you know exactly how to put them back.**

<br/>
## Developing the building blocks to understand net bike flow

I use a statistical technique called [clustering](https://en.wikipedia.org/wiki/Cluster_analysis) to identify the building blocks of overall net bike flow in Divvy.

In order to identify these building blocks more reliably, I divide the overall bike flow pattern above into consecutive 15-minute intervals and try to identify 10 component patterns in each 15-minute timeframe.  Stations with similar net flow pattern will be grouped together and rolled up to 1 distinct component pattern for each 15-minute interval. All of 588 stations will always belong to one of the 10 component patterns in each 15-minute interval.

If we understand which of the 10 component pattern groups each of the 588 stations belong to for a given 15-minute interval, we can then identify the stations that can explain the overall pattern we see.

Below is a chart showing component patterns based on the station building blocks identified in 15 minute intervals. **You see a good separation of varying degress of positive and negative component patterns identified, when added altogether  will result in overall pattern above.**  Each component pattern for a given 15 minute interval include different sets of stations with similar net flow patterns.


![png](/images/2018-12-11-analyze_divvy_rss_feed_part2_files/2018-12-11-analyze_divvy_rss_feed_part2_18_0.png){: .center-image }


Let's try to see each of the 10 component patterns separately.


![png](/images/2018-12-11-analyze_divvy_rss_feed_part2_files/2018-12-11-analyze_divvy_rss_feed_part2_20_0.png){: .center-image }



![png](/images/2018-12-11-analyze_divvy_rss_feed_part2_files/2018-12-11-analyze_divvy_rss_feed_part2_20_1.png){: .center-image }



![png](/images/2018-12-11-analyze_divvy_rss_feed_part2_files/2018-12-11-analyze_divvy_rss_feed_part2_20_2.png){: .center-image }



![png](/images/2018-12-11-analyze_divvy_rss_feed_part2_files/2018-12-11-analyze_divvy_rss_feed_part2_20_3.png){: .center-image }



![png](/images/2018-12-11-analyze_divvy_rss_feed_part2_files/2018-12-11-analyze_divvy_rss_feed_part2_20_4.png){: .center-image }



![png](/images/2018-12-11-analyze_divvy_rss_feed_part2_files/2018-12-11-analyze_divvy_rss_feed_part2_20_5.png){: .center-image }



![png](/images/2018-12-11-analyze_divvy_rss_feed_part2_files/2018-12-11-analyze_divvy_rss_feed_part2_20_6.png){: .center-image }



![png](/images/2018-12-11-analyze_divvy_rss_feed_part2_files/2018-12-11-analyze_divvy_rss_feed_part2_20_7.png){: .center-image }



![png](/images/2018-12-11-analyze_divvy_rss_feed_part2_files/2018-12-11-analyze_divvy_rss_feed_part2_20_8.png){: .center-image }



![png](/images/2018-12-11-analyze_divvy_rss_feed_part2_files/2018-12-11-analyze_divvy_rss_feed_part2_20_9.png){: .center-image }


Separation of component patterns become more clear when looked independently.  Grey-shaded areas are time intervals relevant to our two hypotheses, with the later period further broken down into negative and positive net flow periods. This results in a total of 3 time intervals to examine.

You can see that the redder component patterns contribute to positive net flow and the bluer component to the opposite.  These two component patterns together build up to the overall net flow pattern, and underlying each component pattern are varying sets of stations in 15 minute intervals.

<br/>
## Zooming into specific timeframes

We will now zoom into the three shaded time intervals in the chart above and start getting into the weeds of identifying which stations are driving the redder or bluer component patterns.

**Stations driving redder patterns will be stations where bikes are docking into.  Stations driving bluer patterns will be stations being docked out of.**  These stations in combination can explain the overall bike flows and means that **there is a flow of people moving from bluer to redder pattern stations**.

Below is a chart that shows different levels of component patterns and the stations driving them during **9:00-12:00pm, time period relevant to hypothesis #1**.

The "Decrease" chart sums up all the bluer (negative net flow) component patterns, with further sub-component broken down into different colors in the "Decrease Sub-Component" chart.  The "Increase" chart does that same for redder (positive net flow) component patterns.

The map shows where the bluer and redder component pattern stations are located for this time period.

**We can see a flow of bikes moving from east to west of downtown Chicago, as bikes should be moving from negative net flow areas (blue) to positive net flow area (red).**

Not sure why people use more bikes in east of downtown Chicago during this time, but it might be the tourists.  I think we've just proven hypothesis #1 though.


![png](/images/2018-12-11-analyze_divvy_rss_feed_part2_files/2018-12-11-analyze_divvy_rss_feed_part2_25_0.png){: .center-image }


<br/>
Moving onto the first part of the hypothesis #2 time interval (negative net flow), we see the same set of charts for **4:00-5:30pm** below.

**At this time, we can see bikes moving from the wider downtown area to the surrounding neighborhoods, more into north and northwestern neighborhoods.**

This seems like the early wave of commuters going back home to neighborhoods that are concentrated along the north and northwestern axes.


![png](/images/2018-12-11-analyze_divvy_rss_feed_part2_files/2018-12-11-analyze_divvy_rss_feed_part2_27_0.png){: .center-image }


<br/>
Let's move on to the last time interval of interest which is the positive net flow period of hypothesis #2, **5:30-9:00pm**.

Here, we see **continuous downtown to surrounding neighborhood movement pattern, but with slower negative flow from downtown and to more stations in the surrounding neighborhoods as can be seen from a wider areas colored in red**.

Seems like people are continuing their way home en masse, which seems to be heavily concentrated in the north and northwestern areas surrounding downtown Chicago.

I think we've proven hypothesis #2 here. Q.E.D.


![png](/images/2018-12-11-analyze_divvy_rss_feed_part2_files/2018-12-11-analyze_divvy_rss_feed_part2_29_0.png){: .center-image }


<br/>
Maybe some of the observations above were obvious, but it surely was interesting for me to verify.

Moreover, I was able to develop a process in which I can de-compose an overall bike flow pattern into smaller bits and attribute them to individual stations.  This means that **this process could be used to potentially reveal more interesting "localized" patterns for those curious-minded**.

I'll drop it here though :)  Thanks a lot for reading!

<br/>
## More

Python script to download json feed from Divvy, click [here](https://github.com/lacolombe-nowifi/etl/blob/dev/scrape_divvy_rss_feed.py).

Jupyter notebook for analysis in this post, click [here](https://github.com/ncho-sqd/ncho-sqd.github.io/blob/master/original_posts/analyze_divvy_rss_feed_part2.ipynb).
