import psycopg2
import psycopg2.extras

import shapely
import shapely.geometry

import math


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
  the_counter = 1
  calculate_the_geometries(the_tree, the_counter)
  for a_node in the_tree.walk():
    print(a_node.geometry)
  
  the_connection = psycopg2.connect(the_url_to_the_database)
  
  the_cursor = the_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
  the_cursor.execute("""DELETE FROM myTable;""")
  the_cursor.close()
    
  the_counter = 1
  save_a_tree_as_a_geometry_to_postgresql(the_tree, the_connection, the_counter)
    
  the_connection.commit()
  the_connection.close()
  
  
def calculate_the_geometries(the_tree, the_counter):
  """
  recursive function
  coordinates of a circle : (x – a)² + (y – b)² = R² (center = (a,b))
  -> x² + a² - 2ax + y² + a² - 2ay = R²
  coordinates of a straight line : mx + ny + p = 0 ; 
  passing through (a,b) : ma + nb + p = 0 -> p = -ma -nb -> equation : m(x - a) + n(y - b) = 0
  
  circle : r²(θ) - 2r(θ) * r° * cos(θ - φ) + r°² = a², center = (r°, φ), radius = a
  simple circle : r(θ) = 100
  simple straight line : θ = 45°
  in cartesian coordinates : x = r cos(θ) + x° ; y = r sin(θ) + y° ; (x°,y°) = center of the polaroid coordinates
  """
  the_geometry_of_the_center = shapely.geometry.Point(0, 0)
  try:
    the_geometry_of_the_center = the_tree.geometry
  except AttributeError:
    the_tree.geometry = the_geometry_of_the_center
  
  the_number_of_descendants = len(the_tree.descendants)
  the_other_counter = -1* the_number_of_descendants // 2
  
  for a_sub_tree in the_tree.descendants:
    
    the_sub_tree_longitude = the_geometry_of_the_center.coords[0][0] + (100 / the_counter) *math.cos(the_other_counter * 3.14 / the_number_of_descendants)
    the_sub_tree_latitude = the_geometry_of_the_center.coords[0][1] + (100 / the_counter) *math.sin(the_other_counter * 3.14 / the_number_of_descendants)
    the_sub_tree_last_point = shapely.geometry.Point(the_sub_tree_longitude, the_sub_tree_latitude)
    #the_line_as_a_shapely_geometry = shapely.geometry.LineString([the_geometry_of_the_center, the_sub_tree_last_point])
    a_sub_tree.geometry = the_sub_tree_last_point
    calculate_the_geometries(a_sub_tree, the_counter +1)
    
    the_other_counter += 1


def save_a_tree_as_a_geometry_to_postgresql(the_tree, the_connection, the_counter):
  """recursive function"""
  for a_sub_tree in the_tree.descendants:
    
    if the_counter >= 10000:
      return
    
    the_line_as_a_shapely_geometry = shapely.geometry.LineString([the_tree.geometry, a_sub_tree.geometry])
    
    the_cursor = the_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    psycopg2.extras.register_hstore(the_cursor)
    the_cursor.execute("""\
INSERT INTO mytable 
       ("geometry", "properties") 
VALUES (%(geometry)s, %(properties)s);\
""", {"geometry" : the_line_as_a_shapely_geometry.wkb_hex, "properties" : {"name" : a_sub_tree.name}})
    the_cursor.close()
    
    the_counter += 1
    
    save_a_tree_as_a_geometry_to_postgresql(a_sub_tree, the_connection, the_counter)
