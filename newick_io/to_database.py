import psycopg2
import psycopg2.extras


def save_to_postgresql(the_tree, the_url_to_the_database):
  """
  the_tree = newick object
  
  psql $DATABASE_URL -> 
    CREATE EXTENSION postgis;
    CREATE EXTENSION hstore;
    
    CREATE TABLE "mytable" ("properties"  hstore, "geometry"  geometry);
  """
  print("inside 'save_to_postgresql'")
  print(the_tree.name)
    
  
  the_connection = psycopg2.connect(the_url_to_the_database)
  
  the_cursor = the_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
  the_cursor.execute("""DELETE FROM myTable;""")
  the_cursor.close()
  
  the_osm_datas_as_records = the_osm_datas.to_dict('records')
  
  the_counter = 1
  for a_record in the_osm_datas_as_records:
    
    if the_counter >= 10000:
      break
    
    # work on the geometry column
    a_record["geometry"] = a_record["geometry"].wkb_hex
    
    #print(a_record)
    
    the_cursor = the_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    psycopg2.extras.register_hstore(the_cursor)
    the_cursor.execute("""\
INSERT INTO mytable 
       ("osm_id", "osm_type", "geometry", "properties") 
VALUES (%(id)s, %(osm_type)s, %(geometry)s, %(properties)s);\
""", a_record)
    the_cursor.close()
    
    the_counter += 1
  
  the_connection.commit()
  the_connection.close()
  return
