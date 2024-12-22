from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB bağlantısı
client = MongoClient('mongodb://localhost:27017/')
db = client['universities']
firat_collection = db['firatuniversity']
comments_collection = db['yazilimMComment']
likes_collection = db['yazilimMLikes']
user_collection = db['users']  # Yeni kullanıcı koleksiyonu
izmir_collection = db['izmireconomyuniversity']  # İzmir Ekonomi Üniversitesi koleksiyonu

# Kullanıcı verilerini MongoDB'ye ekleyelim
user_collection.update_one(
    {'username': 'guest_user'},
    {
        '$set': {
            'username': 'guest_user',
            'first_name': 'Misafir',
            'last_name': 'Kullanıcı',
            'likes_given': 0,
            'likes_received': 0,
            'comments_made': 0,
            'birthdate': '20/09/2003',
            'university': 'Fırat Üniversitesi',
            'status': 'Lisans Öğrencisi',
            'interests': ['Kod Yazmak', 'Arkadaş Canlısı', 'Müzik Dinlemeyi Sever']
        }
    },
    upsert=True
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user.html')
def user_profile():
    user = user_collection.find_one({'username': 'guest_user'})
    return render_template('user.html', user=user)

@app.route('/yazilimM.html')
def firat_university_m():
    university = firat_collection.find_one({'Bölüm': 'Yazılım Mühendisliği (Mühendislik Fakültesi)'})
    comments = list(comments_collection.find({}))
    likes = list(likes_collection.find({}))
    liked_articles = [like['makale'] for like in likes if like.get('liked', False)]
    like_counts = {like['makale']: like.get('count', 0) for like in likes}
    comment_counts = {comment['makale']: comments_collection.count_documents({'makale': comment['makale']}) for comment in comments}
    return render_template('yazilimM.html', university_data=university, comments=comments, liked_articles=liked_articles, like_counts=like_counts, comment_counts=comment_counts)

@app.route('/yazilimT.html')
def firat_university_t():
    university = firat_collection.find_one({'Bölüm': 'Yazılım Mühendisliği (Teknoloji Fakültesi)'})
    comments = list(comments_collection.find({}))
    likes = list(likes_collection.find({}))
    liked_articles = [like['makale'] for like in likes if like.get('liked', False)]
    like_counts = {like['makale']: like.get('count', 0) for like in likes}
    comment_counts = {comment['makale']: comments_collection.count_documents({'makale': comment['makale']}) for comment in comments}
    return render_template('yazilimT.html', university_data=university, comments=comments, liked_articles=liked_articles, like_counts=like_counts, comment_counts=comment_counts)

@app.route('/toggle_like', methods=['POST'])
def toggle_like():
    data = request.json
    akademisyen = data['akademisyen']
    makale = data['makale']
    liked = data['liked']
    user_name = data['user_name']

    if liked:
        likes_collection.update_one(
            {'makale': makale},
            {'$inc': {'count': 1}},
            upsert=True
        )
    else:
        likes_collection.update_one(
            {'makale': makale},
            {'$inc': {'count': -1}},
            upsert=True
        )
        # Ensure like count does not go below 0
        likes_collection.update_one(
            {'makale': makale, 'count': {'$lt': 0}},
            {'$set': {'count': 0}}
        )

    return jsonify({'success': True})

@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    data = request.json
    akademisyen = data['akademisyen']
    makale = data['makale']
    comment = data['comment']
    user_name = data['user_name']

    comments_collection.insert_one({
        'akademisyen': akademisyen,
        'makale': makale,
        'comment': comment,
        'user_name': user_name
    })

    return jsonify({'success': True})

@app.route('/izmirE.html')
def izmir_economy_university():
    university = izmir_collection.find_one({'Bölüm': 'Yazılım Mühendisliği'})
    comments = list(comments_collection.find({}))
    likes = list(likes_collection.find({}))
    liked_articles = [like['makale'] for like in likes if like.get('liked', False)]

    # Calculate like counts
    like_counts = {}
    for like in likes:
        makale = like['makale']
        if makale not in like_counts:
            like_counts[makale] = 0
        if like.get('liked', False):
            like_counts[makale] += 1

    # Calculate comment counts
    comment_counts = {}
    for comment in comments:
        makale = comment['makale']
        if makale not in comment_counts:
            comment_counts[makale] = 0
        comment_counts[makale] += 1

    if university:
        print("University data found:", university)  # Hata ayıklama için veri yazdırma
        university.pop('_id', None)  # "_id" alanını şablonda göstermemek için kaldırıyoruz
        return render_template('izmirE.html', university_data=university, comments=comments, liked_articles=liked_articles, like_counts=like_counts, comment_counts=comment_counts)
    else:
        return "University data not found", 404

if __name__ == '__main__':
    app.run(debug=True)