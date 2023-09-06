// window.alert('アプリ開いたね！');
// document.getElementById

window.onload = function() {
  try {
    // 通常販売価格
    var price = document.getElementsByClassName('ItemPrice_price')[0].innerText.replace('円', '').replace(',', '');
    var point_per = document.getElementsByClassName('ItemPointHeader_rate')[0].innerText.replace('%', '');
    float_point_per=parseFloat(point_per)*0.01
    
    var actual_price = parseFloat(price)-(price/1.1*float_point_per);

    // 表示領域を取得
    var ItemPrice_element = document.getElementsByClassName('ItemPrice')[0];
    // 新しいHTML要素を作成
    var new_element = document.createElement('div');
    new_element.textContent = 'ポイント：' + point_per + "｜" + '実質仕入値：' + actual_price;
    // alert('獲得ポイント：' + point_per + "\r\n" + '実質仕入値：' + actual_price);
    // 指定した要素の中の末尾に挿入
    ItemPrice_element.appendChild(new_element);
  } catch(e) {
    console.log( e.message );
  }
};


