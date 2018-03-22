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
from bokeh.palettes import GnBu3, OrRd3

from pprint import pprint

creds = json.load(open('watson_creds.json'))
userdetails = creds['natural-language-understanding'][0]['credentials']

natural_language_understanding = NaturalLanguageUnderstandingV1(
  username=userdetails['username'],
  password=userdetails['password'],
  version='2017-02-27')

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

print("BEGIN NLP_analysis.py")

now = datetime.datetime.now()
date = str(now.year)+"-"+str(now.month).zfill(2)+"-"+str(now.day).zfill(2)
#date = '2018-03-21'

restaurants = ['wilbur_mexicana', 'celebrity_hot_pot', 'hashi_izakaya', 'kinka_izakaya', 'sushi_bong', 'uncle_tetsu']
pattern_wilbur_mexicana = "../scrapy-yelp-tripadvisor/tutorial/spiders/data/json/" + restaurants[0] + "*" + date + "*review*"
pattern_celebrity_hot_pot = "../scrapy-yelp-tripadvisor/tutorial/spiders/data/json/" + restaurants[1] + "*" + date + "*review*"
pattern_hashi_izakaya = "../scrapy-yelp-tripadvisor/tutorial/spiders/data/json/" + restaurants[2] + "*" + date + "*review*"
pattern_kinka_izakaya = "../scrapy-yelp-tripadvisor/tutorial/spiders/data/json/" + restaurants[3] + "*" + date + "*review*"
pattern_sushi_bong = "../scrapy-yelp-tripadvisor/tutorial/spiders/data/json/" + restaurants[4] + "*" + date + "*review*"
pattern_uncle_tetsu = "../scrapy-yelp-tripadvisor/tutorial/spiders/data/json/" + restaurants[5] + "*" + date + "*review*"

files_wilbur_mexicana = glob.glob(pattern_wilbur_mexicana)
files_celebrity_hot_pot = glob.glob(pattern_celebrity_hot_pot)
files_hashi_izakaya = glob.glob(pattern_hashi_izakaya)
files_kinka_izakaya = glob.glob(pattern_kinka_izakaya)
files_sushi_bonga = glob.glob(pattern_sushi_bong)
files_uncle_tetsu = glob.glob(pattern_uncle_tetsu)


analysis_wilbur_mexicana = CreateAnalysisJSON(files_wilbur_mexicana)['analysis']
analysis_celebrity_hot_pot = CreateAnalysisJSON(files_celebrity_hot_pot)['analysis']
analysis_hashi_izakaya = CreateAnalysisJSON(files_hashi_izakaya)['analysis']
analysis_kinka_izakaya = CreateAnalysisJSON(files_kinka_izakaya)['analysis']
analysis_sushi_bonga = CreateAnalysisJSON(files_sushi_bonga)['analysis']
analysis_uncle_tetsu = CreateAnalysisJSON(files_uncle_tetsu)['analysis']

# [JoySum, AngerSum, SadSum, PositiveSum, NeutralSum, NegativeSum]
wilbur_mexicana_emotion_totals = EmotionTotal(analysis_wilbur_mexicana)
celebrity_hot_pot_emotion_totals = EmotionTotal(analysis_celebrity_hot_pot)
hashi_izakaya_emotion_totals = EmotionTotal(analysis_hashi_izakaya)
kinka_izakaya_emotion_totals = EmotionTotal(analysis_kinka_izakaya)
sushi_bonga_emotion_totals = EmotionTotal(analysis_sushi_bonga)
uncle_tetsu_emotion_totals = EmotionTotal(analysis_uncle_tetsu)

output_file("../scrapy-yelp-tripadvisor/tutorial/spiders/data/html/sentiment_graph_1.html")

# restaurants = ['wilbur_mexicana', 'celebrity_hot_pot', 'hashi_izakaya', 'kinka_izakaya', 'sushi_bong', 'uncle_tetsu']
sentiments = ["Joy", "Anger", "Sadness"]
colors = ["#c9d9d3", "#718dbf", "#e84d60"]


data = {'restaurants' : restaurants,
           'Joy'   : [wilbur_mexicana_emotion_totals[0], celebrity_hot_pot_emotion_totals[0], hashi_izakaya_emotion_totals[0], kinka_izakaya_emotion_totals[0], sushi_bonga_emotion_totals[0], uncle_tetsu_emotion_totals[0]],
           'Anger'   : [wilbur_mexicana_emotion_totals[1], celebrity_hot_pot_emotion_totals[1], hashi_izakaya_emotion_totals[1], kinka_izakaya_emotion_totals[1], sushi_bonga_emotion_totals[1], uncle_tetsu_emotion_totals[1]],
           'Sadness'   : [wilbur_mexicana_emotion_totals[2], celebrity_hot_pot_emotion_totals[2], hashi_izakaya_emotion_totals[2], kinka_izakaya_emotion_totals[2], sushi_bonga_emotion_totals[2], uncle_tetsu_emotion_totals[2]]}

source = ColumnDataSource(data=data)

p = figure(x_range=restaurants, plot_height=250, title="Review Sentiment Counts",
           toolbar_location=None, tools="")

p.vbar_stack(sentiments, x='restaurants', width=0.9, color=colors, source=source,
             legend=[value(x) for x in sentiments])

p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.axis.minor_tick_line_color = None
p.outline_line_color = None
p.legend.location = "top_left"
p.legend.orientation = "horizontal"

show(p)


output_file("../scrapy-yelp-tripadvisor/tutorial/spiders/data/html/sentiment_graph_2.html")

# restaurants = ['wilbur_mexicana', 'celebrity_hot_pot', 'hashi_izakaya', 'kinka_izakaya', 'sushi_bong', 'uncle_tetsu']
sentiments = ["Positive", "Neutral", "Negative"]
colors = ["#c9d9d3", "#718dbf", "#e84d60"]


data = {'restaurants' : restaurants,
           'Positive'   : [wilbur_mexicana_emotion_totals[3], celebrity_hot_pot_emotion_totals[3], hashi_izakaya_emotion_totals[3], kinka_izakaya_emotion_totals[3], sushi_bonga_emotion_totals[3], uncle_tetsu_emotion_totals[3]],
           'Neutral'   : [wilbur_mexicana_emotion_totals[4], celebrity_hot_pot_emotion_totals[4], hashi_izakaya_emotion_totals[4], kinka_izakaya_emotion_totals[4], sushi_bonga_emotion_totals[4], uncle_tetsu_emotion_totals[4]],
           'Negative'   : [wilbur_mexicana_emotion_totals[5], celebrity_hot_pot_emotion_totals[5], hashi_izakaya_emotion_totals[5], kinka_izakaya_emotion_totals[5], sushi_bonga_emotion_totals[5], uncle_tetsu_emotion_totals[5]]}

source = ColumnDataSource(data=data)

p = figure(x_range=restaurants, plot_height=250, title="Review Sentiment Counts",
           toolbar_location=None, tools="")

p.vbar_stack(sentiments, x='restaurants', width=0.9, color=colors, source=source,
             legend=[value(x) for x in sentiments])

p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.axis.minor_tick_line_color = None
p.outline_line_color = None
p.legend.location = "top_left"
p.legend.orientation = "horizontal"

show(p)

print("END NLP_analysis.py")
