# coding: utf-8

import pathlib
import folium
import pandas as pd
import geopandas as gpd
import datetime
import shapefile
import simplekml
from folium import plugins

# スプレッドシート読み込み
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ5yTYaZX7YOA0bTx_DYShEVCBXqKntpOyHdBDJWVODzfcXAjpoBDScrMaVF1VSfYMcREZb3E30E0ha/pub?gid=630053475&single=true&output=csv"

df = pd.read_csv(url).fillna("")

# 今日の日付を取得
DIFF_JST_FROM_UTC = 9
now = datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)
today = now.date()
str_today = today.strftime("%Y/%m/%d")

# 行政区域_geojsonファイルの読み込み
Area = "行政区域.geojson"

# TAC_geojsonファイルの読み込み
TAC = "TAC.geojson"

# foliumでマップ作成

# ベースマップ
map = folium.Map(
    tiles = None,
    location = [34.5496419, 135.7788521],
    zoom_start = 12,
    control_scale = True
)

# Googleマップ標準
folium.raster_layers.TileLayer(
    'https://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
    subdomains = ['mt0','mt1','mt2','mt3'],
    name = "Google Map",
    attr = "<a href='https://developers.google.com/maps/documentation' target='_blank'>Google Map</a>"
).add_to(map)

# Googleマップ(航空写真)
folium.raster_layers.TileLayer(
    'https://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}',
    subdomains = ['mt0','mt1','mt2','mt3'],
    name = "Google Map(航空写真)",
    attr = "<a href='https://developers.google.com/maps/documentation' target='_blank'>Google Map</a>"
).add_to(map)

# 国土地理院(白地図)
folium.raster_layers.TileLayer(
    'https://cyberjapandata.gsi.go.jp/xyz/blank/{z}/{x}/{y}.png',
    name = "国土地理院(白地図)",
    attr = "<a href='https://maps.gsi.go.jp/development/ichiran.html'>国土地理院</a>"
).add_to(map)

# 国土地理院(色別標高図)
folium.raster_layers.TileLayer(
    'https://cyberjapandata.gsi.go.jp/xyz/relief/{z}/{x}/{y}.png',
    name = "国土地理院(色別標高図)",
    attr = "<a href='https://maps.gsi.go.jp/development/ichiran.html'>国土地理院 海域部は海上保安庁海洋情報部の資料を使用して作成</a>"
).add_to(map)

# 国土地理院(陰影起伏図)
folium.raster_layers.TileLayer(
    'https://cyberjapandata.gsi.go.jp/xyz/hillshademap/{z}/{x}/{y}.png',
    name = "国土地理院(陰影起伏図)",
    attr = "<a href='https://maps.gsi.go.jp/development/ichiran.html'>国土地理院</a>"
).add_to(map)

circle_group = folium.FeatureGroup(name="半径710m").add_to(map)
cell_group = folium.FeatureGroup(name="基地局").add_to(map)
todayfind_group = folium.FeatureGroup(name="直近確認").add_to(map)
antena_group = folium.FeatureGroup(name="(4G)アンテナ有無",show=False).add_to(map)
mail_group =folium.FeatureGroup(name="情報提供",show=True).add_to(map)

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

for i, r in df.iterrows():

    # tweetリンク有無の処理
    if r["tweet"] != "":
        tweet_link = f' <a href="{r["tweet"]}">ツイートへ</a><br>'
    else:
        tweet_link = ""
    
    # popupの説明内容
    html = ('名称: ' f'{r["名称"]}<br>'
    'eNB-LCID: ' f'{r["eNB-LCID"]}<br>'
    '備考: ' f'{r["備考"]}<br>'
    '設置形態: ' f'{r["設置形態"]}<br>'
    'アンテナ有無: ' f'{r["アンテナ有無"]}<br>'
    '電力線: ' f'{r["電力線"]}<br>'
    '光回線: ' f'{r["光回線"]}<br>'
    '確認日: ' f'{r["確認日"]}<br>'
    + tweet_link +
    f' <a href="{r["URL"]}">Googleマップへ</a><br>')
    
    if r["アイコン種別"] == "4G_OK":
        folium.Marker(
        location = [ r["lat"], r["lng"] ],
        popup = folium.Popup(html, max_width=300),
        icon = folium.features.CustomIcon(
            icon_ok,
            icon_size = (30, 30)
        )
        ).add_to(cell_group)
        
    elif r["アイコン種別"] == "4G_NG":
        folium.Marker(
        location = [ r["lat"], r["lng"] ],
        popup=folium.Popup(html, max_width=300),
        icon = folium.features.CustomIcon(
            icon_ng,
            icon_size = (30, 30)
        )
        ).add_to(cell_group)
        
    elif r["アイコン種別"] == "4G+5G_OK" or r["アイコン種別"] == "4G+5G_NG" or r["アイコン種別"] == "5G_OK" or r["アイコン種別"] == "5G_NG":
        folium.Marker(
        location = [ r["lat"], r["lng"] ],
        popup=folium.Popup(html, max_width=300),
        icon = folium.features.CustomIcon(
            icon_4G5G,
            icon_size = (30, 30)
        )
        ).add_to(cell_group)

    elif r["アイコン種別"] == "4G_OK(仮)":
        folium.Marker(
        location = [ r["lat"], r["lng"] ],
        popup=folium.Popup(html, max_width=300),
        icon = folium.features.CustomIcon(
        icon_ok_tentative,
        icon_size = (30, 30)
        )
        ).add_to(cell_group)
    
    elif r["アイコン種別"] == "4G_NG(仮)":
        folium.Marker(
        location = [ r["lat"], r["lng"] ],
        popup=folium.Popup(html, max_width=300),
        icon = folium.features.CustomIcon(
            icon_ng_tentative,
            icon_size = (30, 30)
        )
        ).add_to(cell_group)

    elif r["アイコン種別"] == "4G(屋内局)_OK":
        folium.Marker(
        location = [ r["lat"], r["lng"] ],
        popup=folium.Popup(html, max_width=300),
        icon = folium.features.CustomIcon(
            icon_indoor,
            icon_size = (30, 30)
        )
        ).add_to(cell_group)

    elif r["アイコン種別"] == "4G_OK(未知局)":
        folium.Marker(
        location = [ r["lat"], r["lng"] ],
        popup=folium.Popup(html, max_width=300),
        icon = folium.features.CustomIcon(
            icon_unknown,
            icon_size = (30, 30)
        )
        ).add_to(cell_group)
        
    # アイコン区分未設定時の設定
    else:
        folium.Marker(location = [ r["lat"], r["lng"] ],
        popup=folium.Popup('【未設定アイコン】<br> '+html, max_width=300),
        icon = folium.features.CustomIcon(
            icon_not_set,
            icon_size = (30, 30)
        )
        ).add_to(cell_group)
        
cell_group.add_to(map)

# 半径710mサークル
for _, r in df[ (df["設置形態"] != "屋内局") & (df["アイコン種別"] != "4G_OK(未知局)") ].iterrows():
    circle_group.add_child(
        folium.vector_layers.Circle(
        location = [ r["lat"], r["lng"] ],
        radius = 710,
        color = "#000000",
        weight = 0.7
        )
    ).add_to(map)

# 直近確認
for i, r in df.iterrows():
    if r["確認日"] == str_today:
        folium.Marker(
        location = [ r["lat"], r["lng"] ],
        icon = folium.features.CustomIcon(
            today_find,
            icon_size = (45, 45)
        )
        ).add_to(todayfind_group)

# 4Gアンテナ有無
for _, r in df[ (df["開局状況"] == "NG" ) | (df["開局状況"] == "NG(仮)" )].iterrows():
    if r["アンテナ有無"] == "OK":
        folium.Marker(
        location = [ r["lat"], r["lng"] ],
        icon = folium.features.CustomIcon(
            antena_ok,
            icon_size = (30, 30)
        )
        ).add_to(antena_group)

    else :
        folium.Marker(
        location = [ r["lat"], r["lng"] ],
        icon = folium.features.CustomIcon(
            antena_ng,
            icon_size = (30, 30)
        )
        ).add_to(antena_group)

antena_group.add_to(map)

# 楽天モバイルエリア4Gマップレイヤー(予定1)
folium.raster_layers.TileLayer(
    name="(4G)楽天モバイルエリア(予定1)",
    tiles='https://gateway-api.global.rakuten.com/dsd/geoserver/4g2m/mno_coverage_map/gwc/service/gmaps?LAYERS=mno_coverage_map:all_map&FORMAT=image/png&TRANSPARENT=TRUE&x={x}&y={y}&zoom={z}',
    fmt='image/png',
    attr="<a href='https://network.mobile.rakuten.co.jp/'>楽天モバイル</a>",
    tms=False,
    overlay=True,
    control=True,
    opacity=1.0,
    show=False,
).add_to(map)

# 楽天モバイルエリア4Gマップレイヤー(予定2)
folium.raster_layers.TileLayer(
    name="(4G)楽天モバイルエリア(予定2)",
    tiles='https://gateway-api.global.rakuten.com/dsd/geoserver/4g4m/mno_coverage_map/gwc/service/gmaps?LAYERS=mno_coverage_map:all_map&FORMAT=image/png&TRANSPARENT=TRUE&x={x}&y={y}&zoom={z}',
    fmt='image/png',
    attr="<a href='https://network.mobile.rakuten.co.jp/'>楽天モバイル</a>",
    tms=False,
    overlay=True,
    control=True,
    opacity=1.0,
    show=False,
).add_to(map)

# 楽天モバイルエリア5Gマップレイヤー
folium.raster_layers.TileLayer(
    name="(5G)楽天モバイルエリア",
    tiles='https://gateway-api.global.rakuten.com/dsd/geoserver/5g/mno_coverage_map/gwc/service/gmaps?LAYERS=mno_coverage_map:all_map&FORMAT=image/png&TRANSPARENT=TRUE&x={x}&y={y}&zoom={z}',
    fmt='image/png',
    attr="<a href='https://network.mobile.rakuten.co.jp/'>楽天モバイル</a>",
    tms=False,
    overlay=True,
    control=True,
    opacity=1.0,
    show=False,
).add_to(map)

# 行政区域レイヤー
folium.features.GeoJson(data=Area,
                        style_function = lambda x:{
                            'fillColor': '#000000',
                            'fillOpacity': 0,
                            'color' : '#000000',
                            'weight': 0.7},
                        name="行政区域(出典：国土交通省)",
                        show=False,
                        popup = folium.features.GeoJsonPopup(["市区町村名"])
                       ).add_to(map)

# TACポリゴンのスタイル指定
def style(feature):
    return {
        "fillColor": feature["properties"]["カラー区分"],
        'fillOpacity': 0.65,
        "stroke": False,
    }

# TACポリゴン
folium.features.GeoJson(data=TAC,
                        style_function=style,
                        name="TAC(行政区域データ(国土交通省)を加工)",
                        show=False,
                        popup = folium.features.GeoJsonPopup(["TAC"])
                       ).add_to(map)

# 情報提供フォーム
html_description = ('<p>このマップは皆さまからの情報により成り立っております。<br>お手数ですが情報をお寄せ下さいませ(匿名厳守)</p>'
'<p style="text-align:center"><a href="https://twitter.com/ZSCCli0y6RMxYmU" target="_blank">管理者Twitterアカウントへ</a></p>'
'<p style="text-align:center"><a href="https://form.run/@rakuten-mobile-map-nara" target="_blank">情報提供フォームへ(匿名)</a></p>'
'<p style="text-align:center"><a href="https://sites.google.com/view/rakuten-map-nara" target="_blank">基地局探しまとめサイト</a></p>')

folium.Marker(location = [ 34.6304528, 135.6563892 ],
    popup=folium.Popup(html_description, 
    max_width=350),
    icon = folium.features.CustomIcon(icon_mail,icon_size = (45, 45)
    )).add_to(mail_group)

# フルスクリーン
folium.plugins.Fullscreen(position = 'bottomright').add_to(map)

# レイヤーコントロール
folium.LayerControl().add_to(map)

# 現在値ボタン
folium.plugins.LocateControl(position = 'bottomright').add_to(map)

# 距離測定ボタン
folium.plugins.MeasureControl().add_to(map)

# お絵かきツール
folium.plugins.Draw(draw_options = {'polygon': False,'rectangle': False,'circlemarker': False}).add_to(map)

# mapフォルダに保存
map_path = pathlib.Path("map", "map.html")

map.save(str(map_path))

# simplekmlでKMZファイル作成( スプシの「アイコン種別」が下記以外の場合の設定をする事 )

# simplekmlおまじない
kml = simplekml.Kml(name="Nara")

# アイコン設定
ok_img = kml.addfile(icon_ok)
ng_img = kml.addfile(icon_ng)
ok_4G5G_img = kml.addfile(icon_4G5G) # 5G関連共通
ok_tentative_img = kml.addfile(icon_ok_tentative)
ng_tentative_img = kml.addfile(icon_ng_tentative)
indoor_img = kml.addfile(icon_indoor)
unknown_img = kml.addfile(icon_unknown)
not_set_img = kml.addfile(icon_not_set)

# 4G_OKノーマルスタイル
ok_normal = simplekml.Style()
ok_normal.iconstyle.scale = 1
ok_normal.iconstyle.icon.href = ok_img

# 4G_OKハイライトスタイル
ok_highlight = simplekml.Style()
ok_highlight.iconstyle.scale = 1
ok_highlight.iconstyle.icon.href = ok_img

# 4G_OKスタイルマップ
ok_stylemap = simplekml.StyleMap()
ok_stylemap.normalstyle = ok_normal
ok_stylemap.highlightstyle = ok_highlight

# 4G_NGノーマルスタイル
ng_normal = simplekml.Style()
ng_normal.iconstyle.scale = 1
ng_normal.iconstyle.icon.href = ng_img

# 4G_NGハイライトスタイル
ng_highlight = simplekml.Style()
ng_highlight.iconstyle.scale = 1
ng_highlight.iconstyle.icon.href = ng_img

# 4G_NGスタイルマップ
ng_stylemap = simplekml.StyleMap()
ng_stylemap.normalstyle = ng_normal
ng_stylemap.highlightstyle = ng_highlight

# 5G関連共通ノーマルスタイル
ok_4G5G_normal = simplekml.Style()
ok_4G5G_normal.iconstyle.scale = 1
ok_4G5G_normal.iconstyle.icon.href = ok_4G5G_img

# 5G関連共通ハイライトスタイル
ok_4G5G_highlight = simplekml.Style()
ok_4G5G_highlight.iconstyle.scale = 1
ok_4G5G_highlight.iconstyle.icon.href = ok_4G5G_img

# 5G関連共通スタイルマップ()
ok_4G5G_stylemap = simplekml.StyleMap()
ok_4G5G_stylemap.normalstyle = ok_4G5G_normal
ok_4G5G_stylemap.highlightstyle = ok_4G5G_highlight

# 4G_OK(仮)ノーマルスタイル
ok_tentative_normal = simplekml.Style()
ok_tentative_normal.iconstyle.scale = 1
ok_tentative_normal.iconstyle.icon.href = ok_tentative_img

# 4G_OK(仮)ハイライトスタイル
ok_tentative_highlight = simplekml.Style()
ok_tentative_highlight.iconstyle.scale = 1
ok_tentative_highlight.iconstyle.icon.href = ok_tentative_img

# 4G_OK(仮)スタイルマップ
ok_tentative_stylemap = simplekml.StyleMap()
ok_tentative_stylemap.normalstyle = ok_tentative_normal
ok_tentative_stylemap.highlightstyle = ok_tentative_highlight

# 4G_NG(仮)ノーマルスタイル
ng_tentative_normal = simplekml.Style()
ng_tentative_normal.iconstyle.scale = 1
ng_tentative_normal.iconstyle.icon.href = ng_tentative_img

# 4G_NG(仮)ハイライトスタイル
ng_tentative_highlight = simplekml.Style()
ng_tentative_highlight.iconstyle.scale = 1
ng_tentative_highlight.iconstyle.icon.href = ng_tentative_img

# 4G_NG(仮)スタイルマップ
ng_tentative_stylemap = simplekml.StyleMap()
ng_tentative_stylemap.normalstyle = ng_tentative_normal
ng_tentative_stylemap.highlightstyle = ng_tentative_highlight

# 4G(屋内局)_OKノーマルスタイル
indoor_normal = simplekml.Style()
indoor_normal.iconstyle.scale = 1
indoor_normal.iconstyle.icon.href = indoor_img

# 4G(屋内局)_OKハイライトスタイル
indoor_highlight = simplekml.Style()
indoor_highlight.iconstyle.scale = 1
indoor_highlight.iconstyle.icon.href = indoor_img

# 4G(屋内局)_OKスタイルマップ
indoor_stylemap = simplekml.StyleMap()
indoor_stylemap.normalstyle = indoor_normal
indoor_stylemap.highlightstyle = indoor_highlight

# unknownノーマルスタイル
unknown_normal = simplekml.Style()
unknown_normal.iconstyle.scale = 1
unknown_normal.iconstyle.icon.href = unknown_img

# unknownハイライトスタイル
unknown_highlight = simplekml.Style()
unknown_highlight.iconstyle.scale = 1
unknown_highlight.iconstyle.icon.href = unknown_img

# unknownスタイルマップ
unknown_stylemap = simplekml.StyleMap()
unknown_stylemap.normalstyle = unknown_normal
unknown_stylemap.highlightstyle = unknown_highlight

# not_setノーマルスタイル
not_set_normal = simplekml.Style()
not_set_normal.iconstyle.scale = 1
not_set_normal.iconstyle.icon.href = not_set_img

# not_setハイライトスタイル
not_set_highlight = simplekml.Style()
not_set_highlight.iconstyle.scale = 1
not_set_highlight.iconstyle.icon.href = not_set_img

# not_setスタイルマップ
not_set_stylemap = simplekml.StyleMap()
not_set_stylemap.normalstyle = not_set_normal
not_set_stylemap.highlightstyle = not_set_highlight

kml.document.stylemaps.append(ok_stylemap)
kml.document.stylemaps.append(ng_stylemap)
kml.document.stylemaps.append(ok_4G5G_stylemap)
kml.document.stylemaps.append(ok_tentative_stylemap)
kml.document.stylemaps.append(ng_tentative_stylemap)
kml.document.stylemaps.append(indoor_stylemap)
kml.document.stylemaps.append(unknown_stylemap)
kml.document.stylemaps.append(not_set_stylemap)

fol = kml.newfolder()

for i, r in df.iterrows():
    
    pnt = fol.newpoint(name=r["名称"])
    pnt.coords = [(r["lng"], r["lat"])]
    pnt.description = f'eNB-LCID: {r["eNB-LCID"]}'
    
    if r["アイコン種別"] == "4G_OK":
        
        pnt.stylemap = kml.document.stylemaps[0]
        
    elif r["アイコン種別"] == "4G_NG":
        
        pnt.stylemap = kml.document.stylemaps[1]
    
    elif r["アイコン種別"] == "4G+5G_OK" or r["アイコン種別"] == "4G+5G_NG" or r["アイコン種別"] == "5G_OK" or r["アイコン種別"] == "5G_NG":
        
        pnt.stylemap = kml.document.stylemaps[2]
        
    elif r["アイコン種別"] == "4G_OK(仮)":
        
        pnt.stylemap = kml.document.stylemaps[3]
        
    elif r["アイコン種別"] == "4G_NG(仮)":
        
        pnt.stylemap = kml.document.stylemaps[4]
        
    elif r["アイコン種別"] == "4G(屋内局)_OK":
        
        pnt.stylemap = kml.document.stylemaps[5]

    elif r["アイコン種別"] == "4G_OK(未知局)":
        
        pnt.stylemap = kml.document.stylemaps[6]
        
    # アイコン未設定時の設定    
    else:
        
        pnt.stylemap = kml.document.stylemaps[7]
    
    ex_data = simplekml.ExtendedData()
    
    for n, v in r.items():
        
        ex_data.newdata(name=str(n), value=str(v))
        
    pnt.extendeddata = ex_data
    
# mapフォルダに保存
kmz_path = pathlib.Path("map", "celldata_nara.kmz")

kml.savekmz(kmz_path)
