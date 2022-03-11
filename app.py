from random import randint
from flask import Flask, jsonify,abort,make_response,request

app = Flask(__name__)

"""prizes=[
    {
        'id':1,
        'description': 'iphone 11'
    },
    {
        'id':2,
        'description': 'ASUS intel core'
    }
]"""

"""participants=[
     {
       'id': 1,
       'name': 'Sam'
     },
     {
       'id': 2,
       'name': 'Tom'
     }
]"""

promo = [
    {
        'id': 1,
        'name': 'phones', 
        'description': 'promoactions of phones',
        'prizes':[
            {
                'id':1,
                'description': 'iphone 11'
            },
            {
                'id':2,
                'description': 'ASUS intel core'
            }
        ],
        'participants':[
                    {
                        'id': 1,
                        'name': 'Sam'
                    },
                    {
                        'id': 2,
                        'name': 'Tom'
                    }
                ]           
    },
    {
        'id': 2,
        'name': 'phones', 
        'description': 'promoactions of phones',
        'prizes':[
            {
                'id':1,
                'description': 'samsung'
            },
            {
                'id':2,
                'description': 'huawey'
            }
        ],
        'participants':[
                    {
                        'id': 1,
                        'name': 'Gally'
                    },
                    {
                        'id': 2,
                        'name': 'Nail'
                    },
                    {
                        'id': 3,
                        'name': 'Harry'
                    }
                ]       
    }
]

result=[
    {
        'winner':[
            {
                'id': 1,
                'name': 'Gally'
            }
        ],
        'prizes':[
            {
                'id':1,
                'description': 'samsung'
            }
        ]
    }
]

@app.route('/promo', methods=['POST'])
def create_task():
    if not request.json or not 'name' in request.json: #or not 'name' => if need! 
        abort(400) 
    #curl -i -H "Content-Type: application/json" -X POST -d "{\"name\":\"big sale\",\"description\":\"phones different\"}" http://localhost:8080/promo
    prom= {
        'id': promo[-1]['id'] + 1,
        'name': request.json.get('name',""),
        'description': request.json.get('description', "")
    }
    promo.append(prom)
    return jsonify(prom['id']), 201

#curl -i -H "Content-Type: application/json" -X GET http://localhost:5000/promo?query=laptop
@app.route('/promo', methods=['GET'])
def get_promo():
    """if request.args.get('query'):
        task=[]
        string = str(request.args.get('query'))
        print(string)
        for i in promo:
            if string in str(i['category_id']):
                task.append(i)
            elif string in i['name']:
                task.append(i)
            elif string in i['description']:
                task.append(i)
        return jsonify({'promo': task})"""
    promos=[]
    for i in promo:
        print(i)
        l={'id':i['id'],'description':i['description'],'name':i['name']}
        print(l)
        promos.append(l)
    return jsonify(promos)

@app.route('/promo/<int:promo_id>', methods=['GET'])
def get_promo_id(promo_id):
    task=-1
    for i in promo:
        print(i['id'])
        print(promo_id)
        if i['id']==promo_id:
            task=i
    if task==(-1):
        abort(404)
    return jsonify(task)

#curl -i -H "Content-Type: application/json" -X PUT -d "{\"name\":\"haha\",\"description\":\"different phones\"}" http://localhost:8080/promo/4
@app.route('/promo/<int:promo_id>', methods=['PUT']) 
def update_task(promo_id):
    for i in promo:
        if i['id']==promo_id:
            task=i
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) != str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    name=request.json.get('name', task['name'])
    print(name)
    if name=="":
        abort(400)
    else: 
        task['name'] = name
    task['description'] = request.json.get('description', task['description'])
    return jsonify(task)

@app.route('/promo/<int:promo_id>', methods=['DELETE'])
def delete_task(promo_id):
    task=-1
    for i in promo:
        if i['id']==promo_id:
            task=i
    if task==(-1):
        abort(404)
    promo.remove(task)
    return jsonify({'result': True})

@app.route('/promo/<int:promo_id>/participant', methods=['POST'])
def create_user(promo_id):
    """if not request.json or not 'name' in request.json: #or not 'name' => if need! 
        abort(400) """
    #curl -i -H "Content-Type: application/json" -X POST -d "{\"name\":\"Tomas\"}" http://localhost:8080/promo/1/participant
    for i in promo:
        if i['id']==promo_id:
            task=i
    participant= {
        'id': task['participants'][-1]['id']  + 1,
        'name': request.json.get('name',""),
    }
    task['participants'].append(participant)
    return jsonify(participant['id']), 201

@app.route('/promo/<int:promo_id>/participant/<int:user_id>', methods=['DELETE'])
def delete_user(promo_id,user_id):
    task=-1
    for i in promo:
        if i['id']==promo_id:
            task=i
    if task==(-1):
        abort(404)
    for j in task['participants']:
        if j['id']==user_id:
            #print(j)
            task['participants'].remove(j)
    return jsonify({'result': True})

@app.route('/promo/<int:promo_id>/prize', methods=['POST'])
def create_prize(promo_id):
    """if not request.json or not 'name' in request.json: #or not 'name' => if need! 
        abort(400) """
    #curl -i -H "Content-Type: application/json" -X POST -d "{\"description\":\"sweet\"}" http://localhost:8080/promo/1/prize
    for i in promo:
        if i['id']==promo_id:
            task=i
    prize= {
        'id': task['prizes'][-1]['id'] + 1,
        'description': request.json.get('description',""),
    }
    task['prizes'].append(prize)
    return jsonify(prize['id']), 201

@app.route('/promo/<int:promo_id>/prize/<int:prize_id>', methods=['DELETE'])
def delete_prize(promo_id,prize_id):
    task=-1
    for i in promo:
        if i['id']==promo_id:
            task=i
    if task==(-1):
        abort(404)
    for j in task['prizes']:
        if j['id']==prize_id:
            #print(j)
            task['prizes'].remove(j)
    return jsonify({'result': True})

@app.route('/promo/<int:promo_id>/raffle', methods=['POST'])
def raffle(promo_id):
    """if not request.json or not 'name' in request.json: #or not 'name' => if need! 
        abort(400) """
    #curl -i -H "Content-Type: application/json" -X POST http://localhost:8080/promo/1/raffle
    for i in promo:
        if i['id']==promo_id:
            task=i
    if len(task['prizes'])==len(task['participants']):
        """pr=randint(1,len(task['prizes']))
        us=randint(1,len(task['participants']))
        for j in task['participants']:
            if j['id']==us:
                winner=j
        for j in task['prize']:
            if j['id']==pr:
                prise=j"""
        raffles=[]
        for i in range(0,len(task['prizes'])):
            tt={
                    'winner':task['participants'][i],
                    'prize':task['prizes'][i]
                }
            raffles.append(tt)
    else:
        abort(409)
    return jsonify(raffles), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(port = 8080,debug=True)
