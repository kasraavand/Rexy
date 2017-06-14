## Preamble


**Rexy** (rec-sy) is an open-source recommendation system based on a general User-Product-Tag schema and a flexible structure that has been designed to be adaptable with variant data-schema. There are a lot of methods and ways that Rexy is used to recommend the products to users. This is contain general recommendations like top products, even based recommendations and Novel products that the user might be interested in. There are other recommendations that are directly related to the user's activities or other users that have a similar behavior as the given user.

Along side the recommendations that are related to user's interests there are also some modules designed to find the most proper products based on other factors like advertisement, social, etc. and don't have the side effects of a commercial advertisement systems. For instance, `Email` and `Search` modules are designed to support such goals.

The underlying codes are entirely written in Python-3.5 in a highly optimized, Pythonic and comprehensive way, that makes it so flexible against changes. It also used [Aerospike](http://www.aerospike.com/) as the database engine which is a high speed, scalable, and reliable NoSQL database.

 -----------
 

![26c982832302ac96d00bab52acbd6537](https://cloud.githubusercontent.com/assets/5694520/20237512/bd2790b0-a8e9-11e6-865d-a9f2be1f5ff2.jpg)


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

`Profile` is almost the widest module in Rexy. It's responsible of every profile in your platform, include user profile, product profile, provider profile, etc.

For a given profile we can show a diverse set of recommendations which are as follows:

 - Top Products

Top products of all time, based on user's interest and other purposes.
 
 - Novel Products

Favorite products during the latest N month/week, based on user's interest and other purposes.

 - Event-based recommendations

Products related to the current events, based on user's interest and other purposes.

 - Recommendations For You

In this part we suggest the products that are based on user's activities or the user's that have similar activities to the given user. Both of these recommendations fall under two accurate and similar categories.

The accurate recommendations are basically based on the common tags among the products. Finding the intersected tags can be done in two level the first one is related to the products that are directly related to the user's products and second one is related to the products that are similar to the similar products of our products.

The similar recommendations are based on the similarities between the common products and similar users in which these similarities are calculated based on the tag densities, common tags, different tags, and some other influential factors. 

 - Top N Picks For You

At this section, we find the top N products from all the aforementioned parts.


 ![#c5f015](https://placehold.it/15/c5f015/000000?text=+) **Search**

The search module is responsible for recommendations during the search process by user. Based on user's in case that the searched products are exist in database, we can show the related products based on some manual policies. In case the word doesn't exist in our database, we can use a prepared list of product names which are tagged properly in order to find the related products and show them to the user. This prepared list of products can be a scraped file or something similar. Another way around this is to ask the users to enter/select some related tags to the searched product and find the similar products based on them.

If the user is a logged in user with a history of activity, in case that the searched word doesn't exist in our database, we can recommend a list of products related to the latest users activities top products the most recently searched product, top popular product among the similar users to the user or other different methods.


# Requirements

The Require 

## Rexy is large an powerful enough, but can we make it more stronger?

Indeed, using Python's state-of-the-art scientific programming tools, such as Numpy, Pandas, scikit-learn in order to harness the power of machine learning algorithms in the most optimized way. Also the structure can be expanded to be able to satisfy the further needs of your system. That's what we call XTRex (Xenomorph Tyrannosaurus Rex).

![image](https://user-images.githubusercontent.com/5694520/27120053-61c5e9e0-50f7-11e7-828a-e375e7766f7a.png)

