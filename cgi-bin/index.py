# -*- coding:utf-8 -*-
import cgi
form = cgi.FieldStorage()

html_body = u"""
<!DOCTYPE html>
<html>
<head><style>html, body, #map { width: 100%; height: 100%; }</style></head>
<body>
<div id="map"></div>

<script>
function initMap() {
    // たくさんの地点...
    var points = [
        new google.maps.LatLng(35.713377, 139.761985),
        new google.maps.LatLng(35.716068, 139.758312),
    ];

    // マップの生成
    var map = new google.maps.Map(document.getElementById("map"), {
        center: new google.maps.LatLng(35.714242, 139.761935), // マップの中心
        zoom: 17 // ズームレベル
    });

    // 地点を分割してルート検索を行います。

    var d = new google.maps.DirectionsService(); // ルート検索オブジェクト
    var origin = null, waypoints = [], dest = null; // 出発地、経由地、目的地
    var resultMap = {}; // 分割してルート検索した結果データ
    var requestIndex = 0; // 検索番号
    var done = 0; // ルート検索が完了した数
    for (var i = 0, len = points.length; i < len; i++) {
        // 最初の場合、originに値をセット
        if (origin == null) {
            origin = points[i];
        }
        // 経由地が8つたまったか最後の地点の場合、ルート検索
        else if (waypoints.length == 8 || i == len - 1) {
            dest = points[i];

            (function(index){
                // ルート検索の条件
                var request = {
                    origin: origin, // 出発地
                    destination: dest, // 目的地
                    waypoints: waypoints, // 経由地
                    travelMode: google.maps.DirectionsTravelMode.WALKING, // 交通手段(歩行。DRIVINGの場合は車)
                };
                console.log(request);
                // ルート検索
                d.route(request, function(result, status){
                    // OKの場合ルートデータ保持
                    if (status == google.maps.DirectionsStatus.OK) {
                        resultMap[index] = result; // 並行でリクエストするので配列だとリクエスト順とずれる場合があります
                        done++;
                    }
                    else {
                        console.log(status); // デバッグ
                    }
                });
            })(requestIndex);

            requestIndex++;
            origin = points[i]; // 今回の目的地を次回の出発地にします。
            waypoints = [];
        }
        // 上記以外、waypointsに地点を追加
        else {
            waypoints.push({ location: points[i], stopover: true });
        }
    }

    // マーカーを表示する場合の準備
    var infoWindow = new google.maps.InfoWindow();
    var mark = function(position, content) {
        var marker = new google.maps.Marker({
            map: map, // 描画先の地図
            position: position // 座標
        });
        // クリック時吹き出しを表示
        marker.addListener("click", function(){
            infoWindow.setContent(content);
            infoWindow.open(map, marker);
        });
    };

    var sid = setInterval(function(){
        // 分割したすべての検索が完了するまで待ちます。
        if (requestIndex > done) return;
        clearInterval(sid);

        // すべての結果のルート座標を順番に取得して平坦な配列にします。
        var path = [];
        var result;
        for (var i = 0, len = requestIndex; i < len; i++) {
            result = resultMap[i]; // 検索結果
            var legs = result.routes[0].legs; // Array<DirectionsLeg>
            for (var li = 0, llen = legs.length; li < llen; li++) {
                var leg = legs[li]; // DirectionLeg
                var steps = leg.steps; // Array<DirectionsStep>
                // DirectionsStepが持っているpathを取得して平坦(2次元配列→1次元配列)にします。
                var _path = steps.map(function(step){ return step.path })
                    .reduce(function(all, paths){ return all.concat(paths) });
                path = path.concat(_path);

                // マーカーが必要ならマーカーを表示します。
                mark(leg.start_location, leg.start_address);
            }
        }
        // マーカーが必要ならマーカーを表示します。(最終)
        var endLeg = result.routes[0].legs[result.routes[0].legs.length-1];
        mark(endLeg.end_location, endLeg.end_address);

        // パスを描画します。
        var line = new google.maps.Polyline({
            map: map, // 描画先の地図
            strokeColor: "#2196f3", // 線の色
            strokeOpacity: 0.8, // 線の不透明度
            strokeWeight: 6, // 先の太さ
            path: path // 描画するパスデータ
        });
    }, 1000);
}
</script>
<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDG_Q0X8u7-_QFk4chZNB93RqvtC2P3zr0&callback=initMap" async defer></script>
</body>
</html>
"""

#content = ''
#content += "Hello %s!</br>" % form.getvalue('name','')

print("Content-type: text/html\n")
print(html_body)
