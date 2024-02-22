from flask import Flask, render_template, request, redirect, url_for
import json
import os


app = Flask(__name__)

@app.route('/')
def index():
    articles = load_articles()
    return render_template('index.html', articles=articles)

@app.route('/create', methods=['GET', 'POST'])
def create_article():
    if request.method == 'POST':
        article_title = request.form['article_title']
        main_author_name = request.form['main_author_name']
        main_author_affiliation = request.form['main_author_affiliation']
        main_author_orcid = request.form['main_author_orcid']
        
        coauthor_names = request.form.getlist('coauthor_name[]')
        coauthor_affiliations = request.form.getlist('coauthor_affiliation[]')
        coauthor_orcids = request.form.getlist('coauthor_orcid[]')
        
        coauthors = []
        for name, affiliation, orcid in zip(coauthor_names, coauthor_affiliations, coauthor_orcids):
            if name.strip():  # Verifica que el nombre no esté en blanco
                coauthor = {
                    'nombre': name,
                    'datos': affiliation,
                    'orcid': orcid
                }
                coauthors.append(coauthor)

        abstract = request.form['abstract']
        keywords = request.form['keywords'].split(', ')
        introduction = request.form['introduction']

        sections_titles = request.form.getlist('section_title[]')
        sections_contents = request.form.getlist('section_content[]')

        sections = []
        for title, content in zip(sections_titles, sections_contents):
            section = {
                'titulo': title,
                'contenido': content,
                'subsecciones': []
            }

            subsection_titles_key = f'subsection_title[{len(sections)}][]'
            subsection_contents_key = f'subsection_content[{len(sections)}][]'

            subsection_titles = request.form.getlist(subsection_titles_key)
            subsection_contents = request.form.getlist(subsection_contents_key)

            for sub_title, sub_content in zip(subsection_titles, subsection_contents):
                if sub_title.strip():  # Verifica que el título no esté en blanco
                    subsection = {
                        'subtitulo': sub_title,
                        'contenido': sub_content
                    }
                    section['subsecciones'].append(subsection)

            sections.append(section)

        conclusion = request.form['conclusion']

        article = {
            'Título_de_articulo': article_title,
            'autor_principal': {
                'nombre': main_author_name,
                'datos': main_author_affiliation,
                'orcid': main_author_orcid
            },
            'coautores': coauthors,
            'resumen': abstract,
            'palabras_clave': keywords,
            'introduccion': introduction,
            'secciones': sections,
            'conclusion': conclusion
        }

        save_article(article)
        return redirect(url_for('index'))

    return render_template('create.html')

def load_articles():
    articles = []
    for filename in os.listdir('articles'):
        with open(os.path.join('articles', filename), 'r', encoding='utf-8') as file:
            try:
                article = json.load(file)
                articles.append(article)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in file {filename}: {str(e)}")
    return articles


def save_article(article):
    if not os.path.exists('articles'):
        os.makedirs('articles')

    article_filename = f"{article['Título_de_articulo'].replace(' ', '_')}.json"
    article_path = os.path.join('articles', article_filename)

    with open(article_path, 'w', encoding='utf-8') as file:
        json.dump(article, file, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    app.run(debug=True)
