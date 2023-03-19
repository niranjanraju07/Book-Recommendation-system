from flask import Flask, request, jsonify, render_template
import pandas as pd
from pickle import load
import numpy
import random

user_base_reco=load(open('user-based.sav','rb'))
books=load(open('Books.sav','rb'))
user=load(open('Users.sav','rb'))
ratings=load(open('ratings.sav','rb'))
#popular_books=load(open('popular_books.sav','rb'))
#ubr = load(open('ubr.sav','rb'))
book_similarity_df=load(open('book_based.sav','rb'))

User_ratings=ratings.merge(user,on='User-ID')
ubr=User_ratings.merge(books,on='ISBN')

count=ratings.groupby('ISBN').count()['Book-Rating'].reset_index()
count.rename(columns={'Book-Rating':'Count'},inplace=True)
avg=ratings.groupby('ISBN').mean()['Book-Rating'].reset_index()
avg.rename(columns={'Book-Rating':'Average'},inplace=True)
popular_books=count.merge(avg,on='ISBN',how='left')
popular_books=popular_books[(popular_books['Count']>=250)&(popular_books['Average']>3)]
popular_books=popular_books.merge(books,on='ISBN',how='left')


def get_user_reco(customer_id):
    ind=list(user_base_reco.index)
    if ind.count(customer_id)>0:
        user_book=ratings[ratings['User-ID']==customer_id]['ISBN'].values 
        tem=list(user_base_reco.sort_values([customer_id],ascending=False).head(5).index)
        book_list=ratings[ratings["User-ID"].isin(tem)]
        book_list=list(book_list.sort_values('Book-Rating',ascending=False)['ISBN'].head(50))
        data=books[books['ISBN'].isin(book_list)]
        data=data.drop_duplicates()
        data=data[~data['ISBN'].isin(user_book)]
        data=data.head(10)
        u_book_title=list(data['Book-Title'].values)
        u_book_author=list(data['Book-Author'].values)
        u_book_year=list(data['Year-Of-Publication'].values)
        u_book_publisher=list(data['Publisher'].values)
        u_book_image=list(data['Image-URL-L'].values)
        return u_book_title,u_book_author,u_book_year,u_book_publisher,u_book_image
    else:
        isbn=list(popular_books["ISBN"])
        top=[]
        for i in range(0,10):
            top.append(random.choice(isbn))
        data=popular_books[popular_books['ISBN'].isin(top)]
        u_book_title=list(data['Book-Title'].values)
        u_book_author=list(data['Book-Author'].values)
        u_book_year=list(data['Year-Of-Publication'].values)
        u_book_publisher=list(data['Publisher'].values)
        u_book_image=list(data['Image-URL-L'].values)
        return u_book_title,u_book_author,u_book_year,u_book_publisher,u_book_image

def trending_book():
    data=popular_books.sort_values('Count',ascending=False).head(5)
    t_book_title=list(data['Book-Title'].values)
    t_book_author=list(data['Book-Author'].values)
    t_book_year=list(data['Year-Of-Publication'].values)
    t_book_publisher=list(data['Publisher'].values)
    t_book_image=list(data['Image-URL-L'].values)
    return t_book_title,t_book_author,t_book_year,t_book_publisher,t_book_image

def popular_country_books(customer_id):
    user_id=int(customer_id)
    country=list(ubr[ubr['User-ID']==user_id]['Country'].head(1))
    if len(country)>0:
        data=ubr[ubr['Country']==country[0]]
        count=ubr.groupby('ISBN').count()['User-ID'].reset_index()
        avg=ubr.groupby('ISBN').mean()['Book-Rating'].reset_index()
        data=count.merge(avg,on='ISBN',how='left')
        data=list(data[data['User-ID']>100].sort_values('Book-Rating',ascending=False)['ISBN'].head(5))
        data=books[books['ISBN'].isin(data)]
        c_book_title=list(data['Book-Title'].values)
        c_book_author=list(data['Book-Author'].values)
        c_book_year=list(data['Year-Of-Publication'].values)
        c_book_publisher=list(data['Publisher'].values)
        c_book_image=list(data['Image-URL-L'].values)
        return c_book_title,c_book_author,c_book_year,c_book_publisher,c_book_image,country[0]
    else:
        c_book_title=['0']
        return c_book_title,0,0,0,0,0

def popular_author(customer_id):
   
    Author=list(ubr[ubr['User-ID']==customer_id].groupby('Book-Author').count()['User-ID'].reset_index().sort_values('User-ID',ascending=False).head(1)['Book-Author'])
    if len(Author)>0:
        bk=ubr[ubr['Book-Author']==Author[0]].groupby('ISBN').mean()['Book-Rating'].reset_index()
        user_books=ubr[(ubr['User-ID']==customer_id) & (ubr['Book-Author']==Author[0])]['ISBN'].values
        new=bk[~bk['ISBN'].isin(user_books)]
        new=list(new.sort_values('Book-Rating')['ISBN'].tail(5))
        data=books[books['ISBN'].isin(new)]
        c_book_title=list(data['Book-Title'].values)
        c_book_author=list(data['Book-Author'].values)
        c_book_year=list(data['Year-Of-Publication'].values)
        c_book_publisher=list(data['Publisher'].values)
        c_book_image=list(data['Image-URL-L'].values)
        return c_book_title,c_book_author,c_book_year,c_book_publisher,c_book_image,Author[0]
    else:
        c_book_title=['0']
        return c_book_title,0,0,0,0,0
    
def popular_publisher(customer_id):
    
    Publisher=list(ubr[ubr['User-ID']==customer_id].groupby('Publisher').count()['User-ID'].reset_index().sort_values('User-ID',ascending=False).head(1)['Publisher'])
    if len(Publisher)>0:
        bk=ubr[ubr['Publisher']==Publisher[0]].groupby('ISBN').mean()['Book-Rating'].reset_index()
        user_books=ubr[(ubr['User-ID']==customer_id) & (ubr['Publisher']==Publisher[0])]['ISBN'].values
        new=bk[~bk['ISBN'].isin(user_books)]
        new=list(new.sort_values('Book-Rating')['ISBN'].tail(5))
        data=books[books['ISBN'].isin(new)]
        c_book_title=list(data['Book-Title'].values)
        c_book_author=list(data['Book-Author'].values)
        c_book_year=list(data['Year-Of-Publication'].values)
        c_book_publisher=list(data['Publisher'].values)
        c_book_image=list(data['Image-URL-L'].values)
        return c_book_title,c_book_author,c_book_year,c_book_publisher,c_book_image,Publisher[0]
    else:
        c_book_title=['0']
        return c_book_title,0,0,0,0,0

def user_profile(user_id):
    data=ubr[ubr['User-ID']==user_id]
    if len(data)>0:
        age=list(data['Age'].head(1))
        city=list(data['City'].head(1))
        state=list(data['State'].head(1))
        country=list(data['Country'].head(1))
        t_ratings=int(data['User-ID'].count())
        image=list(data['Image-URL-S'])
        book_title=list(data['Book-Title'])
        author=list(data['Book-Author'])
        publisher=list(data['Publisher'])
        ratings=list(data['Book-Rating'])
        return age[0],city[0],state[0],country[0],t_ratings,image,book_title,author,publisher,ratings
    else:
        book_title=[]
        return 0,0,0,0,0,0,book_title,0,0,0
    
def book_info(book_title):
    bk=ubr[ubr['Book-Title']==str(book_title)]
    t_ratings=int(bk['User-ID'].count())
    user=list(bk['User-ID'])
    ratings=list(bk['Book-Rating'])
    country=list(bk['Country'])
    image=list(bk['Image-URL-L'].head(1))
    isbn=list(bk['ISBN'].head(1))
    return t_ratings,user,ratings,country,image[0],isbn[0]

def book_reco(isbn):
    ind=list(book_similarity_df.index)
    if ind.count(isbn)>0:
        tem=list(book_similarity_df.sort_values([isbn],ascending=False).head(5).index)
        data=books[books['ISBN'].isin(tem)]
        data=data.drop_duplicates()
        b_book_title=list(data['Book-Title'].values)
        b_book_author=list(data['Book-Author'].values)
        b_book_year=list(data['Year-Of-Publication'].values)
        b_book_publisher=list(data['Publisher'].values)
        b_book_image=list(data['Image-URL-L'].values)
        return b_book_title,b_book_author,b_book_year,b_book_publisher,b_book_image
    else:
        b_book_title=['0']
        return b_book_title,0,0,0,0


app=Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/user',methods=['POST'])
def user():
    customer_id=int(request.form['user_input'])
    u_book_title,u_book_author,u_book_year,u_book_publisher,u_book_image=get_user_reco(customer_id)
    t_book_title,t_book_author,t_book_year,t_book_publisher,t_book_image=trending_book()
    c_book_title,c_book_author,c_book_year,c_book_publisher,c_book_image,country=popular_country_books(customer_id)
    a_book_title,a_book_author,a_book_year,a_book_publisher,a_book_image,author=popular_author(customer_id)
    p_book_title,p_book_author,p_book_year,p_book_publisher,p_book_image,publisher=popular_publisher(customer_id)
    return render_template("user.html",
                            usr=customer_id,
                            u_book_title=u_book_title,
                            u_book_author=u_book_author,
                            u_book_year=u_book_year,
                            u_book_publisher=u_book_publisher,
                            u_book_image=u_book_image,
                            t_book_title=t_book_title,
                            t_book_author=t_book_author,
                            t_book_year=t_book_year,
                            t_book_publisher=t_book_publisher,
                            t_book_image=t_book_image,
                            c_book_title=c_book_title,
                            c_book_author=c_book_author,
                            c_book_year=c_book_year,
                            c_book_publisher=c_book_publisher,
                            c_book_image=c_book_image,
                            country=country,
                            a_book_title=a_book_title,
                            a_book_author=a_book_author,
                            a_book_year=a_book_year,
                            a_book_publisher=a_book_publisher,
                            a_book_image=a_book_image,
                            author=author,
                            p_book_title=p_book_title,
                            p_book_author=p_book_author,
                            p_book_year=p_book_year,
                            p_book_publisher=p_book_publisher,
                            p_book_image=p_book_image,
                            publisher=publisher)

@app.route('/profile', methods=['POST'])
def profile():
    user_id=int(request.form['User_id'])
    age,city,state,country,t_ratings,image,book_title,author,publisher,ratings=user_profile(user_id)
    return render_template('profile.html',
                            user_id=user_id,
                            age=age,
                            city=city,
                            state=state,
                            country=country,
                            t_ratings=t_ratings,
                            image=image,
                            book_title=book_title,
                            author=author,
                            publisher=publisher,
                            ratings=ratings)
@app.route('/image/<book_title>/<author>/<publisher>/<year>/<user_id>')
def image(book_title,author,publisher,year,user_id):
    t_ratings,user,ratings,country,image,isbn=book_info(book_title)
    b_book_title,b_book_author,b_book_year,b_book_publisher,b_book_image=book_reco(isbn)
    return render_template('book.html', 
                            book_title=book_title,
                            author=author,
                            publisher=publisher,
                            year=year,
                            user_id=user_id,
                            t_ratings=t_ratings,
                            user=user,
                            ratings=ratings,
                            country=country,
                            image=image,
                            isbn=isbn,
                            b_book_title=b_book_title,
                            b_book_author=b_book_author,
                            b_book_year=b_book_year,
                            b_book_publisher=b_book_publisher,
                            b_book_image=b_book_image)

if __name__ == "__main__":
    app.run(debug=True)
