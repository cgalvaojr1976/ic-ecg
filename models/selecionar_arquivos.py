import wfdb

# record, fields = wfdb.rdsamp("database_part/s0004_re", channels=[0])

path = []

for i in range(1,562):
    if i < 10:
        path.append(f"database_part/s000{i}_re")
    elif 10 <= i < 100:
        path.append(f"database_part/s00{i}_re")
    else:
        path.append(f"database_part/s0{i}_re")

print(path)

# str1 = "Reason for admission: Myocardial infarction"
# str2 = "Reason for admission: Healthy controls"

# lista_de_pacientes  = []

# for i in range()
# print(type(fields['comments'][4]))