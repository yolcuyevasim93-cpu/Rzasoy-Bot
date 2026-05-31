import asyncio
import random
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from flask import Flask
from threading import Thread

# Konfiqurasiya
BOT_TOKEN = "8421111075:AAGCv5a7M1YyrCrHsrSll780ca17dNDHKKI"
BOT_NAME = "@CroniqueBot".lower()

# Bot və Dispatcher
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# Flask (Serverin daim aktiv qalması üçün)
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# Oyun dataları
aktiv_oyunlar = {}
SOZLER = ["Abraham Linkoln", "Allergiya", "Angina", "Anemiya", "Astma", "Atatürk", "Audi", "BMW", "Bethoven", "Bronxit", 
    "Cəlil Məmmədquluzadə", "Chevrolet", "Corc Vaşinqton", "Depressiya", "Ferrari", "Fikrət Əmirov", "Ford", 
    "Hipertoniya", "Honda", "Hyundai", "İlham Əliyev", "Kia", "Mədəniyyət", "Mercedes", "Mirzə Ələkbər Sabir", 
    "Motsart", "Nelson Mandela", "Nissan", "Nizami Gəncəvi", "Osteoxondroz", "Pnevmoniya", "Porsche", "Qara Qarayev", 
    "Qastrit", "Şarl de Qoll", "Şəkər", "Təbiət", "Tesla", "Texnologiya", "Toyota", "Üzeyir Hacıbəyli", "Abadlıq", 
    "Abidə", "Abonent",    "Plakat", "Plastik", "Plat", "Pleşka", "Plov", "Poçtalyon", "Polad", "Polis", "Portağal", "Pota", 
    "Pozan", "Prezident", "Proqram", "Prospekt", "Pult", "Pusqu", "Qab", "Qabıq", "Qabırğa", "Qadağa", 
    "Qafiyə", "Qala", "Qalereya", "Qalıq", "Qamış", "Qanun", "Qapı", "Qapıçı", "Qara", "Qayda", 
    "Qaynaq", "Qayçı", "Qaz", "Qazan", "Qəbz", "Qədim", "Qəhqəhə", "Qəhrəman", "Qəlbi", "Qələbə", 
    "Qələm", "Qərar", "Qəsidə", "Qəşəng", "Qəza", "Qəzet", "Qəzəb", "Qıfıl", "Qıraq", "Qışqırıq", 
    "Qısa", "Qızğın", "Qızıl", "Qoçaq", "Qol", "Qolbaq", "Qonşu", "Qorxu", "Qovluq", "Qoz", 
    "Qrafika", "Qranit", "Qrup", "Quba", "Qul", "Qum", "Qurğu", "Qurultay", "Quru", "Qutan", 
    "Quyu", "Qüvvə", "Qüzey", "Qrip", "Şəkər", "Astma", "Bronxit", "Qastrit", "Hipertoniya", 
    "Allergiya", "Depressiya", "Osteoxondroz", "Angina", "Pnevmoniya", "Mercedes", "BMW", 
    "Toyota", "Hyundai", "Kia", "Ford", "Tesla", "Audi", "Honda", "Nissan", "Chevrolet", 
    "Porsche", "Ferrari", "İlham Əliyev", "Atatürk", "Corc Vaşinqton", "Abraham Linkoln", 
    "Nelson Mandela", "Şarl de Qoll", "Nizami Gəncəvi", "Üzeyir Hacıbəyli", "Fikrət Əmirov", 
    "Qara Qarayev", "Mirzə Ələkbər Sabir", "Cəlil Məmmədquluzadə", "Bethoven", "Motsart", 
    "Təbiət", "Texnologiya", "Mədəniyyət", "Kalla", "Kama", "Kamera", "Kanal", "Kapot", 
    "Karvan", "Kasa", "Kassir", "Kəbə", "Kəhkəşan", "Kələm", "Kəlbətin", "Kəllə", "Kəmar", 
    "Kənar", "Kəpənək", "Kibrit", "Kilim", "Açıq", "Alovlanma", "Alqı-satqı", "Anbarlama", "Antikvar", "Arzuolunan", "Aşırım", "Atlı", "Aviasiya", "Azlıq",
    "Bədəvi", "Bənövşə", "Bərabərlik", "Bərpaetmə", "Bəxşiş", "Bilikli", "Bölüşmə", "Böyümə", "Bürclü", "Bürokrat",
    "Cəfəngiyat", "Cəhrayı", "Cəllad", "Cəmiyyətşünas", "Cəngəllik", "Cərəyan", "Cəsarətli", "Cırcırama", "Cizgili", "Cücərmə",
    "Çatdırılma", "Çeviklik", "Çılpaqlıq", "Çimərlikdə", "Çiçəklənmə", "Çoxaldıcı", "Çoxmərtəbəli", "Çörəkqırıntısı", "Çubuqçu", "Çuxurlu",
    "Dabanlıq", "Dadi", "Daimi", "Dalğalı", "Damazlıq", "Daraqlı", "Darıxma", "Dəbdəbəli", "Dəfələrlə", "Dəhşətli",
    "Dəmiryol", "Dənizçi", "Dəqiq", "Dərəbəylik", "Dərindən", "Dəstəmaz", "Dəyərləndirmə", "Dəzgahçı", "Dinamika", "Direktorluq",
    "Diskussiya", "Dizaynlı", "Doğulma", "Doğruluq", "Döşəməçi", "Dövriyyə", "Dönərgə", "Dumanlıq", "Düyünlü", "Düyməli",
    "Düzəltmə", "Düzgünlük", "Ekskursiya", "Eksponent", "Ekstremal", "Ekvator", "Elmi", "Elçilik", "Emanətçi", "Eniş",
    "Epizod", "Erkən", "Estetik", "Etibarlı", "Etiraf", "Etnoqraf", "Evdar", "Ezam", "İcraat", "İdarəetmə",
    "İfadəli", "İftira", "İgüd", "İxtiraçı", "İlahi", "İləri", "İmkanlı", "İmtahan", "İncəsənət", "İndi",
    "İnsanlıq", "İnternet", "İntizam", "İpi", "İradəli", "İri", "İsrafçı", "İstəkli", "İstirahət", "İtirilmiş",
    "İzahlı", "İzci", "İzolyasiya", "Jalüz", "Jelatin", "Jetonlu", "Jiletli", "Jurnalsız", "Kabelçilik", "Kafes",
    "Kair", "Kaman", "Kameraçı", "Kanalizasiya", "Kapitan", "Karat", "Karnaval", "Kasaçı", "Kəklikotu", "Kəmiyyət",
    "Kənarlaşdırma", "Kəpənəksiz", "Kəsilmə", "Kəşf", "Kətanlı", "Kibritqabı", "Kifli", "Kilolu", "Kimsə", "Kinoaktyor",
    "Kioskqurucu", "Kirəmit", "Kirpiotu", "Kişilər", "Klassika", "Klimat", "Klinika", "Klip", "Klod", "Köhnə",
    "Köklü", "Köçürmə", "Körpü", "Körpə", "Kölgəli", "Krançı", "Kredit", "Kriminalistika", "Kristallaşma", "Külçə",
    "Kürə", "Kütlə", "Lal", "Laminatçı", "Lampalı", "Ləhcəli", "Ləpə", "Ləqəbli", "Lətafət", "Ləzzətli",
    "Lifli", "Limanlı", "Limonlu", "Linc", "Linzalı", "Litrlik", "Lüğəvi", "Lükslü", "Maqnit", "Məcburi",
    "Məktub", "Məşğul", "Məzəli", "Məhəllə", "Məftunedici", "Məşhurlaşma", "Məqamlı", "Məxfiləşdirmə", "Məzuniyyət", "Meydan",
    "Mənbəli", "Müasir", "Müəllimə", "Müvəffəqiyyət", "Müəssisə", "Müxtəliflik", "Müddətsiz", "Müvəqqəti", "Müdafiəçi", "Müəyyənlik",
    "Mülkiyyət", "Mühasiblik", "Müzakirəli", "Müşahidə", "Nəqliyyatçı", "Nəzarətçi", "Nəzəriyyə", "Nəsilcə", "Nəfəslik", "Nəğməkar",
    "Nəticələnmə", "Neytral", "Neyronlu", "Nigarət", "Nişanlı", "Nizamnamə", "Niyyətli", "Nömrələmə", "Növbətçi", "Nümayiş",
    "Obyektiv", "Ocaqlı", "Oğurluqçu", "Okeanşünas", "Oktyabrda", "Olimpiadalı", "Onluq", "Operativ", "Optik", "Orqanik",
    "Otlaq", "Oturacaqlı", "Ovçu", "Ovuc dolusu", "Oymalı", "Oyunbaz", "Pambıqlı", "Panoramik", "Pandasız", "Pantomim",
    "Paralellik", "Paraşütçü", "Parklı", "Parketçi", "Pasportlu", "Pedaqoji", "Pencərəli", "Pensiyalı", "Pərgarla", "Pələngi",
    "Pərdəli", "Perimetrli", "Peykçi", "Piknikçi", "Piləkənsiz", "Pilotlu", "Pinqvinli", "Pioner", "Plakatlı", "Plastikləşmə",
    "Platlı", "Pleşkalı", "Plovlu", "Poçtalyonsuz", "Poladlı", "Polislik", "Portağallı", "Potansial", "Pozanlı", "Prezidentlik",
    "Proqramçı", "Prospektli", "Pultlu", "Pusquçu", "Qablı", "Qabıqlı", "Qabırğalı", "Qadağalı", "Qafiyəli", "Qalal",
    "Qalereyalı", "Qalıqlı", "Qamışlıq", "Qanunverici", "Qapıçı", "Qaraçı", "Qaydalı", "Qaynaqçı", "Qayçılı", "Qazlı",
    "Qazanlı", "Qəbzlə", "Qədimlik", "Qəhqəhəli", "Qəhrəmanlıq", "Qəlbən", "Qələbəsiz", "Qələmşünas", "Qərargah", "Qəsidəçi",
    "Qəşənglik", "Qəzalı", "Qəzetçi", "Qəzəbli", "Qıfıllı", "Qıraqlı", "Qışqırıqlı", "Qısalıq", "Qızğına", "Qızıllığı",
    "Qoçaqlıq", "Qollu", "Qolbaqlı", "Qonşuluq", "Qorxulu", "Qovluqçu", "Qozlu", "Qrafik", "Qranitli", "Qruplaşma",
    "Qubalı", "Qulluqçu", "Qumluq", "Qurğulu", "Qurultayda", "Quruluş", "Qutanlı", "Quyulu", "Qüvvətli", "Qüzeyli",
    "Qripli", "Şəkərli", "Astmalı", "Bronxitli", "Qastritli", "Hipertoniyalı", "Allergiyalı", "Depressiyalı", "Osteoxondrozlu", "Anginalı",
    "Pnevmoniyalı", "Mercedesli", "BMW-li", "Toyotalı", "Hyundai-lı", "Kialı", "Fordlu", "Teslalı", "Audili", "Hondalı",
    "Nissanlı", "Chevroletli", "Porscheli", "Ferrarili", "İlhamlı", "Atatürkçü", "Corclu", "Abrahamlı", "Nelsonlu", "Şarlı",
    "Nizamili", "Üzeyirli", "Fikrətli", "Qaralı", "Mirzəli", "Cəlilli", "Bethovenli", "Motsartlı", "Təbiətşünas", "Texnoloji",
    "Mədəni", "Kallalı", "Kamalı", "Kamançalı", "Kameralı", "Kanallı", "Kapotlu", "Karvanlı", "Kasalı", "Kassirli",
    "Kəbəli", "Kəfənli", "Kəhkəşanlı", "Kələmli", "Kəlbətinli", "Kəlləli", "Kəmərli", "Kənarlı", "Kəpənəkli", "Kərpicli",
    "Kəşfiyyatçı", "Kəskinlik", "Kətanlıq", "Kibritli", "Kifli", "Kilidli", "Kilimli", "Kilsəli", "Kimyəvi", "Kinoşünas",
    "Kiosklu", "Kirayənişin", "Kirpili", "Kişilik", "Kitabxanalı", "Klassikalı", "Klaviaturalı", "Klişeli", "Klişli", "Klublu",
    "Köməkçilik", "Körpəlik", "Köklü", "Köçərilik", "Kölgələnən", "Kran", "Kriminallıq", "Kristallı", "Küləkli", "Kürsülü",
    "Kütləvi", "Laləli", "Laminatlı", "Lampalı", "Ləhcəsiz", "Ləçəkli", "Ləqəbsiz", "Ləzizli", "Ləzzətsiz", "Lifli",
    "Limanlıq", "Limonat", "Linc", "Linzalı", "Litr", "Lüğətli", "Lükslü", "Maşınlı", "Məişəti", "Məktəbli",
    "Məşğulluq", "Məzmunlu", "Məzəsiz", "Məhəbbətli", "Məftunlu", "Məşhurluq", "Məqamlıq", "Məxfilikli", "Məzunlu", "Meyvəli",
    "Mənbəsiz", "Müasirlik", "Müəllimlik", "Müvəffəq", "Müasir", "Müxtəlif", "Müddəti", "Müvəqqəti", "Müdafiə", "Müəyyən",
    "Mülkü", "Mühasibat", "Müzakirə", "Müşavirəli", "Nəqliyyat", "Nəzarət", "Nəzəri", "Nəsilli", "Nəfəsli", "Nəğməli",
    "Nəticəli", "Neytrallıq", "Neyron", "Nigar", "Nişan", "Nizam", "Niyyət", "Nömrəli", "Növdən", "Nümayəndəlik",
    "Obyektli", "Ocaqlıq", "Oğurluq", "Okeanlı", "Oktyabr", "Olimpiadalıq", "Onurğalı", "Operalı", "Optik", "Orqan",
    "Otlu", "Oturacaq", "Ovvur", "Ovucluq", "Oymaq", "Oyunlu", "Pambıqlıq", "Panamalı", "Pandasız", "Pantomimalı",
    "Paralellər", "Paraşüt", "Parkda", "Parket", "Pasport", "Pedaqoji", "Pencərə", "Pensiyalıq", "Pərgar", "Pələng",
    "Pərdəli", "Perimetr", "Peyk", "Piknik", "Piləkən", "Pilot", "Pinqvin", "Pion", "Plakat", "Plastik",
    "Plat", "Pleşka", "Plovsuz", "Poçt", "Polad", "Polis", "Portağal", "Pota", "Pozan", "Prezident",
    "Proqramlı", "Prospekt", "Pultsuz", "Pusqu", "Qabıq", "Qabıqlı", "Qabırğa", "Birdəfəlik", "Birgəlik",
    "Birincilik", "Birlikdə", "Birokratik", "Bitkili", "Blenderli", "Bloklu", "Boksçu", "Bolca", "Boşluq", "Boyalı",
    "Boyunluq", "Boyunbağılı", "Bölməli", "Bölüşdürən", "Boranılı", "Borulu", "Bozluq", "Böcəkli", "Bölgəli", "Böyüklük",
    "Büdcəli", "Bulaqlı", "Buludlu", "Bürclük", "Bürünclü", "Bürolu", "Buzluq", "Camaatlı", "Cavanlıq", "Cazibədar",
    "Cəbhəçi", "Cədvəlli", "Cəhdlə", "Cəlbedici", "Cəmilik", "Cəmiyyətsiz", "Cənnətli", "Cəriməli", "Cərrahlıq", "Cəsarətsiz",
    "Cəsurca", "Cəzalı", "Cihazlı", "Cildli", "Cizgili", "Cüməli", "Cücəli", "Cürbəcürlük", "Çadırsız", "Çağırışlı",
    "Çalağanlı", "Çalışqanlıq", "Çamadanlı", "Çantalı", "Çapçı", "Çapalı", "Çatlı", "Çatılı", "Çaxırlı", "Çaylı",
    "Çaynikli", "Çəkili", "Çəlikli", "Çəltikli", "Çəmənlik", "Çətinlik", "Çərçivəli", "Çeşidli", "Çığırlı", "Çılçıraqlı",
    "Çiləli", "Çilingərlik", "Çimərlikli", "Çinli", "Çiçəkli", "Çirkinlik", "Çiyinli", "Çobanlıq", "Çoxluqla", "Çörəkçi",
    "Çörəksiz", "Çubuqlu", "Çuxurlu", "Çürüklük", "Dabanlı", "Dadlı", "Dairəvi", "Dalaqlı", "Daldalan", "Dalılı",
    "Damcılı", "Damaqlı", "Damarlı", "Daraqlı", "Darvazalı", "Daxmalı", "Dəbli", "Dəfəlik", "Dəhlizli", "Dəmirsiz",
    "Dəmirçixana", "Dənli", "Dəqiqəlik", "Dərəli", "Dərnəkli", "Dərslik", "Dərsli", "Dəstəkli", "Dəstəli", "Dəvəli",
    "Dəyərli", "Dəyirmançı", "Dəzgahlı", "Dibçək", "Dincəlmə", "Dinamiklik", "Direktor", "Diskli", "Dizaynerlik", "Doğumlu",
    "Doğruluq", "Döllü", "Döşəməli", "Dövri", "Dönüşlü", "Dumanlı", "Düyünlü", "Düyməli", "Düzgün", "Düzənlik",
    "Eksponatlı", "Ekspedisiyalı", "Ekspertiz", "Elektrikli", "Elementli", "Elitalı", "Emanət", "Enlilik", "Epitetli", "Eramlı",
    "Estakadalı", "Etik", "Etnoqrafik", "Evlilik", "Ezamiyyə", "İnflyasiyalı", "İqtisadi", "İnnovasiyalı", "İnvestor", "İşgüzar",
    "İcmalı", "İpəkli", "İbadətli", "İddialı", "İtaliyalılıq", "İzahlı", "İrsiyyət", "İradəsiz", "İtili", "İzahatlı",
    "Jurnallı", "Jurnalistlik", "Jetonlu", "Jiletli", "Jurnalistli", "Kabel", "Kafeterya", "Kafelli", "Kainatlı", "Kamançalı",
    "Kəhrizli", "Kəşfiyyat", "Kəklikli", "Kəramətli", "Kərpicli", "Kəskinlik", "Kətanlı", "Kəfənli", "Kifli", "Kilsəli",
    "Kilidli", "Kinolu", "Kioskalı", "Kirayə", "Kirpili", "Kitabxanalı", "Klaviaturalı", "Klişeli", "Klişli", "Klublu",
    "Köməkçili", "Körpəlik", "Köklü", "Köçərilik", "Kölgəli", "Kranlı", "Kriminallıq", "Kristallı", "Küləkli", "Kürsülü",
    "Kütləvi", "Laləli", "Laminatlı", "Lampalı", "Ləhcəli", "Ləçəkli", "Ləqəbli", "Ləziz", "Ləzzətli", "Lifli",
    "Limanlı", "Limonlu", "Linc", "Linzalı", "Litrli", "Lüğətli", "Lüks", "Maşınlı", "Məişətli", "Məktəbli",
    "Məşğulluq", "Məzmunlu", "Məzəli", "Məhəbbətli", "Məftunlu", "Məşhurluq", "Məqamlı", "Məxfilik", "Məzunlu", "Meyvəlik",
    "Mənbəli", "Müasir", "Müəllimlik", "Müvəffəqiyyətli", "Müasirlik", "Müxtəliflik", "Müddətli", "Müvəqqəti", "Müdafiəli", "Müəyyən",
    "Mülki", "Mühasib", "Müzakirəli", "Müşavirə", "Nəqliyyatlı", "Nəzarət", "Nəzərli", "Nəsilli", "Nəfəsli", "Nəğməli",
    "Nəticəli", "Neytrallıq", "Neyronlu", "Nigar", "Nişanlı", "Nizamlı", "Niyyətli", "Nömrəli", "Növdən", "Nümayəndə",
    "Obyektli", "Ocaqlı", "Oğurluqçu", "Okeanlı", "Oktyabr", "Olimpiadalı", "Onurğalı", "Operalı", "Optik", "Orqan",
    "Otlu", "Oturacaqlı", "Ovlu", "Ovuc", "Oyma", "Oyunçu", "Pambıqlı", "Panamalı", "Pandalı", "Pantomimalı",
    "Paralelli", "Paraşütlü", "Parklı", "Parketli", "Pasportlu", "Pedaqoq", "Pencərəli", "Pensiyalı", "Pərgarlı", "Pələngli",
    "Pərdəli", "Perimetrli", "Peykli", "Piknikli", "Piləkənli", "Pilotlu", "Pinqvinli", "Pionlu", "Plakatlı", "Plastik",
    "Platlı", "Pleşkalı", "Plovlu", "Poçtalyon", "Poladlı", "Polis", "Portağallı", "Potalı", "Pozanlı", "Prezident",
    "Proqramlı", "Prospektli", "Pultlu", "Pusqu", "Qablı", "Qabıqlı", "Qabırğalı", "Qadağalı", "Qafiyəli", "Qalal",
    "Qalereyalı", "Qalıqlı", "Qamışlı", "Qanunlu", "Qapılı", "Qapıçı", "Qaralı", "Qaydalı", "Qaynaqlı", "Qayçılı",
    "Qazlı", "Qazanlı", "Qəbzli", "Qədimlik", "Qəhqəhəli", "Qəhrəmanlıq", "Qəlbi", "Qələbəli", "Qələmli", "Qərarlı",
    "Qəsidəli", "Qəşəng", "Qəzalı", "Qəzetli", "Qəzəbli", "Qıfıllı", "Qıraqlı", "Qışqırıqlı", "Qısalıq", "Qızğın",
    "Qızıllı", "Qoçaqlı", "Qollu", "Qolbaqlı", "Qonşulu", "Qorxulu", "Qovluqlu", "Qozlu", "Qrafik", "Qranitli",
    "Qruplu", "Qubalı", "Qullu", "Qumlu", "Qurğulu", "Qurultaylı", "Qurulu", "Qutanlı", "Quyulu", "Qüvvətli",
    "Qüzeyli", "Qripli", "Şəkərli", "Astmalı", "Bronxitli", "Qastritli", "Hipertoniyalı", "Allergiyalı", "Depressiyalı", "Osteoxondrozlu"
# Maşın markaları
    "BMW", "Mercedes", "Audi", "Toyota", "Hyundai", "Kia", "Ford", "Tesla", "Honda", "Nissan", 
    "Chevrolet", "Porsche", "Ferrari", "Lamborghini", "Bugatti", "Rolls-Royce", "Bentley", "Jaguar", "Land-Rover", "Lexus", 
    "Mazda", "Mitsubishi", "Subaru", "Suzuki", "Volvo", "Volkswagen", "Skoda", "Peugeot", "Renault", "Citroen",
    
    # Geyim markaları
    "Nike", "Adidas", "Puma", "Reebok", "Zara", "Gucci", "Prada", "Chanel", "Versace", "Armani", 
    "Lacoste", "Levis", "H&M", "Bershka", "Mango", "Diesel", "Fendi", "Dior", "Balenciaga", "Under-Armour",
    
    # Paytaxtlar
    "Baku", "Ankara", "London", "Paris", "Berlin", "Roma", "Tokio", "Vaşinqton", "Moskva", "Astana", 
    "Tbilisi", "Tehran", "Madrid", "Amsterdam", "Ottava", "Kamberra", "Pekin", "Seul", "Atina", "Viyana",
    
    # Azərbaycan rayonları
    "Abşeron", "Ağcabədi", "Ağdam", "Ağdaş", "Ağstafa", "Ağsu", "Astara", "Babək", "Balakən", "Bərdə", 
    "Beyləqan", "Biləsuvar", "Cəbrayıl", "Cəlilabad", "Culfa", "Daşkəsən", "Füzuli", "Gədəbəy", "Goranboy", "Göyçay", 
    "Göygöl", "Hacıqabul", "İmişli", "İsmayıllı", "Kəlbəcər", "Kürdəmir", "Laçın", "Lənkəran", "Lerik", "Masallı", 
    "Neftçala", "Oğuz", "Ordubad", "Qəbələ", "Qax", "Qazax", "Qobustan", "Quba", "Qubadlı", "Qusar", 
    "Saatlı", "Sabirabad", "Sədərək", "Salyan", "Samux", "Şabran", "Şahbuz", "Şamaxı", "Şəki", "Şəmkir", 
    "Şərur", "Şuşa", "Siyəzən", "Tərtər", "Tovuz", "Ucar", "Yardımlı", "Yevlax", "Zaqatala", "Zəngilan", "Zərdab",

    # Digər mövzular (Texnologiya, Təbiət, Peşələr, Qida)
    "Kompüter", "Telefon", "Monitor", "Klaviatura", "İnternet", "Server", "Proqram", "Robot", "Dron", "Sensor",
    "Dağ", "Çay", "Dəniz", "Meşə", "Səhra", "Okean", "Bulud", "Ulduz", "Günəş", "Planet",
    "Müəllim", "Həkim", "Mühəndis", "Rəssam", "Memar", "Sürücü", "Aşpaz", "Yazıçı", "Pilot", "Jurnalist",
    "Alma", "Armud", "Üzüm", "Pomidor", "Xiyar", "Pendir", "Çörək", "Bal", "Şokolad", "Kofe",
    "Kitab", "Qələm", "Dəftər", "Çanta", "Saat", "Eynək", "Paltar", "Ayakkabı", "Şapka", "Kəmər",
    
    # +500 əlavə ümumi söz (təkrar olunmayan)
    "Açıqlama", "Axtarış", "Alqış", "Amansız", "Analitika", "Anlayış", "Aparıcı", "Arayış", "Arzu", "Aşpazlıq", 
    "Atəş", "Avadanlıq", "Azadlıq", "Babalıq", "Bahar", "Bələdçi", "Bərabər", "Bərəkət", "Bəsit", "Bəxtəvər", 
    "Bilik", "Birləşmə", "Bölüşmə", "Böyümə", "Büdcə", "Bürünc", "Büro", "Cavanlıq", "Cazibə", "Cəbhə", 
    "Cədvəl", "Cəhd", "Cəlb", "Cəmi", "Cənnət", "Cərimə", "Cərrah", "Cəsarət", "Cəza", "Cihaz", 
    "Cild", "Cizgi", "Cücə", "Çadır", "Çağırış", "Çalışqan", "Çamadan", "Çap", "Çatı", "Çay", 
    "Çəki", "Çəlik", "Çəltik", "Çəmən", "Çərçivə", "Çeşid", "Çətin", "Çığır", "Çılçıraq", "Çilingər", 
    "Çiçək", "Çoban", "Çoxluq", "Çörək", "Çubuq", "Çuxur", "Çürük", "Daban", "Dairə", "Dalaq", 
    "Damcı", "Damaq", "Damar", "Daraq", "Daxma", "Dəb", "Dəfə", "Dəhliz", "Dəmir", "Dənli", 
    "Dəqiqə", "Dərə", "Dərnək", "Dərs", "Dəstək", "Dəstə", "Dəvə", "Dəyər", "Dəyirman", "Dəzgah", 
    "Dibi", "Dinc", "Dinamik", "Disk", "Dizayner", "Doğum", "Doğru", "Döşəmə", "Dövr", "Dönüş", 
    "Duman", "Düyün", "Düymə", "Düzən", "Eksponat", "Ekspert", "Elektrik", "Element", "Elita", "Enli", 
    "Epitet", "Eram", "Estakada", "Etika", "Ev", "Ezamiyyət", "İnflyasiya", "İqtisadiyyat", "İnnovasiya", "İnvestisiya", 
    "İşgüzarlıq", "İcma", "İpək", "İbadət", "İddia", "İzah", "İrs", "İradə", "İti", "İzahat", 
    "Jurnal", "Jeton", "Jilet", "Kabel", "Kafeteriya", "Kafel", "Kainat", "Kamança", "Kəhriz", "Kəşfiyyat", 
    "Kəklik", "Kəramət", "Kərpic", "Kəskin", "Kətan", "Kəfən", "Kif", "Kilsə", "Kilid", "Kino", 
    "Kirayə", "Kirpi", "Kitabxana", "Klaviatura", "Klişe", "Klub", "Köməkçi", "Körpəlik", "Kök", "Köçəri", 
    "Kölgə", "Kran", "Kriminal", "Kristal", "Küləkli", "Kürsü", "Kütləvi", "Lalə", "Laminat", "Lampa", 
    "Ləhcə", "Ləçək", "Ləqəb", "Ləziz", "Ləzzət", "Lif", "Liman", "Limon", "Linza", "Litr", 
    "Lüğət", "Lüks", "Maşın", "Məişət", "Məktəbli", "Məşğuliyyət", "Məzmun", "Məzə", "Məhəbbət", "Məftun", 
    "Məşhur", "Məqam", "Məxfilik", "Məzun", "Meyvəlik", "Mənbə", "Müasir", "Müəllimlik", "Müvəffəq", "Müxtəlif", 
    "Müddət", "Müvəqqəti", "Müdafiə", "Müəyyən", "Mülk", "Mühasib", "Müzakirə", "Müşavirə", "Nəqliyyat", "Nəzarət", 
    "Nəzər", "Nəsil", "Nəfəs", "Nəğmə", "Nəticə", "Neytral", "Neyron", "Nigar", "Nişan", "Nizam", 
    "Niyyət", "Nömrə", "Növ", "Nümayəndə", "Obyekt", "Ocaq", "Oğurluq", "Okean", "Oktyabr", "Olimpiada", 
    "Onurğa", "Opera", "Optika", "Orqanizm", "Ot", "Oturacaq", "Ov", "Ovuc", "Oyma", "Oyunçu", 
    "Pambıq", "Panama", "Panda", "Pantomima", "Paralel", "Paraşüt", "Park", "Parket", "Pasport", "Pedaqoq", 
    "Pencərə", "Pensiya", "Pərgar", "Pələng", "Pərdə", "Perimetr", "Peyk", "Piknik", "Piləkən", "Pilot", 
    "Pinqvin", "Pion", "Plakat", "Plastik", "Plat", "Pleşka", "Plov", "Poçtalyon", "Polad", "Polis", 
    "Portağal", "Pota", "Pozan", "Prezident", "Proqram", "Prospekt", "Pult", "Pusqu", "Qab", "Qabıq", 
    "Qabırğa", "Qadağa", "Qafiyə", "Qala", "Qalereya", "Qalıq", "Qamış", "Qanun", "Qapı", "Qapıçı", 
    "Qara", "Qayda", "Qaynaq", "Qayçı", "Qaz", "Qazan", "Qəbz", "Qədim", "Qəhqəhə", "Qəhrəman", 
    "Qəlbi", "Qələbə", "Qələm", "Qərar", "Qəsidə", "Qəşəng", "Qəza", "Qəzet", "Qəzəb", "Qıfıl", 
    "Qıraq", "Qışqırıq", "Qısa", "Qızğın", "Qızıl", "Qoçaq", "Qol", "Qolbaq", "Qonşu", "Qorxu", 
    "Qovluq", "Qoz", "Qrafika", "Qranit", "Qrup", "Quba", "Qul", "Qum", "Qurğu", "Qurultay", 
    "Quru", "Qutan", "Quyu", "Qüvvə", "Qüzey", "Qrip", "Şəkər", "Astma", "Bronxit", "Qastrit", 
    "Hipertoniya", "Allergiya", "Depressiya", "Osteoxondroz", "Angina", "Pnevmoniya", "Abadlıq", "Abidə", "Abonent", "Abstrakt", 
    "Acar", "Açar", "Acı", "Açıqca", "Ada", "Adaptasiya", "Adət", "Aeroport", "Afina", "Afişa", 
    "Aforizm", "Afrika", "Ağıl", "Ağac", "Ağdam", "Ağlayan", "Ağrı", "Ağrılı", "Ağsaqqal", "Ağzıaçıq", 
    "Ailə", "Ailəvi", "Aksiya", "Aktivist", "Aktyor", "Albom", "Alçaq", "Alın", "Alqı", "Alqış", 
    "Alınmaz", "Alışqan", "Alim", "Alış-veriş", "Alman", "Alpinist", "Alpinizm", "Alqoritm", "Altı", "Alüminium", 
    "Alov", "Almaz", "Ambar", "Amerikan", "Amil", "Amper", "Analiz", "Analitika", "Ancaq", "And", 
    "Anket", "Anlayış", "Anons", "Antenna", "Antarktida", "Antivirus", "Apellyasiya", "Aprel", "Aptek", "Araba", 
    "Araşdırma", "Arayış", "Ardıcıl", "Ardıc", "Arxeoloq", "Arxipelaq", "Arxiv", "Arzu", "Asan", "Asfalt", 
    "Asiya", "Asılılıq", "Asılqan", "Aslan", "Asqırıq", "Asta", "Asudə", "Aşpaz", "At", "Atalar", 
    "Atelye", "Atəş", "Atəşfəşanlıq", "Atışma", "Atmosfer", "Atom", "Atribut", "Atlas", "Avadanlıq", "Avanqard", 
    "Avqust", "Avtomat", "Avtoqraf", "Avtobus", "Avtomobil", "Ayaq", "Ayaqqabı", "Ayaz", "Aydındır", "Aynəbənd", 
    "Aypara", "Ayna", "Azadlıq", "Azərbaycanlı", "Azimut", "Azot", "Babək", "Bacı", "Badam", "Bahar", 
    "Balıq", "Bank", "Bayraq", "Bədii", "Bəhanə", "Bəhrə", "Bəhs", "Bəkar", "Bəkk", "Bəlal", 
    "Bələdiyyə", "Bəlkə", "Bəlli", "Bəmbəyaz", "Bənna", "Bərabər", "Bərbər", "Bərəkət", "Bərk", "Bərpa", 
    "Bəsit", "Bəstəkar", "Bəşər", "Bəxt", "Bəzən", "Bəzi", "Bəzək", "Bıçaq", "Bığ", "Bilavasitə", 
    "Biləcik", "Bilək", "Bilet", "Bildiriş", "Bilgi", "Bilik", "Bilim", "Bina", "Binə", "Birbaşa", 
    "Birdən", "Birgə", "Birinci", "Birlik", "Birokratiya", "Bitki", "Blender", "Blok", "Boks", "Bol", 
    "Boş", "Boy", "Boyun", "Boyunbağı", "Bölmə", "Bölüşdürmə", "Boranı", "Boru", "Boz", "Böcək", 
    "Bölgə", "Böyük", "Büdcə", "Bulaq", "Bulud", "Bürclər", "Bürünc", "Büro", "Buzlaq", "Camaat", 
    "Cavan", "Cazibə", "Cəbhə", "Cədvəl", "Cəhd", "Cəlb", "Cəmi", "Cəmiyyət", "Cənnət", "Cərimə", 
    "Cərrah", "Cəsarət", "Cəsur", "Cəza", "Cihaz", "Cild", "Cizgi", "Cümə", "Cücə", "Cürbəcür", 
    "Çadır", "Çağırış", "Çalağan", "Çalışqan", "Çamadan", "Çanta", "Çap", "Çapa", "Çat", "Çatı", 
    "Çaxır", "Çay", "Çaynik", "Çəki", "Çəlik", "Çəltik", "Çəmən", "Çətin", "Çərçivə", "Çeşid", 
    "Çığır", "Çılçıraq", "Çilə", "Çilingər", "Çimərlik", "Çin", "Çiçək", "Çirkin", "Çiyin", "Çoban", 
    "Çoxluq", "Çörək", "Çörəkçi", "Çubuq", "Çuxur", "Çürük" "Qadağa", "Qafiyə", "Qalan",
    "Qalereya", "Qalıq", "Qamış", "Qanun", "Qapı", "Qapıçı", "Qara", "Qaydalar", "Qaynaq", "Qayçı",
    "Qaz", "Qazan", "Qəbz", "Qədim", "Qəhqəhə", "Qəhrəman", "Qəlbi", "Qələbə", "Qələm", "Qərar",
    "Qəsidə", "Qəşəng", "Qəza", "Qəzet", "Qəzəb", "Qıfıl", "Qıraq", "Qışqırıq", "Qısa", "Qızğın",
    "Qızıl", "Qoçaq", "Qol", "Qolbaq", "Qonşu", "Qorxu", "Qovluq", "Qoz", "Qrafik", "Qranit",
    "Qrup", "Quba", "Qul", "Qum", "Qurğu", "Qurultay", "Quru", "Qutan", "Quyu", "Qüvvə",
    "Qüzey", "Qrip", "Şəkərsiz", "Astmalı", "Bronxit""Abstraksiya", "Acgözlük", "Adət-ənənə", "Afrikalı", "Ağıllı", "Ağrıdan", "Ağsaqqallıq", "Ailəsiz", "Aksiyaçı", "Albomsuz",
    "Alçaqlıq", "Alqışlama", "Alınmazlıq", "Alış-verişsiz", "Almaniya", "Alpinistlik", "Alüminiumlu", "Alovlan", "Almazlı", "Ambarsız",
    "Ampermetr", "Analizator", "Anketçi", "Anlayışlı", "Anonslu", "Antennalı", "Antarktikalı", "Antiviruslu", "Apellyasiyalı", "Apreldə",
    "Aptekçi", "Arabasız", "Araşdırıcı", "Arayışlı", "Ardıcıllıq", "Arxeologiya", "Arxipelaqla", "Arxivçi", "Arzusuz", "Asanlıq",
    "Asfaltlama", "Asiyalı", "Asılılıqdan", "Aslanlı", "Asqı", "Astalıq", "Asudəlik", "Aşpazlıq", "Atçılıq", "Atelyeli",
    "Atəşgah", "Atışmalar", "Atmosferli", "Atomlu", "Atributlu", "Atlaslı", "Avadanlıqlı", "Avanqardlı", "Avqustda", "Avtomatik",
    "Avtoqrafsız", "Avtobuslu", "Avtomobilli", "Ayaqaltı", "Ayaqqabılı", "Ayazlı", "Aydınlıq", "Aynəbəndli", "Ayparalı", "Aynalı",
    "Azadlıqla", "Azərbaycan", "Azimutlu", "Azotlu", "Babəkli", "Bacılı", "Badamlıq", "Baharfəsli", "Balıqçı", "Bankomat",
    "Bayraqlı", "Bədiilik", "Bəhanəçi", "Bəhrəsiz", "Bəhsçi", "Bəkarət", "Bəkkli", "Bəlalılıq", "Bələdiyyəli", "Bəlkəlik",
    "Bəllilik", "Bəmbəyazlıq", "Bənnalıq", "Bərabərsiz", "Bərbərxana", "Bərəkətli", "Bərklik", "Bərpaedici", "Bəsitlik", "Bəstəkarlıq",
    "Bəşəriyyət", "Bəxtli", "Bəzənmiş", "Bəziləri", "Bəzəyən", "Bıçaqlı", "Bığlı", "Bilavasitəlik", "Biləcikli", "Biləklik",
    "Biletçi", "Bildirişli", "Bilgili", "Biliksiz", "Bilimsel", "Binəqədi", "Binəli", "Birbaşa", "Abstrakt", "Acar", "Açar", "Acı", "Açıqca", "Ada", "Adaptasiya", "Adət", "Aeroport", "Afina", 
    "Afişa", "Aforizm", "Afrika", "Ağıl", "Ağac", "Ağdam", "Ağlayan", "Ağrı", "Ağrılı", "Ağsaqqal", "Ağzıaçıq", "Ailə", 
    "Ailəvi", "Aksiya", "Aktivist", "Aktyor", "Albom", "Alçaq", "Alın", "Alqı", "Alqış", "Alınmaz", "Alışqan", "Alim", 
    "Alış-veriş", "Alman", "Alpinist", "Alpinizm", "Alqoritm", "Altı", "Alüminium", "Alov", "Almaz", "Ambar", "Amerikan", 
    "Amil", "Amper", "Analiz", "Analitika", "Ancaq", "And", "Anket", "Anlayış", "Anons", "Antenna", "Antarktida", 
    "Antivirus", "Apellyasiya", "Aprel", "Aptek", "Araba", "Araşdırma", "Arayış", "Ardıcıl", "Ardıc", "Arxeoloq", 
    "Arxipelaq", "Arxiv", "Arzu", "Asan", "Asfalt", "Asiya", "Asılılıq", "Asılqan", "Aslan", "Asqırıq", "Asta", 
    "Asudə", "Aşpaz", "At", "Atalar", "Atelye", "Atəş", "Atəşfəşanlıq", "Atışma", "Atmosfer", "Atom", "Atribut", 
    "Atlas", "Avadanlıq", "Avanqard", "Avqust", "Avtomat", "Avtoqraf", "Avtobus", "Avtomobil", "Ayaq", "Ayaqqabı", 
    "Ayaz", "Aydındır", "Aynəbənd", "Aypara", "Ayna", "Azadlıq", "Azərbaycanlı", "Azimut", "Azot", "Babək", "Bacı", 
    "Badam", "Bahar", "Balıq", "Bank", "Bayraq", "Bədii", "Bəhanə", "Bəhrə", "Bəhs", "Bəkar", "Bəkk", "Bəlal", 
    "Bələdiyyə", "Bəlkə", "Bəlli", "Bəmbəyaz", "Bənna", "Bərabər", "Bərbər", "Bərəkət", "Bərk", "Bərpa", "Bəsit", 
    "Bəstəkar", "Bəşər", "Bəxt", "Bəzən", "Bəzi", "Bəzək", "Bıçaq", "Bığ", "Bilavasitə", "Biləcik", "Bilək", 
    "Bilet", "Bildiriş", "Bilgi", "Bilik", "Bilim", "Bina", "Binə", "Birbaşa", "Birdən", "Birgə", "Birinci", 
    "Birlik", "Birokratiya", "Bitki", "Blender", "Blok", "Boks", "Bol", "Boş", "Boy", "Boyun", "Boyunbağı", 
    "Bölmə", "Bölüşdürmə", "Boranı", "Boru", "Boz", "Böcək", "Bölgə", "Böyük", "Büdcə", "Bulaq", "Bulud", 
    "Bürclər", "Bürünc", "Büro", "Buzlaq", "Camaat", "Cavan", "Cazibə", "Cəbhə", "Cədvəl", "Cəhd", "Cəlb", 
    "Cəmi", "Cəmiyyət", "Cənnət", "Cərimə", "Cərrah", "Cəsarət", "Cəsur", "Cəza", "Cihaz", "Cild", "Cizgi", 
    "Cümə", "Cücə", "Cürbəcür", "Çadır", "Çağırış", "Çalağan", "Çalışqan", "Çamadan", "Çanta", "Çap", "Çapa", 
    "Çat", "Çatı", "Çaxır", "Çay", "Çaynik", "Çəki", "Çəlik", "Çəltik", "Çəmən", "Çətin", "Çərçivə", "Çeşid", 
    "Çığır", "Çılçıraq", "Çilə", "Çilingər", "Çimərlik", "Çin", "Çiçək", "Çirkin", "Çiyin", "Çoban", "Çoxluq", 
    "Çörək", "Çörəkçi", "Çubuq", "Çuxur", "Çürük", "Abadlıq", "Abidə", "Abonent", "Abstrakt", "Acar", "Açar", "Acı", "Açıqca", "Ada", "Adaptasiya", "Adət", "Aeroport", "Afina", 
    "Afişa", "Aforizm", "Afrika", "Ağıl", "Ağac", "Ağdam", "Ağlayan", "Ağrı", "Ağrılı", "Ağsaqqal", "Ağzıaçıq", "Ailə", 
    "Ailəvi", "Aksiya", "Aktivist", "Aktyor", "Albom", "Alçaq", "Alın", "Alqı", "Alqış", "Alınmaz", "Alışqan", "Alim", 
    "Alış-veriş", "Alman", "Alpinist", "Alpinizm", "Alqoritm", "Altı", "Alüminium", "Alov", "Almaz", "Ambar", "Amerikan", 
    "Amil", "Amper", "Analiz", "Analitika", "Ancaq", "And", "Anket", "Anlayış", "Anons", "Antenna", "Antarktida", 
    "Antivirus", "Apellyasiya", "Aprel", "Aptek", "Araba", "Araşdırma", "Arayış", "Ardıcıl", "Ardıc", "Arxeoloq", 
    "Arxipelaq", "Arxiv", "Arzu", "Asan", "Asfalt", "Asiya", "Asılılıq", "Asılqan", "Aslan", "Asqırıq", "Asta", 
    "Asudə", "Aşpaz", "At", "Atalar", "Atelye", "Atəş", "Atəşfəşanlıq", "Atışma", "Atmosfer", "Atom", "Atribut", 
    "Atlas", "Avadanlıq", "Avanqard", "Avqust", "Avtomat", "Avtoqraf", "Avtobus", "Avtomobil", "Ayaq", "Ayaqqabı", 
    "Ayaz", "Aydındır", "Aynəbənd", "Aypara", "Ayna", "Azadlıq", "Azərbaycanlı", "Azimut", "Azot", "Babək", "Bacı", 
    "Badam", "Bahar", "Balıq", "Bank", "Bayraq", "Bədii", "Bəhanə", "Bəhrə", "Bəhs", "Bəkar", "Bəkk", "Bəlal", 
    "Bələdiyyə", "Bəlkə", "Bəlli", "Bəmbəyaz", "Bənna", "Bərabər", "Bərbər", "Bərəkət", "Bərk", "Bərpa", "Bəsit", 
    "Bəstəkar", "Bəşər", "Bəxt", "Bəzən", "Bəzi", "Bəzək", "Bıçaq", "Bığ", "Bilavasitə", "Biləcik", "Bilək", 
    "Bilet", "Bildiriş", "Bilgi", "Bilik", "Bilim", "Bina", "Binə", "Birbaşa", "Birdən", "Birgə", "Birinci", 
    "Birlik", "Birokratiya", "Bitki", "Blender", "Blok", "Boks", "Bol", "Boş", "Boy", "Boyun", "Boyunbağı", 
    "Bölmə", "Bölüşdürmə", "Boranı", "Boru", "Boz", "Böcək", "Bölgə", "Böyük", "Büdcə", "Bulaq", "Bulud", 
    "Bürclər", "Bürünc", "Büro", "Buzlaq", "Camaat", "Cavan", "Cazibə", "Cəbhə", "Cədvəl", "Cəhd", "Cəlb", 
    "Cəmi", "Cəmiyyət", "Cənnət", "Cərimə", "Cərrah", "Cəsarət", "Cəsur", "Cəza", "Cihaz", "Cild", "Cizgi", 
    "Cümə", "Cücə", "Cürbəcür", "Çadır", "Çağırış", "Çalağan", "Çalışqan", "Çamadan", "Çanta", "Çap", "Çapa", 
    "Çat", "Çatı", "Çaxır", "Çay", "Çaynik", "Çəki", "Çəlik", "Çəltik", "Çəmən", "Çətin", "Çərçivə", "Çeşid", 
    "Çığır", "Çılçıraq", "Çilə", "Çilingər", "Çimərlik", "Çin", "Çiçək", "Çirkin", "Çiyin", "Çoban", "Çoxluq", 
    "Çörək", "Çörəkçi", "Çubuq", "Çuxur", "Çürük", "Daban", "Dada", "Dairə", "Dalaq", "Daldı", "Dalı", "Damcı", 
    "Damaq", "Damar", "Daraq", "Darvaza", "Daxma", "Dəb", "Dəfə", "Dəhliz", "Dəmir", "Dəmirçi", "Dənli", 
    "Dəqiqə", "Dərə", "Dərnək", "Dərs", "Dərsli", "Dəstək", "Dəstə", "Dəvə", "Dəyər", "Dəyirman", "Dəzgah", 
    "Dibi", "Dinc", "Dinamik", "Direktor", "Disk", "Dizayner", "Doğum", "Doğru", "Döl", "Döşəmə", "Dövr", 
    "Dönüş", "Duman", "Düyün", "Düymə", "Düz", "Düzən", "Eksponat", "Ekspedisiya", "Ekspert", "Elektrik", 
    "Element", "Elita", "Emanet", "Enli", "Epitet", "Eram", "Estakada", "Etika", "Etnoqrafiya", "Ev", 
    "Ezamiyyət", "İnflyasiya", "İqtisadiyyat", "İnnovasiya", "İnvestisiya", "İşgüzarlıq", "İcma", "İpək", 
    "İbadət", "İddia", "İtaliyalı", "İzah", "İrs", "İradə", "İti", "İzahat", "Jurnal", "Jurnalistika", 
    "Jeton", "Jilet", "Jurnalist", "Kabel", "Kafeteriya", "Kafel", "Kainat", "Kamança", "Kəhriz", "Kəşfiyyat", 
    "Kəklik", "Kəramət", "Kərpic", "Kəskin", "Kətan", "Kəfən", "Kif", "Kilsə", "Kilid", "Kino", "Kioska", 
    "Kirayə", "Kirpi", "Kitabxana", "Klaviatura", "Klişe", "Kliş", "Klub", "Köməkçi", "Körpəlik", "Kök", 
    "Köçəri", "Kölgə", "Kran", "Kriminal", "Kristal", "Küləkli", "Kürsü", "Kütləvi", "Lalə", "Laminat", 
    "Lampa", "Ləhcə", "Ləçək", "Ləqəb", "Ləziz", "Ləzzət", "Lif", "Liman", "Limon", "Linc", "Linza", 
    "Litr", "Lüğət", "Lüks", "Maşın", "Məişət", "Məktəbli", "Məşğuliyyət", "Məzmun", "Məzə", "Məhəbbət", 
    "Məftun", "Məşhur", "Məqam", "Məxfilik", "Məzun", "Meyvəlik", "Mənbə", "Müasir", "Müəllimlik", 
    "Müvəffəq", "Müasirlik", "Müxtəlif", "Müddət", "Müvəqqəti", "Müdafiə", "Müəyyən", "Mülk", 
    "Mühasib", "Müzakirə", "Müşavirə", "Nəqliyyat", "Nəzarət", "Nəzər", "Nəsil", "Nəfəs", "Nəğmə", 
    "Nəticə", "Neytral", "Neyron", "Nigar", "Nişan", "Nizam", "Niyyət", "Nömrə", "Növ", "Nümayəndə", 
    "Obyekt", "Ocaq", "Oğurluq", "Okean", "Oktyabr", "Olimpiada", "Onurğa", "Opera", "Optika", 
    "Orqanizm", "Ot", "Oturacaq", "Ov", "Ovuc", "Oyma", "Oyunçu", "Pambıq", "Panama", "Panda", 
    "Pantomima", "Paralel", "Paraşüt", "Park", "Parket", "Pasport", "Pedaqoq", "Pencərə", "Pensiya", 
    "Pərgar", "Pələng", "Pərdə", "Perimetr", "Peyk", "Piknik", "Piləkən", "Pilot", "Pinqvin", "Pion",  "Alma", "Bakı", "Kompüter", "Telegram", "Avtomobil", "Kitab"]

# Keyboardlar
def dil_secimi_kb():
    b = InlineKeyboardBuilder()
    diller = [("🇦🇿 Az", "az"), ("🇹🇷 Tr", "tr"), ("🇷🇺 Ru", "ru"), 
              ("🇺🇿 Uz", "uz"), ("🇬🇧 En", "en"), ("🇩🇪 De", "de")]
    for text, code in diller:
        b.add(types.InlineKeyboardButton(text=text, callback_data=f"lang_{code}"))
    b.adjust(3)
    return b.as_markup()

def get_game_kb(status="aktiv"):
    b = InlineKeyboardBuilder()
    if status == "gozlemede":
        b.add(types.InlineKeyboardButton(text="Aparıcı olmaq istəyirəm ✅", callback_data="aparici_ol"))
    else:
        b.add(types.InlineKeyboardButton(text="Sözə Baxmaq 🔍", callback_data="soze_bax"))
        b.add(types.InlineKeyboardButton(text="Fikrimi Dəyişdim ❌", callback_data="fikrimi_deyisdim"))
        b.add(types.InlineKeyboardButton(text="Növbəti Söz ♻️", callback_data="novbeti_soz"))
    b.adjust(1)
    return b.as_markup()

# Oyun məntiqi
async def yeni_raund(cid, uid, uname, mid=None):
    sz = random.choice(SOZLER)
    aktiv_oyunlar[cid] = {"soz": sz.lower().strip(), "orig": sz, "uid": uid, "un": uname, "st": "aktiv"}
    txt = f'<a href="tg://user?id={uid}">{uname}</a> - sözü izah edir'
    if mid:
        try: await bot.edit_message_text(chat_id=cid, message_id=mid, text=txt, reply_markup=get_game_kb())
        except: pass
    else:
        await bot.send_message(chat_id=cid, text=txt, reply_markup=get_game_kb())

# Handlerlər
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Dil seçin / Choose language", reply_markup=dil_secimi_kb())

@dp.callback_query(F.data.startswith("lang_"))
async def dil_secildi(c: types.CallbackQuery):
    txt = ("<b>Salam! Mən Cro oyun Botuyam..</b>\n\n"
           "Qrupunuzda dostlarınızla oyun oynamaq üçün məni Qrupunuza əlavə edin.\n"
           "Daha sonra Mənə Yöneticilik (Adminlik) verin və sonra /game komandası ilə oyunu başladın.")
    b = InlineKeyboardBuilder()
    b.add(types.InlineKeyboardButton(text="👥 Məni Qrupa Əlavə Et", url="https://t.me/CroniqueBot?startgroup=true"))
    await c.message.edit_text(txt, reply_markup=b.as_markup())
    await c.answer()

@dp.message()
async def chk(m: types.Message):
    if not m.text: return
    cid, uid, uname = m.chat.id, m.from_user.id, m.from_user.full_name
    msg = m.text.lower().strip()

    if msg == "/game" + BOT_NAME:
        if m.chat.type not in ["group", "supergroup"]: return await m.answer("Qrupda oynayın!")
        if cid in aktiv_oyunlar and aktiv_oyunlar[cid].get("st") == "aktiv": return await m.answer("⚠️ Aktiv oyun var!")
        await yeni_raund(cid, uid, uname)
        return

    if cid not in aktiv_oyunlar: return
    g = aktiv_oyunlar[cid]
    
    if msg == "/kick" + BOT_NAME:
        aktiv_oyunlar[cid]["st"] = "gozlemede"
        await m.answer(f"<b>{uname}</b> - <a href='tg://user?id={g['uid']}'>{g['un']}</a> növbəsini dayandırdı!", reply_markup=get_game_kb("gozlemede"))
        return

    if g.get("st") == "gozlemede" or uid == g["uid"]: return
    if msg == g["soz"]: await yeni_raund(cid, uid, uname)

@dp.callback_query()
async def cb(c: types.CallbackQuery):
    if c.data.startswith("lang_"): return
    cid, uid, uname, data = c.message.chat.id, c.from_user.id, c.from_user.full_name, c.data
    if cid not in aktiv_oyunlar: return
    g = aktiv_oyunlar[cid]
    if data == "soze_bax" and uid == g["uid"]: await c.answer(g['orig'], show_alert=True)
    elif data == "fikrimi_deyisdim" and uid == g["uid"]:
        aktiv_oyunlar[cid]["st"] = "gozlemede"
        await c.message.edit_text(text=f'<a href="tg://user?id={uid}">{g["un"]}</a> - aparıcılıqdan imtina etdi!', reply_markup=get_game_kb("gozlemede"))
    elif data == "aparici_ol" and g.get("st") == "gozlemede": await yeni_raund(cid, uid, uname, c.message.message_id)
    elif data == "novbeti_soz" and uid == g["uid"]:
        sz = random.choice(SOZLER)
        aktiv_oyunlar[cid].update({"soz": sz.lower().strip(), "orig": sz})
        await c.answer(sz, show_alert=True)

# ... (yuxarıdakı kodların hamısı olduğu kimi qalır)

async def main():
    # Flask serverini arxa planda başlat
    Thread(target=run_flask, daemon=True).start()
    
    # KÖHNƏ MESAJLARI SİL (Donmanı və gecikməni kəsən əsas hissə budur)
    await bot.delete_webhook(drop_pending_updates=True) 
    
    print("Bot işə düşdü...")
    
    # Botu başlat
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    

if __name__ == "__main__":
    asyncio.run(main())
                                         
