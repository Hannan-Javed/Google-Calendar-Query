from database_manager import DatabaseManager

def main():
    
    db_manager = DatabaseManager()

    with open('queries.sql', 'r') as file:
        lines = file.read().splitlines()

    query_comment = ''
    query = ''
    for line in lines:
        if line == '': continue
        elif line.startswith('--'):
            query_comment = line.strip()
        elif line.endswith(';'):
            query += line.strip()
            print(f"Query: {query_comment[2:].strip()}") if query_comment!='' else None
            headers, results = db_manager.query_database(query)
            db_manager.format_results(headers, results)
            print()
            query_comment = ''
            query = ''
        else:
            query += line.strip() + ' '
    
if __name__ == '__main__':
    main()