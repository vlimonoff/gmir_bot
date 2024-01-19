import psycopg2

def connect_to_db():
    return psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432',
    )

def get_sections():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM "Sections"')
    sections = cur.fetchall()
    cur.close()
    conn.close()
    return sections

def get_subsections(section_id):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(
        f'SELECT * FROM "Subsections" WHERE section_id = {section_id}'
    )
    subsections = cur.fetchall()
    cur.close()
    conn.close()
    return subsections

def get_halls_by_section(section_id):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(
        f'SELECT * FROM "Halls" WHERE section_id = {section_id}'
    )
    halls = cur.fetchall()
    cur.close()
    conn.close()
    return halls

def get_halls_by_subsection(subsection_id):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(
        f'SELECT * FROM "Halls" WHERE subsection_id = {subsection_id}'
    )
    halls = cur.fetchall()
    cur.close()
    conn.close()
    return halls

def get_exhibits(hall):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(
        f'''SELECT id, number_in_hall FROM "Exhibits"
            WHERE hall_id = {hall}'''
    )
    exhibits = cur.fetchall()
    cur.close()
    conn.close()
    return exhibits

def get_exhibit_info(exhibit):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(
        f'SELECT * FROM "Exhibits" WHERE id = {exhibit}'
    )
    exhibit = cur.fetchall()
    cur.close()
    conn.close()
    return exhibit