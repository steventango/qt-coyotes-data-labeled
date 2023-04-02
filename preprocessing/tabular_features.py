import json
from pathlib import Path
from tqdm import tqdm
from concurrent.futures import as_completed, ProcessPoolExecutor
from datetime import datetime

LOCATION_TO_LATITUDE_LONGITUDE = {
    '39th st east': (41.824185267263125, -87.60883727116504),
    '39th st west': (41.823157941728844, -87.67232376193452),
    'ADC': (41.878738636105375, -87.63858017068397),
    'ASC': (41.878738636105375, -87.63858017068397),
    'All Saints Cemetery': (42.06217035858631, -87.89342895979125),
    'Argonne': (41.7897536649656, -87.60097917513912),
    'BEC': (41.878738636105375, -87.63858017068397),
    'BLW': (41.878738636105375, -87.63858017068397),
    'BON': (41.878738636105375, -87.63858017068397),
    'Beck Lake': (42.066407209692514, -87.86964477328631),
    'Belleau Woods': (42.04401485759403, -87.87596298493759),
    'Big Marsh (Bike Park)': (41.685772137243916, -87.57435905980243),
    'Brighton Park': (41.817316195644004, -87.69922693471878),
    'Brooks Park': (42.00994012867196, -87.80857481561812),
    'Burnham - 47th St NS': (41.80967028028688, -87.59245529158319),
    'Burnham Bird Sanctuary': (41.81227350715695, -87.59143168863365),
    'CAN': (41.878738636105375, -87.63858017068397),
    'CBW': (41.878738636105375, -87.63858017068397),
    'CCC': (41.878738636105375, -87.63858017068397),
    'CLG': (41.878738636105375, -87.63858017068397),
    'CPG': (41.878738636105375, -87.63858017068397),
    'CPR': (41.878738636105375, -87.63858017068397),
    'CTG': (41.878738636105375, -87.63858017068397),
    'Canoe Launch 1': (41.9135193407954, -87.62564991343682),
    'Cantigny Park and Golf Club': (41.85415223239487, -88.15776375286798),
    'Chevy Chase Country Club': (42.15786468491205, -87.91896191376911),
    'Chopin Park': (41.943130781271655, -87.76318423095984),
    'Columbia Woods': (41.732071635996505, -87.88833356453165),
    'Columbus Park golf course': (41.87655074163211, -87.76864751562204),
    "Crane''s Landing GC": (42.19435482524563, -87.923616103962),
    'Cumberland::A': (53.6108736369396, -113.54898752934199),
    'Cumberland::B': (53.60992338880235, -113.5553579472884),
    'DAP': (41.878738636105375, -87.63858017068397),
    'DAW': (41.878738636105375, -87.63858017068397),
    'Dam No. 1 Woods': (42.138693366461396, -87.90153560435884),
    'Dam no. 1 woods': (42.138693366461396, -87.90153560435884),
    'Danby Park': (41.875127834805774, -88.07822969063056),
    'Dunham Park': (41.965967991753246, -87.78456150850889),
    'EDW': (41.878738636105375, -87.63858017068397),
    'Edgebrook Volunteer Center': (41.99802879590498, -87.76408660259243),
    'Edgebrook Woods': (41.991965472611184, -87.7635161493593),
    'FRM': (41.878738636105375, -87.63858017068397),
    'FSP': (41.878738636105375, -87.63858017068397),
    'Falconer::A': (53.46688951775056, -113.58829661241738),
    'Falconer::B': (53.463172289547806, -113.59139929765607),
    'Fermi': (41.79204933993435, -87.60153616956873),
    'Four Seasons Park': (41.853107746026545, -88.02144136918355),
    'Fresh Meadow Golf': (41.849430253615324, -87.90211667224209),
    'GOC': (41.878738636105375, -87.63858017068397),
    'GOF': (41.878738636105375, -87.63858017068397),
    'Glen Oak Cemetery': (41.89743265402755, -88.20565875979615),
    'Glen Oak Forest Preserve': (41.87434846639734, -88.04233004749484),
    'Gompers Park': (41.9762537460606, -87.73676890095768),
    'Hegewisch Marsh': (41.657507689069284, -87.56019420070562),
    'Humboldt Park': (41.899274352632034, -87.72104219921815),
    'ILC': (41.878738636105375, -87.63858017068397),
    'Isle a la Cache': (41.63971451537102, -88.06912454446403),
    'Jackson Park 1 (Wooded Island)': (41.78327415971847, -87.58221392413661),
    'Jackson Park 2 (Bobolink Meadow)': (41.78469601280554, -87.58018517264901),
    'Jarvis BS': (42.01589765782877, -87.66916545812676),
    'KCG': (41.878738636105375, -87.63858017068397),
    'KTP': (41.878738636105375, -87.63858017068397),
    'Keepataw Preserve': (41.67607339277761, -88.03600565795814),
    'Kennicotts Grove': (42.08143814808715, -87.85434048678103),
    'Kinnard::A': (53.55764982430639, -113.45662573303785),
    'Kinnard::B': (53.556946196981464, -113.46712448199915),
    'Kinnard::C': (53.55143941020867, -113.47193100005217),
    'LCP': (41.878738636105375, -87.63858017068397),
    'LEW': (41.878738636105375, -87.63858017068397),
    'LIM': (41.878738636105375, -87.63858017068397),
    'LMP': (41.878738636105375, -87.63858017068397),
    'LNC': (41.878738636105375, -87.63858017068397),
    'LPC': (41.878738636105375, -87.63858017068397),
    'LPP': (41.878738636105375, -87.63858017068397),
    'Lake Meadows Park': (41.83713145959056, -87.61204131562326),
    'LeClaire Park': (41.81353811458374, -87.75066217144926),
    'Lewis University': (41.60378322399772, -88.07825263836715),
    'Lincoln Marsh': (41.872171633857626, -88.1232421714475),
    'Lithuanian National Cemetery': (41.74160706533747, -87.84586935795622),
    'Lockport Cemetery': (41.59125673108862, -88.04849087806284),
    'Lockport Prairie': (41.58394360425325, -88.07672623281509),
    'MAC': (41.878738636105375, -87.63858017068397),
    'MAP': (41.878738636105375, -87.63858017068397),
    'MDU': (41.878738636105375, -87.63858017068397),
    'MHC': (41.878738636105375, -87.63858017068397),
    'MIA': (41.878738636105375, -87.63858017068397),
    'MMP': (41.878738636105375, -87.63858017068397),
    'MMW': (41.878738636105375, -87.63858017068397),
    'MTC': (41.878738636105375, -87.63858017068397),
    'MacArthur Woods': (42.24054106523648, -87.94003337512567),
    'Madison Meadow': (41.872342252474, -88.00169226024677),
    'Maple Park': (41.93940596128716, -87.85396803145846),
    'Marian Byrnes': (41.71453611918353, -87.5761014938719),
    'McKinley Park': (41.824890688812026, -87.68015037255543),
    'Miami Woods': (42.02803016560164, -87.79136749994578),
    'Millers Meadow': (41.857007061167096, -87.82794697329255),
    'Montrose Dunes': (41.96537370913633, -87.63278155607433),
    'Mozart Park': (41.918089229264446, -87.72373700028109),
    'Mt. Carmel': (38.410612495173694, -87.76172962409522),
    'NOC': (41.878738636105375, -87.63858017068397),
    'North Park Village': (41.9882103406513, -87.72419447463182),
    'Northerly Island': (41.86327453173428, -87.60827950994435),
    'Northfield Oakwood Cemetery': (42.09535197953628, -87.87848632726616),
    'OTB': (41.878738636105375, -87.63858017068397),
    'OTW': (41.878738636105375, -87.63858017068397),
    'Oakbrook Terrace Bike Path': (41.84931554514331, -87.959269495809),
    'Ottawa Woods': (41.81110306581812, -87.80705114490132),
    'PAP': (41.878738636105375, -87.63858017068397),
    'PIP': (41.878738636105375, -87.63858017068397),
    'PRC': (41.878738636105375, -87.63858017068397),
    'Panfish Park': (41.856856480167735, -88.05885902911785),
    'Park Ridge Country Club': (42.0196821910525, -87.83089392911302),
    'Piotrowski Park': (41.83489812911754, -87.73084367144861),
    'RCP': (41.878738636105375, -87.63858017068397),
    'RES': (41.878738636105375, -87.63858017068397),
    'RYW': (41.878738636105375, -87.63858017068397),
    'Resurrection Cemetery': (41.76111847337502, -87.82401137837574),
    'Richard Clark Park': (41.94407959999272, -87.694760444455),
    'Rosedale Park': (41.98910085144774, -87.78587171746331),
    'Rosehill Cemetery': (41.98597740872864, -87.67459418159468),
    'Rowland::C': (53.5498914868397, -113.45701016626211),
    'Rowland::E': (53.55013865734685, -113.45549222886218),
    'Rowland::F': (53.550606273276095, -113.45343458038671),
    'Rowland::H': (53.550946961627986, -113.45137693191123),
    'Rowland::J': (53.55122727123708, -113.449784224745),
    'Rowland::K': (53.551493311683416, -113.4474332609281),
    'Rowland::L': (53.551950564792804, -113.44420068567986),
    'Rowland::N': (53.55252348618213, -113.44203417444629),
    'Ryerson Woods': (42.17924399102186, -87.91288358862269),
    'SAG': (41.878738636105375, -87.63858017068397),
    'SCH': (41.878738636105375, -87.63858017068397),
    'SFP': (41.878738636105375, -87.63858017068397),
    'SLT': (41.878738636105375, -87.63858017068397),
    'SMC': (41.878738636105375, -87.63858017068397),
    'SMI': (41.878738636105375, -87.63858017068397),
    'SSP': (41.878738636105375, -87.63858017068397),
    'STJ': (41.878738636105375, -87.63858017068397),
    'STP': (41.878738636105375, -87.63858017068397),
    'Sagawau': (41.69052595514835, -87.92533421661403),
    'Salt Creek Greenway': (41.81227103690568, -87.81076494011779),
    'Santa Fe Prairie': (41.75832340557739, -87.85854688679066),
    'Schroeder Park': (41.860757375872716, -87.84664148867115),
    'Skinner Park': (41.879768489364814, -87.66153744445691),
    'St. Adalbert Cemetery': (42.00557157921229, -87.7962762886279),
    'St. Boniface': (41.97073837980566, -87.666178197501),
    'St. James Cemetery': (42.576335932913054, -87.81352314016853),
    'St. Matthews Cemetery': (42.03586313948021, -87.80353648862696),
    'Stars and Stripes Park': (41.79920215397533, -87.7973829331003),
    'Strathearn::A': (53.53391884129671, -113.46149103202842),
    'Strathearn::B': (53.529123329511, -113.46157686270794),
    'TUW09': (43.65915583951491, -79.38217792261688),
    'TUW09b': (43.65915583951491, -79.38217792261688),
    'TUW1': (43.65915583951491, -79.38217792261688),
    'TUW11': (43.65915583951491, -79.38217792261688),
    'TUW13': (43.65915583951491, -79.38217792261688),
    'TUW14': (43.65915583951491, -79.38217792261688),
    'TUW17': (43.65915583951491, -79.38217792261688),
    'TUW18': (43.65915583951491, -79.38217792261688),
    'TUW19': (43.65915583951491, -79.38217792261688),
    'TUW2': (43.65915583951491, -79.38217792261688),
    'TUW20': (43.65915583951491, -79.38217792261688),
    'TUW21': (43.65915583951491, -79.38217792261688),
    'TUW23': (43.65915583951491, -79.38217792261688),
    'TUW24': (43.65915583951491, -79.38217792261688),
    'TUW25': (43.65915583951491, -79.38217792261688),
    'TUW26': (43.65915583951491, -79.38217792261688),
    'TUW27': (43.65915583951491, -79.38217792261688),
    'TUW28': (43.65915583951491, -79.38217792261688),
    'TUW29': (43.65915583951491, -79.38217792261688),
    'TUW29b': (43.65915583951491, -79.38217792261688),
    'TUW30': (43.65915583951491, -79.38217792261688),
    'TUW31': (43.65915583951491, -79.38217792261688),
    'TUW33b': (43.65915583951491, -79.38217792261688),
    'TUW33c': (43.65915583951491, -79.38217792261688),
    'TUW34': (43.65915583951491, -79.38217792261688),
    'TUW35a': (43.65915583951491, -79.38217792261688),
    'TUW35b': (43.65915583951491, -79.38217792261688),
    'TUW36': (43.65915583951491, -79.38217792261688),
    'TUW36b': (43.65915583951491, -79.38217792261688),
    'TUW37': (43.65915583951491, -79.38217792261688),
    'TUW37b': (43.65915583951491, -79.38217792261688),
    'TUW38b': (43.65915583951491, -79.38217792261688),
    'TUW39': (43.65915583951491, -79.38217792261688),
    'TUW4': (43.65915583951491, -79.38217792261688),
    'TUW40\\Checkup 8 date wrong': (43.65915583951491, -79.38217792261688),
    'TUW41\\Checkup 1': (43.65915583951491, -79.38217792261688),
    'TUW41\\Checkup 12': (43.65915583951491, -79.38217792261688),
    'TUW41\\Checkup 2': (43.65915583951491, -79.38217792261688),
    'TUW41\\Checkup 3': (43.65915583951491, -79.38217792261688),
    'TUW41\\Checkup 7': (43.65915583951491, -79.38217792261688),
    'TUW41\\Checkup 9 wrong date': (43.65915583951491, -79.38217792261688),
    'TUW42': (43.65915583951491, -79.38217792261688),
    'TUW4b': (43.65915583951491, -79.38217792261688),
    'TUW5': (43.65915583951491, -79.38217792261688),
    'TUW6': (43.65915583951491, -79.38217792261688),
    'TUW7': (43.65915583951491, -79.38217792261688),
    'TUWCPC_4\\check6_WW': (43.65915583951491, -79.38217792261688),
    'TUWCPC_5\\Checkup 1': (43.65915583951491, -79.38217792261688),
    'TUWCPC_5\\check2': (43.65915583951491, -79.38217792261688),
    'TUWCPC_5\\check3': (43.65915583951491, -79.38217792261688),
    'TUWCPC_5\\check4': (43.65915583951491, -79.38217792261688),
    'TUWCPC_5\\check5': (43.65915583951491, -79.38217792261688),
    'TUWCPC_6\\check2_WW': (43.65915583951491, -79.38217792261688),
    'VHC': (41.87771613132751, -87.6317137163225),
    'VLG': (41.87771613132751, -87.6317137163225),
    'VTW': (41.87771613132751, -87.6317137163225),
    'Vernon Hills Athletic Complex': (42.22292613011215, -87.95294204444667),
    'Vernon Township Cemetery': (42.20325936529399, -87.93125776605886),
    'Veteran Woods CFP': (41.668499504178115, -88.05964777472482),
    'Veterans Woods': (41.671102135028676, -88.06206210397757),
    'Village Links GC': (41.85177389551859, -88.06908062911803),
    'WAP': (41.87771613132751, -87.6317137163225),
    'WBK': (41.87771613132751, -87.6317137163225),
    'WCP': (41.87771613132751, -87.6317137163225),
    'WDW': (41.87771613132751, -87.6317137163225),
    'WGL': (41.87771613132751, -87.6317137163225),
    'Wagner::B': (53.49956197592921, -113.44953308254958),
    'Wagner::C': (53.50136683474468, -113.44286263070259),
    'Walnut Park': (41.81137309588999, -87.71903151562402),
    'Waterfall Glen': (41.723135108536844, -87.97260877096222),
    'Waterfall Glen CFP': (41.72291917431522, -87.97259676101415),
    'West Chicago Prairie CFP': (41.88875217181778, -88.21757551118641),
    'West DuPage Woods': (41.86990434308745, -88.19444136960301),
    'Willowbrook': (41.76985657755745, -87.93629785434916),
    'YHR': (41.87771613132751, -87.6317137163225),
    'YOW': (41.87771613132751, -87.6317137163225),
    'York High Ridge': (41.86529716856481, -87.98817400397179),
    'York Woods': (41.85851290551518, -87.93347841562262)
}


def add_tabular_features(image):
    try:
        dt = datetime.strptime(image["datetime"], "%Y-%m-%d %H:%M:%S")
    except Exception:
        dt = datetime.strptime(image["datetime"], "%Y-%m-%d %H:%M")

    image["year"] = dt.year
    image["month"] = dt.month
    image["day"] = dt.day

    image["hour"] = dt.hour
    image["minute"] = dt.minute
    image["second"] = dt.second

    location = image["location"]

    image["latitude"] = LOCATION_TO_LATITUDE_LONGITUDE[location][0]
    image["longitude"] = LOCATION_TO_LATITUDE_LONGITUDE[location][1]

    return image


def main():
    with open(Path(MERGED_PATH), "r") as f:
        coco = json.load(f)

    images = coco["images"]

    images_with_tabular_features = []

    with ProcessPoolExecutor() as executor:
        futures = []
        for image in images:
            future = executor.submit(
                add_tabular_features, image
            )
            futures.append(future)

        for future in tqdm(as_completed(futures), total=len(futures)):
            image_with_tabular_features = future.result()
            images_with_tabular_features.append(image_with_tabular_features)

    coco["images"] = images_with_tabular_features

    with open(MERGED_PATH, "w") as f:
        json.dump(coco, f, indent=4)


if __name__ == '__main__':
    MERGED_PATH = Path("data/processed/qt-coyotes-merged.json")
    main()