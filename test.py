import pandas as pd
from geojson import Feature, Point, FeatureCollection
# import geojson
import geopandas as gpd

def geojson(r):
    
    feature = Feature(
        properties={
            '名称': r['名称'],
            'eNB-LCID': r['eNB-LCID'],
            'PCI(a)': r['PCI(a)'],
            'PCI(b)': r['PCI(b)'],
            'PCI(c)': r['PCI(c)'],
            '所在地': r['所在地'],
            '施設名': r['施設名'],
            '備考': r['備考'],
            '設置形態': r['設置形態'],
            '4G/5G': r['4G/5G'],
            'ミリ波/sub6': r['ミリ波/sub6'],
            '開局状況': r['開局状況'],
            'アイコン種別': r['アイコン種別'],
            'TA値': r['TA値'],
            'アンテナ有無': r['アンテナ有無'],
            '電力線': r['電力線'],
            '光回線': r['光回線'],
            '確認日': r['確認日'],
            'lat': r['lat'],
            'lng': r['lng'],
            'tweet': r['tweet'],
            'URL': r['URL']
        },
        geometry=Point((float(r['lng']), float(r['lat'])))
    )
    return feature

# スプレッドシート読み込み
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ5yTYaZX7YOA0bTx_DYShEVCBXqKntpOyHdBDJWVODzfcXAjpoBDScrMaVF1VSfYMcREZb3E30E0ha/pub?gid=630053475&single=true&output=csv"

df = pd.read_csv(url).fillna("")

# DataFrameからgeojson生成
features = []
for _, r in df.iterrows():
    features.append(geojson(r))
feature_collection = FeatureCollection(features)

import geojson
geo = geojson.dumps(feature_collection)

gdf = gpd.read_file(geo)

# アイコン( folium & simplekml共通 )
icon_ok = "./icon/4G_OK.png"
icon_ng = "./icon/4G_NG.png"
icon_4G5G = "./icon/4G+5G_OK.png" # 5G関連共通
icon_ok_tentative = "./icon/4G_OK_tentative.png"
icon_ng_tentative = "./icon/4G_NG_tentative.png"
icon_indoor = "./icon/4G_indoor_OK.png"
icon_unknown = "./icon/unknown.png"
icon_not_set = "./icon/not_set.png"
today_find = "./icon/today_find.png"
antena_ok = "./icon/antena_ok.png"
antena_ng = "./icon/antena_ng.png"
icon_mail = "./icon/mail.png"

import folium
from folium.plugins import Search

m = folium.Map(
    location = [34.5496419, 135.7788521],
    zoom_start = 12
    )


cells = folium.GeoJson(
    gdf,
    marker=folium.Marker(icon=folium.features.CustomIcon(icon_ok, icon_size = (30, 30))),
    popup=folium.GeoJsonPopup(fields=['eNB-LCID', '備考', '設置形態', 'アンテナ有無', '電力線', '光回線', '備考', '確認日', 'tweet', 'URL'])

).add_to(m)

Search(layer=cells, geom_type='Point', placeholder='eNB-LCID', search_label='eNB-LCID').add_to(m)

m.save('test.html')