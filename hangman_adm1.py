import csv


def sort_high_scores():
    with open("high_scores.csv", "r") as f:
        reader = csv.reader(f)
        lst = list(reader)
    with open("high_scores.csv", "w+") as f:
        pass

    sorted_list = []
    while lst:
        highest = lst[0]
        i = 0
        highest_num = i
        for element in lst:
            if float(element[1]) < float(highest[1]):
                highest = element
                highest_num = i
            i += 1
        del lst[highest_num]
        with open("high_scores.csv", "a") as f:
            f.write(f"{highest[0]}, {highest[1]}, {highest[2]}, {highest[3]}, {highest[4]}, {highest[5]}, {highest[6]}, {highest[7]}, {highest[8]}, {highest[9]}\n")
    for element in sorted_list:
        print(f"Highest score is: {element}")


sort_high_scores()
