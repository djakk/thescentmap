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
  print(the_tree.ascii_art(show_internal=False, strict=True))
  
  # put the descendants on an half-circle and the father in the middle of the halfed circle
  calculate_the_geometries(the_tree)
  for a_node in the_tree.walk():
    print(a_node.geometry)
  
  the_connection = psycopg2.connect(the_url_to_the_database)
  
  the_cursor = the_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
  the_cursor.execute("""DELETE FROM myTable;""")
  the_cursor.close()
    
  the_counter = 1
  for a_sub_tree in the_tree.descendants:
    
    if the_counter >= 10000:
      break
    
    the_sub_tree_longitude = the_geometry_of_the_center.coords[0][0] + 100 *the_counter
    the_sub_tree_latitude = the_geometry_of_the_center.coords[0][1] + 100
    the_sub_tree_last_point = shapely.geometry.Point(the_sub_tree_longitude, the_sub_tree_latitude)
    the_line_as_a_shapely_geometry = shapely.geometry.LineString([the_geometry_of_the_center, the_sub_tree_last_point])
    a_sub_tree.geometry = the_sub_tree_last_point
    
    the_cursor = the_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    psycopg2.extras.register_hstore(the_cursor)
    the_cursor.execute("""\
INSERT INTO mytable 
       ("geometry", "properties") 
VALUES (%(geometry)s, %(properties)s);\
""", {"geometry" : the_line_as_a_shapely_geometry.wkb_hex, "properties" : {"name" : a_sub_tree.name}})
    the_cursor.close()
    
    the_counter += 1
  
  the_connection.commit()
  the_connection.close()
  
  
def calculate_the_geometries(the_tree):
  """recursive function"""
  try:
    the_geometry_of_the_center = the_tree.geometry
  except AttributeError:
    the_geometry_of_the_center = shapely.geometry.Point(0, 0)
    the_tree.geometry = the_geometry_of_the_center
    
  the_counter = 1

  for a_sub_tree in the_tree.descendants:

    the_sub_tree_longitude = the_geometry_of_the_center.coords[0][0] + 100 *the_counter
    the_sub_tree_latitude = the_geometry_of_the_center.coords[0][1] + 100
    the_sub_tree_last_point = shapely.geometry.Point(the_sub_tree_longitude, the_sub_tree_latitude)
    #the_line_as_a_shapely_geometry = shapely.geometry.LineString([the_geometry_of_the_center, the_sub_tree_last_point])
    a_sub_tree.geometry = the_sub_tree_last_point
    calculate_the_geometries(a_sub_tree)

    the_counter += 1

