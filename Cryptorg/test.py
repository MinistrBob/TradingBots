import json
from decimal import Decimal


def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON data from '{file_path}'.")
        return None


def main():
    file = read_json_file(r'c:\MyGit\TradingBots\Cryptorg\staff\bot_list.json')
    data = file['data']
    for bot in data:
        # print(bot)
        fo = Decimal(bot['settings']['volume_first_order'])
        leverage = Decimal(bot['leverage'])
        martin = Decimal(bot['settings']['martingale_scale'])
        count_order_max = int(bot['settings']['count_order_max'])
        total_margin = fo
        my_margin = (fo / leverage)
        # print(total_margin.quantize(Decimal('0.00')), my_margin.quantize(Decimal('0.00')))
        no = fo
        for i in range(count_order_max):
            no = no * martin
            no_my = no / leverage
            total_margin = total_margin + no
            my_margin = my_margin + no_my
            # print(no.quantize(Decimal('0.00')), no_my.quantize(Decimal('0.00')))
        # print(bot['pairTitle'], total_margin.quantize(Decimal('0.00')), my_margin.quantize(Decimal('0.00')))
        print(f"{bot['pairTitle'].replace('USDT-','')}\t{total_margin.quantize(Decimal('0.00'))}\t{my_margin.quantize(Decimal('0.00'))}")


if __name__ == '__main__':
    main()
