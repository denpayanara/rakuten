#!/usr/bin/env python
# coding: utf-8

# In[238]:

import pathlib
import folium
import pandas as pd
import geopandas as gpd
import shapefile
from folium import plugins


# In[239]:


url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ5yTYaZX7YOA0bTx_DYShEVCBXqKntpOyHdBDJWVODzfcXAjpoBDScrMaVF1VSfYMcREZb3E30E0ha/pub?gid=630053475&single=true&output=csv"


# In[240]:


df = pd.read_csv(url).fillna("")


# In[242]:


#行政区域シェイプファイル
bound_shape = gpd.read_file("N03-21_29_210101.shp", encoding="shift-jis")
bound_shape.crs = "EPSG:6668"
bound_shape_name_change = bound_shape.rename(columns={'N03_004': '市区町村名'})


# In[243]:


#ベースマップ
map = folium.Map(
    tiles = None,
    location = [34.5496419, 135.7788521],
    zoom_start = 12,
    control_scale = True
)


# In[244]:


#Googleマップ標準
folium.raster_layers.TileLayer(
    'https://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
    subdomains = ['mt0','mt1','mt2','mt3'],
    name = "Google Map",
    attr = "<a href='https://developers.google.com/maps/documentation' target='_blank'>Google Map</a>"
).add_to(map)


# In[245]:


#Googleマップ(航空写真)
folium.raster_layers.TileLayer(
    'https://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}',
    subdomains = ['mt0','mt1','mt2','mt3'],
    name = "Google Map(航空写真)",
    attr = "<a href='https://developers.google.com/maps/documentation' target='_blank'>Google Map</a>"
).add_to(map)


# In[246]:


#国土地理院(白地図)
folium.raster_layers.TileLayer(
    'https://cyberjapandata.gsi.go.jp/xyz/blank/{z}/{x}/{y}.png',
    name = "国土地理院(白地図)",
    attr = "<a href='https://maps.gsi.go.jp/development/ichiran.html'>国土地理院</a>"
).add_to(map)


# In[247]:


#国土地理院(色別標高図)
folium.raster_layers.TileLayer(
    'https://cyberjapandata.gsi.go.jp/xyz/relief/{z}/{x}/{y}.png',
    name = "国土地理院(色別標高図)",
    attr = "<a href='https://maps.gsi.go.jp/development/ichiran.html'>国土地理院 海域部は海上保安庁海洋情報部の資料を使用して作成</a>"
).add_to(map)


# In[248]:


#国土地理院(陰影起伏図)
folium.raster_layers.TileLayer(
    'https://cyberjapandata.gsi.go.jp/xyz/hillshademap/{z}/{x}/{y}.png',
    name = "国土地理院(陰影起伏図)",
    attr = "<a href='https://maps.gsi.go.jp/development/ichiran.html'>国土地理院</a>"
).add_to(map)


# In[249]:


circle_group = folium.FeatureGroup(name="半径710m").add_to(map)
cell_group = folium.FeatureGroup(name="基地局").add_to(map)


# In[250]:


#アイコン
icon_ok = "4G_OK.png"
icon_ng = "4G_NG.png"
icon_4G5G = "4G+5G_OK.png"
icon_ok_tentative = "4G_OK_tentative.png"
icon_ng_tentative = "4G_NG_tentative.png"
icon_indoor = "4G_indoor_OK.png"


# In[251]:


for i, r in df.iterrows():
    if r["アイコン種別"] == "4G_OK":
        folium.Marker(
        location = [ r["lat"], r["lng"] ],
        popup = folium.Popup(
        '名称: ' f'{r["名称"]}<br>'
        'eNB-LCID: ' f'{r["eNB-LCID"]}<br>'
        '備考: ' f'{r["備考"]}<br>'
        '設置形態: ' f'{r["設置形態"]}<br>'
        '電力線: ' f'{r["電力線"]}<br>'
        '光回線: ' f'{r["光回線"]}<br>'
        '確認日: ' f'{r["確認日"]}<br>'
        f' <a href="{r["URL"]}">Googleマップへ</a><br>',
        max_width=300),
        icon = folium.features.CustomIcon(
            icon_ok,
            icon_size = (30, 30)
        )
        ).add_to(cell_group)
        
    elif r["アイコン種別"] == "4G_NG":
        folium.Marker(
        location = [ r["lat"], r["lng"] ],
        popup=folium.Popup(
        '名称: ' f'{r["名称"]}<br>'
        'eNB-LCID: ' f'{r["eNB-LCID"]}<br>'
        '備考: ' f'{r["備考"]}<br>'
        '設置形態: ' f'{r["設置形態"]}<br>'
        '電力線: ' f'{r["電力線"]}<br>'
        '光回線: ' f'{r["光回線"]}<br>'
        '確認日: ' f'{r["確認日"]}<br>'
        f' <a href="{r["URL"]}">Googleマップへ</a><br>',
        max_width=300),
        icon = folium.features.CustomIcon(
            icon_ng,
            icon_size = (30, 30)
        )
        ).add_to(cell_group)
        
    elif r["アイコン種別"] == "4G+5G_OK":
        folium.Marker(
        location = [ r["lat"], r["lng"] ],
        popup=folium.Popup(
        '名称: ' f'{r["名称"]}<br>'
        'eNB-LCID: ' f'{r["eNB-LCID"]}<br>'
        '備考: ' f'{r["備考"]}<br>'
        '設置形態: ' f'{r["設置形態"]}<br>'
        '電力線: ' f'{r["電力線"]}<br>'
        '光回線: ' f'{r["光回線"]}<br>'
        '確認日: ' f'{r["確認日"]}<br>'
        f' <a href="{r["URL"]}">Googleマップへ</a><br>',
        max_width=300),
        icon = folium.features.CustomIcon(
            icon_4G5G,
            icon_size = (30, 30)
        )
        ).add_to(cell_group)

    elif r["アイコン種別"] == "4G_OK(仮)":
        folium.Marker(
        location = [ r["lat"], r["lng"] ],
        popup=folium.Popup(
        '名称: ' f'{r["名称"]}<br>'
        'eNB-LCID: ' f'{r["eNB-LCID"]}<br>'
        '備考: ' f'{r["備考"]}<br>'
        '設置形態: ' f'{r["設置形態"]}<br>'
        '電力線: ' f'{r["電力線"]}<br>'
        '光回線: ' f'{r["光回線"]}<br>'
        '確認日: ' f'{r["確認日"]}<br>'
        f' <a href="{r["URL"]}">Googleマップへ</a><br>',
        max_width=300),
        icon = folium.features.CustomIcon(
        icon_ok_tentative,
        icon_size = (30, 30)
        )
        ).add_to(cell_group)
    
    elif r["アイコン種別"] == "4G_NG(仮)":
        folium.Marker(
        location = [ r["lat"], r["lng"] ],
        popup=folium.Popup(
        '名称: ' f'{r["名称"]}<br>'
        'eNB-LCID: ' f'{r["eNB-LCID"]}<br>'
        '備考: ' f'{r["備考"]}<br>'
        '設置形態: ' f'{r["設置形態"]}<br>'
        '電力線: ' f'{r["電力線"]}<br>'
        '光回線: ' f'{r["光回線"]}<br>'
        '確認日: ' f'{r["確認日"]}<br>'
        f' <a href="{r["URL"]}">Googleマップへ</a><br>',
        max_width=300),
        icon = folium.features.CustomIcon(
            icon_ng_tentative,
            icon_size = (30, 30)
        )
        ).add_to(cell_group)

    elif r["アイコン種別"] == "4G(屋内局)_OK":
        folium.Marker(
        location = [ r["lat"], r["lng"] ],
        popup=folium.Popup(
        '名称: ' f'{r["名称"]}<br>'
        'eNB-LCID: ' f'{r["eNB-LCID"]}<br>'
        '備考: ' f'{r["備考"]}<br>'
        '設置形態: ' f'{r["設置形態"]}<br>'
        '電力線: ' f'{r["電力線"]}<br>'
        '光回線: ' f'{r["光回線"]}<br>'
        '確認日: ' f'{r["確認日"]}<br>'
        f' <a href="{r["URL"]}">Googleマップへ</a><br>',
        max_width=300),
        icon = folium.features.CustomIcon(
            icon_indoor,
            icon_size = (30, 30)
        )
        ).add_to(cell_group)
        
    #アイコン区分未設定時の設定
    else:
        folium.Marker(location = [ r["lat"], r["lng"] ],
        popup=folium.Popup(
        '【アイコン未設定】スプシ要修正！<br>'
        '名称: ' f'{r["名称"]}<br>'
        'eNB-LCID: ' f'{r["eNB-LCID"]}<br>'
        '備考: ' f'{r["備考"]}<br>'
        '設置形態: ' f'{r["設置形態"]}<br>'
        '電力線: ' f'{r["電力線"]}<br>'
        '光回線: ' f'{r["光回線"]}<br>'
        '確認日: ' f'{r["確認日"]}<br>'
        f' <a href="{r["URL"]}">Googleマップへ</a><br>',
        max_width=300),
        icon=folium.Icon(color='red')
        ).add_to(cell_group)


# In[252]:


cell_group.add_to(map)


# In[253]:


#半径710mサークル
for _, r in df[df["設置形態"] != "屋内局"].iterrows():
    circle_group.add_child(
        folium.vector_layers.Circle(
        location = [ r["lat"], r["lng"] ],
        radius = 710,
        color = "#000000",
        weight = 0.7
        )
    ).add_to(map)


# In[254]:


#楽天モバイルエリアマップ
folium.raster_layers.TileLayer(
    name="楽天モバイルエリア",
    tiles='https://gateway-api.global.rakuten.com/dsd/geoserver/4g2m/mno_coverage_map/gwc/service/gmaps?LAYERS=mno_coverage_map:all_map&FORMAT=image/png&TRANSPARENT=TRUE&x={x}&y={y}&zoom={z}',
    fmt='image/png',
    attr="<a href='https://network.mobile.rakuten.co.jp/'>楽天モバイル</a>",
    tms=False,
    overlay=True,
    control=True,
    opacity=0.8,
    show=False,
).add_to(map)


# In[255]:


#行政区域
folium.GeoJson(
    data = bound_shape_name_change,
    name = "行政区域",
    show = False,
    popup = folium.features.GeoJsonPopup(fields=['市区町村名']),
    style_function = lambda x:{
        'fillColor': '#000000',
        'fillOpacity': 0,
        'color' : '#000000',
        'weight': 0.7
    }
    
).add_to(map)


# In[256]:


#TAC_geojsonファイルの読み込み
TAC = "TAC.geojson"


# In[257]:


#スタイル指定
def style(feature):
    return {
        "fillColor": feature["properties"]["カラー区分"],
        'fillOpacity': 0.25,
        "stroke": False,
    }


# In[258]:


#TACポリゴン
folium.features.GeoJson(data=TAC,
                        style_function=style,
                        name="TAC",
                        show=False,
                        popup = folium.features.GeoJsonPopup(["TAC"])).add_to(map)


# In[259]:


#フルスクリーン
folium.plugins.Fullscreen(
    position = 'bottomright'
).add_to(map)


# In[260]:


#レイヤーコントロール
folium.LayerControl().add_to(map)


# In[261]:


#現在値ボタン
folium.plugins.LocateControl(
    position = 'bottomright'
).add_to(map)


# In[262]:


#距離測定ボタン
folium.plugins.MeasureControl().add_to(map)


# In[263]:


#お絵かきツール
folium.plugins.Draw(
    draw_options = {'polygon': False,'rectangle': False,'circlemarker': False}
).add_to(map)


# In[264]:


map_path = pathlib.Path("map", "map.html")

# map_path.parent.mkdir(parents=True, exist_ok=True)

map.save(str(map_path))

