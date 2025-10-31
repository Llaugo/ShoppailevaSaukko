import utils

# Tile size (square of (tileSize x tileSize))
tileSize = 46

# Player's base stats
basePlayerSpeed = 100                # Speed
basePlayerStrength = 0             # Strength
basePlayerSpeechDuration = 120     # Speech text visibility duration

# Floor constants
floorTime = 300     # How much time (sec) there is in each level (300 = 5min)
floorTimeMin = 297  # How much time has to be spent on a level before exit is possible
floorSize = 9       # Floor size (floorSize x floorSize rooms)

# Npc constants
npcWalkDur = 93     # Walking distances
npcWalkSpeed = 1    # Walking speed

# Card constants
cardExp = 0.1       # Amount of experience gained when using a card
maxCardLevel = 3    # Maximum level that a strength card can get to

# Probability constants
itemProbability = 0.05 # Probability that a shelf tile has an item on it
darknessProbability = 0.15 # Probability that a room is dark
crateProbability = 0.66 # Probability that a crate spawns

# Item type rarities with cumulative distributions from the most common item type on the left to the rarest item type on the right.
# The item rarities change with respect to the room distance from the starting room
# Example: The first list tells that the starting room has 78% chance to spawn rarity 1 items
#          and 22% change to spawn rarity type 2 items. The rest of the items can't spawn there
itemRarity = [[0.78,	1,	1,	1,	1],
              [0.68,	0.95,	1,	1,	1],
              [0.59,	0.91,	0.99,	1,	1],
              [0.52,	0.85,	0.97,	0.99,	1],
              [0.45,	0.77,	0.95,	0.99,	1],
              [0.38,	0.66,	0.9,	0.97,	1],
              [0.32,	0.56,	0.81,	0.93,	1],
              [0.26,	0.47,	0.69,	0.86,	1],
              [0.2,	0.4,	0.6,	0.8,	1]]
# Colors used in the game to indicate the rarity levels
rarityColor = [(255,255,140), (255,182,101), (67,255,255), (255,106,233), (255,255,255)]
# Maximum room distance from the start (and index for the "best" item distibution)
roomDistMax = len(itemRarity)-1

'''
The rooms are created randomly from a list of predetermined layouts. 
One layout is a square of numbers, each number representing a type of tile.
0 = Wall
1 = Floor
2 = Shelf (Produces collectable items)
3 = Start/Exit
4 = Crate (can't be passed by without an active strength)
5 = Cart
6 = NPC
7 = Water
8 = Advert screen
'''
lobbyLayout  = utils.readLayout("rooms/lift.csv")
startLayouts = utils.readLayout("rooms/startRooms.csv")
roomLayouts  = utils.readLayout("rooms/roomLayouts.csv")
testRoom     = utils.readLayout("rooms/testRoom.csv")

'''
All the words and sentences used in the game in different languages.
i=0: Suomi
i=1: English
i=2: Svenska
'''
phrase = [
["HISSIIN",                                 # 0: hissinapissa
     "Seuraava kerros",                     # 1: levelin aloitusnapissa
     "Kerros",                              # 2: checkpoint otsikon osa 1 & Kerrosnumeron edessä
     "suoritettu",                          # 3: checkpoint otsikon osa 2
     "OTA\nESINE",                          # 4: esinenapissa
     "TOINEN\nESINE",                       # 5: vaihda kaupattavaa esinettä
     "Huoneessa olevat esineet:",           # 6: huoneen esinelista
     "Ostoslista",                          # 7: Ostoslistan otsikko
     "AKTIVOI\nKORTTI",                     # 8: kortin aktivointinappi
     "Vahvistetaanko kauppa?",              # 9: kaupankäyntinäkymän otsikko
     "KYLLÄ",                               # 10: kaupankäynnin hyväksyntä
     "EI",                                  # 11: kaupankäynnin kielto
     "Takaisin päävalikkoon",               # 12: vahvuusvalikon paluunapissa
     "Arvo vahvuudet",                      # 13: vahvuuksien arpomisnapissa
     "Aloita seikkailu!",                   # 14: vahvuusvalikon hyväksymisnappi
     "Viisaus ja tieto",                    # 15: Vahvuusvalikon vahvuusotsikko
     "Rohkeus",                             # 16: ––––––––––––||––––––––––––
     "Inhimillisyys",                       # 17: ––––––––––––||––––––––––––
     "Oikeudenmukaisuus",                   # 18: ––––––––––––||––––––––––––
     "Kohtuullisuus",                       # 19: ––––––––––––||––––––––––––
     "Henkisyys",                           # 20: ––––––––––––||––––––––––––
     "Kirsikkatomaatti",                    # 21: Kaupan esineet ->
     "Satsuma",                             # 22
     "Valkosipuli",                         # 23
     "Myskikurpitsa",                       # 24
     "Mango",                               # 25
     "Välipalakeksi",                       # 26
     "Fusilli",                             # 27
     "Kaurahiutale",                        # 28
     "Kvinoa",                              # 29
     "Linssisipsit",                        # 30
     "Rasvaton maito",                      # 31
     "Kreikkalainen jogurtti",              # 32
     "Pakastekatkaravut",                   # 33
     "Manchego",                            # 34
     "Halloumi",                            # 35
     "Kasvisliemikuutio",                   # 36
     "Rosmariini",                          # 37
     "Oliiviöljy",                          # 38
     "Inkivääri",                           # 39
     "Balsamico",                           # 40
     "Viiriäisen munat",                    # 41
     "Karambola",                           # 42
     "Sahrami",                             # 43
     "Murot",                               # 44
     "Runebergin torttu",                   # 45 <- kaupan esineet
     "En näe laatikoita tutkittavaksi.",    # 46: uteliaisuuden aktivointi liian kaukana laatikoista
     "Huoneessa on jo valoisaa.",           # 47: oppimisen ilon aktivointi jos huoneessa ei ole pimeä
     "En näe tarjouksia lähettyvillä.",     # 48: rehellisyyden aktivointi ei käännä yhtään tarjousta & Sisu ei tuhoa yhtään tarjousta
     "En näe kärryjä huoneessa.",           # 49: Sosiaalisen älykkyyden aktivointi, jos kärryjä ei ole huoneessa
     "En näe kärryjen omistajia.",          # 50: Sosiaalisen älykkyyden aktivointi, jos ihmisiä ei ole huoneessa
     "En näe ketään ketä peilata.",         # 51: Myötätunnon aktivointi ilman ihmistä edessä
     "Ei ketään kenelle jutella.",          # 52: Reiluuden/Ryhmätyön/johtajuuden/rakkauden aktivointi ilman ihmistä edessä
     "Hänellä ei ole kärryjä.",             # 53: Reiluuden/johtajuuden aktivointi, kun ihmisellä ei ole kärryjä huoneessa
     "Ei ole esineitä millä käydä kauppaa.",# 54: Ryhmätyötaitojen aktivointi, kun ei ole esineitä kerättynä
     "En näe vettä kuivattavaksi.",         # 55: Anteeksiannon aktivointi ilman vettä lähellä
     "Kaikki hyllyt ovat jo täynnä jotakin kiinnostavaa.", # 56: kauneuden arvostuksen aktivointi, kun hyllyt ovat täynnä
     "Hänen kärrynsä ovat jumissa.",        # 57: johtajuuden aktivointi, kun NPC ei pääse kärrynsä luo
     "<3",                                  # 58: Rakkauden onnistunut aktivointi (lataa reppua)
     "Ei tilaa laskeutua.",                 # 59: luovuuden lennokki yrittää laskeutua esteen päälle
     "Kärryä ei voi työntää kynnyksen yli", # 60: kun kärryä työntää oviaukkoa päin
     "Sinulla on jo tallennettu peli olemassa.\nHaluatko poistaa sen?", # 61
     "Onnistuit!",                          # 62
     "Sait kerättyä koko ostoslistan\nennen kaupan sulkemista.", # 63
     "Aika loppui kesken.",         # 64
     "Kauppakeskus suljetaan ja sinut ohjataan ulos.", # 65
     "Aikaa jäljellä:",                     # 66
     "Etsi alla näkyvät asiat.",            # 67
     "Sinulla on 5 minuuttia aikaa etsiä\njoka kerroksessa. Muista palata takaisin\nhissille ennen kuin on liian myöhäistä!", # 68
     "Tallenna ja\npalaa päävalikkoon", # 69
     "Haluatko palata päävalikkoon?\nTämä pelisuoritus poistetaan.", # 70
     "Valitse yksi vahvuus\n jokaisesta kategoriasta.\nSaat lisätietoa mistä tahansa\nkortista vetämällä sen minulle.\nVoit myös arpoa kaikki\nvahvuudet, jos et halua\nitse valita niitä.", # 71
     "Poistu pelistä", # 72
     "Pelin kulku:\nPelin tarkoitus on etsiä ostoslistalla olevat esineet ostoskeskuksen kerroksista, aikapaineen ja muiden esteiden keskellä. \nAvuksi seikkailuun valitaan kortteja, jotka antavat pelaajalle erilaisia taitoja haasteista selviämiseen. Taidot kehittyvät \nkäytettäessä ja jokainen uusi taso tekee kustakin taidosta paremman.\n\nMutkia matkassa\nJokainen pelin taso eli kerros on satunnaisesti generoitu asetelma huoneita. Huoneista löytyviä esteitä ovat märkä lattia, \ntarjousnäytöt, laatikot lattialla sekä tietenkin muut shoppailijat ja heidän ostoskärrynsä. Osa huoneista voi myös olla pimeitä. \nKorteista löytyy keinoja esteiden voittamiseen, esineiden löytämiseen ja sokkeloisissa huoneissa navigoimiseen.\n(Pidä varasi! kauppaan on mahdollista jäädä pysyvästikin jumiin.)\n\nKuka tuo leivän kotiin?\nKaupasta on löydettävä juuri ne esineet, mitä omalla ostoslistalla on. Mitä harvinaisempi esine on, sitä kauemmaksi niitä \nvarten on todennäköisesti kuljettava. Oikeat esineet löytyvät matkan varrelta eri huoneista ja kerroksista.\n\nÄlä unohdu matkalla!\nOstoskeskus sulkeutuu kerros kerrallaan. Aikaa jokaisessa kerroksessa on enintään viisi minuuttia. Jos ei ehdi takaisin \nhissiin ajan loppumista, peli päättyy. Pelin voi tallentaa myöhemmin jatkamista varten vain hississä. \n(Kerroksesta voi löytyä usempi hissihuone.)", # 73
     "Luonteenvahvuuksista:\nTässä pelissä käytössä olevat kortit perustuvat Lotta Uusitalo-Malmivaaran ja Kaisa Vuorisen kehittämiin \nHuomaa hyvä! -toimintakortteihin. Luonteenvahvuudet perustuvat tieteellisesti tutkittuihin vahvuuksiin. \nVIA-luonteenvahvuuksia löytyy 24, joihin Uusitalo ja Malmivaara ovat lisänneet myötätunnon ja sisukkuuden.", # 74
     "Pelin tekijät:\n  Lauri Karanko\n  Heidi Karanko", # 75
     "Luovuuden lennokki\nlennättää käyttäjänsä jonkin\nviereisen laatan yli.",                  # 76: Vahvuuskorttien kuvaukset
     "Uteliaisuuden suurennuslasi\navaa lähellä olevat\nlaatikot ja poistaa ne tieltä.",
     "Arviointikyvyn kaukoputki\nauttaa tunnistamaan huoneessa\nolevat esineet.",
     "Oppimisen ilon hehkulamppu\nvalaisee pimeän huoneen\nkokonaan ja pysyvästi.",
     "Näkökulmanottokyvyn nelikopteri\npaljastaa hetkeksi\nympärillä olevat huoneet.",      # 80
     "Rohkeuden rukkaset\nantavat käyttäjälleen rohkeuden\ntyöntää muiden kärryjä.",
     "Sinnikyyden saappaat\nmahdollistavat märän\nlattian yli kävelemisen.",
     "Rehellisyyden radio\nlähettää aaltoja, jotka\nkääntävät lähellä olevat\ntarjousnäytöt muualle.",
     "Innostuksen juoksukengät\nantavat lisävauhtia\nkäyttäjänsä askeliin.",
     "Sisukkuuden sapeli\ntekee lähistöllä olevat\ntarjousnäytöt\ntoimintakyvyttömiksi.",                   # 85
     "Ystävällisyyden kukkakimppu\nsaa muut shoppailijat\nantamaan tietä.",
     "Rakkauden rakettireppu\nlatautuu toisille jutellessa,\nja täysillä akuilla\nantaa käyttäjälleen\nhetkellisen lentokyvyn.",
     "Sosiaalisen älykkyyden\nsilmälasit näyttävät\nkäyttäjälleen lähellä olevien\nkärryjen sisällön, sekä\nnäiden omistajat.\nKortti toimii hyvin\nyhteen oikeudenmukaisuuden\nvahvuuksien kanssa.",
     "Myötätunnon peili\nauttaa käyttäjäänsä asettumaan\ntoisen shoppailijan asemaan.",
     "Reiluuden lapaset\nantavat kyvyt työntää toisen\nshoppailijan kärryjä, kunhan\ntältä on ensin kysynyt luvan.",                    # 90
     "Johtajuuden päähine\npäässään, kykenee pyytämään\nmuita siirtämään\nomia kärryään.",
     "Ryhmätyötaitojen tarjotin\nantaa mahdollisuuden käydä\nvaihtokauppaa muiden kanssa\nheidän löytämistään esineistä.",
     "Anteeksiantavuuden pyyhe\npyyhkii pois lähellä\nolevat märät lattialaatat.",
     "Vaatimattomuuden viitta\ntekee käyttäjänsä pieneksi.",
     "Harkitsevuuden hörppy\nantaa nautiskelijalleen\naikaa pysähtyä, laatia\nsuunnitelmaa ja odottaa\nvoimien palautumista.",                # 95
     "Itsesäätelyn suojakilpi\nmahdollistaa viisveisaamisen\nkaikenlaisista tarjouksista.",
     "Kauneuden arvostuksen kamera\npaljastaa uuden kiinnostavan\nesineen huoneessa, jota et\naiemmin huomannutkaan.",
     "Kiitollisuuden kivet\nvoi ripotella seikkaillessa\njälkiinsä, jotta paluumatka\nsujuisi joutuisammin.",
     "Toiveikkuuden taskulamppu\nnäyttää tien, vaikka huoneesta\nolisivatkin valot rikki.",
     "Huumorintajun räpylät\nauttavat silloin, kun kurainen\ntilanne meinaa pilata päivän.",                # 100
     "Hengellisyyden kynttilä\nantaa käyttäjälleen\nvaloa, kun kaikki muu\nvalo näyttää hävinneen.",
     "Luovuuden lennokki",                   # 102: Vahvuuskorttien otsikot
     "Uteliaisuuden suurennuslasi",
     "Arviointikyvyn kaukoputki",
     "Oppimisen ilon hehkulamppu",
     "Näkökulmanottokyvyn nelikopteri",
     "Rohkeuden rukkaset",
     "Sinnikyyden saappaat",
     "Rehellisyyden radio",
     "Innostuksen juoksukengät",             # 110
     "Sisukkuuden sapeli",
     "Ystävällisyyden kukkakimppu",
     "Rakkauden rakettireppu",
     "Sosiaalisen älykkyyden silmälasit",
     "Myötätunnon peili",
     "Reiluuden lapaset",
     "Johtajuuden päähine",
     "Ryhmätyötaitojen tarjotin",
     "Anteeksiantavuuden pyyhe",
     "Vaatimattomuuden viitta",              # 120
     "Harkitsevuuden hörppy",
     "Itsesäätelyn suojakilpi",
     "Kauneuden arvostuksen kamera",
     "Kiitollisuuden kivet",
     "Toiveikkuuden taskulamppu",
     "Huumorintajun räpylät",
     "Hengellisyyden kynttilä",              # 127
     "Aika tutkia kerrosta.\nHissi avautuu ",# 128
     "s kuluttua.",                          # 129
     "",
     "",
     "",
     "",
     ""],
["EXIT",
     ""],
["HISSEN",
     ""]]

# All the items that can appear in the shopping list and in the shop
# The first list has the most common items and the last list has the least common items
def shop(lang):
    return [[phrase[lang][21], phrase[lang][22], phrase[lang][23], phrase[lang][24], phrase[lang][25]],
            [phrase[lang][26], phrase[lang][27], phrase[lang][28], phrase[lang][29], phrase[lang][30]],
            [phrase[lang][31], phrase[lang][32], phrase[lang][33], phrase[lang][34], phrase[lang][35]],
            [phrase[lang][36], phrase[lang][37], phrase[lang][38], phrase[lang][39], phrase[lang][40]],
            [phrase[lang][41], phrase[lang][42], phrase[lang][43], phrase[lang][44], phrase[lang][45]]]