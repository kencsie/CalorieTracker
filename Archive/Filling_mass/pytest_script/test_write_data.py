import sys
import os
import re
import pytest

#Add the directory containing write_data.py to sys.path
script_directory = '../' 
if script_directory not in sys.path:
    sys.path.append(script_directory)

#Regex test
from write_data import load_user_name_format

def test_ken_regex():
  user_profile = load_user_name_format('1')
  assert user_profile['name'] == 'Ken'
  assert re.search(user_profile['re_exp'], '20231106_115802') == None
  assert re.search(user_profile['re_exp'], 'IMG_20231106_115802') != None
  assert re.search(user_profile['re_exp'], 'IMG_9415') == None

def test_kenrick_regex():
  user_profile = load_user_name_format('2')
  assert user_profile['name'] == 'Kenrick'
  assert re.search(user_profile['re_exp'], '20231106_115802') != None
  assert re.search(user_profile['re_exp'], 'IMG_20231106_115802') == None
  assert re.search(user_profile['re_exp'], 'IMG_9415') == None

#Unfinished_date_list test
from write_data import create_unfinished_date_list
def test_create_ken_unfinished_date_list():
  user_profile = load_user_name_format('1')
  ken_unfinished_list = create_unfinished_date_list('./test_csv/output.csv', user_profile)
  assert ken_unfinished_list == ['20231122', '20231124', '20231127', '20231128', '20231129', '20231130', '20231201', '20231206', '20231207', '20231208', '20231213', '20231214', '20231215', '20231219', '20231220']

def test_create_kenrick_unfinished_date_list():
  user_profile = load_user_name_format('2')
  kenrick_unfinished_list = create_unfinished_date_list('./test_csv/output.csv', user_profile)
  assert kenrick_unfinished_list == ['20231103', '20231106', '20231107', '20231108', '20231109', '20231110', '20231113', '20231114', '20231116', '20231117', '20231120', '20231121', '20231122', '20231123', '20231124', '20231127', '20231128', '20231129', '20231130', '20231201', '20231205', '20231206', '20231207', '20231208', '20231211', '20231212', '20231213', '20231214', '20231215', '20231219', '20231220', '20231221', '20231222', '20231225', '20231226', '20231228']

#Prompt mass function
from write_data import prompt_mass
def test_prompt_mass(monkeypatch):
  id_list = [str(it)+".0" for it in range(0, 23)]
  mass_list = " ".join(str(it) for it in range(22, -1, -1))

  monkeypatch.setattr('builtins.input', lambda : mass_list)
  mass_dict = prompt_mass(id_list)
  assert mass_dict == {'0.0': 22, '1.0': 21, '2.0': 20, '3.0': 19, '4.0': 18, '5.0': 17, '6.0': 16, '7.0': 15, '8.0': 14, '9.0': 13, '10.0': 12, '11.0': 11, '12.0': 10, '13.0': 9, '14.0': 8, '15.0': 7, '16.0': 6, '17.0': 5, '18.0': 4, '19.0': 3, '20.0': 2, '21.0': 1, '22.0': 0}