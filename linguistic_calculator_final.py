import sqlite3

# Connect to (or create) the SQLite database
conn = sqlite3.connect('verbs.db')
cursor = conn.cursor()

# Create the 'verbs' table with verb base being the primary key
create_table_query = """
CREATE TABLE IF NOT EXISTS verbs (
    id INTEGER PRIMARY KEY,
    base TEXT NOT NULL,
    simple_past TEXT NOT NULL,
    past_participle TEXT NOT NULL,
    gerund TEXT NOT NULL
);
"""

# Insert sample data into the 'verbs' table
insert_data_query = """
INSERT OR IGNORE INTO verbs (base, simple_past, past_participle, gerund) VALUES 
('go', 'went', 'gone', 'going'),
('be', 'was/were', 'been', 'being'),
('eat', 'ate', 'eaten', 'eating'),
('see', 'saw', 'seen', 'seeing'),
('take', 'took', 'taken', 'taking'),
('watch', 'watched', 'watched', 'watching'),
('study', 'studied', 'studied', 'studying');
"""

# Execute the queries
cursor.execute(create_table_query)
cursor.executescript(insert_data_query)

# Commit the changes and close the connection
conn.commit()
conn.close()

# Connect to SQLite database
def connect_to_db():
  conn = sqlite3.connect('verbs.db')
  return conn

# Load verbs from the database
def load_using_verbs(conn):
    c = conn.cursor()
    c.execute("SELECT base, simple_past, past_participle, gerund FROM verbs")
    verbs = c.fetchall()
    using_verbs = {}
    for base, simple_past, past_participle, gerund in verbs:
        using_verbs[base] = {
            'simple_past': simple_past,
            'past_participle': past_participle,
            'gerund': gerund
        }
    return using_verbs

# Form the correct verb conjugation based on tense and aspect
def conjugate(verb, tense, aspect, using_verbs):
    #List exceptions
    suffixes_es1 = {"x", "s", "z", "ch", "sh"}
    suffixes_es2 = {"io", "eo", "oo", "ao", "uo"}

    if tense == 'present':
        if aspect == 'progressive perfect':
            if verb == "be":
                return f"have/has been"
            return f"have/has been {using_verbs.get(verb, {}).get('gerund')}"
        elif aspect == 'progressive': 
            if verb == "be": #This verb doesn't require 'being' in the progressive aspect
                return f"am/is/are"
            return f"am/is/are {using_verbs.get(verb, {}).get('gerund')}"
        elif aspect == 'perfect':
            return f"have/has {using_verbs.get(verb, {}).get('past_participle')}"
        elif aspect == 'simple':
        # Check the verb whether it ends with special suffixes or not
            if any(verb.endswith(suffix) for suffix in suffixes_es1):
                return f"{verb}/{verb}es"
            elif any(verb.endswith(suffix) for suffix in suffixes_es2):
                return f"{verb}/{verb}es"
            elif verb.endswith('y'):
                return f"{verb}/{verb[:-1]}ies"  # Remove 'y' and add 'ies'
            elif verb.endswith('f'):
                return f"{verb}/{verb[:-1]}ves"  # Remove 'f' and add 'ves'
            elif verb.endswith('fe'):
                return f"{verb}/{verb[:-2]}ves"  # Remove 'fe' and add 'ves'
            else:
                if verb == "be": 
                    return f"am/is/are"
                return f"{verb}/{verb}s"  # Regular cases
    
    elif tense == 'past':
        if aspect == 'simple':
            return using_verbs.get(verb, {}).get('simple_past')
        elif aspect == 'progressive':
            if verb == "be": #This verb doesn't require 'being' in the progressive aspect
                return f"was/were"
            return f"was/were {using_verbs.get(verb, {}).get('gerund')}"
        elif aspect == 'perfect':
            return f"had {using_verbs.get(verb, {}).get('past_participle')}"
        elif aspect == 'progressive perfect':
            if verb == "be":
                return f"had been"
            return f"had been {using_verbs.get(verb, {}).get('gerund')}"
    
    elif tense == 'future':
        if aspect == 'simple':
            return f"will {verb}"
        elif aspect == 'progressive':
            if verb == "be":
                return f"will be"
            return f"will be {using_verbs.get(verb, {}).get('gerund')}"
        elif aspect == 'perfect':
            return f"will have {using_verbs.get(verb, {}).get('past_participle')}"
        elif aspect == 'progressive perfect':
            if verb == "be":
                return f"will have been"
            return f"will have been {using_verbs.get(verb, {}).get('gerund')}"
    
    return "The verb inserted is unknown or not added to the calculator."

# Main function to get input and provide the conjugated form
def main():
    conn = connect_to_db()
    using_verbs = load_using_verbs(conn)

    # Input from the user
    verb = input("Enter a verb (ex: be, eat,... ): ").strip().lower()
    
    # Choose tense       
    print("Choose the tense:")
    print("1. Present")
    print("2. Past")
    print("3. Future")
    tense_choice = input("Enter the number of your choice: ").strip()
    tense_type = {
            "1": "present",
            "2": "past",
            "3": "future"
    }
    tense = tense_type.get(tense_choice, None)
				
	# Choose aspect       
    print("Choose the aspect:")
    print("1. Simple")
    print("2. Progressive")
    print("3. Perfect")
    print("4. Progressive Perfect")
    aspect_choice = input("Enter the number of your choice: ").strip()
    aspect_type = {
            "1": "simple",
            "2": "progressive",
            "3": "perfect",
            "4": "progressive perfect"
    }

    aspect = aspect_type.get(aspect_choice, None)

    # Conjugate the verb
    if tense and aspect: #This if for checking if the input is valid or not
        conjugated_form = conjugate(verb, tense, aspect, using_verbs)
        print(f"The correct form of the verb '{verb}' in {aspect} {tense} is:", conjugated_form)
    else:
        print("Invalid tense or aspect choice.")
    
    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()
