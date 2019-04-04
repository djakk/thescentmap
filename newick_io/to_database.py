import psycopg2
import psycopg2.extras

import shapely
import shapely.geometry


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
  
  # put the descendants on an half-circle and the father in the middle of the halfed circle
  the_geometry_of_the_center = shapely.geometry.Point(0, 0)
  
  the_counter = 1
  for a_sub_tree in the_tree.descendants:
    
    if the_counter >= 10000:
      break
    
    the_geometry = shapely.geometry.LineString(the_geometry_of_the_center, shapely.geometry.Point(100, 100))
    
    the_cursor = the_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    psycopg2.extras.register_hstore(the_cursor)
    the_cursor.execute("""\
INSERT INTO mytable 
       ("geometry", "properties") 
VALUES (%(geometry)s, %(properties)s);\
""", {"geometry" : the_geometry.wkb_hex, "properties" : {"name" : a_sub_tree.name}})
    the_cursor.close()
    
    the_counter += 1
  
  the_connection.commit()
  the_connection.close()
  return
