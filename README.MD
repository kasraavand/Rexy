## Preamble


**Rexy** (rec-sy) is an open-source recommendation system based on a general User-Product-Tag schema and a flexible structure that has been designed to be adaptable with variant data-schema. The underlying codes are entirely written in Python-3.5 in a highly optimized, Pythonic and comprehensive way, that makes it so flexible against changes. It also used [Aerospike](http://www.aerospike.com/) as the database engine which is a high speed, scalable, and reliable NoSQL database.

 ----------

 # Structure and Features

Rexy is consist of following major modules:


 ![#c5f015](https://placehold.it/15/c5f015/000000?text=+) **Administration**

This directory is contain administrative modules like visualizer which is supposed do to handle the visualization tasks.

 ![#c5f015](https://placehold.it/15/c5f015/000000?text=+) **Core** 

 The `Core` is contain those modules that handle the core operations and might be used in most of the modules.

 ![#c5f015](https://placehold.it/15/c5f015/000000?text=+) **Email**

 This modules is designed to handle the recommendations through Email. Emails are basically sent on a weekly basis, which means that the users have a fewer interaction with. This makes is a proper place for advertisements and going a little further than the customized recommends. Therefore, this modules is tend to use more diverse and unpopular products.

 Also, in addition to the aforementioned features, in Emails we have more options and space for our recommendations, which makes it possible to involve the new types of recommendations in the future. And this module has been designed in a way to be as flexible as possible against such new changes.  

 ![#c5f015](https://placehold.it/15/c5f015/000000?text=+) **General**

There are also some kind of recommendations that are not specifically personalized for users or products. These are consist of `Novel`, `Top` and `Event`recommendations. The results of these modules, regardless of the subject of the page that we're  planning to show them can be used. For example at home page for everyone or even for not logged-in users.

 - Novel
 
This module is supposed to find the most popular products within a newly certain amount of time. For example, the last month.
  
  - Top
  
Alongside the newly favorite produts we also need to find the all-time popular products among the users. That's exactlly what this module stands for.

  - Event
  
Sometimes we need to go further than regular and common recommendation types, that's where the modules like `Event` come in. This module finds the most relevant products specially for users and in general based on the events on a given calendar. This module is used [Wipazuka](https://github.com/kasramvd/Wipazuka) a multilingual calendar-based wordnet to finds the intended products based on events.

 ![#c5f015](https://placehold.it/15/c5f015/000000?text=+) **Logging**

The logging module that keeps track of the errors and exceptions that happens in the whole application.

 ![#c5f015](https://placehold.it/15/c5f015/000000?text=+) **Profile**

`Profile` is almost the widest module in Rexy. It's responsible of every profile in our platform, include user profile, product profile, provider profile, etc.

For a given profile we can show a diverse set of recommendations like the `Top Products`, `Top N Picks For You`, `Recommendations for you`, etc.

 ![#c5f015](https://placehold.it/15/c5f015/000000?text=+) **Search**

The searc module is responsible for recommendations during the search process by user.
 -----------
 

![26c982832302ac96d00bab52acbd6537](https://cloud.githubusercontent.com/assets/5694520/20237512/bd2790b0-a8e9-11e6-865d-a9f2be1f5ff2.jpg)
