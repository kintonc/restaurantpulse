import json, codecs
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, EntitiesOptions, KeywordsOptions
import datetime
import glob
from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure
from bokeh.models import Legend
from bokeh.palettes import GnBu3, OrRd3
from pprint import pprint

# Picking up API credentials for IBM Watson from file
creds = json.load(open('watson_creds.json'))
userdetails = creds['natural-language-understanding'][0]['credentials']

# Creating objects to query IBM Watson
natural_language_understanding = NaturalLanguageUnderstandingV1(
  username=userdetails['username'],
  password=userdetails['password'],
  version='2017-02-27')

# Send API request to IBM Watson
def analyze(review):
  response = natural_language_understanding.analyze(
    text=review,
    features=Features(
      entities=EntitiesOptions(
        emotion=True,
        sentiment=True,
        limit=3),
      keywords=KeywordsOptions(
        emotion=True,
        sentiment=True,
        limit=3)))
  temp = json.dumps(response, indent=2)
  return json.loads(temp)

# Converts all the data in the files for each restaurant in to JSONs that can be processed
def CreateAnalysisJSON(files):
  analysis = []
  for file in files:
    reviews = json.load(open(file))
    for review in reviews:
      analysis.append(analyze(review['review']))
  data_json = {
    'analysis' : analysis
  }
  return data_json

# Counts the sentiment of each review given by IBM Watson and returns an array
def EmotionTotal(analysis):
  JoySum = 0
  AngerSum = 0
  SadSum = 0
  PositiveSum = 0
  NeutralSum = 0
  NegativeSum = 0
  for record in analysis:
    keyword = record['keywords']
    for emotion in keyword:
      try:
        JoySum += emotion['emotion']['joy']
        AngerSum += emotion['emotion']['anger']
        SadSum += emotion['emotion']['sadness']
        sentiment = emotion['sentiment']['label']
        if sentiment == 'positive':
          PositiveSum += 1
        if sentiment == 'neutral':
         NeutralSum += 1
        if sentiment == 'negative':
          NegativeSum +=1
      except:
        continue
        pass
  return [JoySum, AngerSum, SadSum, PositiveSum, NeutralSum, NegativeSum]


# Stacked chart generation

print("BEGIN NLP_analysis.py")

#now = datetime.datetime.now()
#date = str(now.year)+"-"+str(now.month).zfill(2)+"-"+str(now.day).zfill(2)
date = '2018-03-22'

restaurants = json.load(open('../sendgrid/configs/restaurants.json'))
restaurant_0 = restaurants['0']
restaurant_1 = restaurants['1']
restaurant_2 = restaurants['2']
restaurant_3 = restaurants['3']
restaurant_4 = restaurants['4']

pattern_restaurant_0 = "../scrapy-yelp-tripadvisor/tutorial/spiders/data/json/" + restaurant_0['nospace_name'] + "*" + date + "*review*"
pattern_restaurant_1 = "../scrapy-yelp-tripadvisor/tutorial/spiders/data/json/" + restaurant_1['nospace_name'] + "*" + date + "*review*"
pattern_restaurant_2 = "../scrapy-yelp-tripadvisor/tutorial/spiders/data/json/" + restaurant_2['nospace_name'] + "*" + date + "*review*"
pattern_restaurant_3 = "../scrapy-yelp-tripadvisor/tutorial/spiders/data/json/" + restaurant_3['nospace_name'] + "*" + date + "*review*"
pattern_restaurant_4 = "../scrapy-yelp-tripadvisor/tutorial/spiders/data/json/" + restaurant_4['nospace_name'] + "*" + date + "*review*"

files_restaurant_0 = glob.glob(pattern_restaurant_0)
files_restaurant_1 = glob.glob(pattern_restaurant_1)
files_restaurant_2 = glob.glob(pattern_restaurant_2)
files_restaurant_3 = glob.glob(pattern_restaurant_3)
files_restaurant_4 = glob.glob(pattern_restaurant_4)


analysis_restaurant_0 = CreateAnalysisJSON(files_restaurant_0)['analysis']
analysis_restaurant_1 = CreateAnalysisJSON(files_restaurant_1)['analysis']
analysis_restaurant_2 = CreateAnalysisJSON(files_restaurant_2)['analysis']
analysis_restaurant_3 = CreateAnalysisJSON(files_restaurant_3)['analysis']
analysis_restaurant_4 = CreateAnalysisJSON(files_restaurant_4)['analysis']

# [JoySum, AngerSum, SadSum, PositiveSum, NeutralSum, NegativeSum]
restaurant_0_emotion_totals = EmotionTotal(analysis_restaurant_0)
restaurant_1_emotion_totals = EmotionTotal(analysis_restaurant_1)
restaurant_2_emotion_totals = EmotionTotal(analysis_restaurant_2)
restaurant_3_emotion_totals = EmotionTotal(analysis_restaurant_3)
restaurant_4_emotion_totals = EmotionTotal(analysis_restaurant_4)

output_file("../scrapy-yelp-tripadvisor/tutorial/spiders/data/html/sentiment_graph_1.html")

restaurants = [restaurant_0['name'], restaurant_1['name'], restaurant_2['name'], restaurant_3['name'], restaurant_4['name']]

# Creating sentiment graph 1 that shows "Joy", "Anger" and "Sadness" sentiments
sentiments = ["Joy", "Anger", "Sadness"]
#colors = ["#c9d9d3", "#718dbf", "#e84d60"]
colors = ["#c9d9d3", "#718dbf", "#f57c00"]


data = {'restaurants' : restaurants,
           'Joy'    : [restaurant_0_emotion_totals[0],
                       restaurant_1_emotion_totals[0],
                       restaurant_2_emotion_totals[0],
                       restaurant_3_emotion_totals[0],
                       restaurant_4_emotion_totals[0]],
           'Anger'   : [restaurant_0_emotion_totals[1],
                       restaurant_1_emotion_totals[1],
                       restaurant_2_emotion_totals[1],
                       restaurant_3_emotion_totals[1],
                       restaurant_4_emotion_totals[1]],
           'Sadness': [restaurant_0_emotion_totals[2],
                       restaurant_1_emotion_totals[2],
                       restaurant_2_emotion_totals[2],
                       restaurant_3_emotion_totals[2],
                       restaurant_4_emotion_totals[2]]}

source = ColumnDataSource(data=data)

p = figure(x_range=restaurants, plot_height=250, title="Yelp & TripAdvisor Reviews - Summary",
           toolbar_location=None, tools="")

p.vbar_stack(sentiments, x='restaurants', width=0.9, color=colors, source=source,
             legend=False)

p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.axis.minor_tick_line_color = None
p.outline_line_color = None
p.title.align = 'center'
#p.legend.location = "top_right"
#p.legend.orientation = "horizontal"

#legend = Legend(location=(500, -180))
#p.add_layout(legend, 'outside')

show(p)


output_file("../scrapy-yelp-tripadvisor/tutorial/spiders/data/html/sentiment_graph_2.html")

# Creating sentiment graph 2 that shows the overall sentiment from a review: "Positive", "Neutral" and "Negatie" sentiments
sentiments = ["Positive", "Neutral", "Negative"]
#colors = ["#c9d9d3", "#718dbf", "#e84d60"]
colors = ["#4fb443", "#d9b42c", "#de061a"]


data = {'restaurants' : restaurants,
           'Positive'   : [restaurant_0_emotion_totals[3],
                          restaurant_1_emotion_totals[3],
                          restaurant_2_emotion_totals[3],
                          restaurant_3_emotion_totals[3],
                          restaurant_4_emotion_totals[3]],
           'Neutral'    : [restaurant_0_emotion_totals[4],
                          restaurant_1_emotion_totals[4],
                          restaurant_2_emotion_totals[4],
                          restaurant_3_emotion_totals[4],
                          restaurant_4_emotion_totals[4]],
           'Negative'   : [restaurant_0_emotion_totals[5],
                          restaurant_1_emotion_totals[5],
                          restaurant_2_emotion_totals[5],
                          restaurant_3_emotion_totals[5],
                          restaurant_4_emotion_totals[5]]}

source = ColumnDataSource(data=data)

p = figure(x_range=restaurants, plot_height=250, title="Yelp & TripAdvisor Reviews - Summary",
           toolbar_location=None, tools="")

p.vbar_stack(sentiments, x='restaurants', width=0.9, color=colors, source=source,
             legend=False)

p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.axis.minor_tick_line_color = None
p.outline_line_color = None
p.title.align = 'center'
#p.legend.location = "top_right"
#p.legend.orientation = "horizontal"

show(p)

print("END NLP_analysis.py")
