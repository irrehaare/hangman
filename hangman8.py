# before launching this game you must download pygame
# in unix terminal:
# pip3 install pygame

from os import system
import random
import time
import datetime
import csv
from pygame import mixer

with open("jokes.txt", "r") as f:
    jokes = f.readlines()

# KNOWN BUGS:
# Fatality not playing after ragequit????

# player_letter - string, input from player
# guess - list of 1 character strings, current state of guessing, ______at the beginning, capital name at the end if successful
# game_on - 1 when playing, 0 when lost, 2 when won, 3 for ragequit
# password - string, what user is supposed to guess
# HP - int, game is lost when it drops to 0
# misses - list, letters that user guessed but weren't in password
# err code - int, 1 when non letter found in player_letter, 2 when player_letter is in misses, 3 when user guess wrong password, 4 when player_letter length is != 1 and != password length
# guess_count - number of attempts that player made
# start, end - times of start and ending of game
# game time - time it took player to win


def main():
    (password, guess, HP, misses, err_code, guess_count) = initialise()
    game_on = welcome_screen()
    mixer.music.stop()
    start = time.time()
    while game_on == 1:
        print(password)
        game_screen(guess, HP, misses, err_code)
        (player_letter, password) = get_player_input(password)
        (guess, HP, misses, err_code, game_on, guess_count) = engine(player_letter, guess, password, HP, misses, guess_count)
        if game_on != 1:
            end = time.time()
            game_time = end - start
            if game_on != 3:
                if game_on < 1:
                    lost_game(guess, HP, misses, password, game_time)
                else:
                    won_game(guess, HP, misses, password, guess_count, game_time)
                if yes_no_question("Do you want to see High Scores? "):
                    show_high_scores()
                if yes_no_question("Do you want to play again? "):
                    (password, guess, HP, misses, err_code, guess_count) = initialise()
                    game_on = 1
                    start = time.time()
            else:
                _ = system('clear')
                print(f"Rage quit detected!")
                play_sound("fatality.mp3")
                while mixer.music.get_busy():
                    pass


def game_screen(guess, HP, misses, err_code):
    verse = gallows(HP)
    _ = system('clear')
    for line in verse:
        print(line)
    print("\033[2;13H", end='')
    show_guess(guess)
    print("\033[4;13H", end='')
    print(f"Misses: {misses}")
    print("\033[8;1H", end='')
    print(error_message(err_code))
    print("\033[6;13H", end='')
    print(f"Guess: ", end='')


def get_player_input(password):
    try:
        player_letter = input("")
    except KeyboardInterrupt:
        player_letter = "ragequit"
        password = "ragequit"
    return (player_letter, password)

def engine(player_letter, guess, password, HP, misses, guess_count):
    if password != "ragequit":
        err_code = 0
        game_on = 1
        if not player_letter.isalpha():
            err_code = 1
        else:
            player_letter = player_letter.upper()
            if player_letter == password:
                game_on = 2
            elif player_letter in guess:
                err_code = 5
            elif player_letter in password and len(player_letter) == 1:
                guess = guess_update(guess, player_letter, password)
                if ''.join(guess) == password:
                    game_on = 2
            else:
                (HP, misses, err_code) = is_miss(HP, misses, player_letter, guess)
                if HP <= 0:
                    game_on = 0
        if (err_code == 0 or err_code == 3):
            guess_count += 1
        return (guess, HP, misses, err_code, game_on, guess_count)
    else:
        err_code = 0
        game_on = 3
        return (guess, HP, misses, err_code, game_on, guess_count)


def gallows(HP):
    verse = ["    ____     ", "   |/  |     "]
    if HP >= 6:
        verse.append("   |         ")
    else:
        verse.append("   |   O     ")
    if HP >= 5:
        verse.append("   |         ")
    elif HP == 4:
        verse.append("   |   |     ")
    elif HP == 3:
        verse.append("   |  ‾|     ")
    else:
        verse.append("   |  ‾|‾    ")
    if HP >= 2:
        verse.append("   |         ")
    elif HP == 1:
        verse.append("   |  /      ")
    else:
        verse.append("   |  / \    ")
    verse.append(" _/|\_____   ")
    return verse


def show_guess(guess):
    for letter in guess:
        print(letter, end=' ')


def error_message(err_code):
    if err_code == 0:
        return ''
    elif err_code == 1:
        return "Non-letter input. Please enter letters only (without spaces)."
    elif err_code == 2:
        return "You've tried that already!"
    elif err_code == 3:
        return "Wrong guess. 2 HP lost."
    elif err_code == 4:
        return "Please enter letter or try to guess password."
    elif err_code == 5:
        return "You've already guessed this letter!"
    else:
        return "Unknown error encountered."


def initialise():
    password = create_password()
    guess = hasher(password)
    HP = 6
    misses = []
    err_code = 0
    guess_count = 0
    return (password, guess, HP, misses, err_code, guess_count)


def create_password():
    europe_capitals = ["Tirana", "Andorra", "Yerevan", "Vienna", "Baku", "Minsk", "Brussels", "Sarajevo", "Sofia", "Zagreb", "Nicosia", "Prague", "Copenhagen", "Tallinn", "Paris", "Tbilisi", "Berlin", "Athens", "Budapest", "Reykjavik", "Dublin", "Rome", "Pristina", "Riga", "Vaduz", "Vilnius", "Luxembourg", "Valletta", "Chisinau", "Monaco", "Podgorica", "Amsterdam", "Skopje", "Oslo", "Warsaw", "Lisbon", "Bucharest", "Moscow", "San Marino", "Belgrade", "Bratislava", "Ljubljana", "Madrid", "Stockholm", "Bern", "Ankara", "Kyiv", "London", "Vatican City"]
    random_capitol = europe_capitals[random.randint(0, len(europe_capitals) - 1)].upper()
    random_capitol = random_capitol.replace(" ", "")
    return random_capitol


def hasher(word):
    hashed = []
    for letter in word:
        hashed.append("_")
    return hashed


def guess_update(guess, player_letter, password):
    for counter, char in enumerate(password):
        if char == player_letter:
            guess[counter] = password[counter]
    return guess


def is_miss(HP, misses, player_letter, guess):
    err_code = 0
    if player_letter not in misses and len(player_letter) == 1:
        misses.append(player_letter)
        HP -= 1
    elif len(guess) == len(player_letter):
        HP -= 2
        if HP < 0:
            HP = 0
        err_code = 3
    elif len(player_letter) > 1:
        err_code = 4
    else:
        err_code = 2
    return (HP, misses, err_code)


def lost_game(guess, HP, misses, password, game_time):
    play_sound("wilhelm_scream.mp3")
    verse = gallows(HP)
    _ = system('clear')
    for line in verse:
        print(line)
    print("\033[2;13H", end='')
    show_guess(guess)
    print("\033[3;13H", end='')
    print(f"You have played for {round(game_time, 2)} seconds.")
    print("\033[4;13H", end='')
    print(f"You LOST.")
    print("\033[6;13H", end='')
    print(f"Password was: {password}\n")


def won_game(guess, HP, misses, password, guess_count, game_time):
    play_sound("win_sound.mp3")
    verse = gallows(HP)
    i = 0
    for letter in password:
        guess[i] = letter
        i += 1
    name = ""
    while not name or "," in name:
        _ = system('clear')
        for line in verse:
            print(line)
        print("\033[2;13H", end='')
        show_guess(guess)
        print("\033[3;13H", end='')
        print(f"You have WON! You did it in {guess_count} guesses!")
        print("\033[4;13H", end='')
        print(f"You did it in {round(game_time, 2)} seconds.")
        print("\033[5;13H", end='')
        print(f"Here is a joke as a prize:")
        print("\033[6;13H", end='')
        tell_joke()
        if "," in name:
            print("\033[10;0H", end='')
            print("Name can't have a comma!")
            print("\033[8;0H", end='')
        try:
            name = input("Please enter your name to High Scores. ")
        except KeyboardInterrupt:
            name = "Bezimienny"
            print(" You will be remembered as 'Bezimienny'.")
    date = datetime.datetime.now()
    date = [date.day, date.month, date.year, date.hour, date.minute, date.second]
    with open("high_scores.csv", "r") as f:
        reader = csv.reader(f)
        high_scores = list(reader)
    index = 0
    while index < len(high_scores) and game_time > float(high_scores[index][1]):
        index += 1
    record = [guess_count, game_time, name, date[0], date[1], date[2], date[3], date[4], date[5], password]
    high_scores.insert(index, record)
    with open("high_scores.csv", "w") as f:
        for element in high_scores:
            f.write(f"{element[0]},{element[1]},{element[2]},{element[3]},{element[4]},{element[5]},{element[6]},{element[7]},{element[8]},{element[9]}\n")


def tell_joke():
    print(f"{jokes[random.randint(0,len(jokes)-1)]}")


def yes_no_question(question):
    while True:
        try:
            answear = input(question)
        except KeyboardInterrupt:
            answear = 'n'
            print("   That's a no.")
        if " " not in answear and len(answear) > 0:
            if answear[0] == "Y" or answear[0] == "y":
                return True
            elif answear[0] == "N" or answear[0] == "n":
                return False
        print(f"Sorry, I don't undestand. Please reply 'Yes' or 'No'.\n")


def show_high_scores():
    _ = system('clear')
    with open("high_scores.csv", "r") as f:
        reader = csv.reader(f)
        lst = list(reader)
        max_nick = len(lst[0][2])
        for rank in range(0, min([10, len(lst)])):
            if len(lst[rank][2]) > max_nick:
                max_nick = len(lst[rank][2])
        if max_nick > 30:
            max_nick = 30
        elif max_nick < 10:
            max_nick = 10
        for rank in range(min([10, len(lst)])):
            nick = lst[rank][2].strip()
            nick = nick[0:30]
            day = lst[rank][3].strip()
            month = lst[rank][4].strip()
            year = lst[rank][5].strip()
            hour = lst[rank][6].strip()
            minute = lst[rank][7].strip()
            second = lst[rank][8].strip()
            guess_count = lst[rank][0].strip()
            time = round(float(lst[rank][1].strip()), 2)
            password = lst[rank][9].strip()
            if rank != 9:
                print(f"{rank+1}. {nick}")
            else:
                print(f"{rank+1}.{nick}")
            print(f"\033[{rank+1};{max_nick+4}H", end='')
            print(f"| {day}.{month}.{year} {hour}:{minute}:{second}")
            print(f"\033[{rank+1};{max_nick+26}H", end='')
            print(f"| Guess count: {guess_count}")
            print(f"\033[{rank+1};{max_nick+44}H", end='')
            print(f"| Time: {time}")
            print(f"\033[{rank+1};{max_nick+59}H", end='')
            print(f"| Password: {password}")


def play_sound(file):
    mixer.init()
    mixer.music.load(file)
    mixer.music.play()


def welcome_screen():
    play_sound("cantina.mp3")
    game_on = 1
    delay = 0.2
    _ = system('clear')
    print(" _   _   ___   _   _ _____ ___  ___  ___   _   _ ")
    time.sleep(delay)
    print("| | | | / _ \ | \ | |  __ \|  \/  | / _ \ | \ | |")
    time.sleep(delay)
    print("| |_| |/ /_\ \|  \| | |  \/| .  . |/ /_\ \|  \| |")
    time.sleep(delay)
    print("|  _  ||  _  || . ` | | __ | |\/| ||  _  || . ` |")
    time.sleep(delay)
    print("| | | || | | || |\  | |_\ \| |  | || | | || |\  |")
    time.sleep(delay)
    print("\_| |_/\_| |_/\_| \_/\____/\_|  |_/\_| |_/\_| \_/\n")
    time.sleep(delay)
    try:
        input("Press Enter to start a game!")
    except KeyboardInterrupt:
        game_on = 3
        print(" Bye Bye Bye!")
    return game_on


if __name__ == '__main__':
    main()
