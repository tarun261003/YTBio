import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS links
                 (id INTEGER PRIMARY KEY, category TEXT, link TEXT)''')
    conn.commit()
    conn.close()

def add_link(category, link):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO links (category, link) VALUES (?, ?)", (category, link))
    conn.commit()
    conn.close()

def delete_link(link_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM links WHERE id=?", (link_id,))
    conn.commit()
    conn.close()

def get_links(search_query=None):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    if search_query:
        c.execute("SELECT * FROM links WHERE link LIKE ?", ('%' + search_query + '%',))
    else:
        c.execute("SELECT * FROM links")
    links = c.fetchall()
    conn.close()
    return links
