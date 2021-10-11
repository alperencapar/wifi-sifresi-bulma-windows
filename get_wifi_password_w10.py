import subprocess       #?for system commands
import re               #?reguler expression

#? bilgisayarda kayıtlı olan wifi profillerine bakıyoruz ve gelen metini değişkene kayıt ediyoruz
command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()

#? gelen profil metni sade olarak gelmediği için reguler expression kullanılarak sadece wifi profil adı alınıyor ve liste olarak ekleniyor
#? en baş ve en sondaki parantez gelen veriyi listeye çeviriyor ve değişkene atıyor
profiles = (re.findall("All User Profile     : (.*)\r", command_output))


wifi_list = list()

#? kayıtlı profil var ise
if len(profiles) != 0:
    
    
    for profile in profiles:
        #? tek tek wifi profil adını alıyor
        
        wifi_profile = {}
        
        #? wifi profil adı ile profil bilgisine bakılıyor
        profile_info = subprocess.run(["netsh", "wlan", "show","profile", profile], capture_output = True).stdout.decode()
        
        
        if re.search("Security key           : Absent", profile_info):
            #? wifi profilinin şifresi sistemde kayıtlı değilse:
            continue
            #? şifre sistemde kayıtlı değilse atla
            
        else:
            #? wifi şifresi sistemde kayıtlı ise:
            
            #? dictionary'e ssid anahatarı ve değer olarak profil adı ekleniyor
            wifi_profile["ssid"] = profile
            
            #? sistemden profilin wifi bilgileriyle birlikte şifresini göstermesi isteniyor ve gelen yazı değişkene atanıyor
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", profile, "key=clear"], capture_output = True).stdout.decode()
            
            #? sadece şifresini almak için regular expression ile şifre ayıklaması yapılıyor
            password = re.search("Key Content            : (.*)\r", profile_info_pass)
            
            
            if password == None:
                #? şifre yoksa:
                
                wifi_profile["password"] = None
                
            else:
                #? wifi şifresi var ise dictionary'e password anahtarı altında, şifre değeri ekleniyor
                wifi_profile["password"] = password[1]
            
        #? ssid ve şifrenin kaydedildiği dictionary listeye ekleniyor. Böylece for döngüsü ile hepsine erişilebilir
        wifi_list.append(wifi_profile)
        
#? gelen ssid ve şifrenin olduğu dict. listeye aktarılmıştı, for döngüsü ile hepsini yazdırıyoruz
for i in range(len(wifi_list)):
    print(wifi_list[i])