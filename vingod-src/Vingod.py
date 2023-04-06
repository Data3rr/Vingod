from selenium import webdriver
from selenium.webdriver.common.by import By
from os import system, getcwd, remove, path as _path
from numpy import mean
from discord_webhook import DiscordWebhook, DiscordEmbed
from time import sleep, time
from json import load, dump
import random, string
from colorama import Fore, init
from requests import get
from pypresence import Presence
from pyshorteners import Shortener

# ----- colorama settings -----
c = Fore.LIGHTCYAN_EX
w = Fore.LIGHTWHITE_EX

# ----- banner -----
banner = f""" ██╗   ██╗██╗███╗   ██╗ ██████╗  ██████╗ ██████╗ 
 ██║   ██║██║████╗  ██║██╔════╝ ██╔═══██╗██╔══██╗
 ██║   ██║██║██╔██╗ ██║██║  ███╗██║   ██║██║  ██║
 ╚██╗ ██╔╝██║██║╚██╗██║██║   ██║██║   ██║██║  ██║
  ╚████╔╝ ██║██║ ╚████║╚██████╔╝╚██████╔╝██████╔╝
   ╚═══╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚═════╝ ╚═════╝ 
 {w}Vingod by 0xSpoofed © | Last update: April 2023\n\n -----""".replace('█', f'{w}█{c}')


# <----- rich presence ----->
def rich_presence():
    try:
        start = int(time())
        rpc = Presence("933736221220433950")
        rpc.connect()
        rpc.update(
            large_image= "tool",
            large_text = f"Vingod - Vinted bot",
            details = "Version: Stable",
            state = "by 0xSpoofed",
            )
    except Exception as e:
        pass
    
    
# <----- integrity checker ----->
def integrity_checker():
    paths_to_check = ['geckodriver.exe', 'assets', 'assets/brands.json', 'assets/item_type.json', 'assets/products.json', 'assets/settings.json', 'assets/sizes.json']
    for path in paths_to_check:
        if _path.exists(path) == False:
            if path == paths_to_check[1]:
                classification = "(folder)"
            else:
                classification = "(file)"
            system("cls")
            input(f"\n{banner}\n {c}[{w}!{c}]{w} {path} {classification} is missing. Press enter to exit.")
            exit()
        else: continue
    
    
# <-----  file reader ----->
def write_file(file_path: str, data: dict) -> None:
    with open(file_path, 'w') as f:
        data = f.write(data)
    return data


# <----- json file reader ----->
def read_json(file_path: str) -> dict:
    with open(file_path, 'r') as json_file:
        data = load(json_file)
    return data


# <----- json file writer ----->
def write_json(file_path: str, data: dict) -> None:
    with open(file_path, 'w') as json_file:
        dump(data, json_file)


# <-----  json file cleaner ----->
def json_cleaner(json_path):
    json_data = read_json(f"{getcwd()}\\assets\\{json_path}")
    json_data.clear()
    json_data.update({})
    json_file = write_json(f"{getcwd()}\\assets\\{json_path}", json_data) 

    system('cls')
    print(f"""\n{banner}\n {c}[{w}INFO{c}]{w} {json_path} has been cleaned succesfully !""")
    sleep(2)
    settings_controler()


# <----- random letters gen ----->
def lettergen(lenght):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(int(lenght)))


# <----- brand converter ----->
def brand_converter(bid):
    json_data = read_json(f"{getcwd()}\\assets\\brands.json")
    for brand in json_data:
        if bid == str(brand):
            return json_data[bid]
        else:
            pass
    return f"Unlisted brand ({bid})"


# <----- item type converter ----->
def item_type_converter(iid):
    json_data = read_json(f"{getcwd()}\\assets\\item_type.json")
    for item_id in json_data:
        if iid == str(item_id):
            return json_data[iid]
        else:
            pass
    return f"Unlisted item ({iid})"


# <----- size converter ----->
def size_converter(size):
    json_data = read_json(f"{getcwd()}\\assets\\sizes.json")
    for s in json_data:
        if size == s:
            return json_data[size]
        else:
            pass 
        
        
# <----- remove duplicate ----->
def remove_duplicate(list):
    return [x for i, x in enumerate(list) if x not in list[:i]]


# <----- get settings ----->
def get_settings():
    json_data = read_json(f"{getcwd()}\\assets\\settings.json")
    return json_data["Brand"], json_data["Item type"], json_data["Size"], json_data["Margin"], json_data[
        "Explored_pages"], json_data["Webhook"]


# <----- explored pages updater ----->
def update_explored_pages(banner: str, c: str, w: str):
    system("cls")
    Explored_pages = input(f"\n{banner}\n {c}[{w}->{c}]{w} Enter the number of pages to explore: ")
    try:
        Explored_pages = int(Explored_pages)
        if Explored_pages <= 0 or Explored_pages >= 99:
            raise ValueError
    except ValueError:
        system("cls")
        print(f"\n{banner}\n {c}[{w}!{c}]{w} Please enter a number between 1 and 100 !")
        sleep(2)
        settings_controler()
    except Exception as e:
        system("cls")
        print(f"\n{banner}\n {c}[{w}!{c}]{w} Please enter a correct number !")
        sleep(2)
        settings_controler()

    json_data = read_json(f"{getcwd()}\\assets\\settings.json")
    json_data["Explored_pages"] = str(Explored_pages)
    write_json(f"{getcwd()}\\assets\\settings.json", json_data)

    system('cls')
    print(f""""\n{banner}\n {c}[{w}INFO{c}]{w} The number of explored pages has been succesfully set to "{Explored_pages}" !""")
    sleep(2)
    settings_controler()


# <----- size updater ----->
def update_size(banner: str, c: str, w: str):
    system("cls")
    valid_sizes = ["XS", "S", "M", "L", "XL", "XXL", "XXXL", "4XL", "5XL", "6XL", "7XL", "8XL", "38", "39", "40", "41", "42", "43", "43.5", "44", "44.5", "45", "45.5", "46", "47", "48", "49", "Allsizes"]
    size = input(f"\n{banner}\n {c}[{w}->{c}]{w} Enter a size here (M, S, L, 38, 45.. OR Allsizes): ")
    if size not in valid_sizes:
        system("cls")
        print(f"\n{banner}\n {c}[{w}!{c}]{w} Please enter a correct size like (M, S, L, 38, 45.. OR Allsizes)")
        sleep(2)
        settings_controler()

    settings = read_json(f"{getcwd()}\\assets\\settings.json")
    settings["Size"] = size
    write_json(f"{getcwd()}\\assets\\settings.json", settings)

    system('cls')
    print(f"""\n{banner}\n {c}[{w}INFO{c}]{w} Size: "{size}" has been successfully registered !""")
    sleep(2)
    settings_controler()


# <----- margin updater ----->
def update_margin(banner: str, c: str, w: str):
    system("cls")
    margin = input(f"\n{banner}\n {c}[{w}->{c}]{w} Enter a decrease margin (%): ")
    try:
        margin = int(margin)
        if margin >= 99:
            system("cls")
            print(f"\n{banner}\n {c}[{w}!{c}]{w} Please enter a correct decrease margin (from 0 to 99)")
            sleep(2)
            settings_controler()
    except ValueError:
        system("cls")
        print(f"\n{banner}\n {c}[{w}!{c}]{w} Please enter a correct decrease margin (without the % symbol)")
        sleep(2)
        settings_controler()

    json_data = read_json(f"{getcwd()}\\assets\\settings.json")
    json_data["Margin"] = str(margin)
    write_json(f"{getcwd()}\\assets\\settings.json", json_data)
    
    system('cls')
    print(f"""\n{banner}\n {c}[{w}INFO{c}]{w} The decrease margin has been well defined at "{margin}%" !""")
    sleep(2)
    settings_controler()


# <----- webhhok updater ----->
def update_webhook(banner: str, c: str, w: str):
    system("cls")
    webhook = input(f"\n{banner}\n {c}[{w}->{c}]{w} Enter your discord webhook: ")
    settings = read_json(f"{getcwd()}\\assets\\settings.json")
    settings["Webhook"] = str(webhook)
    write_json(f"{getcwd()}\\assets\\settings.json", settings)

    system('cls')
    print(f"\n{banner}\n {c}[{w}INFO{c}]{w} Webhook: {webhook} has been successfully registered !")
    sleep(2)
    settings_controler()
    
    
# <----- item id updater ----->
def item_id_updater(banner: str, c: str, w: str):
    system('cls')
    item_id = input(f"\n{banner}\n {c}[{w}->{c}]{w} Enter a type item id here: ")
    json_data = read_json(f"{getcwd()}\\assets\\settings.json")
    try:
        int(item_id)
    except Exception as e:
        system("cls")
        print(f"\n{banner}\n {c}[{w}!{c}]{w} Please enter a correct type item ID")
        sleep(2)
        settings_controler()
    
    json_data["Item type"] = str(item_id)
    write_json(f"{getcwd()}\\assets\\settings.json", json_data)
    system('cls')
    print(f"""\n{banner}\n {c}[{w}INFO{c}]{w} Item type: "{item_type_converter(item_id)}" has been successfully registered !""")
    sleep(2)
    settings_controler()


# <----- brand updater ----->
def update_brand(banner: str, c: str, w: str):
    system('cls')
    brand_id = input(f"""\n{banner}\n {c}[{w}->{c}]{w} Enter a brand id here: """)
    try:
        int(brand_id)
    except Exception as e:
        system("cls")
        print(f"""\n{banner}\n {c}[{w}!{c}]{w} Please enter a correct brand ID""")
        sleep(2)
        settings_controler()

    json_data = read_json(f"{getcwd()}\\assets\\settings.json")
    json_data["Brand"] = str(brand_id)
    write_json(f"{getcwd()}\\assets\\settings.json", json_data)

    system('cls')
    print(f"""\n{banner}\n {c}[{w}INFO{c}]{w} Brand "{brand_converter(brand_id)}" has been successfully registered !""")
    sleep(2)
    settings_controler()


# <----- webhook sender ----->
def webhook_sender(item, webhook_link):
    try:
        webhook = DiscordWebhook(
                url=webhook_link,
                username="Vingod")
        embed = DiscordEmbed(title=item[1], color='FF1F1F')
        
        embed.set_image(url=item[6])
        embed.add_embed_field(name='Brand :tickets:', value=item[4].replace(" marque\xa0:", ""))
        embed.add_embed_field(name='Size :nut_and_bolt:', value=item[5].replace(" taille\xa0:", ""))
        embed.add_embed_field(name='Price :dollar:', value=item[2].replace(" prix\xa0:", "" + '€'))
        embed.add_embed_field(name='Date :globe_with_meridians:', value=item[7])
        embed.add_embed_field(name='Location :earth_americas:', value=item[8])
        embed.add_embed_field(name='Seller feedbacks :crystal_ball:', value=item[9])
        embed.add_embed_field(name='Product Link :link:', value=shortlink(item[0]), inline=True)

        embed.set_author(name='Vingod',
                        icon_url='https://thumbs4.imagebam.com/a5/88/be/MEJ5GIK_t.png')
        embed.set_footer(text='Vingod by 0xSp00f3d')
        embed.set_timestamp()
        webhook.add_embed(embed)
        webhook.execute()
        sleep(2)
    except Exception as e:
        system("cls")
        print(f"\n{banner}\n {c}[{w}!{c}]{w} Error while sending products in the webhook !")
        sleep(2)
        main(banner, c, w)


# <----- webhook checker ----->
def webhook_checker(webhook_link):
    try:
        resp = get(webhook_link)
        if resp.status_code != 200:
            return "Invalid"
        else:
            return "Valid"
    except Exception as e: 
        return "Invalid"
    
    
# <----- link builder ----->
def link_builder(brand_id,type_id, size, count):
    size = size_converter(size)
    if size == "none":
        link = f"https://www.vinted.fr/vetements?brand_id[]={brand_id}&catalog[]={type_id}&page{count + 1}"
    else:
        link = f"https://www.vinted.fr/vetements?brand_id[]={brand_id}&catalog[]={type_id}&size_id[]={size}&page{count + 1}"
    return link
    
    
# <----- progress bar ----->
def progressbar(banner, w, bar):
    system("cls")
    print(f"\n{banner}\n {w}{bar}")

def shortlink(link):
    s = Shortener()
    return s.tinyurl.short(link)
    
# <----- settings controler ----->
def settings_controler():
    system("cls")
    setting_choice = input(f"""\n{banner}
 {c}[{w}+{c}]{w} Settings:                    
                        
 {c}[{w}1{c}]{w} Set/change: Brand              |   {c}[{w}4{c}]{w} Set/change: Decrease margin (%)       | {c}[{w}7{c}]{w} Clear product memory
 {c}[{w}2{c}]{w} Set/change: Item type          |   {c}[{w}5{c}]{w} Set/change: Explored pages (number)   | {c}[{w}8{c}]{w} Back to main menu
 {c}[{w}3{c}]{w} Set/change: Size               |   {c}[{w}6{c}]{w} Set/change: Webhook (discord)         |
 -----\n
 {c}[{w}->{c}]{w} Enter your choice here: """)
    try:
        if int(setting_choice) > 8 or int(setting_choice) <= 0:
            system('cls')
            print(f"\n{banner}\n {c}[{w}!{c}]{w} Incorrect choice ! (Please select a number between 1 and 8)")
            sleep(3)
            settings_controler()
        else:
            pass
    except Exception as e:
        system('cls')
        print(f"\n{banner}\n {c}[{w}!{c}]{w} Incorrect choice ! (Please select a correct number)")
        sleep(3)
        settings_controler()

    # brand changer
    if setting_choice == str(1):
        update_brand(banner,c ,w)

    # item type changer
    elif setting_choice == str(2):
        item_id_updater(banner, c, w)

    # item size changer
    elif setting_choice == str(3):
        update_size(banner, c, w)

    # item margin % changer
    elif setting_choice == str(4):
        update_margin(banner, c, w)
        
    # explored pages
    elif setting_choice == str(5):
        update_explored_pages(banner, c, w)

    # discord webhook
    elif setting_choice == str(6):
        update_webhook(banner,c ,w)
    
    # clear json
    elif setting_choice == str(7):
        json_cleaner(f"products.json")
        
    # exit
    elif setting_choice == str(8):
        main(banner, c, w)


# <----- bot ----->
def bot():
    try:
        # webhook checker
        if webhook_checker(get_settings()[5]) != "Valid":        
            system('cls')
            print(f"\n{banner}\n {c}[{w}!{c}]{w} Please enter a valid webhook..")
            sleep(3)
            main(banner, c, w)
        else:
            pass
            
        # bot settings
        brand_id, type_id, size, decrease_margin, exp_pages, webhook_link = get_settings()
        
        # set progressbar
        progressbar(banner, w, f"{c}[{w}█-------------------{c}]{w} 5% - Opening link..")
        
        # <----- selenium configuration ----->
        options = webdriver.FirefoxOptions()
        options.add_argument('-headless')
        driver = webdriver.Firefox(options=options)
        # <----- counting vars ----->
        count = 0
        item_count = 0

        # creation of list
        items_list = []
        final_list = []
        price_list = []
        json_notlisted = []
        good_items = []

        
        # find items
        for _ in range(int(exp_pages)):
            # progressbar
            progressbar(banner, w, f"{c}[{w}██------------------{c}]{w} 10% - Pages exploration... ({int(_)+1} of {exp_pages})")
            try:
                items = []
                driver.get(link_builder(brand_id,type_id, size, count))
                count = count + 1
                items = items + driver.find_elements(By.CLASS_NAME, "web_ui__ItemBox__overlay")

                for item in items:
                    it1 = item.get_attribute('href')
                    it2 = item.get_attribute('title')
                    it = it1 + ", " + it2
                    items_list.append(it)
            except Exception as e:
                pass

        progressbar(banner, w, f"{c}[{w}████----------------{c}]{w} 20% - Item classification..")
    
        # extract scraped elements 
        for num in range(len(items_list)):
            item_count = item_count + 1
            final_list.append(items_list[num].split(","))
        
        # doublets deleter
        final_list = remove_duplicate(final_list)

        # extract price
        for item in final_list:
            try:
                string = str(item[2]).replace(" prix\xa0:", "")
                price_list.append(int(string))
            except Exception as e:
                del item
                
        #progressbar
        progressbar(banner, w, f"{c}[{w}██████--------------{c}]{w} 30% - Writing json files..")
        
        # json system
        
        try:
            products_json = read_json(f"{getcwd()}\\assets\\products.json")
        except Exception as e:
            write_file(f"{getcwd()}\\assets\\products.json", "{}")
            products_json = read_json(f"{getcwd()}\\assets\\products.json")
        json_notlisted = [item for item in final_list if item[0] not in products_json.values()]

        for item in final_list:
            if item[0] not in products_json.values():
                products_json.update({f"{lettergen(5)}": item[0]})

        write_json(f"{getcwd()}\\assets\\products.json", products_json)
            
        # find image and class the products
        for item in json_notlisted:
            picture = []
            progressbar(banner, w, f"{c}[{w}██████████----------{c}]{w} 50% - Exploration of items... ({int(json_notlisted.index(item))+1} of {len(json_notlisted)})")
            try:
                if int(item[2].replace(" prix\xa0:", "")) <= int(int(mean(price_list)) - (int(mean(price_list)) * (int(decrease_margin)/100))):
                    driver.get(item[0])
                    picture = driver.find_element(By.XPATH,
                                                "/html/body/main/div/section/div/main/div/section[1]/section/div[1]/figure[1]/a/img")
                    date = driver.find_element(By.XPATH,
                                                "/html/body/main/div/section/div/main/div/aside/div[1]/div[1]/div[2]/div[9]/div[2]/time")
                    location = driver.find_element(By.XPATH,
                                                "/html/body/main/div/section/div/main/div/aside/div[1]/div[1]/div[2]/div[6]/div[2]")
                    feedback = driver.find_element(By.XPATH,
                                                    "/html/body/main/div/section/div/main/div/aside/div[3]/a/div[2]/div[2]/div")

                    item.append(picture.get_attribute("data-src"))
                    item.append("Day: " + ((date.get_attribute("title")).split(' '))[0] + "\nTime: " + ((date.get_attribute("title")).split(' '))[1])
                    try:
                        if len(((location.text).split(' '))[0]) > 15 :
                            item.append("City: None :x:" + "\nCountry: " + ((location.text).split(','))[1])
                        else:
                            item.append("City: " + ((location.text).split(','))[0] + "\nCountry: " + ((location.text).split(','))[1])
                    except Exception as e:
                        item.append("City: " + ((location.text).split(','))[0] + "\nCountry: " + ((location.text).split(','))[1])
                    try:
                        stars = feedback.get_attribute("aria-label")[13] + "." + feedback.get_attribute("aria-label")[15]
                        item.append(":star:"*int(round(float(stars))) + f" ({stars})")
                    except Exception as e:
                        item.append("This seller have\nno feedbacks :x:")
                        
                    good_items.append(item)
                else:
                    pass
            except Exception as e:
                del item
        
        # detect no product found
        if good_items == []:
            system("cls")
            input(f"\n{banner}\n {c}[{w}INFO{c}]{w} No items found :/")
            main(banner, c, w)
        else:
            pass
    
        progressbar(banner, w, f"{c}[{w}████████████████----{c}]{w} 80% - Sending information to webhook..")  
        # webhook system
        
        for item in good_items:
            #progressbar
            progressbar(banner, w, f"{c}[{w}████████████████----{c}]{w} 80% - Sending information to webhook... ({int(good_items.index(item))+1} of {len(good_items)})")
            webhook_sender(item, webhook_link) 
        
        # end
        progressbar(banner, w, f"{c}[{w}████████████████████{c}]{w} 100% - Operation completed !..")
        driver.close()
        try:
            remove("geckodriver.log")
        except:
            pass
        sleep(2)
        main(banner, c, w)

    except Exception as e:
        system('cls')
        print(f"\n{banner}\n {c}[{w}!{c}]{w} An error has occurred, please check settings and retry..")
        sleep(3)
        main(banner, c, w)


# <----- main & ui ----->
def main(banner, c, w):
    init()
    system("cls")
    choice = input(f"""\n{banner}
 {c}[{w}+{c}]{w} Menu:              |    {c}[{w}INFO{c}]{w} Current Settings:            
                        |
 {c}[{w}1{c}]{w} Start              |    {c}[{w}>{c}]{w} Brand: {brand_converter(get_settings()[0])} ; {c}[{w}>{c}]{w} Decrease margin (%): {str(get_settings()[3]) + "%"}
 {c}[{w}2{c}]{w} Bot setup          |    {c}[{w}>{c}]{w} Item type: {item_type_converter(get_settings()[1])} ; {c}[{w}>{c}]{w} Explored pages (number): {get_settings()[4]}
 {c}[{w}3{c}]{w} Exit               |    {c}[{w}>{c}]{w} Size: {get_settings()[2]} ; {c}[{w}>{c}]{w} Discord webhook: {webhook_checker(get_settings()[5])}
 -----\n
 {c}[{w}->{c}]{w} Enter your choice here: """)
    
    #debug
    try:
        if int(choice) > 3 or int(choice) <= 0:
            system('cls')
            print(f"\n{banner}\n {c}[{w}!{c}]{w} Incorrect choice ! (Please select a number between 1 and 3)")
            sleep(3)
            main(banner, c, w)
        else:
            pass
    except Exception as e:
        system('cls')
        print(f"\n{banner}\n {c}[{w}!{c}]{w} Incorrect choice ! (Please select a correct number)")
        sleep(3)
        main(banner, c, w)

    #bot start
    if choice == "1":
        bot()

    elif choice == "2":
        settings_controler()

    elif choice == "3":
        system("cls")
        print(f"\n{banner}\n {c}[{w}INFO{c}]{w} See you later ;)")
        sleep(2)
        exit()


#main execution
if __name__ == '__main__':
    system("title VINGOD")
    integrity_checker()
    rich_presence()
    main(banner, c, w)