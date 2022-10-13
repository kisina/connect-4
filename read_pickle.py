import pickle

file_name = "q_table_player_1.p"
file_name = "test_learning.p"
file_name = "test_learning_human.p"

q_table = pickle.load(open(file_name, "rb"))

for state, values in q_table.items():
    print(f"{state}: {values}")
# see https://thispointer.com/python-iterate-over-dictionary-with-list-values/
print("end")