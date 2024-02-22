import json

def create_tex_file(data):
    def format_author(author, affiliation_number, corresponding=False):
        author_number = f"{affiliation_number},*" if corresponding else str(affiliation_number)
        return rf"\author[{author_number}]{{{author['nombre'].replace('_', r' ').title()} \orcidlink{{{author['orcid']}}}}}"

    def format_affiliation(author, affiliation_number):
        return rf"\affil[{affiliation_number}]{{{author['datos'].replace('_', r' ').title()}}}"

    def format_abstract_keywords(content):
        return content.replace('_', r' ')

    def format_section(section):
        formatted_section = rf"\section{{{section['titulo'].replace('_', r' ').title()}}}" + "\n"
        formatted_section += section["contenido"].replace('_', r' ') + "\n"
        
        # Subsections
        for subsection in section.get("subsecciones", []):
            formatted_section += rf"\subsection{{{subsection['subtitulo'].replace('_', r' ').title()}}}" + "\n"
            formatted_section += subsection["contenido"].replace('_', r' ') + "\n"

        return formatted_section

    def format_conclusion(conclusion):
        return rf"\section{{Conclusion}}" + "\n" + conclusion.replace('_', r' ')

    # Create affiliation map
    affiliation_map = {}
    affiliations = []
    affiliation_counter = 1

    # Main author
    author = data["autor_principal"]
    affiliation = author['datos']
    if affiliation not in affiliation_map:
        affiliation_map[affiliation] = affiliation_counter
        affiliations.append(format_affiliation(author, affiliation_counter))
        affiliation_counter += 1

    # Coauthors
    for author in data["coautores"]:
        affiliation = author['datos']
        if affiliation not in affiliation_map:
            affiliation_map[affiliation] = affiliation_counter
            affiliations.append(format_affiliation(author, affiliation_counter))
            affiliation_counter += 1

    tex_content = r"""
\documentclass{article}
\usepackage[margin=2cm]{geometry}
\usepackage{orcidlink}
\usepackage{authblk}
\usepackage[utf8]{inputenc}
\usepackage{longtable}
\usepackage{graphicx}
\usepackage{subfig}

\date{}                     
\setcounter{Maxaffil}{0}
\renewcommand\Affilfont{\itshape\small}
\providecommand{\keywords}[1]
{
  \small  
  \textbf{\textit{Keywords---}} #1
} 

\title{%s}
%s
\begin{document}

\maketitle

\begin{abstract}
%s
\end{abstract}

\keywords{%s}

\section{Introduction}
%s

%s
\end{document}
"""

    # Title
    title = data["Título_de_articulo"].replace('_', r' ').title()

    # Authors
    main_author = data["autor_principal"]
    authors = [format_author(main_author, affiliation_map[main_author['datos']], corresponding=True)]
    authors += [format_author(author, affiliation_map[author['datos']]) for author in data["coautores"]]

    # Abstract
    abstract = format_abstract_keywords(data["resumen"])

    # Keywords
    keywords = ", ".join(data["palabras_clave"]).replace('_', r' ')

    # Sections
    sections = ""
    for section in data["secciones"]:
        sections += format_section(section)

    # Conclusion
    conclusion = format_conclusion(data["conclusion"])

    # Fill in the template
    tex_content = tex_content % (title, "\n".join(authors + affiliations), abstract, keywords, data["introduccion"].replace('_', r' '), sections + conclusion)

    # Write to a .tex file
    with open("zzzz.tex", "w", encoding="utf-8") as tex_file:
        tex_file.write(tex_content)

if __name__ == "__main__":
    # Load JSON data
    with open("prueba_articulo_420.json", "r", encoding="utf-8") as json_file:
        json_data = json.load(json_file)

    # Create the .tex file
    create_tex_file(json_data)
