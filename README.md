Twender
=======

Description
-----------
Python project to determine the gender of Twitter users based on the text of
their tweets using machine learning techniques. Provides tools for collecting
tweets to be used as training data as well as building a naive bayes classifier
trained on that data.

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

# mongodb access credentials
MONGO_HOST='localhost'
MONGO_PORT='27017'

# required if using authentication with mongo
MONGO_USERNAME='username'
MONGO_PASSWORD='password'
MONGO_AUTH_SOURCE='auth database name'
```

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
