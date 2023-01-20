from config_data.request_config import current_date


def checking_date(date: str, compare_date=str(current_date)):
    date_list = date.split('-')
    current_date_list = compare_date.split('-')
    if int(date_list[0]) == int(current_date_list[0]):
        if int(date_list[1]) > int(current_date_list[1]):
            return True
        elif int(date_list[1]) == int(current_date_list[1]):
            if int(date_list[2]) >= int(current_date_list[2]):
                return True
            else:
                return False
        else:
            return False
    elif int(date_list[0]) > int(current_date_list[0]):
        return True
    else:
        return False
