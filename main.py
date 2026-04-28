import srs_logic
import utils

def main():
    cards = utils.load_cards()
    d = {
        '1': srs_logic.repeat_card, 
        '2': srs_logic.add_card,
        '3': srs_logic.look
         }
    key = input('''
    Enter 
    1 for repeat cards,
    2 for add_cards,
    3 for look all cards
                ''')
    d[key](cards)





if __name__ == "__main__":
    main()
