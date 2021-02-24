''' A script to generate Wikipedia articles '''
import wikipedia

# Import flask library
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

#  Create a flask object of app.py
app = Flask(__name__)


# Configure the Database
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


# Define the Database
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # will store the article title
    title = db.Column(db.String(80), nullable=False)
    # will store the article url
    url = db.Column(db.String(80), nullable=False)
    
    def __repr__(self):
        return '<Article %r>'  % self.article



# Function to Generate Wikipedia titles and their associate URLs
@app.route('/wiki_gen', methods=['POST','GET'])
def wiki_gen():
    titles = wikipedia.random(pages=3)
    
    for title in titles:
        import wikipediaapi
        # initialize wikipedia object
        wiki = wikipediaapi.Wikipedia('en')
        
        # Turn the titles into pages
        page_py = wiki.page(title)
        # Get page url
        page_url = page_py.fullurl
        
        # Save the page and URL in ab dictionary
        article = {
            'article_title':title,
            'article_url':page_url
        }
                
        print(article)
                
    return article
    


# Create a default homepage route
@app.route('/', methods=['POST', 'GET'])
def index():
    
    if request.method == 'POST':
    
            article = wiki_gen()
        
            new_article = Article(title=article['article_title'], url=article['article_url'])
          
            try:
                db.session.add(new_article)
                db.session.commit()
                return redirect('/')
        
            except:
                return 'There was an issue getting your article from the database'
        
    else:
        articles = Article.query.all()
        return render_template('index.html', articles=articles)


if __name__ == '__main__':
    app.run(debug=True)