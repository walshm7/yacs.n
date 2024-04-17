from psycopg2.extras import RealDictCursor
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


##!!!!!!!!!!!!!!!!!!!!
## TO UPDATE WITH NEW PATHWAYS/CATEGORIES, CHANGE JSON FILE AT BOTTOM OF PAGE
##!!!!!!!!!!!!!!!!!!!!

# https://stackoverflow.com/questions/54839933/importerror-with-from-import-x-on-simple-python-files
if __name__ == "__main__":
    import connection
else:
    from . import connection

class Pathways:
    def __init__(self, db_conn, cache):
        self.db_conn = db_conn
        self.cache = cache
    def add_bulk_pathways(self, json_data): #function is called in app.py
        # Connect to the SQL database
        conn = self.db_conn.get_connection()

        with conn.cursor(cursor_factory=RealDictCursor) as transaction:
            try:
                # Iterate over each entry in the JSON data
                for entry in json_data:
                    for sub in entry['Pathways']:
                        if 'Compatible minor(s)' in sub:
                            #print(sub['Compatible minor(s)'])
                            minor = sub['Compatible minor(s)'][0]
                        else:
                            minor = None
                        for desc in sub:

                            if desc != 'Name' and (desc != 'Compatible minor(s)' and 'Compatible minor(s)' not in desc):
                                for cor in sub[desc]:
                                    #cor = cor.split('-')
                                    #print(cor.split('-'))
                                    if len(cor.split('-')) > 1:
                                        cor2 = cor.split('-')[1]
                                        cor1 = cor.split('-')[0]

                                    elif len(cor.split('–')) > 1:
                                        cor2 = cor.split('–')[1]
                                        cor1 = cor.split('–')[0]
                                    elif len(cor.split(' ',2)) >2:
                                        split = cor.split(' ',2)
                                        cor2 = split[2]
                                        cor1 = split[0] + ' ' + split[1]
                                        #print(cor1)
                                    else:
                                        cor2 = None
                                        cor1 = cor.split('-')[0]
                                        #print(cor1)

                                # print(desc)
                                    try:
                                        # Insert pathways and corresponding category into "pathway" table (tables/pathways.py)
                                        transaction.execute(
                                            """
                                            INSERT INTO pathways (
                                                pathway,
                                                catagory,
                                                course,
                                                course_name,
                                                description,
                                                compatible_minor
                                            ) 
                                            VALUES (
                                                NULLIF(%(pathway)s, ''),
                                                NULLIF(%(catagory)s, ''),
                                                NULLIF(%(course)s, ''),
                                                NULLIF(%(course_name)s, ''),
                                                NULLIF(%(description)s, ''),
                                                NULLIF(%(compatible_minor)s, '')  
                                            )
                                            ON CONFLICT DO NOTHING;
                                            """,
                                            {
                                                "pathway": sub['Name'][0],
                                                "catagory": entry['Category Name'][0],
                                                "course": cor1,
                                                "course_name": cor2,
                                                "description": desc,
                                                "compatible_minor": minor

                                            }
                                        )
                                    except Exception as e:
                                        # Roll back the transaction and return the exception if an error occurs
                                        print("THIS IS THE EXCEPTION:", e)
                                        conn.rollback()
                                        return (False, e)
            except ValueError as ve:
                # Return an error message if the JSON data is invalid
                return (False, f"Invalid JSON data: {str(ve)}")

            # Commit the transaction if all entries are inserted successfully
            conn.commit()

            # Invalidate cache to ensure new data is retrieved
            self.clear_cache()

            # Return success status and no error
            return True, None


    # all pathways
    def get_all_pathways(self):
        return self.db_conn.execute(""" 
                            SELECT DISTINCT pathway FROM pathways
                    """, None, True)
    # list all catagorys
    def get_all_catagorys(self):
        return self.db_conn.execute(""" 
                            SELECT DISTINCT catagory FROM pathways
                    """, None, True)
    #gets pathway by catagory
    def get_pathways_by_catagory(self, catagory):
        if catagory is not None:
            sql = """
                        SELECT
                            *
                        FROM
                            pathways
                        WHERE
                            catagory = '%s'
                        """
            return self.db_conn.execute(sql, (catagory,), True)

    # gets courses by pathway
    def get_courses_by_pathway(self, pathway):
        if pathway is not None:
            sql = """
                SELECT
                    course
                FROM
                    pathways
                WHERE
                    pathway = '%s'
            """
        return self.db_conn.execute(sql, (pathway,), True)

    #get minor by pathway
    def get_compatable_minor_by_pathway(self, pathway):
        if pathway is not None:
            sql = """
                SELECT 
                    compatible_minor
                FROM 
                    pathways
                WHERE
                    pathway = '%s'
            """
        return self.db_conn.execute(sql, (pathway,), True)

    def get_course_info_by_course(self, course):
        if pathway is not None:
            sql = """
                SELECT 
                    course_name, description
                FROM 
                    pathways
                WHERE
                    course = '%s'
            """
        return self.db_conn.execute(sql, (course,), True)
    def clear_cache(self):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            loop.create_task(self.cache.clear(namespace="API_CACHE"))
        else:
            asyncio.run(self.cache.clear("API_CACHE"))
