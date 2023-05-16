import ipinfo
import ipwhois
from colorama import Fore, init

ipinfo_token = 'TOKEN_HERE'

""" *------------------------------------------------------------------------------------------------------------*
    Author: Stian Kvålshagen
    Date: 5.02.2023
*------------------------------------------------------------------------------------------------------------* """

""" *------------------------------------------------------------------------------------------------------------*
    Made using ipwhois. It is slow and gives limited data, but does not requre a user and is unlimited.
    Second option is ipinfo. It is much faster and gives more information. But requires a user/token and is limited to 
    50 000 IP each month. To use ipinfo, log into ipinfo and get your API token. Then place it in the "ipinfo_token" 
    variable. Thank you to UserHonest for showing me IpInfo <3
*------------------------------------------------------------------------------------------------------------* """


def get_geolocation_ipwhois(ip_address):
    global check
    # Run the api call, then ingest the text to useful format.
    try:
        obj = ipwhois.IPWhois(ip_address)
        results = obj.lookup_whois()
        check = True
        refined_result = ""
        if ip_address is not None:
            refined_result += f"IP: {ip_address}\n"
        if results["nets"][0]["country"] is not None:
            refined_result += f"Country: {results['nets'][0]['country']}\n"
        if results["nets"][0]["name"] is not None:
            refined_result += f"Name: {results['nets'][0]['name']}\n"
        if results["nets"][0]["description"] is not None:
            refined_result += f"Description: {results['nets'][0]['description']}\n"
        if results["nets"][0]["city"] is not None:
            refined_result += f"City: {results['nets'][0]['city']}\n"
        if results["nets"][0]["address"] is not None:
            refined_result += f"Address: {results['nets'][0]['address']}\n"
        refined_result += f"\n\n---------------------------------\n\n"
        detailed.append(refined_result)
        if choice_details.lower() == "y":
            print(refined_result)
        else:
            print(ip_address + " -> " + results["nets"][0]["country"])
        return results["nets"][0]["country"]
    except Exception as e:
        check = False
        print(Fore.RED + "Error: " + str(e))
        return str(e) + "," + str(ip_address)



def get_result_whois():
    with open("ipwhois_save.csv", "r") as countries:
        with open("ipwhois_error.csv", "r") as errors:
            countries_buffer, counter, unique = [], [], []

            # Sort unique countries, then count the redundant ones.
            for c in countries:
                split_c = c.replace("\n", "").split(",")
                if split_c[0] not in unique:
                    unique.append(split_c[0])
                countries_buffer.append(split_c[0])

            for u in unique:
                count = 0
                for c2 in countries_buffer:
                    c2_split = c2.replace("\n", "").split(",")
                    if u == c2_split[0]:
                        count += 1
                counter.append(count)
            print("\nFound locations: ")
            for p in range(len(unique)):
                if p != 0:
                    print(unique[p] + ": " + str(counter[p]))

            # Print found locations nr to a file.
            with open("ipwhois_found_nr.csv", "w") as found:
                found.write("country,amount\n")
                for p in range(len(unique)):
                    if p != 0:
                        found.write(unique[p] + "," + str(counter[p]) + "\n")

            # Get errors
            print(Fore.RED + "\nIP addresses not found:")
            for e in errors:
                e_split = e.replace("\n", "").split(",")
                print(e_split[1])


def saved_timesip_whois():
    countries, errors_storeage = [], []

    # Import successful saved items.
    try:
        with open("ipwhois_save.csv", "r") as save:
            for s in save:
                save_split = s.replace("\n", "").split(",")
                if save_split[0] != "country":
                    countries.append(save_split[1])
            print(Fore.BLUE + "Imported items from save!")
    except Exception as e:
        print(f"{Fore.RED}No save found. Error: {str(e)}")
        with open("ipwhois_save.csv", "a") as save:
            save.write("country,ip\n")

    # Import error items.
    try:
        with open("ipwhois_error.csv", "r") as error:
            for s in error:
                error_replaced = s.replace("\n", "")
                error_split = error_replaced.split(",")
                if error_split[0] != "error":
                    errors_storeage.append(error_split[1])
        print(f"{Fore.BLUE}Imported items from error! Working from last checkpoint.")
    except Exception as e:
        print(f"{Fore.RED}No error save found. Error: {str(e)}")
        with open("ipwhois_error.csv", "a") as error:
            error.write("error,ip\n")
    return countries, errors_storeage


def get_geo_ipwhois(countries, errors_storeage, choice_details):
    global detailed
    with open("ip.txt", "r") as file:
        counter = 0
        tick = 5
        counter_tick = tick
        error_buffer, save_buffer = [], []

        # Check if item is already saved, then send the IP to the API to get the location.
        for f in file:
            f = f.replace("\n", "")
            if f not in countries:
                if f not in errors_storeage:
                    geo = get_geolocation_ipwhois(f)
                    counter += 1

                    # If the API call is successful, store it, if not, put it in error list so we can see why.
                    if check or f is not None:
                        countries.append(f"{geo},{str(f)}")
                        save_buffer.append(f"{geo},{str(f)}")
                    if not check or f is None:
                        errors_storeage.append(geo)
                        error_buffer.append(geo)
                    if counter == counter_tick:
                        print(f"{Fore.BLUE}\nSaving progress!\n")

                        # Saving valid IP addresses into save.csv.
                        with open("ipwhois_save.csv", "a") as save:
                            for save_progress in save_buffer:
                                save.write(str(save_progress) + "\n")
                        save_buffer = []

                        # Save detailed information
                        with open("ipwhois_detailed.csv", "a") as save_detailed:
                            for details in detailed:
                                save_detailed.write(str(details))
                        detailed = []

                        # Saving IP addresses that could not be tracked into error.csv
                        with open("ipwhois_error.csv", "a") as error:
                            for error_progress in error_buffer:
                                error.write(str(error_progress) + "\n")
                        error_buffer = []
                        counter_tick = counter_tick + tick

        # Save one final time after it is done.
        print(f"{Fore.BLUE}\nSaving progress!\n")
        with open("ipwhois_save.csv", "a") as save:
            for save_progress in save_buffer:
                save.write(str(save_progress) + "\n")
        with open("ipwhois_error.csv", "a") as error:
            for error_progress in error_buffer:
                error.write(str(error_progress) + "\n")


def init_ipwhois():
    print("Only make new save files if you want to clear the old one. Take backups if unsure!")
    choice_save = input("Do you want a new save file? [y/n]\n")
    choice_error = input("Do you want a new error file? [y/n]\n")
    choice_detialed_file = input("Do you want a new detailed file? [y/n]\n")
    choice_details = input("Do you want to print detailed information (Will be saved regardless)? [y/n]\n")
    if choice_save.lower() == "y":
        with open("ipwhois_save.csv", "w") as save:
            save.write("country,ip\n")

    if choice_error.lower() == "y":
        with open("ipwhois_error.csv", "w") as error:
            error.write("error,ip\n")

    if choice_detialed_file.lower() == "y":
        with open("ipwhois_detailed.csv", "w") as details:
            details.write("detailed:")
    return choice_details


def init_ipinfo():
    print("Only make new save files if you want to clear the old one. Take backups if unsure!")
    choice_save = input("Do you want a new save file? [y/n]\n")
    if choice_save.lower() == "y":
        with open("ipinfo_save.csv", "w") as save:
            save.write("country,ip\n")


def get_geolocation_ipinfo(ip_address):
    global check
    data_list = []

    # Run the api call, then ingest the text to useful format.
    try:
        check = True
        for key, value in ipinfo.getHandler(ipinfo_token).getDetails(ip_address).all.items():
            print(f"{key}: {value}")
            data_list.append(f"{key}: {value}")
        print("\n----------\n")
        data_list.append("\n----------\n")
        detailed.append(data_list)
        return data_list
    except Exception as e:
        check = False
        print(f"{Fore.RED}Error: " + str(e))
        return str(e) + "," + str(ip_address)


def get_geo_ipinfo():
    global detailed
    with open("ip.txt", "r") as ip_file:

        # Check if item is already saved, then send the IP to the API to get the location.
        for f in ip_file:
            f = f.replace("\n", "")
            with open("ipinfo_save.csv", "a", encoding="utf-8") as save:
                for r in get_geolocation_ipinfo(f):
                    save.write(r + "\n")


if __name__ == "__main__":

    check = False
    init(autoreset=True)
    detailed = []

    choice_software = input("Do you want to use ipwhois[1] or ipinfo?[2]?")
    if choice_software == "1":
        # Import saved items.
        choice_details = init_ipwhois()
        imported_items = saved_timesip_whois()

        # Get Geo from ipwhois API.
        get_geo_ipwhois(imported_items[0], imported_items[1], choice_details)

        # Print results
        get_result_whois()

    if choice_software == "2":
        init_ipinfo()
        get_geo_ipinfo()
