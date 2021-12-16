from typing import Text
import urllib.parse, urllib.request, urllib.error, json
from flask import Flask, render_template, request
import logging

app = Flask(__name__)

def safe_get(params=None):
  url = "http://makeup-api.herokuapp.com/api/v1/products.json"
  if params is not None:
    url = url + "?" + urllib.parse.urlencode(params)

  app.logger.info(url)
  try:
      result = urllib.request.urlopen(url)
      return result
  except urllib.error.URLError as e:
      if hasattr(e, "code"):
          print("The server couldn't fulfill the request.")
          print("Error code: ", e.code)
      elif hasattr(e, "reason"):
          print("We failed to reach a server.")
          print("Reason: ", e.reason)
      return None

def make_menu_dictionary():
  #menu_dictionary = {"brand": [], "product_type": {}, "tag_list": []}
  #menu_dictionary = {"brand": [], "product_type": {}}
  menu_dictionary = {"brand": [], "product_type": []}
  results = json.load(safe_get())
  for result in results:
    product_type = result['product_type']
    brand = result['brand']
    #tags = result['tag_list']
    if brand not in menu_dictionary["brand"]:
      menu_dictionary['brand'].append(brand)

    if product_type not in menu_dictionary['product_type']:
      menu_dictionary["product_type"].append(result["product_type"])

    #if product_type not in menu_dictionary['product_type'].keys():
      #menu_dictionary["product_type"].append(result["product_type"])
    #  menu_dictionary["product_type"][product_type] = menu_dictionary['product_type'].get(product_type, [])

    #for tag in tags:
    #  if tag not in menu_dictionary['product_type'][product_type]:
    #    menu_dictionary["product_type"][product_type].append(tag)

  return menu_dictionary

def make_results(params):
  results = json.load(safe_get(params))
  app.logger.info(results)
  return results

@app.route('/')
def get_all():
  menu_dictionary = make_menu_dictionary()
  if request.args.getlist('menu'):
    menu = request.args.getlist('menu')
    params = {}

    if menu[0] == 'select' and menu[1] == 'select':
      text = "- Please select either a product type or a brand! -"
      return(render_template('index.html', menu_dictionary=menu_dictionary, text=text))
    elif menu[0] != 'select' and menu[1] != 'select':
      text = "- " + menu[0] + ", " + menu[1] + " -"
      params["product_type"] = menu[0]
      params["brand"] = menu[1]
    else:
      if menu[0] != 'select':
        text = "- " + menu[0] + " -"
        params["product_type"] = menu[0]
      else:
        text = "- " + menu[1] + " -"
        params["brand"] = menu[1]

    results = make_results(params)
    if results == []:
      text = "- No result for " + menu[0] + " in " + menu[1] + " -"
      return(render_template('index.html', menu_dictionary=menu_dictionary, text=text))
    else:
      return(render_template('index.html', menu_dictionary=menu_dictionary, text=text, results=results))

  return(render_template('index.html', menu_dictionary=menu_dictionary))

@app.route("/detail")
def detail():
  src = request.args.get('src')
  return(render_template('detail.html', src=src))

if __name__ == "__main__":
  app.run(host='localhost', port=8080, debug=True)