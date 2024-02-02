import pickle
from flask import *
from flask_cors import CORS
from flaskwebgui import FlaskUI
import webbrowser
from scraper import scrape_url
import autopost
import multiprocessing as mp





def scrape(url):
    result, s, f = scrape_url(url.strip())
    return result, s, f







app = Flask(__name__,
static_folder='./templates/static')
app.debug = True
CORS(app)
# ui = FlaskUI(app,fullscreen=True,port=5000)
results = []
@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/home", methods=['GET'])
def home():
    return render_template('some_page.html')

@app.route("/run_scrape", methods=['GET','POST'])
def run_scrape():
    if(request.method == 'POST'):
        global results
        data = json.loads(request.data)
        urls = data['urls']
        urls = [u.strip() for u in urls]
        urls = [u for u in urls if u != '']
        print(urls)
        results  = []
        s_count = 0
        f_count = 0
        #try:
        # Create a pool of workers
        pool = mp.Pool()

        # Use map to apply the scrape function to each url in urls and collect the results as a list of tuples
        results = pool.map(scrape, urls)

        # Close the pool and wait for the workers to finish
        pool.close()
        pool.join()

        # Unpack the results into separate lists
        results, s_counts, f_counts = zip(*results)

        # Sum up the s_counts and f_counts
        s_count = sum(s_counts)
        f_count = sum(f_counts)
        if(len(results) > 0):
            return jsonify({'success' : True,'s_count' : s_count , 'f_count' :f_count})
        else:
            return jsonify({'success' : False,'message' : 'No results'})
            #except Exception as e:
            #return jsonify({'success' : False , 'message' : str(e)})

@app.route("/run_post", methods=['GET','POST'])
def run_post():
    if(request.method == 'POST'):
        data = json.loads(request.data)
        username = data['username']
        password = data['password']



        list_to_post = autopost.get_list_to_post()


        try:
            s_count , f_count = autopost.run_post(username , password , list_to_post)
            return jsonify({'success' : True,'s_count' : s_count , 'f_count':f_count})
        except Exception as e:
            return jsonify({'success' : False , 'message' : str(e)})

if __name__ == "__main__":
    # app.run() for debug

    webbrowser.open_new('http://127.0.0.1:5000')
    app.run(use_reloader=False)
