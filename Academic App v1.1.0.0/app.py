from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB bağlantısı
client = MongoClient('mongodb://localhost:27017/')
db = client['universities']
firat_collection = db['firatuniversity']
izmir_collection = db['izmireconomyuniversity']
comments_collection = db['yazilimMComment']
likes_collection = db['yazilimMLikes']
users_collection = db['users']
user_likes_collection = db['user_likes']


@app.route('/yazilimM.html')
def firat_university_m():
    university = firat_collection.find_one({'Bölüm': 'Yazılım Mühendisliği (Mühendislik Fakültesi)'})
    comments = list(comments_collection.find({}))
    likes = list(likes_collection.find({}))
    liked_articles = [like['makale'] for like in likes if like['liked']]

    # Calculate like counts
    like_counts = {}
    for like in likes:
        makale = like['makale']
        if makale not in like_counts:
            like_counts[makale] = 0
        if like['liked']:
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
        return render_template('yazilimM.html', university_data=university, comments=comments, liked_articles=liked_articles, like_counts=like_counts, comment_counts=comment_counts)
    else:
        return "University data not found", 404

@app.route('/yazilimT.html')
def firat_university_t():
    university = firat_collection.find_one({'Bölüm': 'Yazılım Mühendisliği (Teknoloji Fakültesi)'})
    comments = list(comments_collection.find({}))
    likes = list(likes_collection.find({}))
    liked_articles = [like['makale'] for like in likes if like['liked']]

    # Calculate like counts
    like_counts = {}
    for like in likes:
        makale = like['makale']
        if makale not in like_counts:
            like_counts[makale] = 0
        if like['liked']:
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
        return render_template('yazilimT.html', university_data=university, comments=comments, liked_articles=liked_articles, like_counts=like_counts, comment_counts=comment_counts)
    else:
        return "University data not found", 404

@app.route('/izmireconomy.html')
def izmir_economy_university():
    university = izmir_collection.find_one({'Bölüm':'Yazılım Mühendisliği'})
    comments = list(comments_collection.find({}))
    likes = list(likes_collection.find({}))
    liked_articles = [like['makale'] for like in likes if like['liked']]

    # Calculate like counts
    like_counts = {}
    for like in likes:
        makale = like['makale']
        if makale not in like_counts:
            like_counts[makale] = 0
        if like['liked']:
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
        return render_template('izmireconomy.html', university_data=university, comments=comments, liked_articles=liked_articles, like_counts=like_counts, comment_counts=comment_counts)
    else:
        return "University data not found", 404

@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    data = request.get_json()
    akademisyen = data.get('akademisyen')
    makale = data.get('makale')
    comment = data.get('comment')
    user_name = 'Misafir Kullanıcı'
    

    if not akademisyen or not makale or not comment or not user_name:
        return jsonify({'success': False, 'message': 'Missing data'}), 400

    # Save the comment to the database
    comment_data = {
        'akademisyen': akademisyen,
        'makale': makale,
        'comment': comment,
        'user_name': user_name,
        
    }
    comments_collection.insert_one(comment_data)

    return jsonify({'success': True, 'message': 'Comment submitted successfully'})

@app.route('/toggle_like', methods=['POST'])
def toggle_like():
    data = request.get_json()
    akademisyen = data.get('akademisyen')
    makale = data.get('makale')
    liked = data.get('liked')
    user_name = 'Misafir Kullanıcı'

    if not akademisyen or not makale:
        return jsonify({'success': False, 'message': 'Missing data'}), 400

    # Update the like status in the database
    like_data = {
        'akademisyen': akademisyen,
        'makale': makale,
        'liked': liked,
        'user_name': user_name
    }
    likes_collection.update_one(
        {'akademisyen': akademisyen, 'makale': makale},
        {'$set': like_data},
        upsert=True
    )

    return jsonify({'success': True, 'message': 'Like status updated successfully'})

if __name__ == '__main__':
    app.run(debug=True)
@app.route('/profile.html')
def profile():
    user_name = 'Misafir Kullanıcı'  # Bu örnekte kullanıcı adı sabit, gerçek uygulamada oturumdan alınabilir

    # Kullanıcı bilgilerini al
    user = users_collection.find_one({'user_name': user_name})
    if not user:
        # Kullanıcı yoksa, yeni bir kullanıcı oluştur
        user = {
            'user_name': user_name,
            'following_count': 0,
            'followers_count': 0
        }
        users_collection.insert_one(user)

    # Kullanıcının beğendiği makaleleri al
    liked_articles = list(user_likes_collection.find({'user_name': user_name, 'liked': True}))

    # Kullanıcının okuduğu makaleleri al
    read_articles = list(comments_collection.find({'user_name': user_name}))

    return render_template('profile.html', liked_articles=liked_articles, read_articles=read_articles, following_count=user['following_count'], followers_count=user['followers_count'])

if __name__ == '__main__':
    app.run(debug=True)
