import pickle

file_name = "q_table_player_1.p"
q_table = pickle.load(open(file_name, "rb"))

for _, values in q_table:
    print(values)
# see https://thispointer.com/python-iterate-over-dictionary-with-list-values/
print("end")