---
title: How I got my Gmail inbox count down by 50% using Python
author: nacho
layout: post
---
My Gmail inbox was counting close to **30,000**.  Not a pretty number at all, so I decided I should do something about it.

Just like a good data analyst would do, I wanted to clean up my inbox in a **_systematic and data-driven_** manner.

I wanted something easy, quick, and high payoff, not something like a full-blown spam classification algorithm using Natural Language Processing, although that'd be fun as well.  So I settled on a **50% rule**, where I'll get rid of at least 50% of unnecessary emails.

You'd be surprise to learn that the [pareto principle](https://en.wikipedia.org/wiki/Pareto_principle) of 20% of causes explaining 80% of the effect also holds in my Gmail inbox.  12% of senders accounted for 80% of all emails in my case and **only 18 senders accounted for approximately 50% of all my emails!**


![png](/images/2018-10-15-clean_email_inbox_files/2018-10-15-clean_email_inbox_6_0.png){: .center-image }


Here you can see, how concentrated my inbox is with regards to unique senders.  There's a steep curve up until the 200th unique sender, meaning that there are at least 200 email senders that contribute most to my cluttered inbox.  The red dotted horizontal line indicates 50% of my total mail count to give a sense of how quickly the curve reaches that point.

Good to know, but I'm not going to review the top 200 senders because that's already too many.  Instead, I'm going focus on the dotted square portion of the distribution for now.


![png](/images/2018-10-15-clean_email_inbox_files/2018-10-15-clean_email_inbox_8_0.png){: .center-image }


Zooming into the dotted square portion of the chart above, we can see that **50% of all my emails (~15,000) are from the top 18 most frequent senders**.  Now that's a number that I can manage to review.  Blue bars show the number of emails sent by each unique sender and the grey bars show cumulative numbers of those.

I wonder who the most frequent sender is (first blue bar) as it has sent a whopping 5,000 emails to me so far.  Next up (second blue bar) is equally as persistent at around 2,000 emails.  Wonder who that is as well...




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
    <tr style="text-align: left;">
      <th></th>
      <th>name</th>
      <th>organization</th>
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>newtech-1</td>
      <td>meetup.com</td>
      <td>5559</td>
    </tr>
    <tr>
      <th>2</th>
      <td>info</td>
      <td>meetup.com</td>
      <td>2354</td>
    </tr>
    <tr>
      <th>3</th>
      <td>hello</td>
      <td>mealpal.com</td>
      <td>902</td>
    </tr>
    <tr>
      <th>4</th>
      <td>support</td>
      <td>streeteasy.com</td>
      <td>523</td>
    </tr>
    <tr>
      <th>5</th>
      <td>usmail</td>
      <td>expediamail.com</td>
      <td>371</td>
    </tr>
    <tr>
      <th>6</th>
      <td>notify</td>
      <td>buildinglink.com</td>
      <td>361</td>
    </tr>
    <tr>
      <th>7</th>
      <td>travelocity</td>
      <td>ac.travelocity.com</td>
      <td>354</td>
    </tr>
    <tr>
      <th>8</th>
      <td>alert</td>
      <td>indeed.com</td>
      <td>335</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Top-Free-Events-Today-announce</td>
      <td>meetup.com</td>
      <td>323</td>
    </tr>
    <tr>
      <th>10</th>
      <td>godiva</td>
      <td>e.godiva.com</td>
      <td>318</td>
    </tr>
    <tr>
      <th>11</th>
      <td>email</td>
      <td>usa.uniqlo.com</td>
      <td>302</td>
    </tr>
    <tr>
      <th>12</th>
      <td>XXX</td>
      <td>uchicago.edu</td>
      <td>299</td>
    </tr>
    <tr>
      <th>13</th>
      <td>groups-noreply</td>
      <td>linkedin.com</td>
      <td>288</td>
    </tr>
    <tr>
      <th>14</th>
      <td>zales</td>
      <td>em.zales.com</td>
      <td>287</td>
    </tr>
    <tr>
      <th>15</th>
      <td>XXX</td>
      <td>uchicago.edu</td>
      <td>286</td>
    </tr>
    <tr>
      <th>16</th>
      <td>katespade</td>
      <td>em.katespade.com</td>
      <td>274</td>
    </tr>
    <tr>
      <th>17</th>
      <td>noreply</td>
      <td>r.groupon.com</td>
      <td>266</td>
    </tr>
    <tr>
      <th>18</th>
      <td>info</td>
      <td>twitter.com</td>
      <td>240</td>
    </tr>
  </tbody>
</table>
</div>



Turns out, the two most frequent senders are from ***Meetup***!  Specifically, "newtech-1", which I remember as a New York Tech Meetup, and "info" should be some general update on all Meetup events that I subscribe to.

**Mealpal**, which is a discounted email-based lunch subscription service that I had for a few months also sent me quite some emails, and so did **StreetEasy, Expedia, Uniqlo, Godiva** etc...  Maybe I shouldn't have given my email out to all those websites...

There were some individuals from **UChicago**(alma mater) as well, which I anonymized with "XXX".  Brings back memories.

I think I can delete all emails from the top 18 senders, so I extracted all mail ids corresponding to these senders and used Python and the `imaplib` module to automatically delete ~13,000 emails.

Voila! I just reduced my inbox count to half what is was without worrying about deleting any important emails!  Below is a progress bar that shows that I deleted 12,862 emails in 1:21 hours.

    100%|██████████| 12862/12862 [1:21:03<00:00,  4.23it/s]


<br/>
## More
If you'd like to see the Python script to download email data used in this process, please click [here](https://github.com/ncho-sqd/emailtools/blob/master/main.py).

For Jupyter notebook walking through the email deletion process laid out on this page (after downloaded email data), please click [here](https://github.com/ncho-sqd/emailtools/blob/master/clean_email_inbox.ipynb).
