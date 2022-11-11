import pandas as pd
df = pd.read_csv('adult.csv')
train_set = df.sample(frac=0.8)
test_set = df.drop(train_set.index)

set_education = []
set_status = []
set_others = []
set_skin_color = []

for item, value in train_set.iterrows():
    set_education.append(value["Education"])
    set_status.append(value["Status"])
    set_others.append(value["Others"])
    set_skin_color.append(value["Skin Color"])

set_education = set(set_education)
set_status = set(set_status)
set_others = set(set_others)
set_skin_color = set(set_skin_color)

education_value = [[], []]
status_value = [[], []]
others_value = [[], []]
skin_color_value = [[], []]

for item in set_education:
    education_value[0].append({"key": item, "value": 0})
    education_value[1].append({"key": item, "value": 0})

for item in set_status:
    status_value[0].append({"key": item, "value": 0})
    status_value[1].append({"key": item, "value": 0})

for item in set_others:
    others_value[0].append({"key": item, "value": 0})
    others_value[1].append({"key": item, "value": 0})

for item in set_skin_color:
    skin_color_value[0].append({"key": item, "value": 0})
    skin_color_value[1].append({"key": item, "value": 0})

for item, value in train_set.iterrows():
    if value["Sex"] == " Male":
        for i in range(len(education_value[0])):
            if education_value[0][i]["key"] == value["Education"]:
                education_value[0][i]["value"] += 1
                break

        for i in range(len(status_value[0])):
            if status_value[0][i]["key"] == value["Status"]:
                status_value[0][i]["value"] += 1
                break

        for i in range(len(others_value[0])):
            if others_value[0][i]["key"] == value["Others"]:
                others_value[0][i]["value"] += 1
                break

        for i in range(len(skin_color_value[0])):
            if skin_color_value[0][i]["key"] == value["Skin Color"]:
                skin_color_value[0][i]["value"] += 1
                break
    else:

        for i in range(len(education_value[1])):
            if education_value[1][i]["key"] == value["Education"]:
                education_value[1][i]["value"] += 1
                break

        for i in range(len(status_value[1])):
            if status_value[1][i]["key"] == value["Status"]:
                status_value[1][i]["value"] += 1
                break

        for i in range(len(others_value[1])):
            if others_value[1][i]["key"] == value["Others"]:
                others_value[1][i]["value"] += 1
                break

        for i in range(len(skin_color_value[1])):
            if skin_color_value[1][i]["key"] == value["Skin Color"]:
                skin_color_value[1][i]["value"] += 1
                break

all_male = 0
all_female = 0
total = 0
for item, value in train_set.iterrows():
    if value["Sex"] == " Male":
        all_male += 1
    else:
        all_female += 1
    total += 1

true_prediction = 0
false_prediction = 0

for item, value in test_set.iterrows():
    male_probability = 0
    female_probability = 0

    education_probability = 0
    status_probability = 0
    others_probability = 0
    skin_color_probability = 0

    for i in range(len(education_value[0])):
         if education_value[0][i]["key"] == value["Education"]:
            education_probability = education_value[0][i]["value"]
            break

    for i in range(len(status_value[0])):
        if status_value[0][i]["key"] == value["Status"]:
            status_probability = status_value[0][i]["value"]
            break

    if value["Others"] != " ?":
        for i in range(len(others_value[0])):
            if others_value[0][i]["key"] == value["Others"]:
                others_probability = others_value[0][i]["value"]
                break

    for i in range(len(skin_color_value[0])):
        if skin_color_value[0][i]["key"] == value["Skin Color"]:
            skin_color_probability = skin_color_value[0][i]["value"]
            break

    if value["Others"] != " ?":
        male_probability = (education_probability / all_male) * (status_probability / all_male) * (
            others_probability / all_male) * (skin_color_probability / all_male)
    else:
        male_probability = (education_probability / all_male) * (
            status_probability / all_male) * (skin_color_probability / all_male)
    male_probability *= (all_male / total)

    education_probability = 0
    status_probability = 0
    others_probability = 0
    skin_color_probability = 0

    for i in range(len(education_value[1])):
         if education_value[1][i]["key"] == value["Education"]:
            education_probability = education_value[1][i]["value"]
            break

    for i in range(len(status_value[1])):
        if status_value[1][i]["key"] == value["Status"]:
            status_probability = status_value[1][i]["value"]
            break

    if value["Others"] != " ?":
        for i in range(len(others_value[1])):
            if others_value[1][i]["key"] == value["Others"]:
                others_probability = others_value[1][i]["value"]
                break

    for i in range(len(skin_color_value[1])):
        if skin_color_value[1][i]["key"] == value["Skin Color"]:
            skin_color_probability = skin_color_value[1][i]["value"]
            break

    if value["Others"] != " ?":
        female_probability = (education_probability / all_female) * (status_probability / all_female) * (
            others_probability / all_female) * (skin_color_probability / all_female)
    else:
        female_probability = (education_probability / all_female) * (
            status_probability / all_female) * (skin_color_probability / all_female)
    female_probability *= (all_female / total)

    label_male = male_probability / (male_probability + female_probability)
    label_female = female_probability / \
        (male_probability + female_probability)

    if (label_male >= label_female and value["Sex"] == " Male") or (label_male < label_female and value["Sex"] == " Female"):
        true_prediction += 1
    else:
        false_prediction += 1

print(true_prediction / (true_prediction + false_prediction))
