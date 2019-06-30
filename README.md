Twender
=======

Description
-----------
Python project to determine the gender of Twitter users based on the text of their 
tweets using machine learning techniques. Provides tools for collecting tweets to 
be used as training data as well as building a naive bayes classifier trained on 
that data. In order to provide the labeled training data used for supervised learning 
(naive bayes) this project uses name and gender data from social security card 
applications to create a mapping from first name to gender. It then uses that mapping to
label a tweet as male or female based on the name they supplied to their twitter account.
The Twender web application takes a twitter handle from the user and uses the internal
classifier to classify each of their most recent tweets and then uses that to calculate 
the overall gender of that user.

You can find the application live at <http://twender.mtstanley.tech/>

Setup
-----
Clone this repo using `git clone https://github.com/mthstanley/twender.git`
Then setup a new python virtual environment using `virtualenv -p python3 venv`
afterwards run `source venv/bin/activate` next install required python packages 
`pip install -r requirements.txt`. 

Then create a .env file in the same directory as the config.py file, similar to the following:

```
# .env configuration using environment variables
SECRET_KEY='hard to guess string'

# twitter api access credentials
TWITTER_CONSUMER_KEY=''
TWITTER_CONSUMER_SECRET=''
TWITTER_ACCESS_TOKEN=''
TWITTER_ACCESS_TOKEN_SECRET=''

# mongodb setup
MONGO_URI='mongodb://[username:password@]host1[:port1][,...hostN[:portN]]][/[database][?options]]'
```

NOTE: For the `MONGO_URI` format check out [their docs](https://docs.mongodb.com/manual/reference/connection-string/)

Build
-----
The classifier that Twender uses needs to be trained on some labeled tweet data, in 
order to do this Twender first needs a list of valid names with a corresponding gender.
To build this list use `flask mkvalidnames --save <src files>`, the data files used for doing 
this can be found at <http://www.ssa.gov/oact/babynames/limits.html>. Once this is done you'll
need to collect and label some tweets, to do so run `flask collecttweets --save`.

Run
---
Then run the web application with `flask run`.
