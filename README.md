# iGeo

This python program is used to retrieve geolocation information of an IP address. You can use two methods to do this: the ipwhois package and the ipinfo package.

![bilde](https://github.com/SpaceyLad/iGeo_ip_scanner/assets/87969837/97136b60-b93e-4c48-86ae-55f5d83a86f1)

### Installation

pip install -r requirements.txt

### Limitations

ipwhois is slow and provides limited data, but it does not require a user token and has no limit on the number of IP addresses that can be processed.

ipinfo is faster and provides more information, but it requires a user token and is limited to 50,000 IPs per month.

## Setting Up ipinfo
You need to create an account on ipinfo and get your API token if you want to use ipinfo.
Before running the program, replace TOKEN_HERE with your ipinfo API token in the ipinfo_token variable.

### How It Works

This program reads IP addresses from a file named ip.txt, which should be present in the same directory as the python script. To add IP adresses, simply put them into the ip.txt file. The program will read each line as a unique IP address. 

When the program is run, it asks whether you want to use ipwhois or ipinfo.

#### If you select ipwhois (by entering 1), the program:
1. Asks a series of questions about whether you want to create new save files and whether you want to print detailed information.
2. Reads the IP addresses from ip.txt and retrieves geolocation information for each IP.
3. Stores the results in several CSV files: ipwhois_save.csv (for valid IP addresses), ipwhois_error.csv (for IP addresses that couldn't be tracked), and ipwhois_detailed.csv (for detailed information about each IP address).
4. Prints the results to the console.
#### If you select ipinfo (by entering 2), the program:
1. Asks whether you want to create a new save file.
2. Reads the IP addresses from ip.txt and retrieves geolocation information for each IP.
3. Stores the results in ipinfo_save.csv and prints the results while doing so.

Error Handling

The program has robust error handling. It checks if the API calls are successful. If not, it saves the errors along with the corresponding IP address for further investigation.
