import finalP 
from finalP import job_categories
from flask import Flask, render_template, url_for,jsonify,request,redirect
from flask_pymongo import PyMongo
from datetime import date

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/jobs"
mongo = PyMongo(app)
collection = mongo.db.roles
collection2 = mongo.db.filled

# Jobs_L = finalP.updating(job_categories)
# print(len(Jobs_L))


@app.route("/", methods=["GET"])
def home():
    output = []
    for obj in collection.find():
        output.append({"Title": obj["title"],"Description": obj["Description"], "JobCategory": obj["category"]})
    return jsonify({'result' : output})

@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/index2")
def index2():
    return render_template('index2.html')


@app.route("/f", methods=["GET"])
def field():
    resultado = []
    for obj in collection2.find():
        resultado.append({"Category": obj["category"]}, {"Jobs_added": obj["#_Jobs_added"]}, {"Jobs_filled": obj["#_Jobs_filled"]},{"Dates": obj["Date"]})
    return jsonify({'resul' : resultado})












@app.route("/updating")
def updating():
    Jobs_L = finalP.updating(job_categories)
    for new_job in Jobs_L[1]:
        for job in Jobs_L[3]:
            if new_job == job["Job_ID"]:
                collection.insert_one(job)

    for filled_job in Jobs_L[2]:
        collection.delete_one({"Job_ID" : filled_job})

    today = date.today()
    jobs_filled = {}
    jobs_F = []
    for j in range(0,len(Jobs_L[0])):
        jobs_filled["category"] = job_categories[j]
        jobs_filled["#_Jobs_added"] = Jobs_L[0][j][0]
        jobs_filled["#_Jobs_filled"] = Jobs_L[0][j][1]
        jobs_filled["Date"] = today.strftime("%m/%d/%y")
        jobs_F.append(jobs_filled.copy())
    
    collection2.insert(jobs_F)




if __name__=='__main__':
    app.run(debug=True)









